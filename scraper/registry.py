import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.source import NewsSource
from app.services.source_service import news_source_service

logger = logging.getLogger(__name__)

class SourceRegistry:
    """
    Manages the registration and retrieval of active news sources from the database.
    This acts as a central point for scraper components to discover which sources to process.
    """
    def __init__(self, service: news_source_service = news_source_service):
        self.service = service

    def get_active_sources(self, db: Session) -> List[NewsSource]:
        """
        Fetches all news sources currently marked as active in the database.
        
        Args:
            db (Session): The database session.
            
        Returns:
            List[NewsSource]: A list of active NewsSource objects.
        """
        try:
            active_sources = self.service.get_active_news_sources(db)
            logger.info(f"Retrieved {len(active_sources)} active news sources.")
            return active_sources
        except Exception as e:
            logger.error(f"Error retrieving active news sources: {e}")
            return []

source_registry = SourceRegistry()
