from typing import Dict, List

from cats.signals.types import SignalResult

# The four signals do not share a common polarity (architecture.md → Signal
# Polarity & Scoring): coherence is "higher = more reliable", the other three
# are "higher = LESS reliable". Aggregation inverts the negative-polarity
# signals so every term enters the weighted mean as a reliability contribution
# and weights stay interpretable as non-negative importances.
NEGATIVE_POLARITY = frozenset({"volatility", "silence", "gaming"})

# Bump when aggregation semantics change (scores stop being comparable).
# Stored on every TrustScore row so /explain can flag rows scored under an
# older engine instead of silently re-decomposing them with current semantics.
ENGINE_VERSION = "1.3"


def reliability_value(signal: SignalResult) -> float:
    """Signal value on the reliability axis (negative-polarity signals inverted)."""
    return 100.0 - signal.value if signal.name in NEGATIVE_POLARITY else signal.value


def aggregate_score(signals: List[SignalResult], weights: Dict[str, float]) -> float:
    ws, wt = 0.0, 0.0
    for s in signals:
        w = weights.get(s.name, 0.25)
        ws += reliability_value(s) * w
        wt += w
    return ws / wt if wt else 50.0


def determine_band(score: float) -> str:
    if score >= 80:
        return "high"
    if score >= 60:
        return "medium_high"
    if score >= 40:
        return "medium"
    if score >= 20:
        return "low"
    return "very_low"


def requires_human_review(score: float, band: str, signals: List[SignalResult]) -> bool:
    if band in {"low", "very_low"}:
        return True
    if any(s.confidence < 0.3 for s in signals) and score < 50:
        return True
    return False
