from typing import Dict, List, Optional

from cats.signals.types import SignalResult

# The four behavioural signals do not share a common polarity (architecture.md →
# Signal Polarity & Scoring): coherence is "higher = more reliable", the other
# three are "higher = LESS reliable". Aggregation inverts the negative-polarity
# signals so every term enters the weighted mean as a reliability contribution
# and weights stay interpretable as non-negative importances.
NEGATIVE_POLARITY = frozenset({"volatility", "silence", "gaming"})

# Domain-provenance enters scoring as an ASYMMETRIC PENALTY, not a weighted
# signal: it only ever *lowers* the score (impersonation/clone red-flags), never
# raises it. A symmetric weighted term would reward a clean domain — and most
# fake-news lives on ordinary domains that score 0, so that would wrongly inflate
# the low tail. Coefficient validated on the 28-Jul-2026 future holdout: applying
# `score - 0.6 * domain_red_flag` moved pairwise concordance 0.755 -> 0.775 and
# corrected regular-cadence clones that `silence` misses
# (docs/signal_research_2026-07.md).
DOMAIN_PENALTY_WEIGHT = 0.6

# Bump when aggregation semantics change (scores stop being comparable).
# Stored on every TrustScore row so /explain can flag rows scored under an
# older engine instead of silently re-decomposing them with current semantics.
# 1.4: domain-provenance penalty added (affects sources evaluated with a URL).
ENGINE_VERSION = "1.4"


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


def apply_domain_penalty(
    score: float,
    domain: Optional[SignalResult],
    weight: float = DOMAIN_PENALTY_WEIGHT,
) -> float:
    """Subtract the domain-provenance red-flag penalty from a behavioural score.

    Asymmetric by design: a clean domain (``value`` 0) is a no-op, so the penalty
    never rewards a source — it only pulls impersonation/clone domains down. When
    no domain was assessed (``domain`` is ``None`` or zero-confidence, e.g. no URL
    supplied) the behavioural score is returned unchanged.
    """
    if domain is None or domain.confidence <= 0:
        return score
    return max(0.0, score - weight * domain.value)


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
