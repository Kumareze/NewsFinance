from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class ScrapeLogBase(BaseModel):
    """Shared base fields for scrape log schemas."""
    source_id: UUID
    started_at: datetime
    finished_at: datetime
    total_news: int = Field(default=0, ge=0)
    success_news: int = Field(default=0, ge=0)
    failed_news: int = Field(default=0, ge=0)
    status: str = Field(..., max_length=50)
    message: Optional[str] = None


class ScrapeLogCreate(ScrapeLogBase):
    """Schema for creating a new scrape log entry."""
    pass


class ScrapeLogResponse(ScrapeLogBase):
    """Schema for scrape log responses (includes DB-generated fields)."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True