"""
Seed script for FinPulse news sources.

Inserts the default news sources into the news_sources table.
This must be run BEFORE the scraper pipeline.

Usage:
    cd backend
    python -m scripts.seed_sources
"""
import sys
import os

# Add the backend directory to Python path so 'app' can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from app.core.database import SessionLocal
from app.models.source import NewsSource

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

DEFAULT_SOURCES = [
    {
        "name": "CNBC Indonesia",
        "website": "https://www.cnbcindonesia.com",
        "rss_url": "https://www.cnbcindonesia.com/rss",
        "active": True,
    },
    {
        "name": "Detik Finance",
        "website": "https://finance.detik.com",
        "rss_url": "https://finance.detik.com/rss",
        "active": True,
    },
    {
        "name": "Bisnis.com",
        "website": "https://www.bisnis.com",
        "rss_url": "https://feeds.feedburner.com/Bisniscom",
        "active": True,
    },
    {
        "name": "Kontan Investasi",
        "website": "https://investasi.kontan.co.id",
        "rss_url": "https://investasi.kontan.co.id/rss",
        "active": True,
    },
    {
        "name": "Kontan Keuangan",
        "website": "https://keuangan.kontan.co.id",
        "rss_url": "https://keuangan.kontan.co.id/rss",
        "active": True,
    },
    {
        "name": "Tempo Bisnis",
        "website": "https://bisnis.tempo.co",
        "rss_url": "https://rss.tempo.co/?ch=bisnis",
        "active": True,
    },
    {
        "name": "Antara Ekonomi",
        "website": "https://www.antaranews.com",
        "rss_url": "https://www.antaranews.com/rss/ekonomi.xml",
        "active": True,
    },
    {
        "name": "Republika Ekonomi",
        "website": "https://www.republika.co.id",
        "rss_url": "https://www.republika.co.id/rss/ekonomi",
        "active": True,
    },
    {
        "name": "IDX Channel",
        "website": "https://www.idxchannel.com",
        "rss_url": "https://www.idxchannel.com/rss",
        "active": True,
    },
    {
        "name": "Katadata",
        "website": "https://www.katadata.co.id",
        "rss_url": "https://www.katadata.co.id/rss",
        "active": True,
    },
    {
        "name": "CNN Indonesia Ekonomi",
        "website": "https://www.cnnindonesia.com/ekonomi",
        "rss_url": "https://www.cnnindonesia.com/ekonomi/rss",
        "active": True,
    },
    {
        "name": "Yahoo Finance",
        "website": "https://finance.yahoo.com",
        "rss_url": "https://finance.yahoo.com/news/rssindex",
        "active": True,
    },
    {
        "name": "WSJ Markets",
        "website": "https://www.wsj.com",
        "rss_url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        "active": True,
    },
    {
        "name": "MarketWatch",
        "website": "https://www.marketwatch.com",
        "rss_url": "https://feeds.marketwatch.com/marketwatch/topstories",
        "active": True,
    },
    {
        "name": "Financial Times",
        "website": "https://www.ft.com",
        "rss_url": "https://www.ft.com/world?format=rss",
        "active": True,
    },
    {
        "name": "CNBC US Markets",
        "website": "https://www.cnbc.com",
        "rss_url": "https://www.cnbc.com/id/10000664/device/rss/rss.html",
        "active": True,
    },
]


def seed_sources() -> None:
    """Insert default news sources if they don't already exist."""
    db = SessionLocal()
    try:
        for src in DEFAULT_SOURCES:
            existing = (
                db.query(NewsSource)
                .filter(NewsSource.name == src["name"])
                .first()
            )
            if existing:
                logger.info(f"Source '{src['name']}' already exists (id={existing.id}). Skipping.")
                continue

            source = NewsSource(
                name=src["name"],
                website=src["website"],
                rss_url=src["rss_url"],
                active=src["active"],
            )
            db.add(source)
            db.commit()
            db.refresh(source)
            logger.info(f"Created source '{source.name}' (id={source.id}).")

        # Show all sources
        all_sources = db.query(NewsSource).all()
        logger.info("=" * 50)
        logger.info(f"Total sources in database: {len(all_sources)}")
        for s in all_sources:
            logger.info(f"  [{s.id}] {s.name} | active={s.active} | rss={s.rss_url}")
        logger.info("=" * 50)

    except Exception as e:
        db.rollback()
        logger.error(f"Failed to seed sources: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_sources()