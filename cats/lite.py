"""Zero-infrastructure scoring: the CATS signal pipeline as a library call.

The full CATS deployment (FastAPI + PostgreSQL + Redis) exists for audited,
GDPR-compliant production use. For research, notebooks and quick evaluation
none of that is needed — the four signals and the aggregation are pure
computation. This module exposes them directly:

    from cats.lite import score

    result = score(
        [
            {"timestamp": "2026-01-01T08:00:00Z", "text": "Il governo annuncia un piano."},
            {"timestamp": "2026-01-01T09:00:00Z", "text": "I sindacati commentano il piano."},
            {"timestamp": "2026-01-02T10:00:00Z", "text": "Il parlamento discute il piano."},
        ],
        source_type="news",
    )
    print(result["trust_score"], result["band"])

No database, no Redis, no API keys. The runtime settings that normally come
from the environment (``COHERENCE_BACKEND``, ``CATS_WEIGHTS_FILE``, …) are
still honoured when set; the infrastructure-only settings (database, Redis,
audit encryption) are defaulted to inert placeholders because nothing in this
path touches them.

Same caveats as the API: scores are ordinal (WP 4.3), the default NLP is
Italian-optimised (WP 4.1) and, without ``init_nlp``/the spaCy model,
NER coherence degrades to a neutral zero-confidence value.
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional

# The signal/scoring modules read ``cats.core.config.settings`` at import time,
# which fails fast when the deployment-only variables are missing — correct for
# the API, pointless for pure scoring. Default them (only if unset) to inert
# placeholders *before* those imports. Real values from the environment always
# win because setdefault never overrides.
_LITE_ENV_DEFAULTS = {
    "CATS_API_KEY": "lite-mode-unused",
    "DATABASE_URL": "postgresql+asyncpg://lite:lite@localhost:1/unused",
    "REDIS_URL": "redis://localhost:1/0",
    "AUDIT_ENCRYPTION_KEY": "bGl0ZS1tb2RlLXBsYWNlaG9sZGVyLW5vdC1hLWtleT0=",
}
for _k, _v in _LITE_ENV_DEFAULTS.items():
    os.environ.setdefault(_k, _v)

from cats.pipeline.normalizer import normalize_messages  # noqa: E402
from cats.scoring.engine import (  # noqa: E402
    aggregate_score,
    apply_domain_penalty,
    determine_band,
    requires_human_review,
)
from cats.scoring.explainer import generate_explanation  # noqa: E402
from cats.scoring.weights import get_dynamic_weights  # noqa: E402
from cats.signals import coherence  # noqa: E402
from cats.signals.coherence import compute_coherence  # noqa: E402
from cats.signals.domain_provenance import compute_domain_provenance  # noqa: E402
from cats.signals.gaming import compute_gaming  # noqa: E402
from cats.signals.silence import compute_silence  # noqa: E402
from cats.signals.types import SignalResult  # noqa: E402
from cats.signals.volatility import compute_volatility  # noqa: E402

_nlp_attempted = False


def init_nlp(model_name: Optional[str] = None) -> bool:
    """Load the spaCy NER model once (idempotent); returns True on success.

    Without it the NER coherence backend degrades to a neutral,
    zero-confidence value — exactly as the API does when the model is missing.
    """
    global _nlp_attempted
    if coherence.nlp is not None:
        return True
    if _nlp_attempted:
        return False
    _nlp_attempted = True
    try:
        from cats.core.config import settings

        coherence.init_nlp(model_name or settings.spacy_model)
        return True
    except Exception:  # model not downloaded — degrade, don't crash
        return False


def score(
    messages: List[dict],
    source_type: str = "default",
    weights: Optional[Dict[str, float]] = None,
    explain: bool = True,
    load_nlp: bool = True,
    url: Optional[str] = None,
) -> Dict:
    """Score one source's message history with the CATS signal pipeline.

    ``messages``: list of ``{"timestamp": ISO-8601, "text": str}`` dicts.
    ``weights``: optional signal-name -> weight override; defaults to the
    static/calibrated table for ``source_type`` (``CATS_WEIGHTS_FILE`` honoured).
    ``url``: optional source URL/domain. When given, the domain-provenance
    penalty is applied (impersonation/clone red-flags only lower the score).

    Returns ``{trust_score, band, requires_human_review, signals, explanation}``.
    """
    if load_nlp:
        init_nlp()
    msgs = normalize_messages(messages)
    if not msgs:
        raise ValueError("no valid messages after normalisation (need timestamp + text)")

    behavioural: List[SignalResult] = [
        compute_coherence(msgs),
        compute_volatility(msgs),
        compute_silence(msgs, source_type),
        compute_gaming(msgs),
    ]
    w = weights or get_dynamic_weights({"source_type": source_type})
    value = aggregate_score(behavioural, w)

    domain = compute_domain_provenance(url or "")
    value = apply_domain_penalty(value, domain)
    signals: List[SignalResult] = behavioural + ([domain] if domain.confidence > 0 else [])
    band = determine_band(value)
    result = {
        "trust_score": round(value, 2),
        "band": band,
        "requires_human_review": requires_human_review(value, band, signals),
        "signals": {s.name: round(s.value, 2) for s in signals},
    }
    if explain:
        result["explanation"] = generate_explanation(value, band, signals, w)
    return result
