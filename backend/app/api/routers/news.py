"""
News API Router for FinPulse.

Provides CRUD endpoints for news articles:
- GET /news/ — List/search with pagination, filtering, sorting
- GET /news/{slug} — Get single article by slug
- POST /news/ — Create article (admin)
- PUT /news/{slug} — Update article (admin)
- DELETE /news/{slug} — Delete article (admin/admin)
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_news_service
from app.schemas.news import (
    NewsCreate,
    NewsUpdate,
    NewsResponse,
    NewsSearchResult,
)
from app.services.news_service import NewsService

router = APIRouter()


@router.get("/", response_model=NewsSearchResult)
def list_news(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    sentiment: Optional[str] = Query(None, description="Filter by sentiment"),
    source: Optional[str] = Query(None, description="Filter by source name"),
    sort: str = Query("latest", regex="^(latest|oldest|positive|negative|mixed)$"),
    q: Optional[str] = Query(None, description="Search query"),
    db: Session = Depends(get_db),
    service: NewsService = Depends(get_news_service),
):
    """
    Retrieve news articles with pagination, filtering, sorting, and search.
    """
    skip = (page - 1) * page_size

    if q:
        items = service.search_news(db, q=q, skip=skip, limit=page_size)
        total = service.count_search_results(db, q=q)
    else:
        items = service.get_multiple_news(
            db, skip=skip, limit=page_size, sentiment=sentiment,
            source_name=source, sort=sort
        )
        total = service.count_news(db, sentiment=sentiment, source_name=source)

    return NewsSearchResult(
        items=[NewsResponse.model_validate(item) for item in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{slug}", response_model=NewsResponse)
def get_news_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    service: NewsService = Depends(get_news_service),
):
    """Retrieve a single news article by its slug."""
    article = service.get_news_article(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="News article not found")
    return article


@router.post("/", response_model=NewsResponse, status_code=201)
def create_news(
    data: NewsCreate,
    db: Session = Depends(get_db),
    service: NewsService = Depends(get_news_service),
):
    """Create a new news article (admin use)."""
    try:
        article = service.create_news(db, data)
        return article
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{slug}", response_model=NewsResponse)
def update_news(
    slug: str,
    data: NewsUpdate,
    db: Session = Depends(get_db),
    service: NewsService = Depends(get_news_service),
):
    """Update an existing news article (admin use)."""
    article = service.update_news(db, slug, data)
    if not article:
        raise HTTPException(status_code=404, detail="News article not found")
    return article


@router.delete("/{slug}", status_code=204)
def delete_news(
    slug: str,
    db: Session = Depends(get_db),
    service: NewsService = Depends(get_news_service),
):
    """Delete a news article by its slug (admin use)."""
    article = service.delete_news(db, slug)
    if not article:
        raise HTTPException(status_code=404, detail="News article not found")
    return None