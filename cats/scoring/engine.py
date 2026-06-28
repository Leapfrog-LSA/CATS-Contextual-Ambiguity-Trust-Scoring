from typing import Dict, List

from cats.signals.types import SignalResult


def aggregate_score(signals: List[SignalResult], weights: Dict[str, float]) -> float:
    ws, wt = 0.0, 0.0
    for s in signals:
        w = weights.get(s.name, 0.25)
        ws += s.value * w
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
