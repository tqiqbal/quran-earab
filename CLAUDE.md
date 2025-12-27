# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

This is a static HTML application with zero dependencies. No build system, package managers, or compilation required.

**Run locally:**
```bash
# Option 1: Python
python -m http.server 8000

# Option 2: Node.js
npx http-server

# Then open http://localhost:8000
```

**Or simply:** Open `index.html` or `sarf.html` directly in a browser.

## Architecture Overview

### Three Main Pages

**[index.html](index.html)** - E'arab (grammatical analysis) tool
- Surah/Ayah selection interface
- **Loads E'arab data from local JSON files** (pre-scraped via Python scraper)
- Fallback to CORS proxies if local data unavailable
- Displays English/Urdu translations from local data
- Sequential navigation between ayahs
- Embedded page-specific JavaScript

**[sarf.html](sarf.html)** - Morphology analysis tool
- Arabic word input
- Fetches morphological breakdown from aratools.com API
- Displays form, gloss, POS, root, and measure in table format
- Embedded page-specific JavaScript

**[about.html](about.html)** - Information page
- Data source attribution
- Disclaimer and privacy information
- Contact details
- No page-specific JavaScript

### Shared Resources

**[style.css](style.css)** - Unified stylesheet
- CSS variable-based theming (emerald green & gold)
- Responsive design with mobile-first approach
- Desktop top navigation and mobile bottom navigation styles
- RTL support for Arabic/Urdu content

**[script.js](script.js)** - Shared utilities
- Navigation highlighting based on current page
- Loading state management helpers
- Used by all pages for consistent navigation behavior

### Theming System

CSS variables in [style.css](style.css) define the visual theme:
```css
:root {
    --primary: #32de84;        /* Emerald green - primary actions */
    --primary-hover: #26c673;  /* Darker on hover */
    --secondary: #D97706;      /* Amber/gold - secondary actions */
    --bg-body: #fefefe;        /* Page background */
    --bg-card: #FFFFFF;        /* Card/container background */
    --text-main: #1F2937;      /* Main text color */
    --font-main: 'Inter', sans-serif;
    --font-arabic: 'Amiri', 'Traditional Arabic', serif;
}
```

**When modifying styles:**
- Use CSS variables instead of hardcoded colors
- Maintain RTL support for Arabic/Urdu content
- Test responsive breakpoints: desktop (default), tablet (≤768px), mobile (≤480px)
- Arabic text uses `--font-arabic` (Amiri font)
- English/UI text uses `--font-main` (Inter font)

### Data Loading System

**Primary: Local JSON Data** (NEW)
- Pre-scraped E'arab and translation data stored in `/data` folder
- One JSON file per surah (114 files total)
- Fast loading, no external API dependencies
- Offline capability

**Fallback: CORS Proxy System**
- Used only when local data unavailable
- 4-level fallback with 10-second timeouts:
  - `api.allorigins.win` (returns JSON with 'contents' field)
  - `corsproxy.io` (raw HTML)
  - `thingproxy.freeboard.io` (raw HTML)
  - `api.codetabs.com` (raw HTML)
- Validates response, handles different formats
- Falls back to next proxy on failure

### Python Scraper

**Location**: `/scraper`

**Purpose**: Pre-fetch all E'arab and translation data to eliminate CORS proxy dependency

**Key Features**:
- Scrapes all 114 surahs (~6,236 ayahs)
- Respectful rate limiting (1 second between requests)
- Retry logic with exponential backoff
- Error logging and progress tracking
- Generates manifest file

**Usage**:
```bash
cd scraper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Scrape all surahs (takes 2-4 hours)
python scraper.py

# Test with single surah
python scraper.py --surah 1
```

**Output**: JSON files in `/data` with structure:
```json
{
  "surahNo": 1,
  "surahName": "Al-Faatiha",
  "totalAyah": 7,
  "ayahs": [{
    "ayahNo": 1,
    "arabic": "...",
    "english": "...",
    "urdu": "...",
    "earab": {
      "title_html": "<h2>...</h2>",
      "cards_html": ["<div>...</div>"],
      "source_url": "https://..."
    }
  }]
}
```

### API Integration

