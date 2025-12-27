#!/usr/bin/env python3
"""
Quran E'arab Scraper
Fetches E'arab and translation data for all 6,236 ayahs across 114 surahs
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from tqdm import tqdm

from config import *
from utils.fetcher import HTTPFetcher
from utils.parser import EarabParser
from utils.logger import get_logger

logger = get_logger(__name__)


class QuranScraper:
    """Main scraper class for Quran E'arab data"""

    def __init__(self):
        """Initialize the scraper"""
        self.fetcher = HTTPFetcher(
            timeout=REQUEST_TIMEOUT,
            rate_limit=RATE_LIMIT_DELAY
        )
        self.surahs = self._load_surah_metadata()
        self.errors = []

        # Create data directory
        DATA_DIR.mkdir(exist_ok=True)
        logger.info(f"Data directory: {DATA_DIR}")

    def _load_surah_metadata(self) -> List[dict]:
        """
        Load surah metadata from surah.json

        Returns:
            List of surah dictionaries
        """
        logger.info(f"Loading surah metadata from {SURAH_JSON_PATH}")

        if not SURAH_JSON_PATH.exists():
            logger.error(f"Surah metadata file not found: {SURAH_JSON_PATH}")
            sys.exit(1)

        with open(SURAH_JSON_PATH, 'r', encoding='utf-8') as f:
            surahs = json.load(f)

        logger.info(f"Loaded {len(surahs)} surahs")
        return surahs

    def scrape_ayah(self, surah_num: int, ayah_num: int) -> Optional[dict]:
        """
        Scrape single ayah data (translation + E'arab)

        Args:
            surah_num: Surah number (1-114)
            ayah_num: Ayah number

        Returns:
            Ayah data dictionary or None if failed
        """
        try:
            # Fetch translation
            translation_url = f"{TRANSLATION_API_BASE}/{surah_num}/{ayah_num}.json"
            translation_data = self.fetcher.fetch_json(translation_url)

            # Fetch E'arab HTML
            earab_url = EARAB_URL_TEMPLATE.format(surah=surah_num, ayah=ayah_num)
            earab_html = self.fetcher.fetch_html(earab_url)

            # Parse E'arab
            parser = EarabParser(earab_html)
            earab_data = parser.extract_earab_data(max_cards=MAX_CARDS_TO_EXTRACT)

            return {
                'ayahNo': ayah_num,
                'arabic': translation_data.get('arabic1', ''),
                'english': translation_data.get('english', ''),
                'urdu': translation_data.get('urdu', ''),
                'earab': {
                    'title_html': earab_data['title_html'],
                    'cards_html': earab_data['cards_html'],
                    'source_url': earab_url
                }
            }

        except Exception as e:
            error_info = {
                'surah': surah_num,
                'ayah': ayah_num,
                'error': str(e),
                'type': type(e).__name__
            }
            self.errors.append(error_info)
            logger.error(f"Failed to scrape Surah {surah_num}, Ayah {ayah_num}: {e}")
            return None

    def scrape_surah(self, surah_num: int) -> dict:
        """
        Scrape all ayahs in a surah

        Args:
            surah_num: Surah number (1-114)

        Returns:
            Complete surah data dictionary
        """
        if surah_num < 1 or surah_num > 114:
            raise ValueError(f"Invalid surah number: {surah_num}")

        surah_info = self.surahs[surah_num - 1]
        total_ayahs = surah_info['totalAyah']

        logger.info(f"Scraping Surah {surah_num}: {surah_info['surahName']} ({total_ayahs} ayahs)")

        surah_data = {
            'surahNo': surah_num,
            'surahName': surah_info['surahName'],
            'surahNameArabic': surah_info['surahNameArabic'],
            'surahNameTranslation': surah_info.get('surahNameTranslation', ''),
            'revelationPlace': surah_info.get('revelationPlace', ''),
            'totalAyah': total_ayahs,
            'ayahs': []
        }

        # Scrape each ayah sequentially (to respect rate limits)
        for ayah_num in tqdm(range(1, total_ayahs + 1),
                            desc=f"Surah {surah_num}",
                            leave=False):
            ayah_data = self.scrape_ayah(surah_num, ayah_num)
            if ayah_data:
                surah_data['ayahs'].append(ayah_data)
            else:
                logger.warning(f"Skipped Surah {surah_num}, Ayah {ayah_num} due to error")

        return surah_data

    def save_surah_data(self, surah_data: dict):
        """
        Save surah data to JSON file

        Args:
            surah_data: Complete surah data dictionary
        """
        surah_num = surah_data['surahNo']
        filename = OUTPUT_FILE_PATTERN.format(surah_num=surah_num)
        filepath = DATA_DIR / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(surah_data, f, ensure_ascii=False, indent=2)

        file_size = filepath.stat().st_size / 1024  # KB
        logger.info(f"Saved {filename} ({file_size:.1f} KB)")

    def scrape_all(self, start_surah: int = 1, end_surah: int = 114):
        """
        Scrape all surahs in range

        Args:
            start_surah: Starting surah number (default: 1)
            end_surah: Ending surah number (default: 114)
        """
        logger.info(f"Starting scrape: Surahs {start_surah}-{end_surah}")
        logger.info(f"Rate limit: {RATE_LIMIT_DELAY} seconds between requests")

        start_time = datetime.now()

        for surah_num in tqdm(range(start_surah, end_surah + 1),
                             desc="Overall Progress"):
            try:
                surah_data = self.scrape_surah(surah_num)
                self.save_surah_data(surah_data)
            except Exception as e:
                logger.error(f"Failed to scrape Surah {surah_num}: {e}")

        # Calculate duration
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"Scraping completed in {duration}")

        # Save error log
        if self.errors:
            error_file = DATA_DIR / ERROR_LOG_FILE
            with open(error_file, 'w', encoding='utf-8') as f:
                json.dump(self.errors, f, ensure_ascii=False, indent=2)
            logger.warning(f"Encountered {len(self.errors)} errors. See {error_file}")
        else:
            logger.info("No errors encountered!")

        # Generate manifest
        self.generate_manifest()

        logger.info("Scraping complete!")

    def generate_manifest(self):
        """Generate manifest file listing all available data"""
        manifest = {
            'generated_at': datetime.now().isoformat(),
            'total_surahs': 114,
            'total_ayahs': sum(s['totalAyah'] for s in self.surahs),
            'files': []
        }

        for surah_num in range(1, 115):
            filename = OUTPUT_FILE_PATTERN.format(surah_num=surah_num)
            filepath = DATA_DIR / filename
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                manifest['files'].append({
                    'surah': surah_num,
                    'filename': filename,
                    'size_bytes': filepath.stat().st_size,
                    'ayah_count': len(data.get('ayahs', []))
                })

        manifest_path = DATA_DIR / MANIFEST_FILE
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        logger.info(f"Generated manifest: {manifest_path}")
        logger.info(f"Total files: {len(manifest['files'])}")


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Scrape Quran E\'arab and translation data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape all surahs
  python scraper.py

  # Scrape single surah (for testing)
  python scraper.py --surah 1

  # Scrape range of surahs
  python scraper.py --start 1 --end 10
        """
    )

    parser.add_argument('--start', type=int, default=1,
                       help='Start surah number (default: 1)')
    parser.add_argument('--end', type=int, default=114,
                       help='End surah number (default: 114)')
    parser.add_argument('--surah', type=int,
                       help='Scrape single surah (overrides --start and --end)')

    args = parser.parse_args()

    # Validate arguments
    if args.surah:
        if args.surah < 1 or args.surah > 114:
            parser.error("Surah number must be between 1 and 114")

    scraper = QuranScraper()

    try:
        if args.surah:
            logger.info(f"Scraping single surah: {args.surah}")
            surah_data = scraper.scrape_surah(args.surah)
            scraper.save_surah_data(surah_data)
            scraper.generate_manifest()
        else:
            scraper.scrape_all(args.start, args.end)
    except KeyboardInterrupt:
        logger.warning("\nScraping interrupted by user")
        if scraper.errors:
            error_file = DATA_DIR / ERROR_LOG_FILE
            with open(error_file, 'w', encoding='utf-8') as f:
                json.dump(scraper.errors, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved partial error log to {error_file}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
