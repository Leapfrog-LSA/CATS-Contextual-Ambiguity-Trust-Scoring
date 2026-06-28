from typing import Dict

DEFAULT_WEIGHTS: Dict[str, float] = {
    "coherence": 0.30,
    "volatility": 0.25,
    "silence": 0.25,
    "gaming": 0.20,
}

if abs(sum(DEFAULT_WEIGHTS.values()) - 1.0) > 1e-6:
    raise ValueError("Default weights must sum to 1.0")


def _validate_weights(w: Dict[str, float]) -> Dict[str, float]:
    if abs(sum(w.values()) - 1.0) > 1e-6:
        raise ValueError(f"Weights must sum to 1.0, got {sum(w.values())}")
    return w


def get_dynamic_weights(context: Dict) -> Dict[str, float]:
    src = context.get("source_type", "unknown")
    if src == "social":
        return _validate_weights({"coherence": 0.25, "volatility": 0.30, "silence": 0.20, "gaming": 0.25})
    elif src == "news":
        return _validate_weights({"coherence": 0.35, "volatility": 0.20, "silence": 0.25, "gaming": 0.20})
    return DEFAULT_WEIGHTS.copy()
