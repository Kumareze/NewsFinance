"""
API package for FinPulse.
Exposes RESTful endpoints under the /api/v1 prefix.
"""
from app.api.routers import api_router

__all__ = ["api_router"]