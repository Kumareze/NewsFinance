from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, HttpUrl


class SourceBase(BaseModel):
    """Shared base fields for news source schemas."""
    name: str = Field(..., min_length=1, max_length=100)
    website: str = Field(..., max_length=2048)
    rss_url: str = Field(..., max_length=2048)
    active: bool = Field(default=True)


class SourceCreate(SourceBase):
    """Schema for creating a new news source."""
    pass


class SourceUpdate(BaseModel):
    """Schema for updating an existing news source (partial update)."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    website: Optional[str] = Field(None, max_length=2048)
    rss_url: Optional[str] = Field(None, max_length=2048)
    active: Optional[bool] = None


class SourceResponse(SourceBase):
    """Schema for news source responses (includes DB-generated fields)."""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
