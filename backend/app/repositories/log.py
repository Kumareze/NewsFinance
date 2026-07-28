from typing import Optional
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.models.log import ScrapeLog
from app.repositories.base import BaseRepository

class ScrapeLogRepository(BaseRepository[ScrapeLog]):
    """
    Repository class specialized for handling 'scrape_logs' table queries.
    """
    def __init__(self):
        super().__init__(ScrapeLog)

    def get_latest_log_for_source(self, db: Session, source_id: any) -> Optional[ScrapeLog]:
        """Fetch the most recent scrape log entry for a specific news source."""
        return (
            db.query(self.model)
            .filter(self.model.source_id == source_id)
            .order_by(desc(self.model.started_at))
            .first()
        )

scrape_log_repo = ScrapeLogRepository()
