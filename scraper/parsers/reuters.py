import logging
from datetime import datetime
from typing import Any, Dict, Optional
from bs4 import BeautifulSoup
from scraper.base.parser import BaseParser

logger = logging.getLogger(__name__)

class ReutersParser(BaseParser):
    """
    Parses RSS feed entries and full article HTML for Reuters.
    Extracts title, URL, thumbnail, published date, summary, and content.
    """

    async def parse(self, raw_content: Dict[str, Any], **kwargs) -> Optional[Dict[str, Any]]:
        """
        Parses a single RSS feed entry from Reuters.
        
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
            
            # Reuters RSS often includes an image in the summary or media_content
            thumbnail = None
            if "media_content" in raw_content and raw_content["media_content"]:
                thumbnail = raw_content["media_content"][0].get("url")
            
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
                "source_name": "Reuters" # Hardcoded as this parser is specific
            }
        except Exception as e:
            logger.error(f"Error parsing Reuters RSS entry {raw_content.get("link", "N/A")}: {e}")
            return None

    async def parse_article_content(self, url: str, html_content: str, **kwargs) -> Optional[str]:
        """
        Parses the main article content from Reuters HTML page.
        
        Args:
            url (str): The URL of the article page.
            html_content (str): The raw HTML content of the article page.
            
        Returns:
            Optional[str]: The extracted main article content as a string, or None if extraction fails.
        """
        try:
            soup = BeautifulSoup(html_content, "html.parser")
            # Reuters article content is typically within specific divs/paragraphs
            # This can vary greatly, so a common approach is to look for article body or specific section
            article_body = soup.find("div", class_="ArticleBody_body__NY5aQ") # Example class, needs verification

            if not article_body:
                # Fallback for older/different layouts or when the primary class is not found
                article_body = soup.find("div", class_="StandardArticleBody_body__C4AS6") # Another common class
            
            if article_body:
                # Remove unwanted elements like share buttons, ads, etc.
                for unwanted in article_body.find_all(["div", "script", "style", "figure", "p", "blockquote"]):
                    # Example of content to exclude
                    if unwanted.get_text(strip=True).startswith("Reporting by") or \
                       unwanted.get_text(strip=True).startswith("Our Standards:"):
                        unwanted.extract()
                
                content = article_body.get_text(separator=" ", strip=True)
                logger.info(f"Successfully extracted article content from {url}")
                return content
            
            logger.warning(f"Could not find main content div for Reuters article: {url}")
            return None
        except Exception as e:
            logger.error(f"Error parsing Reuters article content from {url}: {e}")
            return None

reuters_parser = ReutersParser()
