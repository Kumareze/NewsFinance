from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.source import NewsSource
from app.repositories.base import BaseRepository

class NewsSourceRepository(BaseRepository[NewsSource]):
    """
    Repository class specialized for handling 'news_sources' table queries.
    """
    def __init__(self):
        super().__init__(NewsSource)

    def get_by_name(self, db: Session, name: str) -> Optional[NewsSource]:
        """Fetch a news source by its unique media name."""
        return db.query(self.model).filter(self.model.name == name).first()

    def get_by_rss_url(self, db: Session, rss_url: str) -> Optional[NewsSource]:
        """Fetch a news source by its RSS Feed URL."""
        return db.query(self.model).filter(self.model.rss_url == rss_url).first()

    def get_active_sources(self, db: Session) -> List[NewsSource]:
        """Fetch all currently active news sources."""
        return db.query(self.model).filter(self.model.active == True).all()

news_source_repo = NewsSourceRepository()
