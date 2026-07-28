from typing import Optional
from sqlalchemy.orm import Session
from app.models.log import ScrapeLog
from app.repositories.log import scrape_log_repo
from app.schemas.log import ScrapeLogCreate

class ScrapeLogService:
    """
    Service layer for managing scrape log entries.
    Primarily handles recording and retrieving scraping operation logs.
    """
    def __init__(self, repository: scrape_log_repo = scrape_log_repo):
        self.repository = repository

    def create_scrape_log(self, db: Session, log_in: ScrapeLogCreate) -> ScrapeLog:
        """
        Create a new scrape log entry.
        """
        obj_in_data = log_in.model_dump()
        db_obj = ScrapeLog(**obj_in_data)
        return self.repository.create(db, obj=db_obj)

    def get_latest_log_for_source(self, db: Session, source_id: str) -> Optional[ScrapeLog]:
        """
        Retrieve the most recent scrape log for a specific news source.
        """
        return self.repository.get_latest_log_for_source(db, source_id)

scrape_log_service = ScrapeLogService()
