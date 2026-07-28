"""
Generic RSS Parser for FinPulse.

Works with any standard RSS feed. Extracts title, URL, thumbnail,
published date, and summary from feedparser output.
No source-specific logic needed since feedparser normalizes fields.
"""
import logging
from datetime import datetime
from typing import Any, Dict, Optional
from bs4 import BeautifulSoup
from scraper.base.parser import BaseParser

logger = logging.getLogger(__name__)

class GenericParser(BaseParser):
    """
    Parses RSS feed entries from any standard RSS source.
    Uses feedparser's normalized field names so it works universally.
    """

    async def parse(self, raw_content: Dict[str, Any], **kwargs) -> Optional[Dict[str, Any]]:
        """
        Parses a single RSS feed entry from any source.

        Args:
            raw_content (Dict[str, Any]): A dictionary representing an RSS entry from feedparser.

        Returns:
            Optional[Dict[str, Any]]: A dictionary with extracted news data, or None if parsing fails.
        """
        try:
            title = raw_content.get("title")
            link = raw_content.get("link")
            published_parsed = raw_content.get("published_parsed")
            summary = raw_content.get("summary") or raw_content.get("description")

            if not title or not link:
                logger.warning(f"Skipping incomplete RSS entry: {title or 'N/A'}")
                return None

            published_at = None
            if published_parsed:
                try:
                    published_at = datetime(*published_parsed[:6])
                except (TypeError, ValueError):
                    published_at = None

            # Extract thumbnail from various standard locations
            thumbnail = None

            # 1. media_thumbnail (standard RSS media extension)
            media_thumb = raw_content.get("media_thumbnail")
            if media_thumb and isinstance(media_thumb, list) and len(media_thumb) > 0:
                thumbnail = media_thumb[0].get("url")

            # 2. media_content
            if not thumbnail:
                media_content = raw_content.get("media_content")
                if media_content and isinstance(media_content, list) and len(media_content) > 0:
                    thumbnail = media_content[0].get("url")

            # 3. links with image type
            if not thumbnail:
                links = raw_content.get("links", [])
                for link in links:
                    if link.get("type", "").startswith("image/"):
                        thumbnail = link.get("href")
                        break

            # 4. extracted from summary HTML
            if not thumbnail and summary:
                soup = BeautifulSoup(summary, "html.parser")
                img_tag = soup.find("img")
                if img_tag and img_tag.get("src"):
                    thumbnail = img_tag.get("src")

            # Clean summary HTML to plain text
            clean_summary = None
            if summary:
                clean_summary = BeautifulSoup(summary, "html.parser").get_text(
                    separator=" ", strip=True
                )

            return {
                "title": title,
                "url": link,
                "thumbnail": thumbnail,
                "published_at": published_at,
                "summary": clean_summary,
                "source_name": None,  # Will be filled by pipeline
            }
        except Exception as e:
            logger.error(f"Error parsing generic RSS entry {raw_content.get('link', 'N/A')}: {e}")
            return None

    async def parse_article_content(self, url: str, html_content: str, **kwargs) -> Optional[str]:
        """
        Generic article content extraction from HTML.
        Tries common article container patterns.
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # Try common article content selectors
            for selector in [
                "article", "main", ".article-body", ".article-content",
                ".story-body", ".entry-content", ".post-content",
                "#article-body", "#story-body", '[itemprop="articleBody"]',
            ]:
                content_div = soup.select_one(selector)
                if content_div:
                    # Remove unwanted elements
                    for unwanted in content_div.find_all(["script", "style", "nav", "footer", "aside"]):
                        unwanted.extract()
                    content = content_div.get_text(separator=" ", strip=True)
                    if len(content) > 100:  # Only accept if we got meaningful content
                        logger.info(f"Extracted article content from {url} using selector '{selector}'")
                        return content

            logger.warning(f"Could not extract article content from {url}")
            return None
        except Exception as e:
            logger.error(f"Error parsing article content from {url}: {e}")
            return None


generic_parser = GenericParser()