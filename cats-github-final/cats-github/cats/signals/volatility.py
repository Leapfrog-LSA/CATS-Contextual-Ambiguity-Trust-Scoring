from typing import List
from textblob import TextBlob
import structlog
from cats.signals.types import Message, VolatilityResult

logger = structlog.get_logger()

# N-05: Italian negation words
_NEG_WORDS = {"non", "no", "mai", "niente", "nessuno", "senza"}


def _sentiment(text: str) -> float:
    p = TextBlob(text).sentiment.polarity
    if any(w in text.lower().split() for w in _NEG_WORDS):
        p *= -0.8
    return p


def compute_volatility(messages: List[Message], spike_threshold: float = 0.4) -> VolatilityResult:
    if len(messages) < 3:
        return VolatilityResult(
            name="volatility", value=0.0, confidence=0.0,
            metadata={"reason": "insufficient_messages"},
        )
    sents  = [_sentiment(m.text) for m in messages]
    deltas = [abs(sents[i] - sents[i - 1]) for i in range(1, len(sents))]
    spikes = sum(1 for d in deltas if d > spike_threshold)
    max_d  = max(deltas) if deltas else 0.0
    score  = min((spikes / len(deltas)) * 100, 100.0) if deltas else 0.0
    return VolatilityResult(
        name="volatility",
        value=score,
        confidence=min(len(messages) / 20, 1.0),
        metadata={"threshold": spike_threshold},
        sentiment_spikes=spikes,
        max_delta=max_d,
    )
