"""
Configuration file for Quran E'arab Scraper
"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SURAH_JSON_PATH = PROJECT_ROOT / "surah.json"

# API Endpoints
TRANSLATION_API_BASE = "https://quranapi.pages.dev/api"
EARAB_URL_TEMPLATE = "https://surahquran.com/quran-search/e3rab-aya-{ayah}-sora-{surah}.html"

# Scraping Configuration
REQUEST_TIMEOUT = 30          # seconds
RETRY_ATTEMPTS = 5
RETRY_DELAY = 2              # seconds
RATE_LIMIT_DELAY = 1         # seconds between requests (be respectful)

# HTML Parsing
EARAB_TITLE_SELECTOR = "#e3rab"
EARAB_CARD_SELECTOR = ".card.mt-3"
MAX_CARDS_TO_EXTRACT = 2

# Output
OUTPUT_FILE_PATTERN = "surah-{surah_num}.json"
MANIFEST_FILE = "manifest.json"
ERROR_LOG_FILE = "scraping_errors.json"
