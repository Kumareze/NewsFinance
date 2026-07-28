"""
Validator module for the FinPulse scraper pipeline.

Ensures that normalized articles meet the minimum quality requirements
before being saved to the database. Specification defined in 07_SCRAPER.md section 10.
"""
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


REQUIRED_FIELDS = ["title", "url", "source_name", "published_at"]


def validate_article(article: Optional[Dict[str, Any]]) -> bool:
    """
    Validates a normalized article dictionary.

    An article is considered valid if it has all required fields with truthy values.

    Required fields (per spec section 10):
        - title
        - url
        - published_at
        - source_name

    Args:
        article: The normalized article dictionary.

    Returns:
        True if the article is valid, False otherwise.
    """
    if not article or not isinstance(article, dict):
        logger.warning("Validation failed: article is None or not a dict.")
        return False

    missing = []
    for field in REQUIRED_FIELDS:
        value = article.get(field)
        if not value:
            missing.append(field)

    if missing:
        logger.warning(
            f"Validation failed for article '{article.get('title', 'N/A')[:50]}': "
            f"missing fields: {', '.join(missing)}"
        )
        return False

    # Additional quality checks per spec section 23
    title = str(article.get("title", "")).strip()
    if len(title) < 3:
        logger.warning(
            f"Validation failed: title too short '{title[:50]}'"
        )
        return False

    url = str(article.get("url", "")).strip()
    if not url.startswith(("http://", "https://")):
        logger.warning(
            f"Validation failed: invalid URL format '{url[:80]}'"
        )
        return False

    logger.debug(f"Article passed validation: '{title[:50]}'")
    return True