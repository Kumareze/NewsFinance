"""
Unit tests for sentiment analysis module.
"""

import pytest
from app.sentiment.analyzer import analyze_sentiment


class TestSentimentAnalyzer:
    """Test cases for the rule-based sentiment analyzer."""

    def test_positive_sentiment(self):
        """Test detection of positive sentiment."""
        text = "Saham BRI naik signifikan hari ini dengan laba yang meningkat tajam"
        result = analyze_sentiment(text)
        assert result.sentiment == "positive"
        assert result.confidence > 0.5

    def test_negative_sentiment(self):
        """Test detection of negative sentiment."""
        text = "Rupiah melemah tajam akibat inflasi yang melonjak tinggi"
        result = analyze_sentiment(text)
        assert result.sentiment == "negative"
        assert result.confidence > 0.5

    def test_neutral_sentiment(self):
        """Test detection of neutral sentiment."""
        text = "Bank Indonesia mengumumkan rapat dewan gubernur bulanan"
        result = analyze_sentiment(text)
        assert result.sentiment == "neutral"

    def test_empty_text(self):
        """Test handling of empty text input."""
        result = analyze_sentiment("")
        assert result.sentiment == "neutral"
        assert result.confidence == 0.0

    def test_confidence_range(self):
        """Test that confidence scores are always within valid range."""
        texts = [
            "Saham naik tajam hari ini",
            "Pasar saham turun drastis",
            "Perusahaan mengadakan rapat rutin",
        ]
        for text in texts:
            result = analyze_sentiment(text)
            assert 0.0 <= result.confidence <= 1.0
