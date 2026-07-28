import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class Normalizer:
    """
    Normalizes raw news data into a consistent format required by the application.
    This includes creating a slug, cleaning text, and ensuring data types are correct.
    """
    async def normalize(self, news_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Normalizes a single piece of news data.
        
        Args:
            news_data (Dict[str, Any]): Raw news data dictionary from a parser.
            
        Returns:
            Optional[Dict[str, Any]]: Normalized news data, or None if essential data is missing.
        """
        if not news_data or not news_data.get("title") or not news_data.get("url"): 
            logger.warning("Skipping normalization due to missing title or URL.")
            return None

        published_at = news_data.get("published_at")
        if published_at is not None:
            # Ensure published_at is timezone-aware (UTC)
            if isinstance(published_at, datetime):
                if published_at.tzinfo is None:
                    published_at = published_at.replace(tzinfo=timezone.utc)
            else:
                published_at = None

        normalized_data = {
            "title": self._clean_text(news_data["title"]),
            "slug": self._slugify(news_data["title"]),  # Generate URL-friendly slug
            "url": news_data["url"], # URL is kept as is for duplicate checking
            "thumbnail": news_data.get("thumbnail"),
            "published_at": published_at,
            "summary": self._clean_text(news_data.get("summary")) if news_data.get("summary") else None,
            "content": self._clean_text(news_data.get("content")) if news_data.get("content") else None,
            "source_name": news_data.get("source_name"),
            # sentiment and scraped_at will be added later in the pipeline
        }

        logger.info(f"Normalized news: {normalized_data.get("title")}")
        return normalized_data

    def _slugify(self, text: str) -> str:
        """
        Create a simple URL-safe slug without external dependencies.
        """
        cleaned = self._clean_text(text) or ""
        slug = cleaned.lower()
        slug = re.sub(r"[^a-z0-9\s-]", "", slug)
        slug = re.sub(r"[\s_-]+", "-", slug)
        slug = re.sub(r"^-+|-+$", "", slug)
        return slug or "untitled"

    def _clean_text(self, text: Optional[str]) -> Optional[str]:
        """
        Cleans text by stripping whitespace and ensuring consistent spacing.
        
        Args:
            text (Optional[str]): The input text.
            
        Returns:
            Optional[str]: Cleaned text, or None if input is None.
        """
        if text is None:
            return None
        # Remove extra whitespace and replace multiple spaces with single space
        cleaned_text = re.sub(r"\s+", " ", text).strip()
        return cleaned_text

normalizer = Normalizer()
