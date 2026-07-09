"""Research spike (roadmap item 7, part 2): message-level diagnosis of the two
dead-weight signals.

The ablation/LOSO diagnosis (research/signal_ablation_spike.py,
docs/signal_diagnosis_2026-07.md) showed volatility and gaming contribute
~nothing to the calibrated aggregate. This spike digs one level deeper, from
the stored signal *vectors* down to the message histories, to answer WHY —
using only committed snapshot data and no NLP model assets (gaming is pure
tokenisation; volatility's TextBlob backend ships with the test stack):

  1. **Gaming sub-score ablation** — the stored value averages four sub-scores
     (repetition, TTR, burst, vocab); are they individually informative and
     mutually cancelling, or all dead?
  2. **Volatility spike-threshold sweep** — is the 0.4 threshold the problem,
     or is the signal structurally starved? Includes the starvation
     diagnostic: the fraction of messages whose TextBlob polarity is exactly
     0.0 (Italian text the sentiment lexicon cannot see).
  3. **Silence threshold sweep** (diagnostic only, feeds roadmap item 13) —
     how sensitive is the one informative signal to its unvalidated 72 h
     threshold?

Protocol mirrors the 6-Jul validation: train = merged 02/03/05-Jul snapshots,
holdout = the unseen 06-Jul snapshot. Sweeps replicate compute_volatility's
math on per-source polarity series computed once (verified equal to the
production function at the current threshold); silence sweeps call the
production function directly.

Run from the repo root:

    python research/gaming_volatility_diagnosis_spike.py
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
from cats.signals.gaming import compute_gaming  # noqa: E402
from cats.signals.sentiment import sentiment_polarity  # noqa: E402
from cats.signals.silence import compute_silence  # noqa: E402
from cats.signals.volatility import compute_volatility  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / "data" / "snapshots"
TRAIN_SNAPSHOTS = ["labelled_sources_2026-07-02", "labelled_sources_2026-07-03", "labelled_sources_2026-07-05"]
HOLDOUT_SNAPSHOT = "labelled_sources_2026-07-06"

GAMING_SUBSCORES = ("repetition", "ttr", "burst", "vocab")
VOLATILITY_THRESHOLDS = (0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8)
SILENCE_THRESHOLDS_H = (24.0, 48.0, 72.0, 96.0, 120.0, 168.0)


def load_sources(paths: Sequence[Path]) -> List[dict]:
    """Merged labelled sources with normalised, non-empty message histories."""
    records, _, _ = merge_records([_read_jsonl(p) for p in paths])
    out = []
    for r in records:
        msgs = normalize_messages(r.get("messages") or [])
        if msgs and "label" in r:
            out.append({"label": float(r["label"]), "source_type": str(r.get("source_type") or "news"), "msgs": msgs})
    return out


def gaming_subscores(sources: Sequence[dict]) -> Dict[str, List[float]]:
    cols: Dict[str, List[float]] = {k: [] for k in (*GAMING_SUBSCORES, "value", "label")}
    for s in sources:
        g = compute_gaming(s["msgs"])
        cols["repetition"].append(g.repetition_score)
        cols["ttr"].append(g.ttr_score)
        cols["burst"].append(g.burst_score)
        cols["vocab"].append(g.vocab_score)
        cols["value"].append(g.value)
        cols["label"].append(s["label"])
    return cols


def polarity_series(sources: Sequence[dict]) -> List[Tuple[List[float], float]]:
    """Per source: TextBlob polarity per message (computed once) + label."""
    return [([sentiment_polarity(m.text) for m in s["msgs"]], s["label"]) for s in sources]


def volatility_from_polarities(sents: List[float], threshold: float) -> float:
    """compute_volatility's scoring math on a precomputed polarity series."""
    if len(sents) < 3:
        return 0.0
    deltas = [abs(sents[i] - sents[i - 1]) for i in range(1, len(sents))]
    return min((sum(1 for d in deltas if d > threshold) / len(deltas)) * 100, 100.0)


