import functools
import json
from pathlib import Path
from typing import Dict

import structlog

logger = structlog.get_logger()

DEFAULT_WEIGHTS: Dict[str, float] = {
    "coherence": 0.30,
    "volatility": 0.25,
    "silence": 0.25,
    "gaming": 0.20,
}

if abs(sum(DEFAULT_WEIGHTS.values()) - 1.0) > 1e-6:
    raise ValueError("Default weights must sum to 1.0")

# Hand-picked fallback weights per source-type group (WP 4.1 initial estimates).
_STATIC_WEIGHTS: Dict[str, Dict[str, float]] = {
    "social": {"coherence": 0.25, "volatility": 0.30, "silence": 0.20, "gaming": 0.25},
    "news": {"coherence": 0.35, "volatility": 0.20, "silence": 0.25, "gaming": 0.20},
    "default": DEFAULT_WEIGHTS,
}


def _validate_weights(w: Dict[str, float]) -> Dict[str, float]:
    if abs(sum(w.values()) - 1.0) > 1e-6:
        raise ValueError(f"Weights must sum to 1.0, got {sum(w.values())}")
    return w


@functools.lru_cache(maxsize=1)
def _calibrated_table() -> Dict[str, Dict[str, float]]:
    """Load empirically calibrated weights if ``CATS_WEIGHTS_FILE`` is configured.

    Returns an empty table (so callers fall back to the static estimates) when
    the setting is unset, the file is missing, or the contents are invalid.
    """
    try:
        from cats.core.config import settings

        path = getattr(settings, "weights_file", None)
    except Exception:  # settings may be unavailable in tooling/test contexts
        path = None
    if not path:
        return {}

    p = Path(path)
    if not p.exists():
        logger.warning("calibrated_weights_missing", path=str(p))
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        table = data.get("weights", data)
        return {g: _validate_weights({k: float(v) for k, v in w.items()}) for g, w in table.items()}
    except (ValueError, KeyError, TypeError) as exc:
        logger.error("calibrated_weights_invalid", path=str(p), error=str(exc))
        return {}


def get_dynamic_weights(context: Dict) -> Dict[str, float]:
    src = context.get("source_type", "unknown")
    group = src if src in ("social", "news") else "default"

    calibrated = _calibrated_table()
    if group in calibrated:
        return dict(calibrated[group])
    return dict(_STATIC_WEIGHTS[group])
