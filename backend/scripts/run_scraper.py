"""
Manual scraper trigger script for FinPulse.

Runs the full scraper pipeline once and prints a summary.
This is used for manual/on-demand news ingestion.

Usage:
    cd backend
    python -m scripts.run_scraper
"""
import sys
import os

# Add the backend directory to Python path so 'app' can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from datetime import datetime, timezone

# Configure logging for visible console output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Run the scraper pipeline once and report results."""
    logger.info("=" * 60)
    logger.info("MANUAL SCRAPER TRIGGER")
    logger.info(f"Started at: {datetime.now(timezone.utc).isoformat()}")
    logger.info("=" * 60)

    from scraper.pipelines.pipeline import pipeline

    summary = pipeline.run_full_pipeline()

    logger.info("=" * 60)
    logger.info("SCRAPING SUMMARY")
    logger.info(f"  Sources processed:  {summary['sources_processed']}")
    logger.info(f"  Articles fetched:   {summary['articles_fetched']}")
    logger.info(f"  Articles new:       {summary['articles_new']}")
    logger.info(f"  Articles duplicate: {summary['articles_duplicate']}")
    logger.info(f"  Articles failed:    {summary['articles_failed']}")
    if summary.get("errors"):
        logger.error(f"  Errors: {len(summary['errors'])}")
        for err in summary["errors"]:
            logger.error(f"    - {err}")
    logger.info("=" * 60)

    total_saved = summary.get("articles_new", 0)
    if total_saved > 0:
        logger.info(f"SUCCESS: {total_saved} new article(s) saved to database.")
    else:
        logger.warning("No new articles were saved. Check logs above for details.")


if __name__ == "__main__":
    main()