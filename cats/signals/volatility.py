from typing import List

import structlog

from cats.signals.sentiment import sentiment_polarity
from cats.signals.types import Message, VolatilityResult

logger = structlog.get_logger()


def compute_volatility(messages: List[Message], spike_threshold: float = 0.3) -> VolatilityResult:
    # 0.3 replaces the original 0.4 (fixed 2026-08-26, see
    # docs/volatility_retune_2026-08.md): a threshold sweep on the committed
    # calibration snapshots (research/gaming_volatility_diagnosis_spike.py)
    # found 0.4 was locally the *worst* choice in the semantically correct
    # (negative) direction -- rho +0.028 train / -0.053 holdout, essentially
    # noise -- while 0.3 gives rho -0.141 train / -0.151 holdout, the
    # strongest and most consistent point in the grid on both splits (~3x
    # the prior holdout information). Roughly half of all messages carry
    # TextBlob polarity exactly 0.0 on Italian text (the lexicon can't see
    # it), which caps this signal's ceiling regardless of threshold; this
    # change only fixes an avoidable own-goal within that ceiling.
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
