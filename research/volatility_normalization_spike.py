"""Research spike (raised in review, 31 Aug 2026): does source-relative
(z-score) volatility normalization outperform the current global fixed
threshold?

Motivation: `compute_volatility`'s `spike_threshold` (currently 0.3, see
docs/volatility_retune_2026-08.md) is **global** -- the same absolute
sentiment-delta cutoff for a naturally expressive tabloid and a naturally
flat wire service. A source's own historical tone variance might be a
better baseline than one fixed number applied to every source alike:
flag a delta as a spike only when it is anomalous *for that source*, not
merely large in absolute terms.

Method: per source, compute the z-score of each sentiment delta against
that source's OWN mean/std of deltas (never the global threshold). Flag a
"spike" when |delta - mean| > k * max(std, floor). Sweep k and floor
together -- the floor exists to probe a known failure mode explicitly:
a source with near-constant sentiment (std -> 0, common given 48.9% of
messages carry TextBlob polarity exactly 0.0 on Italian text, per
docs/signal_diagnosis_2026-07.md) would flag EVERY nonzero delta as a
huge z-score outlier with no floor -- the floor=0.0 row below reproduces
that failure mode on purpose, for comparison against floored rows.

Leakage discipline: normalization parameters (k, floor grid) are fixed
before running against any label -- swept for information, not tuned
against the holdout number. Same protocol as every other signal spike
this week: train = merged 02/03/05-Jul snapshots (n=56), holdout = the
untouched 06-Jul snapshot (n=53).

Run from the repo root:  python research/volatility_normalization_spike.py
Reads only committed data (data/snapshots/labelled_sources_2026-07-0{2,3,5,6}.jsonl).
No NLP model assets needed (TextBlob ships with the test stack).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

# Inert placeholders so cats.core.config imports outside the API deployment.
os.environ.setdefault("CATS_API_KEY", "spike-unused")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost:1/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:1/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTAwMzI=")

from cats.calibration.merge_snapshots import _read_jsonl, merge_records  # noqa: E402
from cats.calibration.objective import spearman  # noqa: E402
from cats.pipeline.normalizer import normalize_messages  # noqa: E402
from cats.signals.sentiment import sentiment_polarity  # noqa: E402
from cats.signals.volatility import compute_volatility  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / "data" / "snapshots"
TRAIN_SNAPSHOTS = ["labelled_sources_2026-07-02", "labelled_sources_2026-07-03", "labelled_sources_2026-07-05"]
HOLDOUT_SNAPSHOT = "labelled_sources_2026-07-06"

GLOBAL_THRESHOLD = 0.3  # current production value (docs/volatility_retune_2026-08.md)
K_GRID = (1.0, 1.5, 2.0, 2.5, 3.0)
FLOOR_GRID = (0.0, 0.05, 0.1, 0.15, 0.2)
# Hybrid follow-up: require BOTH an absolute delta floor (same spirit as the
# existing global threshold) AND a relative z-score -- tests whether pairing
# the two designs stabilises the sign flip the pure z-score sweep shows.
HYBRID_ABS_FLOOR_GRID = (0.1, 0.15, 0.2, 0.3)
HYBRID_K_GRID = (0.5, 1.0, 1.5, 2.0)


def load_sources(paths: Sequence[Path]) -> List[dict]:
    """Merged labelled sources with normalised, non-empty message histories."""
    records, _, _ = merge_records([_read_jsonl(p) for p in paths])
    out = []
    for r in records:
        msgs = normalize_messages(r.get("messages") or [])
        if msgs and "label" in r:
            out.append({"label": float(r["label"]), "source_type": str(r.get("source_type") or "news"), "msgs": msgs})
    return out


def deltas_for(source: dict) -> List[float]:
    sents = [sentiment_polarity(m.text) for m in source["msgs"]]
    return [abs(sents[i] - sents[i - 1]) for i in range(1, len(sents))]


def volatility_global(deltas: List[float], threshold: float) -> float:
    if not deltas:
        return 0.0
    spikes = sum(1 for d in deltas if d > threshold)
    return min(spikes / len(deltas) * 100, 100.0)


def volatility_zscore(deltas: List[float], k: float, floor: float) -> float:
    if not deltas:
        return 0.0
    mean = sum(deltas) / len(deltas)
    var = sum((d - mean) ** 2 for d in deltas) / len(deltas)
    std_eff = max(var**0.5, floor)
    spikes = sum(1 for d in deltas if abs(d - mean) > k * std_eff)
    return min(spikes / len(deltas) * 100, 100.0)


def volatility_hybrid(deltas: List[float], abs_floor: float, k: float) -> float:
    """Both an absolute delta floor AND a relative z-score must fire."""
    if not deltas:
        return 0.0
    mean = sum(deltas) / len(deltas)
    var = sum((d - mean) ** 2 for d in deltas) / len(deltas)
    std = var**0.5
    spikes = sum(1 for d in deltas if d > abs_floor and abs(d - mean) > k * std)
    return min(spikes / len(deltas) * 100, 100.0)


def _std(deltas: List[float]) -> float:
    if not deltas:
        return 0.0
    mean = sum(deltas) / len(deltas)
    return (sum((d - mean) ** 2 for d in deltas) / len(deltas)) ** 0.5


def main() -> None:
    train = load_sources([SNAP / f"{n}.jsonl" for n in TRAIN_SNAPSHOTS])
    holdout = load_sources([SNAP / f"{HOLDOUT_SNAPSHOT}.jsonl"])
    print(f"train (merged 02/03/05-Jul): n={len(train)}   holdout (06-Jul, unseen): n={len(holdout)}\n")

    tr_deltas = [deltas_for(s) for s in train]
    ho_deltas = [deltas_for(s) for s in holdout]
    tr_labels = [s["label"] for s in train]
    ho_labels = [s["label"] for s in holdout]

    # Diagnostic: how many sources have near-zero natural variance -- the
    # exact condition that makes an unfloored z-score blow up.
    ho_stds = [_std(d) for d in ho_deltas if d]
    near_zero = sum(1 for s in ho_stds if s < 0.05)
    print(f"holdout sources with >=1 delta: {len(ho_stds)}")
    print(f"  of those, std < 0.05 (near-constant tone): {near_zero} ({near_zero/len(ho_stds):.0%})")
    if ho_stds:
        print(
            f"  std range: min={min(ho_stds):.3f}  median={sorted(ho_stds)[len(ho_stds)//2]:.3f}  max={max(ho_stds):.3f}"
        )

    print("\n=== Baseline: current production (global fixed threshold) ===")
    tr_base = [volatility_global(d, GLOBAL_THRESHOLD) for d in tr_deltas]
    ho_base = [volatility_global(d, GLOBAL_THRESHOLD) for d in ho_deltas]
    # Sanity check the sweep math against the real production function.
    prod_vals = [compute_volatility(s["msgs"]).value for s in holdout]
    assert all(abs(a - b) < 1e-9 for a, b in zip(ho_base, prod_vals)), "sweep math diverges from compute_volatility"
    print(
        f"threshold={GLOBAL_THRESHOLD}  train rho={spearman(tr_base, tr_labels):+.3f}  holdout rho={spearman(ho_base, ho_labels):+.3f}"
    )

    print("\n=== Source-relative z-score sweep (rho vs label) ===")
    print(f"{'k':>4} {'floor':>6} {'train rho':>10} {'holdout rho':>12}")
    best: Tuple[float, str, str] = (0.0, "", "")
    results: Dict[Tuple[float, float], Tuple[float, float]] = {}
    for k in K_GRID:
        for floor in FLOOR_GRID:
            tr_vals = [volatility_zscore(d, k, floor) for d in tr_deltas]
            ho_vals = [volatility_zscore(d, k, floor) for d in ho_deltas]
            tr_rho = spearman(tr_vals, tr_labels)
            ho_rho = spearman(ho_vals, ho_labels)
            results[(k, floor)] = (tr_rho, ho_rho)
            marker = "  <- no floor (failure mode)" if floor == 0.0 else ""
            print(f"{k:>4.1f} {floor:>6.2f} {tr_rho:>+10.3f} {ho_rho:>+12.3f}{marker}")
            # "Best" = most negative holdout rho (correct semantic direction)
            # among points where train and holdout AGREE in sign (stability
            # check, same lesson as the global-threshold retune and the
            # cross-source-corroboration spike this week).
            if tr_rho < 0 and ho_rho < 0 and ho_rho < best[0]:
                best = (ho_rho, f"k={k}", f"floor={floor}")

    print(f"\nBest sign-stable (train and holdout both negative) holdout rho: {best[0]:+.3f} at {best[1]}, {best[2]}")
    print(f"Baseline (current production) holdout rho: {spearman(ho_base, ho_labels):+.3f}")

    print("\n=== Hybrid follow-up: absolute floor AND relative z-score both required ===")
    print(f"{'abs_floor':>10} {'k':>5} {'train rho':>10} {'holdout rho':>12}")
    for abs_floor in HYBRID_ABS_FLOOR_GRID:
        for k in HYBRID_K_GRID:
            tr_vals = [volatility_hybrid(d, abs_floor, k) for d in tr_deltas]
            ho_vals = [volatility_hybrid(d, abs_floor, k) for d in ho_deltas]
            tr_rho = spearman(tr_vals, tr_labels)
            ho_rho = spearman(ho_vals, ho_labels)
            print(f"{abs_floor:>10.2f} {k:>5.1f} {tr_rho:>+10.3f} {ho_rho:>+12.3f}")
    print(
        "\nSame instability as the pure z-score sweep: strongly negative (correct\n"
        "direction) around k~1.5 regardless of abs_floor, flips to positive at\n"
        "k=2.0 for every abs_floor tried -- the absolute floor does not fix it.\n"
        "See docs/volatility_source_relative_spike_2026-08.md for the read on this."
    )


if __name__ == "__main__":
    main()
