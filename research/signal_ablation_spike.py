"""Research spike (roadmap item 7): diagnose the three "mute" behavioural signals.

The 6-Jul future-snapshot validation showed CATS's rank information rests
almost entirely on `silence`; coherence/volatility/gaming carry ~none
(docs/calibration_findings_2026-07-28.md). Before designing new signals or
recalibrating, this spike quantifies — on the committed calibration datasets,
whose signal values are precomputed, so no NLP assets are needed:

  1. per-signal rank correlation with the label (train and future holdout);
  2. inter-signal rank correlation (is any pair redundant?);
  3. each signal ALONE as a ranker (concordance / Spearman on the holdout);
  4. leave-one-signal-out (LOSO) from the shipped calibrated weights,
     renormalised — each signal's marginal contribution to the aggregate;
  5. mean signal value by label band (does the signal separate the tails?).

Read-only inputs: data/train.jsonl, data/holdout_future.jsonl,
data/calibrated_weights.json. Findings: docs/signal_diagnosis_2026-07.md.

Run from the repo root:

    python research/signal_ablation_spike.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, Sequence

# Inert placeholders so cats.core.config imports outside the API deployment.
os.environ.setdefault("CATS_API_KEY", "spike-unused")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost:1/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:1/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTAwMzI=")

from cats.calibration.dataset import SIGNAL_NAMES, LabeledSample, load_dataset  # noqa: E402
from cats.calibration.objective import pairwise_concordance, predict_scores, spearman  # noqa: E402
from cats.scoring.engine import NEGATIVE_POLARITY  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WeightsByGroup = Dict[str, Dict[str, float]]


def reliability(name: str, value: float) -> float:
    """Signal value on the reliability axis (as aggregate_score sees it)."""
    return 100.0 - value if name in NEGATIVE_POLARITY else value


def load_weights() -> WeightsByGroup:
    data = json.loads((ROOT / "data" / "calibrated_weights.json").read_text(encoding="utf-8"))
    return data["weights"]


def loso(weights: WeightsByGroup, drop: str) -> WeightsByGroup:
    """Zero one signal's weight and renormalise the rest (per group).

    The dropped weight is set to 0.0 rather than removed: aggregate_score
    substitutes a default 0.25 for *missing* weights, which would silently
    re-add the signal.
    """
    out: WeightsByGroup = {}
    for grp, w in weights.items():
        kept_total = sum(v for k, v in w.items() if k != drop)
        out[grp] = {k: (0.0 if k == drop else v / kept_total) for k, v in w.items()}
    return out


def solo(weights: WeightsByGroup, keep: str) -> WeightsByGroup:
    """All weight on one signal (per group)."""
    return {grp: {k: (1.0 if k == keep else 0.0) for k in w} for grp, w in weights.items()}


def per_signal_rho(samples: Sequence[LabeledSample]) -> Dict[str, float]:
    labels = [s.label for s in samples]
    return {name: spearman([s.signals[name] for s in samples], labels) for name in SIGNAL_NAMES}


def band_means(samples: Sequence[LabeledSample], name: str) -> Dict[str, float]:
    low = [s.signals[name] for s in samples if s.label <= 30]
    high = [s.signals[name] for s in samples if s.label >= 70]
    return {
        "low": sum(low) / len(low) if low else float("nan"),
        "high": sum(high) / len(high) if high else float("nan"),
    }


def metrics(samples: Sequence[LabeledSample], weights: WeightsByGroup) -> Dict[str, float]:
    preds = predict_scores(samples, weights)
    labels = [s.label for s in samples]
    return {"concordance": pairwise_concordance(preds, labels), "spearman": spearman(preds, labels)}


def main() -> None:
    train = load_dataset(ROOT / "data" / "train.jsonl")
    holdout = load_dataset(ROOT / "data" / "holdout_future.jsonl")
    weights = load_weights()

    print(f"train: n={len(train)}   holdout (future, unseen): n={len(holdout)}")
    print(f"calibrated weights: {json.dumps(weights)}\n")

    print("1) Per-signal Spearman rho vs label (raw signal values)")
    rho_tr, rho_ho = per_signal_rho(train), per_signal_rho(holdout)
    print(f"   {'signal':<12} {'train':>8} {'holdout':>8}   polarity")
    for name in SIGNAL_NAMES:
        pol = "higher=worse" if name in NEGATIVE_POLARITY else "higher=better"
        print(f"   {name:<12} {rho_tr[name]:>+8.3f} {rho_ho[name]:>+8.3f}   {pol}")

    print("\n2) Inter-signal Spearman rho (holdout, raw values)")
    print("   " + " ".join(f"{n[:9]:>10}" for n in ("", *SIGNAL_NAMES)))
    for a in SIGNAL_NAMES:
        row = [spearman([s.signals[a] for s in holdout], [s.signals[b] for s in holdout]) for b in SIGNAL_NAMES]
        print(f"   {a[:9]:>10} " + " ".join(f"{v:>+10.3f}" for v in row))

    print("\n3) Each signal ALONE as ranker (holdout, reliability axis)")
    print(f"   {'signal':<12} {'concordance':>12} {'spearman':>10}")
    for name in SIGNAL_NAMES:
        m = metrics(holdout, solo(weights, name))
        print(f"   {name:<12} {m['concordance']:>12.3f} {m['spearman']:>+10.3f}")

    full = metrics(holdout, weights)
    print("\n4) Leave-one-signal-out from the calibrated weights (holdout)")
    print(f"   {'dropped':<12} {'concordance':>12} {'spearman':>10} {'delta_conc':>11}")
    print(f"   {'(none)':<12} {full['concordance']:>12.3f} {full['spearman']:>+10.3f} {'-':>11}")
    for name in SIGNAL_NAMES:
        m = metrics(holdout, loso(weights, name))
        print(
            f"   {name:<12} {m['concordance']:>12.3f} {m['spearman']:>+10.3f} "
            f"{m['concordance'] - full['concordance']:>+11.3f}"
        )

    print("\n5) Mean raw signal value by label band (holdout: label<=30 vs >=70)")
    print(f"   {'signal':<12} {'low tail':>9} {'high tail':>10}")
    for name in SIGNAL_NAMES:
        b = band_means(holdout, name)
        print(f"   {name:<12} {b['low']:>9.1f} {b['high']:>10.1f}")


if __name__ == "__main__":
    main()
