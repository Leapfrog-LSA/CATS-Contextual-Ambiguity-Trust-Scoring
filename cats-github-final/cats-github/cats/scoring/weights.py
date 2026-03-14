from typing import Dict

DEFAULT_WEIGHTS: Dict[str, float] = {
    "coherence": 0.30,
    "volatility": 0.25,
    "silence":    0.25,
    "gaming":     0.20,
}
# A-02: import-time invariant assert
assert abs(sum(DEFAULT_WEIGHTS.values()) - 1.0) < 1e-6, "Weights must sum to 1.0"


def get_dynamic_weights(context: Dict) -> Dict[str, float]:
    src = context.get("source_type", "unknown")
    if src == "social":
        w = {"coherence": 0.25, "volatility": 0.30, "silence": 0.20, "gaming": 0.25}
    elif src == "news":
        w = {"coherence": 0.35, "volatility": 0.20, "silence": 0.25, "gaming": 0.20}
    else:
        w = DEFAULT_WEIGHTS.copy()
    assert abs(sum(w.values()) - 1.0) < 1e-6
    return w
