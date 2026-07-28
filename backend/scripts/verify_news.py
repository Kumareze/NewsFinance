"""Verify news articles exist in database."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from app.core.database import SessionLocal
from app.models.news import News

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

db = SessionLocal()
try:
    count = db.query(News).count()
    logger.info(f"Total news articles in database: {count}")
    
    if count > 0:
        articles = db.query(News).order_by(News.published_at.desc()).limit(5).all()
        logger.info("--- Latest 5 articles ---")
        for a in articles:
            logger.info(f"  [{a.id}] {a.title}")
            logger.info(f"       source_id={a.source_id} slug={a.slug} published={a.published_at}")
    else:
        logger.warning("NO ARTICLES FOUND in database!")
except Exception as e:
    logger.error(f"Error: {e}")
    raise
finally:
    db.close()