**1. Surah List API**
- Endpoint: `https://quranapi.pages.dev/api/surah.json`
- Returns array of 114 Surahs with names, ayah counts
- Used to populate dropdown on page load

**2. Translation API**
- Pattern: `https://quranapi.pages.dev/api/{surahNo}/{ayahNo}.json`
- Returns Arabic text, English and Urdu translations
- Direct fetch (no CORS proxy needed)

**3. E'arab Content Source**
- Pattern: `https://surahquran.com/quran-search/e3rab-aya-{ayah}-sora-{surah}.html`
- HTML scraping via CORS proxies
- Extracts: title with `id="e3rab"` and first two `.card.mt-3` elements
- Uses DOMParser API for HTML parsing

**4. Morphology API**
- Pattern: `https://aratools.com/api/v1/dictionary/lookup/ar/{word}?filter_diacritics=true&_={timestamp}`
- Returns JSON with `words` array containing morphological data
- Fetched via CORS proxies with same fallback strategy

### HTML Parsing Pattern

```javascript
const parser = new DOMParser();
const doc = parser.parseFromString(html, 'text/html');

// Extract specific elements from surahquran.com
const earabTitle = doc.querySelector('#e3rab');
const cards = doc.querySelectorAll('.card.mt-3');
const firstTwoCards = Array.from(cards).slice(0, 2);
```

### Navigation System

**Page Navigation:**
- Desktop: Top navigation bar with logo and page links
- Mobile: Bottom navigation bar (≤768px) with icons and labels
- Active page highlighting via [script.js](script.js)
- Navigation links: E'arab (index.html), Sarf (sarf.html), About (about.html)

**Ayah Browsing (E'arab page):**
- Previous/Next buttons with boundary detection
- Automatically disables at first ayah (1) and last ayah (totalAyahs)
- Updates input field, fetches new content, smooth scrolls to results
- Maintains state: current surah, current ayah, total ayahs

## Important Context

**Third-Party Dependencies:**
- All content fetched from external sources (surahquran.com, quranapi.pages.dev, aratools.com)
- Service availability not guaranteed
- CORS proxies are third-party services with their own terms
- See comprehensive disclaimer in [README.md](README.md) lines 6-73

**No Backend:**
- Entirely client-side processing
- All JavaScript runs in browser
- No user data collection or storage
- Requests subject to third-party API privacy policies

**External Font Dependencies:**
- Google Fonts used for typography: Inter (UI) and Amiri (Arabic)
- Font URLs: `https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Amiri:wght@400;700`
- Application will work without fonts but with degraded typography (falls back to system fonts)

**Responsive Design:**
- Desktop (default), Tablet (≤768px), Mobile (≤480px)
- RTL support for Arabic and Urdu text
- Minimized side margins for maximum reading space

## Key Files

### Web Application
- [index.html](index.html) - E'arab analysis page (main entry point)
- [sarf.html](sarf.html) - Morphology analysis page
- [about.html](about.html) - About page with data sources and contact info
- [style.css](style.css) - Shared stylesheet with CSS variables and responsive design
- [script.js](script.js) - Shared JavaScript utilities for navigation and loading states
- [surah.json](surah.json) - Surah metadata (114 surahs with names and ayah counts)

### Python Scraper
- [scraper/scraper.py](scraper/scraper.py) - Main scraper script
- [scraper/config.py](scraper/config.py) - Configuration constants
- [scraper/utils/fetcher.py](scraper/utils/fetcher.py) - HTTP fetching with retry logic
- [scraper/utils/parser.py](scraper/utils/parser.py) - HTML parsing for E'arab extraction
- [scraper/utils/logger.py](scraper/utils/logger.py) - Logging setup
- [scraper/requirements.txt](scraper/requirements.txt) - Python dependencies
- [scraper/README.md](scraper/README.md) - Scraper usage documentation

### Data
- `data/surah-{1-114}.json` - Pre-scraped E'arab and translation data (generated by scraper)
- `data/manifest.json` - Index of all scraped files (generated by scraper)
- `data/scraping_errors.json` - Error log (generated if scraping errors occur)

### Documentation
- [README.md](README.md) - Comprehensive documentation with API details, response structures, error handling
- [CLAUDE.md](CLAUDE.md) - This file - development guide for Claude Code
