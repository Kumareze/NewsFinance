from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.news import News
from app.repositories.news import news_repo
from app.schemas.news import NewsCreate, NewsUpdate

class NewsService:
    """
    Service layer for managing news articles.
    Handles business logic related to fetching, creating, updating, and searching news.
    """
    def __init__(self, repository: news_repo = news_repo):
        self.repository = repository

    def get_news_article(self, db: Session, slug: str) -> Optional[News]:
        """Retrieve a single news article by its slug."""
        return self.repository.get_by_slug(db, slug)

    def get_multiple_news(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 20,
        sentiment: Optional[str] = None,
        source_name: Optional[str] = None,
        sort: str = "latest"
    ) -> List[News]:
        """
        Retrieve multiple news articles with pagination, filtering, and sorting.
        """
        return self.repository.get_filtered(
            db,
            skip=skip,
            limit=limit,
            sentiment=sentiment,
            source_name=source_name,
            sort=sort
        )

    def count_news(
        self,
        db: Session,
        sentiment: Optional[str] = None,
        source_name: Optional[str] = None
    ) -> int:
        """Count total news articles based on filters."""
        return self.repository.get_filtered_count(
            db,
            sentiment=sentiment,
            source_name=source_name
        )

    def search_news(
        self,
        db: Session,
        q: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[News]:
        """
        Search news articles by title keyword with pagination.
        """
        return self.repository.search(db, q=q, skip=skip, limit=limit)

    def count_search_results(self, db: Session, q: str) -> int:
        """Count total news articles matching a search query."""
        return self.repository.search_count(db, q=q)

    def create_news(self, db: Session, news_in: NewsCreate) -> News:
        """
        Create a new news article.
        Note: In FinPulse, news creation is primarily handled by the scraper.
        This method is provided for completeness or admin use.
        """
        obj_in_data = news_in.model_dump()
        db_obj = News(**obj_in_data)
        return self.repository.create(db, obj=db_obj)

    def update_news(self, db: Session, slug: str, news_in: NewsUpdate) -> Optional[News]:
        """
        Update an existing news article.
        Note: In FinPulse, news updates are not a primary use case via API.
        This is for completeness or admin use.
        """
        db_obj = self.repository.get_by_slug(db, slug)
        if not db_obj:
            return None
        
        for field, value in news_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_news(self, db: Session, slug: str) -> Optional[News]:
        """
        Delete a news article by its slug.
        Note: Data retention policy handles automated deletion for old news.
        This method is for completeness or admin use.
        """
        news_article = self.repository.get_by_slug(db, slug)
        if news_article:
            return self.repository.delete(db, id=news_article.id)
        return None

news_service = NewsService()
