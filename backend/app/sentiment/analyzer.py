"""
Sentiment Analyzer for FinPulse.

Implements a keyword-based sentiment analysis engine per spec 08_SENTIMENT.md.
The analyzer scans article titles and content for predefined positive/negative
financial keywords and returns a classification: 'positive', 'negative', or 'neutral'.
"""
import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

# Financial-domain keywords for sentiment classification
POSITIVE_KEYWORDS = [
    # --- Bahasa Inggris ---
    "bullish", "rally", "surge", "soar", "gain", "profit", "growth",
    "upgrade", "outperform", "buy", "positive", "boom", "expansion",
    "recovery", "rise", "rising", "upside", "breakthrough", "innovation",
    "record high", "all-time high", "beat expectations", "outlook positive",
    "strong demand", "earnings beat", "revenue growth", "dividend increase",
    "share buyback", "bull market", "uptrend", "momentum", "outperformance",
    "breakout", "undervalued", "accumulation", "overweight",
    
    # --- Bahasa Indonesia ---
    "reli", "melonjak", "meroket", "untung", "cuan", "laba", 
    "pertumbuhan", "tumbuh", "beli", "positif", "ekspansi", 
    "pemulihan", "pulih", "naik", "meningkat", "rekor tertinggi", 
    "melampaui ekspektasi", "prospek positif", "permintaan kuat", 
    "laba bersih naik", "pendapatan naik", "kenaikan dividen", "bagi dividen", 
    "tebar dividen", "buyback", "tren naik", "akumulasi", "ara", 
    "auto reject atas", "prospek cerah", "kinerja solid", 
    "target harga naik", "rekomendasi beli", "sentimen positif", "meraup untung"
]

NEGATIVE_KEYWORDS = [
    # --- Bahasa Inggris ---
    "bearish", "plunge", "crash", "slump", "drop", "decline", "loss",
    "downgrade", "underperform", "sell", "negative", "recession", "inflation",
    "slowdown", "fall", "falling", "downside", "bankruptcy", "layoff",
    "record low", "all-time low", "miss expectations", "outlook negative",
    "weak demand", "earnings miss", "revenue decline", "dividend cut",
    "debt crisis", "bear market", "downtrend", "volatility", "uncertainty",
    "sanctions", "tariff", "trade war", "default", "distribution", "panic selling",
    
    # --- Bahasa Indonesia ---
    "anjlok", "ambruk", "jatuh", "turun", "merosot", "rugi", 
    "boncos", "koreksi", "terkoreksi", "jual", "negatif", 
    "resesi", "inflasi", "perlambatan", "lambat", "bangkrut", "pailit", 
    "phk", "rekor terendah", "di bawah ekspektasi", "meleset dari ekspektasi",
    "prospek negatif", "permintaan lemah", "laba turun", "pendapatan turun", 
    "potong dividen", "absen dividen", "krisis utang", "tren turun", 
    "volatilitas", "ketidakpastian", "sanksi", "gagal bayar", "distribusi", 
    "arb", "auto reject bawah", "overvalued", "buang barang", 
    "suspend", "suspensi", "delisting", "tekanan jual", "sentimen negatif"
]

# Neutralizing context words that flip negative financial terms
POSITIVE_CONTEXT = [
    "recovery", "rebound", "bounce", "improve", "improving", "better-than-expected",
]

# Words that negate sentiment (e.g., "not positive" → negative)
NEGATION_WORDS = {"not", "no", "never", "neither", "nor", "cannot", "can't", "don't"}


class SentimentAnalyzer:
    """
    Keyword-based sentiment analyzer for financial news articles.

    Analysis logic (per spec 08_SENTIMENT.md 3.0):
        1. Tokenize and lowercase the text.
        2. Count keyword matches with context awareness.
        3. Classify based on weighted score.
        4. Return 'positive', 'negative', or 'neutral'.
    """

    def __init__(
        self,
        positive_keywords: Optional[list] = None,
        negative_keywords: Optional[list] = None,
    ):
        self.positive_keywords = positive_keywords or POSITIVE_KEYWORDS
        self.negative_keywords = negative_keywords or NEGATIVE_KEYWORDS

    def analyze(self, text: str) -> str:
        """
        Analyze sentiment of the given text.

        Args:
            text: The article title and/or content to analyze.

        Returns:
            'positive', 'negative', or 'neutral'.
        """
        if not text or not text.strip():
            return "neutral"

        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)

        # Count keyword matches
        positive_score = self._count_matches(text_lower, self.positive_keywords)
        negative_score = self._count_matches(text_lower, self.negative_keywords)

        # Apply negation handling: check for negation words near sentiment keywords
        positive_score = self._apply_negation(words, positive_score, self.positive_keywords)
        negative_score = self._apply_negation(words, negative_score, self.negative_keywords)

        logger.debug(
            f"Sentiment scores - positive: {positive_score}, negative: {negative_score}"
        )

        # Classify based on dominant score
        if positive_score > negative_score:
            return "positive"
        elif negative_score > positive_score:
            return "negative"
        else:
            return "neutral"

    def _count_matches(self, text_lower: str, keywords: list) -> int:
        """Count how many distinct keywords are found in the text."""
        count = 0
        for keyword in keywords:
            if keyword in text_lower:
                count += 1
        return count

    def _apply_negation(self, words: list, score: int, keywords: list) -> int:
        """
        Reduce score for keywords that are negated (e.g., preceded by 'not').

        For each keyword found, check if the preceding word is a negation.
        If so, reduce the score contribution.
        """
        # Simple approach: if a negation word appears within 3 words before
        # a keyword match, reduce the score
        adjusted_score = score
        for i, word in enumerate(words):
            if word in NEGATION_WORDS:
                # Check next 3 words for any keyword match
                for j in range(1, 4):
                    idx = i + j
                    if idx < len(words):
                        next_word = words[idx]
                        for keyword in keywords:
                            if keyword == next_word or keyword.startswith(next_word):
                                adjusted_score = max(0, adjusted_score - 1)
                                break
        return adjusted_score


# Singleton instance for application-wide use
analyzer = SentimentAnalyzer()


def analyze_sentiment(text: str) -> str:
    """
    Convenience function to analyze sentiment of a text.

    Args:
        text: The text to analyze.

    Returns:
        'positive', 'negative', or 'neutral'.
    """
    return analyzer.analyze(text)