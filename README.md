# Quran E'arab Learning Application

A web application for learning Arabic grammatical analysis (E'arab/إعراب) of Quranic verses with integrated translations and morphological analysis (Sarf/صرف).

## Disclaimer

**IMPORTANT: Please read this disclaimer carefully before using this application.**

This application is an educational tool created for learning purposes only. Users should be aware of the following:

### Third-Party Services
- This application uses **third-party APIs and websites** that are **NOT owned, controlled, or maintained** by this project
- The content is fetched from:
  - **quranapi.pages.dev** - for Surah lists and translations
  - **surahquran.com** - for E'arab (grammatical analysis) content
  - **aratools.com** - for morphological analysis (Sarf)
- These services are independent and may change, become unavailable, or modify their content at any time

### Content Ownership
- **All Quranic content, translations, and E'arab analysis belong to their respective original sources**
- This application does not claim ownership of any fetched content
- Content is displayed in its original form from the source websites
- All copyrights and intellectual property rights remain with the original content providers

### Service Availability
- The application depends on external services and CORS proxy servers
- **Service availability is NOT guaranteed** and may be affected by:
  - API or website downtime
  - CORS proxy service interruptions
  - Network connectivity issues
  - Changes to source website structure
- If content fails to load, users can access the original sources directly via provided links

### CORS Proxy Usage
- This application uses public CORS proxy services to fetch content:
  - api.allorigins.win
  - corsproxy.io
  - thingproxy.freeboard.io
  - api.codetabs.com
- **These are third-party services** with their own terms and usage policies
- The availability and reliability of these proxies are beyond our control
- Users should be aware that content passes through these intermediate servers

### Educational Purpose
- This application is intended **solely for educational purposes** to facilitate learning Arabic grammar through Quranic verses
- It is designed to supplement traditional learning methods, not replace them
- Users are encouraged to verify content with authentic Islamic scholarly sources

### No Warranty
- This application is provided "AS IS" without any warranties, express or implied
- The developers make no guarantees about:
  - Accuracy of fetched content
  - Availability or uptime of the service
  - Compatibility with all browsers or devices
  - Freedom from errors or interruptions

### Respect for Source Terms
- Users are expected to respect the terms of service of all source websites and APIs
- Commercial use of content should comply with the original sources' licensing terms
- This tool should not be used to circumvent any access restrictions or terms of service of source websites

### Privacy
- This application runs entirely in the user's browser (client-side)
- No user data is collected, stored, or transmitted by this application
- However, requests to third-party APIs and proxy services are subject to their respective privacy policies

### Recommendation
For the most authentic and reliable content, users are encouraged to visit the source websites directly:
- [surahquran.com](https://surahquran.com) - for E'arab analysis
- [quranapi.pages.dev](https://quranapi.pages.dev) - for Quran data and translations
- [aratools.com](https://aratools.com) - for morphological analysis

**By using this application, you acknowledge that you have read and understood this disclaimer.**

---

## Features

### E'arab Analysis (index.html)
- **Surah Selection**: Dropdown menu with all 114 Surahs (Arabic and English names)
- **Ayah Input**: Smart validation preventing invalid ayah numbers
- **E'arab Display**: Grammatical analysis fetched and displayed from surahquran.com
- **Translations**: English and Urdu translations for selected verses
- **Navigation**: Previous/Next buttons for seamless ayah browsing

### Morphology Analysis (sarf.html)
- **Arabic Word Input**: Enter any Arabic word for morphological analysis
- **Comprehensive Analysis**: Displays vocalized form, meaning, part of speech, root, and measure
- **Multiple Forms**: Shows all possible morphological interpretations
- **Table Display**: Clean tabular format for easy comparison
- **Real-time API**: Fetches data from aratools.com API

### Common Features
- **Responsive Design**: Mobile-friendly layout with optimized spacing
- **RTL Support**: Proper right-to-left rendering for Arabic and Urdu text
- **Loading States**: Visual feedback with spinners during content fetching
- **Error Handling**: Graceful error messages in Arabic and English
- **Cross-page Navigation**: Easy navigation between E'arab and Sarf tools

## Performance Enhancement: Python Scraper

### Overview

To eliminate dependency on unreliable CORS proxy servers and improve performance, this project includes a Python scraper that pre-fetches all E'arab (grammatical analysis) and translation data.

### Benefits

- ⚡ **Fast Loading**: Load times reduced from 5-10 seconds to <1 second
- 🚀 **No CORS Issues**: Eliminates dependency on third-party proxy servers
- 📴 **Offline Capability**: Complete offline functionality with pre-scraped data
- 🔄 **Backward Compatible**: Automatically falls back to CORS proxies if local data unavailable

### Data Architecture

**Pre-Scraped Data:**
- 114 JSON files (one per surah) in `/data` folder
- Contains E'arab HTML and translations for all ~6,236 ayahs
- Total size: ~50-100MB
- Committed to repository for instant availability

**Loading Strategy:**
1. **Primary**: Load from local JSON files (`data/surah-{N}.json`)
2. **Fallback**: Use CORS proxies if local data unavailable

### Using the Scraper

#### Quick Start

```bash
cd scraper

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Scrape all surahs (takes 2-4 hours)
python scraper.py
```

#### Commands

```bash
# Scrape all 114 surahs
python scraper.py

# Test with single surah
python scraper.py --surah 1

# Scrape range of surahs
python scraper.py --start 1 --end 10
```

#### Output

- **Data files**: `data/surah-{1-114}.json`
- **Manifest**: `data/manifest.json` (index of all files)
- **Errors**: `data/scraping_errors.json` (if any errors occur)

### Scraper Features

- ✅ Respectful rate limiting (1 second between requests)
- ✅ Automatic retry with exponential backoff
- ✅ Progress bars and logging
- ✅ Error tracking and recovery
- ✅ Resume capability

See [scraper/README.md](scraper/README.md) for detailed documentation.

## APIs Used

### 1. Surah List API
**Endpoint**: `https://quranapi.pages.dev/api/surah.json`

**Purpose**: Fetches list of all 114 Surahs

**Response Structure**:
```json
[
  {
    "number": 1,
    "name": "Al-Fatihah",
    "englishName": "The Opening",
    "englishNameTranslation": "The Opening",
    "numberOfAyahs": 7,
    "revelationType": "Meccan"
  },
  ...
]
```

**Usage**: Populates the Surah dropdown on page load

### 2. Translation API
**Endpoint**: `https://quranapi.pages.dev/api/{surahNo}/{ayahNo}.json`

**Purpose**: Fetches translations for specific ayah

**Example**: `https://quranapi.pages.dev/api/3/4.json`

**Response Structure**:
```json
{
  "surahNo": 3,
  "surahName": "Ali 'Imran",
  "surahNameArabic": "آل عمران",
  "ayahNo": 4,
  "totalAyah": 200,
  "english": "English translation text...",
  "urdu": "اردو ترجمہ...",
  "arabic": "Arabic text..."
}
```

**Usage**: Displays English and Urdu translations after E'arab content

### 3. E'arab Content Source
**URL Pattern**: `https://surahquran.com/quran-search/e3rab-aya-{ayah}-sora-{surah}.html`

**Purpose**: Source for grammatical analysis content

**Example**: `https://surahquran.com/quran-search/e3rab-aya-4-sora-3.html`

**Access Method**: Fetched via CORS proxies (see Technical Architecture)

### 4. Morphology API (Sarf)
**Endpoint**: `https://aratools.com/api/v1/dictionary/lookup/ar/{word}?filter_diacritics=true&_={timestamp}`

**Purpose**: Fetches morphological analysis for Arabic words

**Example**: `https://aratools.com/api/v1/dictionary/lookup/ar/رددنا?filter_diacritics=true&_=1763286324737`

**Response Structure**:
```json
{
  "words": [
    {
      "form": "رددنا",
      "voc_form": "رَدَدْنا",
      "gloss": "answer;reply;return we <verb>",
      "nice_gloss": "we answer;reply;return",
      "pos": "radad/VERB_PERFECT+nA/PVSUFF_SUBJ:1P",
      "pos_abbr": "VERB_PERFECT_PVSUFF_SUBJ:1P",
      "pos_nice": "Perfect tense verb, suffixed subject (1. person, plural)",
      "lemma": "rad~-u_1",
      "root": "رد",
      "measure": "I",
      "tags": [...]
    }
  ]
}
```

**Usage**: Displays morphological breakdown in tabular format showing:
- Form: Vocalized Arabic form
- Gloss: English translation
- POS: Part of speech description
- Root: Arabic root letters
- Measure: Verb form (I-X)

## Technical Architecture

### CORS Proxy Implementation

Since surahquran.com doesn't allow direct cross-origin requests, the application uses multiple fallback CORS proxy services:

1. **api.allorigins.win** (Primary)
   - Format: `https://api.allorigins.win/get?url={encoded_url}`
   - Returns JSON with content in `contents` field

2. **corsproxy.io** (Fallback #1)
   - Format: `https://corsproxy.io/?{encoded_url}`
   - Returns raw HTML

3. **thingproxy.freeboard.io** (Fallback #2)
   - Format: `https://thingproxy.freeboard.io/fetch/{url}`
   - Returns raw HTML

4. **api.codetabs.com** (Fallback #3)
   - Format: `https://api.codetabs.com/v1/proxy?quest={encoded_url}`
   - Returns raw HTML

**Fallback Strategy**:
- Each proxy has 10-second timeout
- Automatically tries next proxy on failure
- Validates response content length (>100 chars)
- Proper JSON parsing for api.allorigins.win

### HTML Parsing

The application extracts E'arab content using the DOMParser API:

```javascript
const parser = new DOMParser();
const doc = parser.parseFromString(html, 'text/html');

// Extract title with id="e3rab"
const earabTitle = doc.querySelector('#e3rab');

// Extract first two .card.mt-3 elements
const cards = doc.querySelectorAll('.card.mt-3');
const firstTwoCards = Array.from(cards).slice(0, 2);
```

**Extracted Elements**:
- Title section (id="e3rab")
- First two card elements containing grammatical analysis

### Navigation System

**Features**:
- Previous/Next buttons for sequential ayah browsing
- Automatic boundary detection (disables at first/last ayah)
- Updates input field dynamically
- Fetches new E'arab and translation content
- Smooth scrolling to results section

**Implementation**:
```javascript
function navigateAyah(direction) {
    // Calculate new ayah number
    // Validate boundaries
    // Update UI and fetch new content
    // Smooth scroll to results
}
```

## How to Use

### E'arab Analysis (index.html)

1. **Select a Surah**: Choose from the dropdown menu (shows Arabic and English names)
2. **Enter Ayah Number**: Type the ayah number (validated against total ayahs)
3. **Click "عرض الإعراب"**: Displays E'arab content and translations
4. **Navigate**: Use Previous/Next buttons to browse sequential ayahs
5. **View Source**: Click "عرض الصفحة الأصلية" to open original page
6. **Switch to Sarf**: Click the "صرف القرآن (Morphology) →" button to analyze word morphology

### Morphology Analysis (sarf.html)

1. **Enter Arabic Word**: Type any Arabic word (e.g., رددنا)
2. **Click "تحليل الصرف"**: Analyzes and displays morphological breakdown
3. **View Results**: Table shows form, gloss, POS, root, and measure for all possible interpretations
4. **Switch to E'arab**: Click "← إعراب القرآن (E'arab)" to return to verse analysis

## Project Structure

### Application Files
The application consists of two standalone HTML files:

**`index.html`** - E'arab Analysis Page
- Surah and Ayah selection interface
- E'arab content display
- Translation display (English and Urdu)
- Navigation between ayahs
- Embedded CSS and JavaScript
- No external dependencies

**`sarf.html`** - Morphology Analysis Page
- Arabic word input interface
- Morphological analysis display
- Table-based result presentation
- Embedded CSS and JavaScript
- No external dependencies

### Key Components

**1. Form Section**
- Surah dropdown (populated from API)
- Ayah number input (with validation)
- Submit button

**2. Results Section**
- Navigation buttons (Previous/Next)
- E'arab content display
- Translation display (English and Urdu)
- Source link

**3. Loading States**
- Spinner animation during content fetch
- Disabled navigation during loading

## Responsive Design

### Breakpoints

**Desktop (default)**
- Max-width: 1000px
- Padding: 35px 30px
- Body padding: 20px 8px

**Tablet (≤768px)**
- Padding: 28px 22px
- Body padding: 15px 6px
- Reduced font sizes

**Mobile (≤480px)**
- Padding: 24px 18px
- Body padding: 12px 4px
- Compact layout
- Smaller borders and shadows

### Design Features
- Minimized side margins for maximum reading space
- Clean grey background (#f5f5f5)
- White card-style content container
- Soft shadows for depth
- Smooth animations (slide-in effects)

## Browser Compatibility

**Requirements**:
- Modern browser with JavaScript enabled
- Fetch API support
- DOMParser support
- CSS Flexbox support

**Tested On**:
- Chrome/Edge (Chromium)
- Firefox
- Safari

## Technical Details

### Technologies Used
- HTML5
- CSS3 (Flexbox, Media Queries, Animations)
- Vanilla JavaScript (ES6+)
- Fetch API
- DOMParser API
- AbortController (for timeouts)

### Key Functions

**`fetchSurahs()`**
- Fetches Surah list on page load
- Populates dropdown with 114 Surahs
- Error handling for API failures

**`populateSurahDropdown()`**
- Creates dropdown options
- Formats: "number. Arabic Name (English Name)"

**`validateAyah()`**
- Real-time validation of ayah input
- Enforces min (1) and max (totalAyah) boundaries

**`generateEarab()`**
- Main form submission handler
- Generates E'arab URL
- Fetches both E'arab and translation content
- Updates UI and navigation state

**`fetchEarabContent(url)`**
- Tries multiple CORS proxies with fallback
- Parses HTML to extract E'arab content
- Displays with loading states

**`fetchTranslation(surahNo, ayahNo)`**
- Fetches translation from API
- Displays English and Urdu
- Shows Surah info (name, ayah count)

**`navigateAyah(direction)`**
- Handles Previous/Next navigation
- Updates current ayah
- Fetches new content
- Smooth scrolling

**`updateNavigationButtons()`**
- Enables/disables buttons based on boundaries
- Prevents navigation beyond valid range

## Installation

No installation required! Simply:

1. Download `index.html`
2. Open in any modern web browser
3. Start learning E'arab

**OR**

Host on any static web server:
```bash
# Using Python
python -m http.server 8000

# Using Node.js (http-server)
npx http-server

# Then open http://localhost:8000
```

## Error Handling

**Common Errors and Solutions**:

1. **"عذراً، حدث خطأ أثناء تحميل السور"**
   - Cause: Failed to fetch Surah list
   - Solution: Check internet connection, refresh page

2. **"عذراً، حدث خطأ أثناء تحميل الإعراب"**
   - Cause: All CORS proxies failed
   - Solution: Use "عرض الصفحة الأصلية" link to view original page

3. **"عذراً، حدث خطأ أثناء تحميل الترجمة"**
   - Cause: Translation API failed
   - Solution: Check internet connection, try different ayah

## Future Enhancements

Potential features for future development:
- Offline support with Service Workers
- Bookmark favorite ayahs
- Search functionality
- Additional translations (Bengali, Turkish, etc.)
- Audio recitation integration
- Tafsir (commentary) display
- Dark mode toggle
- Export to PDF

## Credits

**Data Sources**:
- Surah and Translation API: [quranapi.pages.dev](https://quranapi.pages.dev)
- E'arab Content: [surahquran.com](https://surahquran.com)
- Morphology API: [aratools.com](https://aratools.com)

**CORS Proxies**:
- api.allorigins.win
- corsproxy.io
- thingproxy.freeboard.io
- api.codetabs.com

## License

This project is open source and available for educational purposes.

---

**Note**: This application requires an active internet connection to fetch Surah data, E'arab content, morphological analysis, and translations from external APIs.
