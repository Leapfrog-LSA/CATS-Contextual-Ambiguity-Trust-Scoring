from typing import List

import structlog

from cats.signals.sentiment import sentiment_polarity
from cats.signals.types import Message, VolatilityResult

logger = structlog.get_logger()


def compute_volatility(messages: List[Message], spike_threshold: float = 0.4) -> VolatilityResult:
    if len(messages) < 3:
        return VolatilityResult(
            name="volatility",
            value=0.0,
            confidence=0.0,
            metadata={"reason": "insufficient_messages"},
        )
    sents = [sentiment_polarity(m.text) for m in messages]
    deltas = [abs(sents[i] - sents[i - 1]) for i in range(1, len(sents))]
    spikes = sum(1 for d in deltas if d > spike_threshold)
    max_d = max(deltas) if deltas else 0.0
    score = min((spikes / len(deltas)) * 100, 100.0) if deltas else 0.0
    return VolatilityResult(
        name="volatility",
        value=score,
        confidence=min(len(messages) / 20, 1.0),
        metadata={"threshold": spike_threshold},
        sentiment_spikes=spikes,
        max_delta=max_d,
    )
