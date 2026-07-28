import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.source import NewsSource

class ScrapeLog(BaseModel):
    """
    SQLAlchemy model representing a log entry for scraper execution monitoring.
    Maps to the 'scrape_logs' table.
    """
    __tablename__ = "scrape_logs"

    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("news_sources.id", ondelete="CASCADE"),
        nullable=False
    )
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    total_news: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    success_news: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    failed_news: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationships
    source: Mapped["NewsSource"] = relationship("NewsSource", back_populates="logs")
