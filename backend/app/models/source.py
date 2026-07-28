import uuid
from typing import TYPE_CHECKING, List
from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.news import News
    from app.models.log import ScrapeLog

class NewsSource(BaseModel):
    """
    SQLAlchemy model representing a news source (e.g., CNBC Indonesia, Reuters).
    Maps to the 'news_sources' plural table.
    """
    __tablename__ = "news_sources"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    website: Mapped[str] = mapped_column(Text, nullable=False)
    rss_url: Mapped[str] = mapped_column(Text, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    news: Mapped[List["News"]] = relationship(
        "News",
        back_populates="source",
        cascade="all, delete-orphan"
    )
    logs: Mapped[List["ScrapeLog"]] = relationship(
        "ScrapeLog",
        back_populates="source",
        cascade="all, delete-orphan"
    )
