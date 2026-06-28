from collections import Counter
from datetime import datetime
from typing import List

import structlog

from cats.core.config import settings
from cats.signals.types import GamingResult, Message

logger = structlog.get_logger()  # N-06: structlog JSON renderer


def _ttr(tokens: List[str]) -> float:
    return len(set(tokens)) / len(tokens) if tokens else 1.0


def _repetition(tokens: List[str]) -> float:
    if len(tokens) < 3:
        return 0.0
    bigrams = [tuple(tokens[i : i + 2]) for i in range(len(tokens) - 1)]
    mx = max(Counter(bigrams).values(), default=1)
    return min((mx - 1) / 10, 1.0)


def _burst(messages: List[Message]) -> float:
    if len(messages) < 5:
        return 0.0
    ts = sorted(datetime.fromisoformat(m.timestamp.replace("Z", "+00:00")) for m in messages)
    ivs = [(ts[i] - ts[i - 1]).total_seconds() for i in range(1, len(ts))]
    avg = sum(ivs) / len(ivs)
    if avg == 0:
        return 1.0
    return min(sum(1 for iv in ivs if iv < avg / 3) / len(ivs), 1.0)


def _vocab_diversity(tokens: List[str]) -> float:
    if len(tokens) < 50:
        return 1.0
    return 1.0 - min(len(set(tokens)) / len(tokens), 1.0)


def compute_gaming(messages: List[Message]) -> GamingResult:
    tokens = [t for m in messages for t in m.text.lower().split()]
    # N-02: guard min tokens
    if len(tokens) < settings.nlp_gaming_min_tokens:
        logger.info("gaming_skipped", reason="below_min_tokens", count=len(tokens))
        return GamingResult(
            name="gaming",
            value=0.0,
            confidence=0.0,
            metadata={"reason": "insufficient_tokens"},
        )
    rep = _repetition(tokens)
    ttr = 1.0 - _ttr(tokens)
    burst = _burst(messages)
    vocab = _vocab_diversity(tokens)
    return GamingResult(
        name="gaming",
        value=((rep + ttr + burst + vocab) / 4) * 100,
        confidence=min(len(messages) / 50, 1.0),
        metadata={"token_count": len(tokens)},
        repetition_score=rep,
        ttr_score=ttr,
        burst_score=burst,
        vocab_score=vocab,
    )
