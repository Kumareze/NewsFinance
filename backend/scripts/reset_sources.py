"""Reset sources: delete old, seed new ones."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from app.core.database import SessionLocal
from app.models.source import NewsSource

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_SOURCES = [
    {"name": "CNBC Indonesia", "website": "https://www.cnbcindonesia.com", "rss_url": "https://www.cnbcindonesia.com/rss", "active": True},
    {"name": "Yahoo Finance", "website": "https://finance.yahoo.com", "rss_url": "https://finance.yahoo.com/news/rssindex", "active": True},
    {"name": "WSJ Markets", "website": "https://www.wsj.com", "rss_url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml", "active": True},
    {"name": "MarketWatch", "website": "https://www.marketwatch.com", "rss_url": "https://feeds.marketwatch.com/marketwatch/topstories", "active": True},
    {"name": "Financial Times", "website": "https://www.ft.com", "rss_url": "https://www.ft.com/world?format=rss", "active": True},
    {"name": "CNBC US Markets", "website": "https://www.cnbc.com", "rss_url": "https://www.cnbc.com/id/10000664/device/rss/rss.html", "active": True},
]

db = SessionLocal()
try:
    db.query(NewsSource).delete()
    db.commit()
    logger.info("Deleted all existing sources.")

    for src in DEFAULT_SOURCES:
        source = NewsSource(name=src["name"], website=src["website"], rss_url=src["rss_url"], active=src["active"])
        db.add(source)
        db.commit()
        db.refresh(source)
        logger.info(f"Created source '{source.name}' (id={source.id}) url={source.rss_url}")

    all_sources = db.query(NewsSource).all()
    logger.info(f"Total sources: {len(all_sources)}")
    for s in all_sources:
        logger.info(f"  [{s.id}] {s.name} -> {s.rss_url}")
except Exception as e:
    db.rollback()
    logger.error(f"Error: {e}")
    raise
finally:
    db.close()