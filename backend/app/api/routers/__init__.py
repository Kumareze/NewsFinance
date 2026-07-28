"""
Router aggregation for FinPulse API.
All sub-routers are combined under the api_router.
"""
from fastapi import APIRouter
from app.api.routers.news import router as news_router
from app.api.routers.sources import router as sources_router

api_router = APIRouter()

api_router.include_router(news_router, prefix="/news", tags=["News"])
api_router.include_router(sources_router, prefix="/sources", tags=["Sources"])