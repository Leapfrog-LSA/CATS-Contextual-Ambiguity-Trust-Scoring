"""Sentiment polarity with a pluggable backend.

Default backend is **TextBlob** (lightweight, no extra dependencies). Set
``SENTIMENT_BACKEND=bert`` to use a transformers Italian sentiment model.
``transformers`` / ``torch`` are optional (see ``requirements-bert.txt``); if
they are missing or the model fails to load, the backend transparently falls
back to TextBlob, so the default install stays light and never crashes.
"""

from __future__ import annotations

import structlog
from textblob import TextBlob

from cats.core.config import settings

logger = structlog.get_logger()

# N-05: Italian negation words. Applied only to the TextBlob backend, which has
# no negation handling; the BERT model handles negation itself.
_NEG_WORDS = {"non", "no", "mai", "niente", "nessuno", "senza"}

_bert_pipeline = None
_bert_failed = False


def _textblob_polarity(text: str) -> float:
    p = TextBlob(text).sentiment.polarity
    if any(w in text.lower().split() for w in _NEG_WORDS):
        p *= -0.8
    return p


def _get_bert_pipeline():
    """Lazily load the transformers sentiment pipeline once; cache the result.

    On any failure (transformers/torch missing, model load error) mark the
    backend as failed so callers fall back to TextBlob without retrying.
    """
    global _bert_pipeline, _bert_failed
    if _bert_pipeline is not None or _bert_failed:
        return _bert_pipeline
    try:
        from transformers import pipeline

        _bert_pipeline = pipeline("sentiment-analysis", model=settings.sentiment_model)
        logger.info("sentiment_bert_loaded", model=settings.sentiment_model)
    except Exception as exc:
        _bert_failed = True
        logger.warning("sentiment_bert_unavailable", error=str(exc), fallback="textblob")
    return _bert_pipeline


def _bert_polarity(text: str) -> float:
    pipe = _get_bert_pipeline()
    if pipe is None:
        return _textblob_polarity(text)
    try:
        res = pipe(text[:512])[0]
    except Exception as exc:
        logger.warning("sentiment_bert_inference_failed", error=str(exc), fallback="textblob")
        return _textblob_polarity(text)
    label = str(res.get("label", "")).lower()
    score = float(res.get("score", 0.0))
    if "neg" in label or label in {"1 star", "2 stars"}:
        return -score
    if "pos" in label or label in {"4 stars", "5 stars"}:
        return score
    return 0.0


def sentiment_polarity(text: str) -> float:
    """Sentiment polarity in [-1, 1]; higher is more positive."""
    if settings.sentiment_backend == "bert":
        return _bert_polarity(text)
    return _textblob_polarity(text)
