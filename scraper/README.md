# Quran E'arab Scraper

Python scraper to pre-fetch all E'arab (grammatical analysis) and translation data for the Quran, eliminating dependency on CORS proxies and improving web app performance.

## Overview

This scraper fetches data from:
- **Translation API**: `quranapi.pages.dev` - English and Urdu translations
- **E'arab Source**: `surahquran.com` - Arabic grammatical analysis

**Output**: 114 JSON files (one per surah) containing all ayahs with translations and E'arab HTML.

## Installation

1. **Create virtual environment** (recommended):
```bash
cd scraper
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

### Scrape All Surahs
```bash
python scraper.py
```

This will scrape all 114 surahs (~6,236 ayahs). **Estimated time: 2-4 hours** due to rate limiting.

### Scrape Single Surah (Testing)
```bash
python scraper.py --surah 1
```

### Scrape Range of Surahs
```bash
python scraper.py --start 1 --end 10
```

## Output

### Data Files
- **Location**: `../data/`
- **Format**: `surah-{N}.json` where N is 1-114
- **Structure**:

```json
{
  "surahNo": 1,
  "surahName": "Al-Faatiha",
  "surahNameArabic": "الفاتحة",
  "surahNameTranslation": "The Opening",
  "revelationPlace": "Mecca",
  "totalAyah": 7,
  "ayahs": [
    {
      "ayahNo": 1,
      "arabic": "بِسْمِ ٱللَّهِ...",
      "english": "In the Name of Allah...",
      "urdu": "شروع کرتا ہوں...",
      "earab": {
        "title_html": "<h2 id='e3rab'>...</h2>",
        "cards_html": ["<div class='card'>...</div>"],
        "source_url": "https://surahquran.com/..."
      }
    }
  ]
}
```

### Manifest File
- **Location**: `../data/manifest.json`
- **Purpose**: Index of all scraped files with metadata
- **Example**:

```json
{
  "generated_at": "2025-12-27T10:30:00",
  "total_surahs": 114,
  "total_ayahs": 6236,
  "files": [
    {
      "surah": 1,
      "filename": "surah-1.json",
      "size_bytes": 15234,
      "ayah_count": 7
    }
  ]
}
```

### Error Log
- **Location**: `../data/scraping_errors.json`
- **Created**: Only if errors occur during scraping
- **Contains**: List of failed ayahs with error details

## Configuration

Edit `config.py` to customize:

- **Rate Limiting**: `RATE_LIMIT_DELAY` (default: 1 second)
- **Timeouts**: `REQUEST_TIMEOUT` (default: 30 seconds)
- **Retry Attempts**: `RETRY_ATTEMPTS` (default: 5)
- **Cards to Extract**: `MAX_CARDS_TO_EXTRACT` (default: 2)

## Features

- ✅ **Retry Logic**: Exponential backoff on failures (up to 5 attempts)
- ✅ **Rate Limiting**: Respectful 1-second delay between requests
- ✅ **Progress Bars**: Visual progress with `tqdm`
- ✅ **Error Logging**: Detailed error tracking
- ✅ **Resume Capability**: Can re-run to scrape missing surahs
- ✅ **Manifest Generation**: Automatic index of scraped data

## Architecture

```
scraper/
├── config.py          # Configuration constants
├── scraper.py         # Main scraper logic
├── requirements.txt   # Python dependencies
├── utils/
│   ├── fetcher.py    # HTTP fetching with retry
│   ├── parser.py     # HTML parsing
│   └── logger.py     # Logging setup
└── README.md         # This file
```

## Troubleshooting

### Rate Limiting / Blocking
If you encounter frequent failures:
1. Increase `RATE_LIMIT_DELAY` in `config.py` to 2-3 seconds
2. Reduce `RETRY_ATTEMPTS` to avoid aggressive retries

### Timeout Errors
If requests time out frequently:
1. Increase `REQUEST_TIMEOUT` in `config.py`
2. Check your internet connection

### Partial Scrape
If scraping is interrupted:
1. Check `data/scraping_errors.json` for failed ayahs
2. Re-run scraper with specific surah: `python scraper.py --surah {N}`

## Re-scraping

To update existing data:
```bash
# Re-scrape all
python scraper.py

# Re-scrape specific surah
python scraper.py --surah 2
```

Existing files will be overwritten.

## Performance

- **Rate**: ~1-2 ayahs per second (with 1s rate limit)
- **Total Time**: 2-4 hours for all 6,236 ayahs
- **Output Size**: ~50-100MB total for all 114 files

## Dependencies

- `requests` - HTTP library
- `beautifulsoup4` - HTML parsing
- `lxml` - Fast XML/HTML parser
- `tenacity` - Retry logic
- `tqdm` - Progress bars

## License

Same as parent project - educational use only.

## Notes

- **Respectful Scraping**: Built-in rate limiting to avoid overloading source servers
- **Third-Party Content**: All scraped content belongs to original sources
- **Educational Purpose**: For Quran study and Arabic grammar learning
