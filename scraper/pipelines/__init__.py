from scraper.pipelines.normalization import normalizer, Normalizer
from scraper.pipelines.validator import validate_article
from scraper.pipelines.duplicate_checker import DuplicateChecker
from scraper.pipelines.pipeline import ScraperPipeline

__all__ = [
    "normalizer",
    "Normalizer",
    "validate_article",
    "DuplicateChecker",
    "ScraperPipeline",
]