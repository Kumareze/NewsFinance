from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl


class NewsBase(BaseModel):
    """Shared base fields for news article schemas."""
    title: str = Field(..., min_length=3, max_length=512)
    summary: Optional[str] = None
    content: Optional[str] = None
    url: str = Field(..., max_length=2048)
    thumbnail: Optional[str] = None
    sentiment: str = Field(default="neutral")
    published_at: datetime


class NewsCreate(NewsBase):
    """Schema for creating a new news article."""
    source_id: UUID
    slug: str = Field(..., max_length=512)


class NewsUpdate(BaseModel):
    """Schema for updating an existing news article (partial update)."""
    title: Optional[str] = Field(None, min_length=3, max_length=512)
    summary: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = Field(None, max_length=2048)
    thumbnail: Optional[str] = None
    sentiment: Optional[str] = None
    published_at: Optional[datetime] = None


class NewsResponse(NewsBase):
    """Schema for news article responses (includes DB-generated fields)."""
    id: UUID
    source_id: UUID
    slug: str
    scraped_at: datetime

    class Config:
        from_attributes = True


class NewsSearchResult(BaseModel):
    """Schema for search result listing."""
    items: list[NewsResponse]
    total: int
    page: int
    page_size: int