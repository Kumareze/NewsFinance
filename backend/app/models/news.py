import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Text, String, DateTime, ForeignKey, Index, CheckConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.source import NewsSource

class News(BaseModel):
    """
    SQLAlchemy model representing a news article.
    Maps to the 'news' table with constraints and indexes for high performance.
    """
    __tablename__ = "news"

    source_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("news_sources.id", ondelete="CASCADE"),
        nullable=False
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    slug: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    thumbnail: Mapped[str] = mapped_column(Text, nullable=True)
    sentiment: Mapped[str] = mapped_column(String(20), nullable=False)
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    scraped_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False
    )

    # Relationships
    source: Mapped["NewsSource"] = relationship("NewsSource", back_populates="news")

    __table_args__ = (
        CheckConstraint("sentiment IN ('positive', 'negative', 'neutral')", name="chk_news_sentiment"),
        Index("idx_news_published", text("published_at DESC")),
        Index("idx_news_sentiment", "sentiment"),
        Index("idx_news_source", "source_id"),
        Index("idx_news_slug", "slug"),
        Index("idx_news_url", "url"),
    )
