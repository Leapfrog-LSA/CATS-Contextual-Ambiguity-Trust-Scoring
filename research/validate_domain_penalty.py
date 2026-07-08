"""Re-validate the domain-provenance penalty through the PRODUCTION scoring path.

The research spike (`domain_provenance_spike.py`) showed a `score - 0.6*domain`
penalty moved future-holdout concordance 0.755 -> 0.775 using inline math. This
script confirms the *integrated* code (cats.scoring.engine.aggregate_score +
apply_domain_penalty, cats.scoring.weights.get_dynamic_weights,
cats.signals.domain_provenance.compute_domain_provenance) reproduces that gain,
so the wiring — not just the prototype — delivers the benefit.

Reads only committed data: behavioural signals + labels from
data/holdout_future.jsonl (the unseen 06-Jul future snapshot), source URLs from
the aligned data/snapshots/labelled_sources_2026-07-06.jsonl, and the shipped
calibrated weights (data/calibrated_weights.json).

Run from the repo root:
    CATS_WEIGHTS_FILE=data/calibrated_weights.json python research/validate_domain_penalty.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("CATS_WEIGHTS_FILE", "data/calibrated_weights.json")
# Inert placeholders so cats.core.config imports outside the API deployment.
os.environ.setdefault("CATS_API_KEY", "validate-unused")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost:1/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:1/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTAwMzI=")

from cats.scoring.engine import aggregate_score, apply_domain_penalty  # noqa: E402
from cats.scoring.weights import get_dynamic_weights  # noqa: E402
from cats.signals.domain_provenance import compute_domain_provenance  # noqa: E402
from cats.signals.types import SignalResult  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def _rank(v):
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(xs, ys) -> float:
    rx, ry = _rank(xs), _rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def concordance(preds, labels) -> float:
    n = len(preds)
    num = den = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            if labels[i] == labels[j]:
                continue
            den += 1
            hi, lo = (i, j) if labels[i] > labels[j] else (j, i)
            if preds[hi] > preds[lo]:
                num += 1
            elif preds[hi] == preds[lo]:
                num += 0.5
    return num / den if den else 0.0


def behavioural_score(rec) -> float:
    signals = [SignalResult(name=k, value=float(v), confidence=1.0) for k, v in rec["signals"].items()]
    weights = get_dynamic_weights({"source_type": rec.get("source_type", "default")})
    return aggregate_score(signals, weights)


def main() -> None:
    hold = [json.loads(line) for line in open(ROOT / "data/holdout_future.jsonl")]
    snap = [json.loads(line) for line in open(ROOT / "data/snapshots/labelled_sources_2026-07-06.jsonl")]
    assert len(hold) == len(snap), (len(hold), len(snap))

    labels = [r["label"] for r in hold]
    beh = [behavioural_score(r) for r in hold]
    domains = [compute_domain_provenance(s.get("url", "")) for s in snap]
    combined = [apply_domain_penalty(b, d) for b, d in zip(beh, domains)]

    n_fired = sum(1 for d in domains if d.value > 0)
    print(f"Future holdout n={len(hold)}  (domain penalty fired on {n_fired} source(s))\n")
    print(f"{'':28s}{'concordance':>12s}{'spearman':>10s}")
    print(f"{'behavioural (calibrated)':28s}{concordance(beh, labels):>12.3f}{spearman(beh, labels):>10.3f}")
    print(
        f"{'behavioural + domain penalty':28s}{concordance(combined, labels):>12.3f}{spearman(combined, labels):>10.3f}"
    )

    print("\nCorrections (sources the penalty moved):")
    for h, s, b, c in zip(hold, snap, beh, combined):
        if abs(c - b) > 1e-9:
            print(f"  label={h['label']:>3}  {b:6.2f} -> {c:6.2f}   {s.get('url','')}")


if __name__ == "__main__":
    main()
