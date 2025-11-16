# Quran E'arab Learning Application

A single-page web application for learning Arabic grammatical analysis (E'arab/إعراب) of Quranic verses with integrated translations.

## Features

- **Surah Selection**: Dropdown menu with all 114 Surahs (Arabic and English names)
- **Ayah Input**: Smart validation preventing invalid ayah numbers
- **E'arab Display**: Grammatical analysis fetched and displayed from surahquran.com
- **Translations**: English and Urdu translations for selected verses
- **Navigation**: Previous/Next buttons for seamless ayah browsing
- **Responsive Design**: Mobile-friendly layout with optimized spacing
- **RTL Support**: Proper right-to-left rendering for Arabic and Urdu text
- **Loading States**: Visual feedback with spinners during content fetching
- **Error Handling**: Graceful error messages in Arabic

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

1. **Select a Surah**: Choose from the dropdown menu (shows Arabic and English names)
2. **Enter Ayah Number**: Type the ayah number (validated against total ayahs)
3. **Click "عرض الإعراب"**: Displays E'arab content and translations
4. **Navigate**: Use Previous/Next buttons to browse sequential ayahs
5. **View Source**: Click "عرض الصفحة الأصلية" to open original page

## Project Structure

### Single File Application
The entire application is contained in `index.html` with:
- HTML structure
- Embedded CSS styles
- JavaScript functionality
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

**CORS Proxies**:
- api.allorigins.win
- corsproxy.io
- thingproxy.freeboard.io
- api.codetabs.com

## License

This project is open source and available for educational purposes.

---

**Note**: This application requires an active internet connection to fetch Surah data, E'arab content, and translations from external APIs.
