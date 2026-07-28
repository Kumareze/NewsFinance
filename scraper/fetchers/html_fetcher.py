import logging
import httpx
from typing import Any, Dict, Optional
from scraper.base.fetcher import BaseFetcher

logger = logging.getLogger(__name__)

class HtmlFetcher(BaseFetcher):
    """
    Fetches raw HTML content from a given URL.
    Uses httpx for making asynchronous HTTP requests.
    """
    async def fetch(self, url: str, **kwargs) -> Optional[str]:
        """
        Fetches HTML content from the specified URL.
        
        Args:
            url (str): The URL to fetch HTML from.
            **kwargs: Arbitrary keyword arguments (e.g., timeout, headers) passed to httpx.get.
            
        Returns:
            Optional[str]: The raw HTML content as a string if successful, otherwise None.
        """
        try:
            timeout = kwargs.get("timeout", 10)  # Default to 10 seconds timeout
            headers = kwargs.get("headers", {
                "User-Agent": "FinPulseBot/1.0 (https://finpulse.com)" # Custom User-Agent
            })
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=timeout, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
                
            logger.info(f"Successfully fetched HTML from {url}")
            return response.text
            
        except httpx.RequestError as e:
            logger.error(f"HTTPX Request Error while fetching HTML from {url}: {e}")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP Status Error {e.response.status_code} while fetching HTML from {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred while fetching HTML from {url}: {e}")
            return None

html_fetcher = HtmlFetcher()
