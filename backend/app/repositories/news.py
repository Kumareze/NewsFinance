from typing import List, Optional
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from app.models.news import News
from app.models.source import NewsSource
from app.repositories.base import BaseRepository

class NewsRepository(BaseRepository[News]):
    """
    Repository class specialized for handling 'news' table queries,
    including advanced filtering, search capabilities, and count aggregations.
    """
    def __init__(self):
        super().__init__(News)

    def get_by_slug(self, db: Session, slug: str) -> Optional[News]:
        """Fetch a single news article by its unique SEO slug."""
        return db.query(self.model).filter(self.model.slug == slug).first()

    def get_by_url(self, db: Session, url: str) -> Optional[News]:
        """Fetch a single news article by its original article source URL."""
        return db.query(self.model).filter(self.model.url == url).first()

    def get_filtered(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 20,
        sentiment: Optional[str] = None,
        source_name: Optional[str] = None,
        sort: str = "latest"
    ) -> List[News]:
        """
        Query articles with support for paginating, filtering on sentiment level
        and publishing source, and ordering results.
        """
        query = db.query(self.model).join(NewsSource)

        if sentiment and sentiment != "all":
            query = query.filter(self.model.sentiment == sentiment.lower())

        if source_name and source_name != "all":
            query = query.filter(NewsSource.name == source_name)

        if sort == "latest":
            query = query.order_by(desc(self.model.published_at))
        elif sort == "oldest":
            query = query.order_by(asc(self.model.published_at))

        return query.offset(skip).limit(limit).all()

    def get_filtered_count(
        self,
        db: Session,
        *,
        sentiment: Optional[str] = None,
        source_name: Optional[str] = None
    ) -> int:
        """
        Get total matching articles count based on sentiment or news source filters.
        Used primarily for calculating pagination offsets on the client.
        """
        query = db.query(self.model).join(NewsSource)

        if sentiment and sentiment != "all":
            query = query.filter(self.model.sentiment == sentiment.lower())

        if source_name and source_name != "all":
            query = query.filter(NewsSource.name == source_name)

        return query.count()

    def search(self, db: Session, *, q: str, skip: int = 0, limit: int = 20) -> List[News]:
        """
        Perform a case-insensitive keyword search on article titles.
        Returns matching records sorted by most recently published first.
        """
        return (
            db.query(self.model)
            .filter(self.model.title.ilike(f"%{q}%"))
            .order_by(desc(self.model.published_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_count(self, db: Session, *, q: str) -> int:
        """Get total matching articles count for a keyword search query."""
        return db.query(self.model).filter(self.model.title.ilike(f"%{q}%")).count()

news_repo = NewsRepository()
