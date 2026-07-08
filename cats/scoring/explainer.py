from typing import Dict, List

from cats.scoring.engine import DOMAIN_PENALTY_WEIGHT, NEGATIVE_POLARITY, reliability_value
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
    # domain-provenance is a post-aggregation penalty, not a weighted signal, so
    # it is decomposed separately from the behavioural weighted mean.
    behavioural = [s for s in signals if s.name != "domain_provenance"]
    domain = next((s for s in signals if s.name == "domain_provenance"), None)

    # Contributions are computed on the reliability axis: negative-polarity
    # signals (volatility/silence/gaming) are inverted exactly as in
    # aggregate_score, so contribution/score_share_pct decompose the actual score.
    weighted = {s.name: reliability_value(s) * weights.get(s.name, 0.0) for s in behavioural}
    total = sum(weighted.values())
    details = [
        {
            "signal": s.name,
            "value": round(s.value, 2),
            "polarity": "negative" if s.name in NEGATIVE_POLARITY else "positive",
            "reliability_value": round(reliability_value(s), 2),
            "weight": round(weights.get(s.name, 0.0), 2),
            "contribution": round(weighted[s.name], 2),
            # Share of the weighted score attributable to this signal (SHAP-like
            # attribution for a linear model): makes "what drove the score" explicit.
            "score_share_pct": round(100.0 * weighted[s.name] / total, 1) if total else 0.0,
            "confidence": round(s.confidence, 2),
            "metadata": s.metadata,
        }
        for s in behavioural
    ]
    primary_driver = max(weighted, key=lambda name: weighted[name]) if weighted else None
    explanation = {
        "trust_score": round(score, 2),
        "band": band,
        "signals": details,
        "primary_driver": primary_driver,
        "methodology": (
            "Weighted aggregation of 4 behavioural signals on a common "
            "reliability axis (negative-polarity signals inverted as 100 - value); "
            "score_share_pct is each signal's share of the weighted score. "
            "Domain-provenance, when present, is applied afterwards as an "
            "asymmetric penalty (see domain_penalty)."
        ),
        "disclaimer": _DISCLAIMER,
    }
    if domain is not None and domain.confidence > 0:
        penalty = DOMAIN_PENALTY_WEIGHT * domain.value
        explanation["domain_penalty"] = {
            "domain_red_flag_score": round(domain.value, 2),
            "penalty_weight": DOMAIN_PENALTY_WEIGHT,
            "penalty_applied": round(penalty, 2),
            "confidence": round(domain.confidence, 2),
            "metadata": domain.metadata,
            "note": (
                "Asymmetric penalty: subtracted from the weighted behavioural score "
                "(clamped at 0), only lowers the score for impersonation/clone "
                "domains, never raises it. A clean domain applies no penalty."
            ),
        }
    return explanation
