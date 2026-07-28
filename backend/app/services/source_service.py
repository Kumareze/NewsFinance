from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.source import NewsSource
from app.repositories.source import news_source_repo
from app.schemas.source import SourceCreate, SourceUpdate

class NewsSourceService:
    """
    Service layer for managing news sources.
    Handles business logic related to fetching, creating, and updating news sources.
    """
    def __init__(self, repository: news_source_repo = news_source_repo):
        self.repository = repository

    def get_source_by_id(self, db: Session, source_id: str) -> Optional[NewsSource]:
        """Retrieve a single news source by its unique ID."""
        return self.repository.get(db, source_id)

    def get_source_by_name(self, db: Session, name: str) -> Optional[NewsSource]:
        """Retrieve a news source by its unique name."""
        return self.repository.get_by_name(db, name)

    def get_all_sources(self, db: Session, skip: int = 0, limit: int = 100) -> List[NewsSource]:
        """Retrieve multiple news sources with pagination."""
        return self.repository.get_multi(db, skip=skip, limit=limit)

    def get_active_news_sources(self, db: Session) -> List[NewsSource]:
        """Retrieve all active news sources."""
        return self.repository.get_active_sources(db)

    def create_news_source(self, db: Session, source_in: SourceCreate) -> NewsSource:
        """
        Create a new news source.
        Checks for duplicate names or RSS URLs before creation.
        """
        existing_by_name = self.repository.get_by_name(db, source_in.name)
        if existing_by_name:
            raise ValueError(f"News source with name '{source_in.name}' already exists.")

        existing_by_rss = self.repository.get_by_rss_url(db, source_in.rss_url)
        if existing_by_rss:
            raise ValueError(f"News source with RSS URL '{source_in.rss_url}' already exists.")

        obj_in_data = source_in.model_dump()
        db_obj = NewsSource(**obj_in_data)
        return self.repository.create(db, obj=db_obj)

    def update_news_source(self, db: Session, source_id: str, source_in: SourceUpdate) -> Optional[NewsSource]:
        """
        Update an existing news source.
        Checks for duplicate names or RSS URLs (excluding current source) before update.
        """
        db_obj = self.repository.get(db, source_id)
        if not db_obj:
            return None

        update_data = source_in.model_dump(exclude_unset=True)

        if "name" in update_data and update_data["name"] != db_obj.name:
            existing_by_name = self.repository.get_by_name(db, update_data["name"])
            if existing_by_name and existing_by_name.id != db_obj.id:
                raise ValueError(f"News source with name '{update_data["name"]}' already exists.")

        if "rss_url" in update_data and update_data["rss_url"] != db_obj.rss_url:
            existing_by_rss = self.repository.get_by_rss_url(db, update_data["rss_url"])
            if existing_by_rss and existing_by_rss.id != db_obj.id:
                raise ValueError(f"News source with RSS URL '{update_data["rss_url"]}' already exists.")

        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete_news_source(self, db: Session, source_id: str) -> Optional[NewsSource]:
        """Delete a news source by its ID."""
        return self.repository.delete(db, id=source_id)

news_source_service = NewsSourceService()