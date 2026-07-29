"""
Lightweight self-ping service for keeping Render web service warm.

Runs in a background daemon thread and periodically calls the configured
health endpoint while the FastAPI process is alive.
"""
import logging
import threading
import time
from typing import Optional
from urllib import error, request

from app.core.config import settings

logger = logging.getLogger(__name__)


class SelfPingService:
    """Simple background self-ping worker."""

    def __init__(
        self,
        url: Optional[str] = None,
        interval_minutes: Optional[int] = None,
        enabled: Optional[bool] = None,
    ):
        self.url = url or settings.SELF_PING_URL
        self.interval_minutes = interval_minutes or settings.SELF_PING_INTERVAL_MINUTES
        self.enabled = settings.SELF_PING_ENABLED if enabled is None else enabled

        # Guard against invalid values from env
        self.interval_minutes = max(1, int(self.interval_minutes))
        self._interval_seconds = self.interval_minutes * 60

        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    @property
    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self) -> None:
        if not self.enabled:
            logger.info("Self-ping is disabled by configuration.")
            return

        if self.is_running:
            logger.warning("Self-ping is already running.")
            return

        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run_loop,
            name="self-ping-service",
            daemon=True,
        )
        self._thread.start()
        logger.info(
            "Self-ping started (url=%s, interval=%s minute(s)).",
            self.url,
            self.interval_minutes,
        )

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("Self-ping stopped.")

    def _run_loop(self) -> None:
        # Ping immediately once, then continue on interval.
        while not self._stop_event.is_set():
            self._ping_once()
            for _ in range(self._interval_seconds):
                if self._stop_event.is_set():
                    break
                time.sleep(1)

    def _ping_once(self) -> None:
        try:
            req = request.Request(self.url, method="GET")
            with request.urlopen(req, timeout=10) as resp:
                status_code = resp.getcode()

            if 200 <= status_code < 300:
                logger.info("Self-ping OK (%s) -> HTTP %s", self.url, status_code)
            else:
                logger.warning(
                    "Self-ping non-2xx (%s) -> HTTP %s", self.url, status_code
                )
        except (error.URLError, error.HTTPError, TimeoutError, OSError) as exc:
            logger.warning("Self-ping failed for %s: %s", self.url, exc)


self_ping_service = SelfPingService()