def check_sweep_math(sources: Sequence[dict], series: List[Tuple[List[float], float]]) -> None:
    """The sweep math must reproduce the production function at the current threshold."""
    for s, (sents, _) in zip(sources, series):
        prod = compute_volatility(s["msgs"]).value
        mine = volatility_from_polarities(sents, 0.4)
        assert abs(prod - mine) < 1e-9, f"sweep math diverges from compute_volatility: {prod} != {mine}"


def main() -> None:
    train = load_sources([SNAP / f"{n}.jsonl" for n in TRAIN_SNAPSHOTS])
    holdout = load_sources([SNAP / f"{HOLDOUT_SNAPSHOT}.jsonl"])
    print(f"train (merged 02/03/05-Jul): n={len(train)}   holdout (06-Jul, unseen): n={len(holdout)}\n")

    print("1) Gaming sub-score ablation — Spearman rho vs label (raw sub-scores, higher=worse)")
    print(f"   {'sub-score':<12} {'train':>8} {'holdout':>8}")
    tr, ho = gaming_subscores(train), gaming_subscores(holdout)
    for k in (*GAMING_SUBSCORES, "value"):
        print(f"   {k:<12} {spearman(tr[k], tr['label']):>+8.3f} {spearman(ho[k], ho['label']):>+8.3f}")
    print("   drop-one recomposition (mean of the other 3), holdout rho vs label:")
    for k in GAMING_SUBSCORES:
        others = [o for o in GAMING_SUBSCORES if o != k]
        recomposed = [sum(ho[o][i] for o in others) / 3 * 100 for i in range(len(ho["label"]))]
        print(f"     without {k:<11} {spearman(recomposed, ho['label']):>+8.3f}")

    print("\n2) Volatility spike-threshold sweep — Spearman rho vs label")
    tr_series, ho_series = polarity_series(train), polarity_series(holdout)
    check_sweep_math(holdout, ho_series)
    print(f"   {'threshold':<12} {'train':>8} {'holdout':>8}")
    for t in VOLATILITY_THRESHOLDS:
        rho_tr = spearman([volatility_from_polarities(s, t) for s, _ in tr_series], [lb for _, lb in tr_series])
        rho_ho = spearman([volatility_from_polarities(s, t) for s, _ in ho_series], [lb for _, lb in ho_series])
        marker = "  <- current" if t == 0.4 else ""
        print(f"   {t:<12} {rho_tr:>+8.3f} {rho_ho:>+8.3f}{marker}")
    all_sents = [p for sents, _ in ho_series for p in sents]
    zero_frac = sum(1 for p in all_sents if p == 0.0) / len(all_sents)
    all_zero_sources = sum(1 for sents, _ in ho_series if all(p == 0.0 for p in sents))
    print(f"   starvation: {zero_frac:.1%} of holdout messages have polarity exactly 0.0;")
    print(f"   {all_zero_sources}/{len(ho_series)} sources have an all-zero polarity series (volatility always 0)")

    print("\n3) Silence threshold sweep — Spearman rho vs label (production compute_silence)")
    print(f"   {'threshold_h':<12} {'train':>8} {'holdout':>8}")
    for t in SILENCE_THRESHOLDS_H:
        rho_tr = spearman(
            [compute_silence(s["msgs"], s["source_type"], anomaly_threshold_hours=t).value for s in train],
            [s["label"] for s in train],
        )
        rho_ho = spearman(
            [compute_silence(s["msgs"], s["source_type"], anomaly_threshold_hours=t).value for s in holdout],
            [s["label"] for s in holdout],
        )
        marker = "  <- current" if t == 72.0 else ""
        print(f"   {t:<12} {rho_tr:>+8.3f} {rho_ho:>+8.3f}{marker}")


if __name__ == "__main__":
    main()
