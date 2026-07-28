"""
Scraper Pipeline Orchestrator for FinPulse.

Coordinates the full pipeline flow per spec 07_SCRAPER.md section 4:
    Scheduler → Registry → Fetcher → Parser → Normalizer → Validator
    → Duplicate Checker → Sentiment → Database

Handles error isolation so a failure in one source doesn't stop others.
"""
from datetime import datetime, timezone
import logging
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.news import News
from app.models.source import NewsSource
from app.sentiment.analyzer import analyze_sentiment

from scraper.registry import source_registry
from scraper.fetchers.rss_fetcher import rss_fetcher
from scraper.parsers.cnbc import cnbc_parser
from scraper.parsers.reuters import reuters_parser
from scraper.parsers.generic import generic_parser
from scraper.pipelines.normalization import normalizer
from scraper.pipelines.validator import validate_article
from scraper.pipelines.duplicate_checker import duplicate_checker

logger = logging.getLogger(__name__)

# Map source names to their parsers. Falls back to generic_parser for unknown sources.
PARSER_MAP: Dict[str, Any] = {
    "CNBC Indonesia": cnbc_parser,
    "Reuters": reuters_parser,
}


class ScraperPipeline:
    """
    Orchestrates the entire scraper pipeline for all active news sources.
    Each source is processed independently to ensure fault isolation.
    """

    def __init__(
        self,
        registry=source_registry,
        fetcher=rss_fetcher,
        normalizer=normalizer,
        duplicate_checker=duplicate_checker,
    ):
        self.registry = registry
        self.fetcher = fetcher
        self.normalizer = normalizer
        self.duplicate_checker = duplicate_checker

    def run_full_pipeline(self) -> Dict[str, Any]:
        """
        Executes the full scraper pipeline for all active sources.

        Returns a summary dict with counts of results, duplicates, errors, etc.
        """
        db = SessionLocal()
        try:
            return self._run_pipeline(db)
        finally:
            db.close()

    def _run_pipeline(self, db: Session) -> Dict[str, Any]:
        """Internal pipeline execution with an existing DB session."""
        summary = {
            "sources_processed": 0,
            "articles_fetched": 0,
            "articles_new": 0,
            "articles_duplicate": 0,
            "articles_failed": 0,
            "errors": [],
        }

        logger.info("=" * 60)
        logger.info("SCRAPER PIPELINE STARTED")
        logger.info("=" * 60)

        # Step 1: Get active sources from registry
        active_sources: List[NewsSource] = self.registry.get_active_sources(db)
        if not active_sources:
            logger.warning("No active news sources found. Pipeline finished.")
            return summary

        logger.info(f"Found {len(active_sources)} active source(s) to process.")

        for source in active_sources:
            try:
                self._process_source(db, source, summary)
            except Exception as e:
                error_msg = f"Unhandled error processing source '{source.name}': {e}"
                logger.exception(error_msg)
                summary["errors"].append(error_msg)
                summary["articles_failed"] += 1

        logger.info("=" * 60)
        logger.info(f"SCRAPER PIPELINE FINISHED: {summary}")
        logger.info("=" * 60)

        return summary

    def _process_source(
        self, db: Session, source: NewsSource, summary: Dict[str, Any]
    ) -> None:
        """Process a single news source through the pipeline."""
        logger.info(f"--- Processing source: {source.name} ---")

        summary["sources_processed"] += 1

        # Step 2: Fetch RSS feed
        feed_data = self._fetch_source(source)
        if not feed_data:
            logger.warning(f"Source '{source.name}' returned no data, skipping.")
            return

        # Step 3: Parse entries (generic_parser as fallback)
        parser = PARSER_MAP.get(source.name, generic_parser)

        entries = feed_data.get("entries", []) if isinstance(feed_data, dict) else []
        if not entries:
            logger.info(f"No entries found in feed for source '{source.name}'.")
            return

        summary["articles_fetched"] += len(entries)
        logger.info(f"Fetched {len(entries)} entries from '{source.name}'.")

        for entry in entries:
            self._process_entry(db, source, parser, entry, summary)

    def _fetch_source(self, source: NewsSource) -> Optional[Any]:
        """Fetch RSS feed for a given source with retry logic (max 3 attempts)."""
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                result = asyncio_run(self.fetcher.fetch(source.rss_url))
                if result is not None:
                    return result
                logger.warning(
                    f"Fetch attempt {attempt}/{max_retries} for '{source.name}' returned None."
                )
            except Exception as e:
                logger.error(
                    f"Fetch attempt {attempt}/{max_retries} for '{source.name}' failed: {e}"
                )

        logger.error(
            f"All {max_retries} fetch attempts failed for source '{source.name}'."
        )
        return None

    def _process_entry(
        self,
        db: Session,
        source: NewsSource,
        parser: Any,
        entry: Dict[str, Any],
        summary: Dict[str, Any],
    ) -> None:
        """Process a single RSS entry through the pipeline stages."""
        try:
            # Step 3b: Parse the entry
            parsed = asyncio_run(parser.parse(entry))
            if not parsed:
                logger.debug("Parser returned None for entry, skipping.")
                summary["articles_failed"] += 1
                return

            # Step 4: Normalize
            normalized = asyncio_run(self.normalizer.normalize(parsed))
            if not normalized:
                logger.debug("Normalizer returned None, skipping.")
                summary["articles_failed"] += 1
                return

            # Attach source metadata before validation & dedup
            normalized["source_id"] = source.id
            normalized["source_name"] = source.name

            # Step 5: Validate
            if not validate_article(normalized):
                logger.debug("Article failed validation, skipping.")
                summary["articles_failed"] += 1
                return

            # Step 6: Duplicate check
            url = normalized.get("url", "")
            if self.duplicate_checker.is_duplicate(db, url):
                summary["articles_duplicate"] += 1
                return

            normalized["sentiment"] = analyze_sentiment(
                " ".join(
                    part for part in [
                        normalized.get("title"),
                        normalized.get("summary"),
                        normalized.get("content"),
                    ]
                    if part
                )
            )
            normalized["scraped_at"] = datetime.now(timezone.utc)

            # Step 7: Save to database
            self._save_article(db, normalized)
            summary["articles_new"] += 1

        except Exception as e:
            logger.warning(f"Error processing entry: {e}")
            summary["articles_failed"] += 1

    def _save_article(self, db: Session, article_data: Dict[str, Any]) -> None:
        """Persist a validated, normalized article to the database."""
        try:
            # Build News model instance
            news_entry = News(
                source_id=article_data.get("source_id"),
                title=article_data.get("title"),
                slug=article_data.get("slug"),
                summary=article_data.get("summary"),
                content=article_data.get("content"),
                url=article_data.get("url"),
                thumbnail=article_data.get("thumbnail"),
                sentiment=article_data.get("sentiment", "neutral"),
                published_at=article_data.get("published_at"),
                scraped_at=article_data.get("scraped_at"),
            )

            db.add(news_entry)
            db.commit()
            db.refresh(news_entry)

            logger.info(
                f"Saved article: '{news_entry.title[:60]}...' (slug={news_entry.slug})"
            )
        except Exception as e:
            db.rollback()
            logger.error(f"Database save failed for article: {e}")
            raise


def asyncio_run(coro):
    """Helper to run an async coroutine in a sync context."""
    import asyncio
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # We're already inside an async context; use a new event loop
        import threading
        result = []
        exception = []

        def run_in_thread():
            new_loop = asyncio.new_event_loop()
            try:
                r = new_loop.run_until_complete(coro)
                result.append(r)
            except Exception as e:
                exception.append(e)
            finally:
                new_loop.close()

        thread = threading.Thread(target=run_in_thread)
        thread.start()
        thread.join()
        if exception:
            raise exception[0]
        return result[0]
    else:
        return asyncio.run(coro)


pipeline = ScraperPipeline()