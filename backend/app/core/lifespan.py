"""
FastAPI application lifespan manager for the FinPulse backend.

Handles startup and shutdown lifecycle:
  - Starts the scraper scheduler on application startup.
  - Stops the scraper scheduler gracefully on application shutdown.
  - Prevents duplicate scheduler instances when running with --reload.
"""
import logging
import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI

# ── Path Setup ───────────────────────────────────────────────────────────────
# Ensure the scraper package (at the project root) is importable.
# The scraper/ directory lives alongside backend/ at the project root.
# In Docker:  /app/app/... = backend code,  /app/scraper = scraper module
# In local:   <project>/backend/... = backend code,  <project>/scraper = scraper
#
# Strategy: walk up from this file's directory until we find the project root
# (a directory containing both "app" and a sibling "scraper" directory).

_current_file = Path(__file__).resolve()
for parent in _current_file.parents:
    # Look for the parent that contains "scraper" as a sibling to "app"
    if (parent / "scraper").is_dir():
        _project_root = str(parent)
        if _project_root not in sys.path:
            sys.path.insert(0, _project_root)
        break

logger = logging.getLogger(__name__)

# Import the singleton scheduler instance
from scraper.scheduler import scheduler  # noqa: E402
from app.core.self_ping import self_ping_service  # noqa: E402

# Track whether the scheduler was started to prevent duplicate starts
_scheduler_started = False
_self_ping_started = False


def _is_reloader_process() -> bool:
    """
    Detect whether we are running in the uvicorn reloader process.

    When uvicorn runs with --reload, there are two processes:
      1. The reloader (file watcher) — this should NOT start the scheduler.
      2. The worker (serves requests) — this SHOULD start the scheduler.

    Returns:
        True if this is the reloader process, False otherwise.
    """
    # Uvicorn >= 0.20.0 sets this env var in the reloader parent process
    if os.environ.get("UVICORN_RELOAD") == "1":
        return True
    return False


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    ASGI lifespan context manager for FinPulse.

    Startup phase:
      - Starts the background scraper scheduler if we are not in the reloader process.

    Shutdown phase:
      - Stops the scraper scheduler gracefully with a timeout.
    """
    # ── STARTUP ──────────────────────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("FinPulse application starting up...")
    logger.info("=" * 60)

    if _is_reloader_process():
        logger.info(
            "Detected reloader process — scheduler will run in the worker process."
        )
    else:
        _start_scheduler()
        _start_self_ping()

    yield  # Application runs here

    # ── SHUTDOWN ─────────────────────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("FinPulse application shutting down...")
    logger.info("=" * 60)

    _stop_scheduler()
    _stop_self_ping()

    logger.info("FinPulse shutdown complete.")


def _start_scheduler() -> None:
    """Start the background scraper scheduler with duplicate protection."""
    global _scheduler_started

    if _scheduler_started:
        logger.warning("Scheduler already started — skipping duplicate start.")
        return

    try:
        logger.info(
            f"Starting scraper scheduler "
            f"(interval: {scheduler.interval_minutes} minute(s))..."
        )
        scheduler.start()
        _scheduler_started = True
        logger.info("Scraper scheduler started successfully.")
    except Exception as e:
        logger.error(f"Failed to start scraper scheduler: {e}")
        # Do not re-raise — the API should still start even if the scheduler fails.
        # The scheduler will retry on its next scheduled interval.


def _stop_scheduler() -> None:
    """Stop the background scraper scheduler gracefully."""
    global _scheduler_started

    if not _scheduler_started:
        logger.debug("Scheduler was not started — nothing to stop.")
        return

    try:
        logger.info("Stopping scraper scheduler...")
        scheduler.stop()
        _scheduler_started = False
        logger.info("Scraper scheduler stopped gracefully.")
    except Exception as e:
        logger.error(f"Error stopping scraper scheduler: {e}")


def _start_self_ping() -> None:
    """Start the lightweight self-ping background worker."""
    global _self_ping_started

    if _self_ping_started:
        logger.warning("Self-ping already started — skipping duplicate start.")
        return

    try:
        self_ping_service.start()
        if self_ping_service.is_running:
            _self_ping_started = True
            logger.info("Self-ping started successfully.")
        else:
            logger.info("Self-ping is disabled or did not start.")
    except Exception as e:
        logger.error(f"Failed to start self-ping service: {e}")


def _stop_self_ping() -> None:
    """Stop the lightweight self-ping background worker."""
    global _self_ping_started

    if not _self_ping_started and not self_ping_service.is_running:
        logger.debug("Self-ping was not started — nothing to stop.")
        return

    try:
        self_ping_service.stop()
        _self_ping_started = False
        logger.info("Self-ping stopped gracefully.")
    except Exception as e:
        logger.error(f"Error stopping self-ping service: {e}")