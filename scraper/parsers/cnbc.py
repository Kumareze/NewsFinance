import logging
from datetime import datetime
from typing import Any, Dict, Optional
from bs4 import BeautifulSoup
from scraper.base.parser import BaseParser

logger = logging.getLogger(__name__)

class CnbcParser(BaseParser):
    """
    Parses RSS feed entries and full article HTML for CNBC Indonesia.
    Extracts title, URL, thumbnail, published date, summary, and content.
    """

    async def parse(self, raw_content: Dict[str, Any], **kwargs) -> Optional[Dict[str, Any]]:
        """
        Parses a single RSS feed entry from CNBC Indonesia.
        
        Args:
            raw_content (Dict[str, Any]): A dictionary representing an RSS entry from feedparser.
            
        Returns:
            Optional[Dict[str, Any]]: A dictionary with extracted news data, or None if parsing fails.
        """
        try:
            title = raw_content.get("title")
            link = raw_content.get("link")
            published_parsed = raw_content.get("published_parsed")
            summary = raw_content.get("summary")
            
            if not all([title, link, published_parsed]):
                logger.warning(f"Skipping incomplete RSS entry: {raw_content.get("title", "N/A")}")
                return None
            
            published_at = datetime(*published_parsed[:6]) if published_parsed else None
            
            # Extract thumbnail from media_thumbnail if available
            thumbnail = None
            if "media_thumbnail" in raw_content and raw_content["media_thumbnail"]:
                # media_thumbnail is often a list, take the first one
                thumbnail = raw_content["media_thumbnail"][0].get("url")
            
            # Fallback to searching in summary HTML for an image
            if not thumbnail and summary:
                soup = BeautifulSoup(summary, "html.parser")
                img_tag = soup.find("img")
                if img_tag and img_tag.get("src"):
                    thumbnail = img_tag.get("src")

            return {
                "title": title,
                "url": link,
                "thumbnail": thumbnail,
                "published_at": published_at,
                "summary": BeautifulSoup(summary, "html.parser").get_text(separator=" ", strip=True) if summary else None,
                "source_name": "CNBC Indonesia" # Hardcoded as this parser is specific
            }
        except Exception as e:
            logger.error(f"Error parsing CNBC RSS entry {raw_content.get("link", "N/A")}: {e}")
            return None

    async def parse_article_content(self, url: str, html_content: str, **kwargs) -> Optional[str]:
        """
        Parses the main article content from CNBC Indonesia\'s HTML page.
        
        Args:
            url (str): The URL of the article page.
            html_content (str): The raw HTML content of the article page.
            
        Returns:
            Optional[str]: The extracted main article content as a string, or None if extraction fails.
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            # CNBC article content is typically within a div with specific classes
            content_div = soup.find("div", class_="detail_text") # Adjust class as needed for CNBC
            
            if content_div:
                # Remove unwanted elements like share buttons, ads, etc.
                for unwanted in content_div.find_all(["div", "script", "style", "figure"]): 
                    unwanted.extract()
                
                content = content_div.get_text(separator=" ", strip=True)
                logger.info(f"Successfully extracted article content from {url}")
                return content
            
            logger.warning(f"Could not find main content div for CNBC article: {url}")
            return None
        except Exception as e:
            logger.error(f"Error parsing CNBC article content from {url}: {e}")
            return None

cnbc_parser = CnbcParser()
