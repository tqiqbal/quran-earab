"""
HTTP fetcher with retry logic and rate limiting
"""

import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from typing import Optional, Dict, Any
import time
from .logger import get_logger

logger = get_logger(__name__)


class HTTPFetcher:
    """Handles HTTP requests with retry logic and rate limiting"""

    def __init__(self, timeout: int = 30, rate_limit: float = 1.0):
        """
        Initialize HTTP fetcher

        Args:
            timeout: Request timeout in seconds
            rate_limit: Minimum seconds between requests
        """
        self.timeout = timeout
        self.rate_limit = rate_limit
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.last_request_time = 0

    def _rate_limit_wait(self):
        """Enforce rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def fetch_html(self, url: str) -> str:
        """
        Fetch HTML content with retry logic

        Args:
            url: URL to fetch

        Returns:
            HTML content as string

        Raises:
            requests.RequestException: If all retries fail
            ValueError: If response is too short
        """
        self._rate_limit_wait()
        logger.debug(f"Fetching HTML: {url}")

        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        response.encoding = 'utf-8'

        if len(response.text) < 100:
            raise ValueError(f"Response too short ({len(response.text)} chars)")

        return response.text

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def fetch_json(self, url: str) -> Dict[str, Any]:
        """
        Fetch JSON data with retry logic

        Args:
            url: URL to fetch

        Returns:
            Parsed JSON as dictionary

        Raises:
            requests.RequestException: If all retries fail
        """
        self._rate_limit_wait()
        logger.debug(f"Fetching JSON: {url}")

        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()

        return response.json()
