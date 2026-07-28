from app.repositories.base import BaseRepository
from app.repositories.news import news_repo
from app.repositories.source import news_source_repo
from app.repositories.log import scrape_log_repo

__all__ = [
    "BaseRepository",
    "news_repo",
    "news_source_repo",
    "scrape_log_repo"
]
