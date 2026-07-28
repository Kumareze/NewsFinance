"""
API Dependencies for FinPulse.

Provides reusable FastAPI dependencies:
- Database session (get_db)
- Service injection helpers
"""
from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db as _get_db
from app.services.news_service import news_service
from app.services.source_service import news_source_service


def get_db() -> Generator[Session, None, None]:
    """Dependency that yields a database session."""
    yield from _get_db()


def get_news_service():
    """Dependency that returns the news service singleton."""
    return news_service


def get_source_service():
    """Dependency that returns the source service singleton."""
    return news_source_service