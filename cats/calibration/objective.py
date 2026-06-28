"""Encoding and fitness for weight calibration.

A genome packs the four signal weights for every source-type group present in
the dataset. CATS scoring distinguishes three groups — ``social``, ``news`` and
``default`` (used for any other / unknown source) — so each group contributes
four raw, non-negative genes that are normalised to sum to 1.0 on decode.

Because CATS scores are ordinal rankings (WP 4.3), fitness measures rank
agreement between predicted scores and ground-truth labels:
  * ``spearman``    — Spearman rank correlation (default)
  * ``concordance`` — pairwise concordance (AUC-like), ties counted as 0.5
"""

from __future__ import annotations

from typing import Callable, Dict, List, Sequence, Tuple

from cats.calibration.dataset import SIGNAL_NAMES, LabeledSample
from cats.scoring.engine import aggregate_score
from cats.signals.types import SignalResult

WeightsByGroup = Dict[str, Dict[str, float]]


def canonical_source_type(src: str) -> str:
    """Map an arbitrary source type onto a CATS scoring group."""
    return src if src in ("social", "news") else "default"


def make_groups(samples: Sequence[LabeledSample]) -> List[str]:
    return sorted({canonical_source_type(s.source_type) for s in samples})


def bounds_for(groups: Sequence[str]) -> List[Tuple[float, float]]:
    # Lower bound > 0 keeps at least a sliver of every signal and avoids a
    # degenerate all-zero gene vector that would make normalisation undefined.
    return [(0.01, 1.0)] * (len(groups) * len(SIGNAL_NAMES))


def decode(genome: Sequence[float], groups: Sequence[str]) -> WeightsByGroup:
    out: WeightsByGroup = {}
    n = len(SIGNAL_NAMES)
    for gi, grp in enumerate(groups):
        raw = list(genome[gi * n : (gi + 1) * n])
        total = sum(raw)
        if total <= 0:
            out[grp] = {name: 1.0 / n for name in SIGNAL_NAMES}
        else:
            out[grp] = {name: raw[i] / total for i, name in enumerate(SIGNAL_NAMES)}
    return out


def predict_scores(samples: Sequence[LabeledSample], weights_by_group: WeightsByGroup) -> List[float]:
    preds: List[float] = []
    for s in samples:
        weights = weights_by_group[canonical_source_type(s.source_type)]
        sigs = [SignalResult(name=name, value=s.signals[name], confidence=1.0) for name in SIGNAL_NAMES]
        preds.append(aggregate_score(sigs, weights))
    return preds


def _rank(xs: Sequence[float]) -> List[float]:
    """Average (fractional) ranks, 1-based, with ties averaged."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg_rank
        i = j + 1
    return ranks


def _pearson(a: Sequence[float], b: Sequence[float]) -> float:
    n = len(a)
    if n == 0:
        return 0.0
    ma = sum(a) / n
    mb = sum(b) / n
    cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    va = sum((x - ma) ** 2 for x in a) ** 0.5
    vb = sum((x - mb) ** 2 for x in b) ** 0.5
    if va == 0.0 or vb == 0.0:
        return 0.0
    return cov / (va * vb)


def spearman(preds: Sequence[float], labels: Sequence[float]) -> float:
    return _pearson(_rank(preds), _rank(labels))


def pairwise_concordance(preds: Sequence[float], labels: Sequence[float]) -> float:
    num = 0.0
    den = 0.0
    n = len(preds)
    for i in range(n):
        for j in range(i + 1, n):
            if labels[i] == labels[j]:
                continue
            den += 1.0
            hi, lo = (i, j) if labels[i] > labels[j] else (j, i)
            if preds[hi] > preds[lo]:
                num += 1.0
            elif preds[hi] == preds[lo]:
                num += 0.5
    return num / den if den else 0.0


METRICS: Dict[str, Callable[[Sequence[float], Sequence[float]], float]] = {
    "spearman": spearman,
    "concordance": pairwise_concordance,
}


def build_fitness(
    samples: Sequence[LabeledSample], metric: str = "spearman"
) -> Tuple[Callable[[Sequence[float]], float], List[str]]:
    if metric not in METRICS:
        raise ValueError(f"unknown metric '{metric}'; choose from {sorted(METRICS)}")
    groups = make_groups(samples)
    metric_fn = METRICS[metric]
    labels = [s.label for s in samples]

    def fitness(genome: Sequence[float]) -> float:
        return metric_fn(predict_scores(samples, decode(genome, groups)), labels)

    return fitness, groups
