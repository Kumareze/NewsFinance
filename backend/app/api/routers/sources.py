"""
Sources API Router for FinPulse.

Provides CRUD endpoints for news sources:
- GET /sources/ — List all sources with pagination
- GET /sources/active — List only active sources
- GET /sources/{source_id} — Get single source by ID
- POST /sources/ — Create new source
- PUT /sources/{source_id} — Update source
- DELETE /sources/{source_id} — Delete source
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_source_service
from app.schemas.source import SourceCreate, SourceUpdate, SourceResponse
from app.services.source_service import NewsSourceService

router = APIRouter()


@router.get("/", response_model=List[SourceResponse])
def list_sources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    service: NewsSourceService = Depends(get_source_service),
):
    """Retrieve all news sources with pagination."""
    return service.get_all_sources(db, skip=skip, limit=limit)


@router.get("/active", response_model=List[SourceResponse])
def list_active_sources(
    db: Session = Depends(get_db),
    service: NewsSourceService = Depends(get_source_service),
):
    """Retrieve all active news sources."""
    return service.get_active_news_sources(db)


@router.get("/{source_id}", response_model=SourceResponse)
def get_source(
    source_id: str,
    db: Session = Depends(get_db),
    service: NewsSourceService = Depends(get_source_service),
):
    """Retrieve a single news source by its ID."""
    source = service.get_source_by_id(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="News source not found")
    return source


@router.post("/", response_model=SourceResponse, status_code=201)
def create_source(
    data: SourceCreate,
    db: Session = Depends(get_db),
    service: NewsSourceService = Depends(get_source_service),
):
    """Create a new news source."""
    try:
        return service.create_news_source(db, data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{source_id}", response_model=SourceResponse)
def update_source(
    source_id: str,
    data: SourceUpdate,
    db: Session = Depends(get_db),
    service: NewsSourceService = Depends(get_source_service),
):
    """Update an existing news source."""
    try:
        source = service.update_news_source(db, source_id, data)
        if not source:
            raise HTTPException(status_code=404, detail="News source not found")
        return source
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{source_id}", status_code=204)
def delete_source(
    source_id: str,
    db: Session = Depends(get_db),
    service: NewsSourceService = Depends(get_source_service),
):
    """Delete a news source by its ID."""
    source = service.delete_news_source(db, source_id)
    if not source:
        raise HTTPException(status_code=404, detail="News source not found")
    return None