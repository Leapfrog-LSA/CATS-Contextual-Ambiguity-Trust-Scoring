"""Evaluate scoring quality on a labelled dataset (reproducible eval harness).

Calibration *tunes* weights; this module *measures* how well a given set of
weights ranks sources against ground-truth labels — the question the audit
raised: "are the score bands meaningful?". It reuses the calibration metrics so
the numbers match what calibration optimises.

For a dataset of ``{source_type, signals, label}`` records it reports:
  * rank-agreement metrics — Spearman and pairwise concordance (AUC-like)
  * a per-(predicted-)band table: count, mean predicted score, mean label
  * band agreement — how often the predicted band matches the band the *label*
    falls into (exact and within one band)
  * a per-source_type breakdown

Usage::

    python -m cats.calibration.evaluate --dataset examples/calibration_sample.jsonl
    python -m cats.calibration.evaluate --dataset holdout.jsonl --weights calibrated_weights.json

With ``--weights`` the harness scores using a calibrated weights file (the
output of ``python -m cats.calibration``); otherwise it uses the static WP 4.1
estimates. This makes "before vs after calibration" a one-command comparison.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from cats.calibration.dataset import SIGNAL_NAMES, LabeledSample, load_dataset
from cats.calibration.objective import (
    WeightsByGroup,
    canonical_source_type,
    make_groups,
    pairwise_concordance,
    predict_scores,
    spearman,
)
from cats.scoring.engine import determine_band
from cats.scoring.weights import _STATIC_WEIGHTS

# Bands from worst to best; index distance drives the "adjacent" agreement.
BAND_ORDER = ["very_low", "low", "medium", "medium_high", "high"]
_BAND_INDEX = {b: i for i, b in enumerate(BAND_ORDER)}


@dataclass
class BandRow:
    band: str
    count: int
    mean_predicted: float
    mean_label: float


@dataclass
class GroupRow:
    source_type: str
    count: int
    spearman: Optional[float]  # None when too few samples to be meaningful (< 3)
    concordance: Optional[float]


@dataclass
class EvalReport:
    n: int
    weights_source: str
    spearman: float
    concordance: float
    band_agreement_exact: float
    band_agreement_adjacent: float
    bands: List[BandRow] = field(default_factory=list)
    per_source_type: List[GroupRow] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def render(self) -> str:
        lines = [
            f"Samples            : {self.n}",
            f"Weights            : {self.weights_source}",
            f"Spearman           : {self.spearman:+.3f}",
            f"Concordance (AUC~) : {self.concordance:.3f}",
            f"Band agreement     : {self.band_agreement_exact:.1%} exact, "
            f"{self.band_agreement_adjacent:.1%} within 1 band",
            "",
            "Per predicted band:",
            f"  {'band':12s} {'n':>4s} {'mean_pred':>10s} {'mean_label':>11s}",
        ]
        for r in self.bands:
            lines.append(f"  {r.band:12s} {r.count:>4d} {r.mean_predicted:>10.1f} {r.mean_label:>11.1f}")
        lines.append("")
        lines.append("Per source_type:")
        lines.append(f"  {'source_type':12s} {'n':>4s} {'spearman':>9s} {'concord':>8s}")
        for g in self.per_source_type:
            sp = f"{g.spearman:+.3f}" if g.spearman is not None else "   n/a"
            co = f"{g.concordance:.3f}" if g.concordance is not None else "  n/a"
            lines.append(f"  {g.source_type:12s} {g.count:>4d} {sp:>9s} {co:>8s}")
        return "\n".join(lines)


def _mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def static_weights_for(groups: Sequence[str]) -> WeightsByGroup:
    """The hand-picked WP 4.1 estimates, restricted to the groups in play."""
    return {g: dict(_STATIC_WEIGHTS[g]) for g in groups}


def load_weights_file(path: Path, groups: Sequence[str]) -> WeightsByGroup:
    """Load a calibrated weights file, falling back to static per missing group.

    Accepts the calibrator's output shape (``{"weights": {...}}``) or a bare
    ``{group: {...}}`` table.
    """
    data = json.loads(path.read_text(encoding="utf-8"))
    table = data.get("weights", data) if isinstance(data, dict) else {}
    out: WeightsByGroup = {}
    for g in groups:
        w = table.get(g)
        if isinstance(w, dict) and all(name in w for name in SIGNAL_NAMES):
            out[g] = {name: float(w[name]) for name in SIGNAL_NAMES}
        else:
            out[g] = dict(_STATIC_WEIGHTS[g])
    return out


def _band_agreement(preds: Sequence[float], labels: Sequence[float]) -> tuple[float, float]:
    exact = adjacent = 0
    for p, lbl in zip(preds, labels):
        di = abs(_BAND_INDEX[determine_band(p)] - _BAND_INDEX[determine_band(lbl)])
        exact += di == 0
        adjacent += di <= 1
    n = len(preds)
    return (exact / n, adjacent / n) if n else (0.0, 0.0)


def evaluate_dataset(
    samples: Sequence[LabeledSample],
    weights_by_group: WeightsByGroup,
    weights_source: str = "static",
) -> EvalReport:
    """Score every sample with ``weights_by_group`` and summarise quality."""
    if not samples:
        raise ValueError("no samples to evaluate")
    preds = predict_scores(samples, weights_by_group)
    labels = [s.label for s in samples]

    exact, adjacent = _band_agreement(preds, labels)

    # Per predicted band.
    by_band: Dict[str, List[int]] = {b: [] for b in BAND_ORDER}
    for i, p in enumerate(preds):
        by_band[determine_band(p)].append(i)
    bands = [
        BandRow(
            band=b,
            count=len(idxs),
            mean_predicted=round(_mean([preds[i] for i in idxs]), 2),
            mean_label=round(_mean([labels[i] for i in idxs]), 2),
        )
        for b in BAND_ORDER
        for idxs in [by_band[b]]
        if idxs
    ]

    # Per source_type (canonical group).
    per_group: List[GroupRow] = []
    for g in make_groups(samples):
        idxs = [i for i, s in enumerate(samples) if canonical_source_type(s.source_type) == g]
        gp = [preds[i] for i in idxs]
        gl = [labels[i] for i in idxs]
        meaningful = len(idxs) >= 3
        per_group.append(
            GroupRow(
                source_type=g,
                count=len(idxs),
                spearman=round(spearman(gp, gl), 3) if meaningful else None,
                concordance=round(pairwise_concordance(gp, gl), 3) if meaningful else None,
            )
        )

    return EvalReport(
        n=len(samples),
        weights_source=weights_source,
        spearman=round(spearman(preds, labels), 4),
        concordance=round(pairwise_concordance(preds, labels), 4),
        band_agreement_exact=round(exact, 4),
        band_agreement_adjacent=round(adjacent, 4),
        bands=bands,
        per_source_type=per_group,
    )


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m cats.calibration.evaluate",
        description="Measure scoring quality (rank agreement + band agreement) on a labelled dataset.",
    )
    parser.add_argument("--dataset", required=True, type=Path, help="labelled dataset (.jsonl/.json)")
    parser.add_argument(
        "--weights",
        type=Path,
        default=None,
        help="calibrated weights file; omit to use the static WP 4.1 estimates",
    )
    parser.add_argument("--json", action="store_true", help="emit the report as JSON")
    args = parser.parse_args(argv)

    if not args.dataset.exists():
        parser.error(f"dataset not found: {args.dataset}")

    samples = load_dataset(args.dataset)
    groups = make_groups(samples)

    if args.weights is not None:
        if not args.weights.exists():
            parser.error(f"weights file not found: {args.weights}")
        weights = load_weights_file(args.weights, groups)
        source = str(args.weights)
    else:
        weights = static_weights_for(groups)
        source = "static (WP 4.1 estimates)"

    report = evaluate_dataset(samples, weights, weights_source=source)
    print(report.to_json() if args.json else report.render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
