from typing import Dict, List

from cats.signals.types import SignalResult

# A-01: WP 4.1/4.3 disclaimer
_DISCLAIMER = (
    "Scores are ordinal rankings of source reliability patterns, not absolute "
    "probabilities. NLP accuracy ~55-62%, parameters not empirically calibrated "
    "(WP 4.1). Not suitable as sole basis for autonomous decisions (WP 4.3)."
)


def generate_explanation(
    score: float,
    band: str,
    signals: List[SignalResult],
    weights: Dict[str, float],
) -> Dict:
    details = [
        {
            "signal": s.name,
            "value": round(s.value, 2),
            "weight": round(weights.get(s.name, 0.0), 2),
            "contribution": round(s.value * weights.get(s.name, 0.0), 2),
            "confidence": round(s.confidence, 2),
            "metadata": s.metadata,
        }
        for s in signals
    ]
    return {
        "trust_score": round(score, 2),
        "band": band,
        "signals": details,
        "methodology": "Weighted aggregation of 4 behavioural signals",
        "disclaimer": _DISCLAIMER,
    }
