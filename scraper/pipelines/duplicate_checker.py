"""
Duplicate Checker module for the FinPulse scraper pipeline.

Checks whether an article URL already exists in the database to avoid
storing duplicate articles. Specification defined in 07_SCRAPER.md section 11.
"""
import logging
from typing import Optional
from sqlalchemy.orm import Session
from app.repositories.news import news_repo

logger = logging.getLogger(__name__)


class DuplicateChecker:
    """
    Checks article URLs against the database to identify duplicates.
    Uses the news repository's get_by_url method for the lookup.
    """

    def __init__(self, repo=news_repo):
        self.repo = repo

    def is_duplicate(self, db: Session, url: str) -> bool:
        """
        Checks if an article with the given URL already exists in the database.

        Per spec section 11: duplicate detection is based on URL.
        If the URL already exists, the article is skipped.

        Args:
            db: SQLAlchemy database session.
            url: The article URL to check.

        Returns:
            True if the URL already exists (duplicate), False otherwise.
        """
        if not url:
            logger.warning("DuplicateChecker received empty URL, treating as duplicate.")
            return True

        existing = self.repo.get_by_url(db, url)
        is_dup = existing is not None

        if is_dup:
            logger.info(f"Duplicate article found, skipping URL: {url[:80]}")
        else:
            logger.debug(f"URL is new: {url[:80]}")

        return is_dup


duplicate_checker = DuplicateChecker()