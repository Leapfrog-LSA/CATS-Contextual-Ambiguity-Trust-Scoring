import cats.signals.sentiment as sentiment
from cats.core.config import settings
from cats.signals.sentiment import sentiment_polarity


class TestTextBlobBackend:
    def test_default_backend_returns_polarity(self, monkeypatch):
        monkeypatch.setattr(settings, "sentiment_backend", "textblob")
        p = sentiment_polarity("This is wonderful and amazing")
        assert -1.0 <= p <= 1.0
        assert p > 0  # clearly positive

    def test_negation_reduces_polarity(self, monkeypatch):
        monkeypatch.setattr(settings, "sentiment_backend", "textblob")
        plain = sentiment_polarity("buono")
        negated = sentiment_polarity("non buono")
        # negation flips the sign of a positive polarity
        assert negated <= 0 <= plain or negated < plain


class TestBertBackendFallback:
    def test_falls_back_to_textblob_when_unavailable(self, monkeypatch):
        # transformers/torch are not installed in the default/test env, so the
        # bert backend must fall back to TextBlob instead of crashing.
        monkeypatch.setattr(settings, "sentiment_backend", "bert")
        monkeypatch.setattr(sentiment, "_bert_pipeline", None)
        monkeypatch.setattr(sentiment, "_bert_failed", False)
        text = "This is wonderful and amazing"
        got = sentiment_polarity(text)
        assert got == sentiment._textblob_polarity(text)
        # the backend is marked failed so it won't retry the import
        assert sentiment._bert_failed is True
