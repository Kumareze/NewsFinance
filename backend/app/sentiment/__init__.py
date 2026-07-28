"""
Sentiment Analysis module for FinPulse.

Provides a pluggable analyzer interface (per spec 08_SENTIMENT.md) for
classifying news article sentiment as 'positive', 'negative', or 'neutral'.
Default implementation is a keyword-based analyzer.
"""
from app.sentiment.analyzer import SentimentAnalyzer, analyze_sentiment

__all__ = ["SentimentAnalyzer", "analyze_sentiment"]