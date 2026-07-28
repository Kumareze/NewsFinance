"""
Scheduler module for the FinPulse scraper.

Runs the scraper pipeline on a configurable interval (default: 30 minutes).
Per spec 07_SCRAPER.md section 6: the scheduler triggers the full pipeline
at regular intervals to keep news data current.
"""
import logging
import threading
import time
from typing import Optional

from datetime import datetime, timedelta, timezone

from sqlalchemy import delete as sa_delete

from scraper.pipelines.pipeline import pipeline
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.news import News

logger = logging.getLogger(__name__)

# ── Retention Policy ────────────────────────────────────────────────────────
RETENTION_DAYS = 30  # News older than this will be purged automatically


def _cleanup_old_news() -> int:
    """
    Delete news articles older than RETENTION_DAYS days.
    
    This prevents unbounded table growth and keeps the database lean.
    Runs synchronously before each pipeline cycle.
    
    Returns:
        Number of deleted rows.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)
    db = SessionLocal()
    try:
        result = db.execute(
            sa_delete(News).where(News.published_at < cutoff)
        )
        db.commit()
        deleted = result.rowcount
        if deleted:
            logger.info(
                f"Retention cleanup: deleted {deleted} article(s) older than "
                f"{RETENTION_DAYS} days (before {cutoff.isoformat()})."
            )
        else:
            logger.debug(
                f"Retention cleanup: no articles older than {RETENTION_DAYS} days found."
            )
        return deleted
    except Exception as e:
        db.rollback()
        logger.error(f"Retention cleanup failed: {e}")
        return 0
    finally:
        db.close()


class ScraperScheduler:
    """
    A simple background-thread-based scheduler that runs the scraper
    pipeline at a fixed interval (in minutes).

    The scheduler:
        - Runs in a daemon thread so it doesn't block application shutdown.
        - Logs each run's start, duration, and summary.
        - Can be stopped gracefully via the stop() method.
    """

    def __init__(self, interval_minutes: Optional[int] = None):
        """
        Args:
            interval_minutes: Minutes between pipeline runs.
                              Falls back to settings.SCRAPER_INTERVAL (default 30).
        """
        self.interval_minutes = interval_minutes or settings.SCRAPER_INTERVAL
        self._interval_seconds = self.interval_minutes * 60
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    @property
    def is_running(self) -> bool:
        """Check whether the scheduler thread is alive."""
        return self._thread is not None and self._thread.is_alive()

    def start(self) -> None:
        """
        Start the scheduler in a background daemon thread.
        The first run happens immediately after start.
        """
        if self.is_running:
            logger.warning("Scheduler is already running.")
            return

        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run_loop,
            name="scraper-scheduler",
            daemon=True,
        )
        self._thread.start()
        logger.info(
            f"Scraper scheduler started with interval of {self.interval_minutes} minute(s)."
        )

    def stop(self) -> None:
        """
        Signal the scheduler to stop after the current run completes.
        """
        logger.info("Stopping scraper scheduler...")
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=10)
            logger.info("Scraper scheduler stopped.")

    def _run_loop(self) -> None:
        """Main scheduler loop: run pipeline, then sleep for the interval."""
        while not self._stop_event.is_set():
            self._run_once()
            # Sleep in small increments to allow responsive shutdown
            for _ in range(self._interval_seconds):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

    def _run_once(self) -> None:
        """Execute a single pipeline run with timing."""
        logger.info("=" * 60)
        logger.info(f"SCHEDULER TRIGGER: Running scraper pipeline...")
        logger.info(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
        logger.info("=" * 60)

        # Run retention cleanup before each pipeline cycle
        _cleanup_old_news()

        start_time = time.monotonic()
        try:
            summary = pipeline.run_full_pipeline()
            elapsed = time.monotonic() - start_time
            logger.info(
                f"Pipeline run completed in {elapsed:.2f}s. "
                f"Sources: {summary['sources_processed']}, "
                f"New: {summary['articles_new']}, "
                f"Duplicates: {summary['articles_duplicate']}, "
                f"Failed: {summary['articles_failed']}"
            )
        except Exception as e:
            elapsed = time.monotonic() - start_time
            logger.exception(
                f"Pipeline run failed after {elapsed:.2f}s with error: {e}"
            )

    def run_once_now(self) -> dict:
        """
        Trigger a single pipeline run immediately (useful for manual/API-triggered runs).

        Returns:
            The pipeline summary dict.
        """
        logger.info("Manual pipeline trigger requested.")
        return pipeline.run_full_pipeline()


# Singleton instance for application-wide use
scheduler = ScraperScheduler()