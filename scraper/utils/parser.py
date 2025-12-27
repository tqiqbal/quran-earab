"""
HTML parser for E'arab content
"""

from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from .logger import get_logger

logger = get_logger(__name__)


class EarabParser:
    """Parses E'arab HTML content from surahquran.com"""

    def __init__(self, html: str):
        """
        Initialize parser with HTML content

        Args:
            html: Raw HTML string
        """
        self.soup = BeautifulSoup(html, 'lxml')

    def extract_earab_data(self, max_cards: int = 2) -> Dict[str, any]:
        """
        Extract E'arab title and cards as raw HTML

        Args:
            max_cards: Maximum number of cards to extract (default: 2)

        Returns:
            Dictionary with title_html and cards_html
        """
        data = {
            'title_html': None,
            'cards_html': []
        }

        # Extract title with id="e3rab"
        title_elem = self.soup.select_one('#e3rab')
        if title_elem:
            data['title_html'] = str(title_elem)
            logger.debug("Extracted E'arab title")
        else:
            logger.warning("E'arab title (#e3rab) not found")

        # Extract first N cards with class .card.mt-3
        card_elems = self.soup.select('.card.mt-3')
        if card_elems:
            for card in card_elems[:max_cards]:
                data['cards_html'].append(str(card))
            logger.debug(f"Extracted {min(len(card_elems), max_cards)} cards")
        else:
            logger.warning("No E'arab cards (.card.mt-3) found")

        return data

    def get_full_page_html(self) -> str:
        """
        Get the complete HTML (fallback option)

        Returns:
            Full HTML content as string
        """
        return str(self.soup)
