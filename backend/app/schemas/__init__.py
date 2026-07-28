from app.schemas.news import NewsCreate, NewsUpdate, NewsResponse, NewsSearchResult
from app.schemas.source import SourceCreate, SourceUpdate, SourceResponse
from app.schemas.log import ScrapeLogResponse

# Backward-compatible aliases used by services
NewsSourceCreate = SourceCreate
NewsSourceUpdate = SourceUpdate

__all__ = [
    "NewsCreate",
    "NewsUpdate",
    "NewsResponse",
    "NewsSearchResult",
    "SourceCreate",
    "SourceUpdate",
    "SourceResponse",
    "NewsSourceCreate",
    "NewsSourceUpdate",
    "ScrapeLogResponse",
]
