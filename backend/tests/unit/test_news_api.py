"""
Unit tests for News API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestNewsEndpoints:
    """Test cases for news-related API endpoints."""

    def test_get_news_list(self):
        """Test GET /api/v1/news/ returns a list of articles."""
        response = client.get("/api/v1/news/")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "page_size" in data

    def test_get_news_with_pagination(self):
        """Test news list supports pagination."""
        response = client.get("/api/v1/news/?page=1&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["page_size"] == 10

    def test_get_news_with_sentiment_filter(self):
        """Test filtering news by sentiment."""
        response = client.get("/api/v1/news/?sentiment=positive")
        assert response.status_code == 200

    def test_get_news_by_slug_not_found(self):
        """Test GET /api/v1/news/{slug} returns 404 for non-existent slug."""
        response = client.get("/api/v1/news/non-existent-slug-12345")
        assert response.status_code == 404

    def test_get_active_sources(self):
        """Test GET /api/v1/sources/active returns active sources."""
        response = client.get("/api/v1/sources/active")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
