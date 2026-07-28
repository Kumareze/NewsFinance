import logging
import httpx
import feedparser
from typing import Any, Dict, Optional
from scraper.base.fetcher import BaseFetcher

logger = logging.getLogger(__name__)

# Browser-like User-Agent to avoid 403 from many news sites
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
}

class RssFetcher(BaseFetcher):
    """
    Fetches content from an RSS feed URL.
    Uses httpx for HTTP requests and feedparser for RSS parsing.
    Follows redirects automatically and sends browser-like headers.
    """
    async def fetch(self, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Fetches and parses an RSS feed.
        
        Args:
            url (str): The RSS feed URL to fetch.
            **kwargs: Arbitrary keyword arguments (e.g., timeout, headers) passed to httpx.get.
            
        Returns:
            Optional[Dict[str, Any]]: A dictionary representation of the parsed RSS feed
                                     (as returned by feedparser), or None if fetching fails.
        """
        try:
            timeout = kwargs.get("timeout", 30)  # Default to 30 seconds timeout
            # Merge provided headers with defaults; provided headers override defaults
            custom_headers = kwargs.get("headers", {})
            headers = {**DEFAULT_HEADERS, **custom_headers}
            
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(url, timeout=timeout, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
                
            feed = feedparser.parse(response.text)
            logger.info(f"Successfully fetched and parsed RSS feed from {url}")
            return feed
            
        except httpx.RequestError as e:
            logger.error(f"HTTPX Request Error while fetching RSS from {url}: {e}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Status Error {e.response.status_code} while fetching RSS from {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred while fetching RSS from {url}: {e}")
            return None

rss_fetcher = RssFetcher()