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

### Two Standalone Pages

**[index.html](index.html)** - E'arab (grammatical analysis) tool
- Surah/Ayah selection interface
- Fetches E'arab content via CORS proxies from surahquran.com
- Displays English/Urdu translations from quranapi.pages.dev
- Sequential navigation between ayahs

**[sarf.html](sarf.html)** - Morphology analysis tool
- Arabic word input
- Fetches morphological breakdown from aratools.com API
- Displays form, gloss, POS, root, and measure in table format

Both files are completely self-contained with embedded CSS and JavaScript.

### CORS Proxy Fallback System

Critical architectural pattern for fetching content from surahquran.com:

```javascript
// 4-level fallback with 10-second timeouts
const proxies = [
    `https://api.allorigins.win/get?url=${encodeURIComponent(url)}`,      // Returns JSON with 'contents' field
    `https://corsproxy.io/?${encodeURIComponent(url)}`,                    // Returns raw HTML
    `https://thingproxy.freeboard.io/fetch/${url}`,                        // Returns raw HTML
    `https://api.codetabs.com/v1/proxy?quest=${encodeURIComponent(url)}`  // Returns raw HTML
];
```

Each proxy attempt:
1. Uses `AbortController` with 10-second timeout
2. Validates response (checks content length >100 chars)
3. Handles different response formats (JSON wrapper vs raw HTML)
4. Falls back to next proxy on failure

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

Sequential ayah browsing in [index.html](index.html):
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

**Responsive Design:**
- Desktop (default), Tablet (≤768px), Mobile (≤480px)
- RTL support for Arabic and Urdu text
- Minimized side margins for maximum reading space

## Key Files

- [index.html](index.html) - E'arab analysis page (main entry point)
- [sarf.html](sarf.html) - Morphology analysis page
- [README.md](README.md) - Comprehensive documentation with API details, response structures, error handling
