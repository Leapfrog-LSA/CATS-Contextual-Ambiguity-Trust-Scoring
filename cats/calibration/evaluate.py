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
  * per-class precision / recall / F1 over the reliable-vs-unreliable split,
    plus their macro-F1 — rank metrics average over the whole range and can
    stay high while the low tail is missed, which is the tail that matters
  * a per-source_type breakdown

Usage::

    python -m cats.calibration.evaluate --dataset examples/calibration_sample.jsonl
    python -m cats.calibration.evaluate --dataset holdout.jsonl --weights calibrated_weights.json

With ``--weights`` the harness scores using a calibrated weights file (the
output of ``python -m cats.calibration``); otherwise it uses the static WP 4.1
estimates. This makes "before vs after calibration" a one-command comparison.

Optionally (``--bootstrap-replicates`` + ``--bootstrap-level``, with
``--bootstrap-seed``) it also reports a percentile bootstrap interval for
concordance, Spearman and the ``unreliable`` recall, and with
``--compare-weights`` a *paired* comparison of two weight tables on the same
resampled rows. Without those options the output is unchanged. The resampled
unit is the dataset row: the records carry no source identifier, so on a
message-axis split a row is a source *slice*, not a whole source.
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence

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

# The binary split the per-class metrics are computed over. Defined through
# `determine_band` rather than a literal cutoff so it always follows the shipped
# band semantics: changing the band thresholds moves this split with them, and
# introduces no second threshold to keep in sync. "Unreliable" is the rare,
# harder class — reporting its F1 separately is the point of the split.
UNRELIABLE_BANDS = frozenset({"low", "very_low"})


def is_unreliable(score: float) -> bool:
    """Whether a score (predicted or label) falls in the unreliable low tail."""
    return determine_band(score) in UNRELIABLE_BANDS


@dataclass
class BandRow:
    band: str
    count: int
    mean_predicted: float
    mean_label: float


@dataclass
class ClassRow:
    """Precision/recall/F1 for one side of the reliable-vs-unreliable split.

    ``None`` marks a quantity the data cannot define rather than a zero:
    precision needs at least one prediction of the class, recall at least one
    labelled member, F1 either. Reporting 0.0 there would read as "the model
    failed" when the truth is "this dataset cannot say".
    """

    label: str
    support: int  # samples whose *label* falls in this class
    predicted: int  # samples *predicted* into this class
    precision: Optional[float]
    recall: Optional[float]
    f1: Optional[float]


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
    macro_f1: Optional[float]
    bands: List[BandRow] = field(default_factory=list)
    per_class: List[ClassRow] = field(default_factory=list)
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
            f"Macro-F1           : {self.macro_f1:.3f}" if self.macro_f1 is not None else "Macro-F1           : n/a",
            "",
            "Per predicted band:",
            f"  {'band':12s} {'n':>4s} {'mean_pred':>10s} {'mean_label':>11s}",
        ]
        for r in self.bands:
            lines.append(f"  {r.band:12s} {r.count:>4d} {r.mean_predicted:>10.1f} {r.mean_label:>11.1f}")
        lines.append("")
        lines.append("Per class (unreliable = bands low/very_low):")
        lines.append(f"  {'class':12s} {'supp':>5s} {'pred':>5s} {'precis':>7s} {'recall':>7s} {'f1':>7s}")
        for c in self.per_class:
            pr = f"{c.precision:.3f}" if c.precision is not None else "n/a"
            rc = f"{c.recall:.3f}" if c.recall is not None else "n/a"
            f1 = f"{c.f1:.3f}" if c.f1 is not None else "n/a"
            lines.append(f"  {c.label:12s} {c.support:>5d} {c.predicted:>5d} {pr:>7s} {rc:>7s} {f1:>7s}")
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
    if not isinstance(table, dict):  # e.g. {"weights": [...]}: treat as no groups
        table = {}
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


def _class_metrics(preds: Sequence[float], labels: Sequence[float]) -> List[ClassRow]:
    """Precision/recall/F1 for each side of the reliable-vs-unreliable split.

    Both the prediction and the label are reduced to a class by the band they
    fall into, so this measures the same thing a reader of the band does: did
    the score put this source in the low tail, and did the label agree?

    F1 uses the ``2·tp / (2·tp + fp + fn)`` form: identical to the harmonic
    mean of precision and recall wherever both are defined, and it still yields
    0.0 (rather than a division by zero) for a class that was missed entirely
    but does occur in the data.
    """
    rows: List[ClassRow] = []
    for name, want_unreliable in (("unreliable", True), ("reliable", False)):
        tp = fp = fn = 0
        for p, lbl in zip(preds, labels):
            pred_in = is_unreliable(p) == want_unreliable
            label_in = is_unreliable(lbl) == want_unreliable
            if pred_in and label_in:
                tp += 1
            elif pred_in:
                fp += 1
            elif label_in:
                fn += 1
        rows.append(
            ClassRow(
                label=name,
                support=tp + fn,
                predicted=tp + fp,
                precision=round(tp / (tp + fp), 4) if tp + fp else None,
                recall=round(tp / (tp + fn), 4) if tp + fn else None,
                f1=round(2 * tp / (2 * tp + fp + fn), 4) if 2 * tp + fp + fn else None,
            )
        )
    return rows


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
    per_class = _class_metrics(preds, labels)
    defined_f1 = [c.f1 for c in per_class if c.f1 is not None]

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
        macro_f1=round(_mean(defined_f1), 4) if defined_f1 else None,
        bands=bands,
        per_class=per_class,
        per_source_type=per_group,
    )


# --------------------------------------------------------------------------- #
# Uncertainty: percentile bootstrap over dataset rows (measurement only)
# --------------------------------------------------------------------------- #

BOOTSTRAP_METHOD = (
    "percentile bootstrap (resample rows with replacement; linear interpolation between order statistics)"
)
RESAMPLING_UNIT = "dataset row"
UNCERTAINTY_METRICS = ("concordance", "spearman", "recall_unreliable")

# Literal accepted by ``--compare-weights`` for the static WP 4.1 estimates.
STATIC_WEIGHTS_LITERAL = "static"


def _concordance_or_none(preds: Sequence[float], labels: Sequence[float]) -> Optional[float]:
    # pairwise_concordance returns 0.0 when no pair has different labels:
    # that is "undefined", not "every pair discordant", so it is caught first.
    if len(set(labels)) < 2:
        return None
    return pairwise_concordance(preds, labels)


def _spearman_or_none(preds: Sequence[float], labels: Sequence[float]) -> Optional[float]:
    # spearman returns 0.0 for constant predictions or labels: undefined, not "no correlation".
    if len(set(preds)) < 2 or len(set(labels)) < 2:
        return None
    return spearman(preds, labels)


def _recall_unreliable_or_none(preds: Sequence[float], labels: Sequence[float]) -> Optional[float]:
    # Recall is undefined when no label is unreliable (_class_metrics gives None too).
    if not any(is_unreliable(lbl) for lbl in labels):
        return None
    rows = {r.label: r for r in _class_metrics(preds, labels)}
    return rows["unreliable"].recall


_METRIC_FNS: Dict[str, Callable[[Sequence[float], Sequence[float]], Optional[float]]] = {
    "concordance": _concordance_or_none,
    "spearman": _spearman_or_none,
    "recall_unreliable": _recall_unreliable_or_none,
}


def _percentile(sorted_xs: Sequence[float], q: float) -> float:
    """Linear-interpolation percentile of an already sorted, non-empty sequence."""
    if len(sorted_xs) == 1:
        return sorted_xs[0]
    pos = q * (len(sorted_xs) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(sorted_xs) - 1)
    frac = pos - lo
    return sorted_xs[lo] + (sorted_xs[hi] - sorted_xs[lo]) * frac


def _interval(values: Sequence[float], level: float) -> tuple[Optional[float], Optional[float]]:
    if not values:
        return None, None
    xs = sorted(values)
    alpha = 1.0 - level
    return _percentile(xs, alpha / 2.0), _percentile(xs, 1.0 - alpha / 2.0)


def _r(x: Optional[float]) -> Optional[float]:
    return round(x, 4) if x is not None else None


def _bootstrap_indices(n: int, replicates: int, seed: int) -> List[List[int]]:
    """Row indices for each replicate, drawn with replacement (same stdlib RNG style as the GA)."""
    rng = random.Random(seed)
    return [[rng.randrange(n) for _ in range(n)] for _ in range(replicates)]


def _validate_bootstrap_params(n: int, replicates: int, level: float) -> None:
    if n <= 0:
        raise ValueError("no samples to resample")
    if replicates < 1:
        raise ValueError("replicates must be >= 1")
    if not 0.0 < level < 1.0:
        raise ValueError("level must be strictly between 0 and 1 (e.g. 0.9)")


@dataclass
class MetricInterval:
    """Point estimate and bootstrap interval for one metric.

    ``excluded`` counts replicates where the metric was undefined (see the
    ``*_or_none`` helpers); they are left out of the interval, never counted as 0.
    """

    metric: str
    point: Optional[float]
    lower: Optional[float]
    upper: Optional[float]
    defined: int
    excluded: int


@dataclass
class MetricDifference:
    """Paired difference ``primary − reference`` for one metric on the same resampled rows."""

    metric: str
    primary: Optional[float]
    reference: Optional[float]
    point_difference: Optional[float]
    lower: Optional[float]
    upper: Optional[float]
    defined: int
    excluded: int


@dataclass
class PairedComparison:
    primary_weights: str
    reference_weights: str
    metrics: List[MetricDifference] = field(default_factory=list)


@dataclass
class UncertaintyReport:
    method: str
    resampling_unit: str
    replicates: int
    seed: int
    level: float
    metrics: List[MetricInterval] = field(default_factory=list)
    paired_comparison: Optional[PairedComparison] = None

    def to_dict(self) -> dict:
        return asdict(self)

    def render(self) -> str:
        def fmt(x: Optional[float], signed: bool = False) -> str:
            if x is None:
                return "n/a"
            return f"{x:+.3f}" if signed else f"{x:.3f}"

        lines = [
            "Uncertainty:",
            f"  method          : {self.method}",
            f"  resampling unit : {self.resampling_unit}",
            f"  replicates      : {self.replicates}",
            f"  seed            : {self.seed}",
            f"  level           : {self.level:g}",
            f"  {'metric':18s} {'point':>7s} {'lower':>7s} {'upper':>7s} {'defined':>8s} {'excluded':>9s}",
        ]
        for m in self.metrics:
            signed = m.metric == "spearman"
            lines.append(
                f"  {m.metric:18s} {fmt(m.point, signed):>7s} {fmt(m.lower, signed):>7s} "
                f"{fmt(m.upper, signed):>7s} {m.defined:>8d} {m.excluded:>9d}"
            )
        pc = self.paired_comparison
        if pc is not None:
            lines.append("")
            lines.append("Paired comparison (difference = primary - reference, same resampled rows):")
            lines.append(f"  primary   : {pc.primary_weights}")
            lines.append(f"  reference : {pc.reference_weights}")
            lines.append(
                f"  {'metric':18s} {'primary':>8s} {'refer.':>8s} {'diff':>7s} {'lower':>7s} {'upper':>7s} "
                f"{'defined':>8s} {'excluded':>9s}"
            )
            for d in pc.metrics:
                signed = d.metric == "spearman"
                lines.append(
                    f"  {d.metric:18s} {fmt(d.primary, signed):>8s} {fmt(d.reference, signed):>8s} "
                    f"{fmt(d.point_difference, True):>7s} {fmt(d.lower, True):>7s} {fmt(d.upper, True):>7s} "
                    f"{d.defined:>8d} {d.excluded:>9d}"
                )
        return "\n".join(lines)


def bootstrap_metrics(
    samples: Sequence[LabeledSample],
    weights_by_group: WeightsByGroup,
    *,
    replicates: int,
    level: float,
    seed: int,
) -> List[MetricInterval]:
    """Percentile bootstrap interval for concordance, Spearman and unreliable recall.

    Scores are computed once with ``predict_scores`` and then resampled by row
    index, so the weights and the scoring path are exactly those of
    :func:`evaluate_dataset`. ``replicates`` and ``level`` have no default on
    purpose: they are methodological choices left to the caller.
    """
    _validate_bootstrap_params(len(samples), replicates, level)
    preds = predict_scores(samples, weights_by_group)
    labels = [s.label for s in samples]
    draws = _bootstrap_indices(len(samples), replicates, seed)
    out: List[MetricInterval] = []
    for name in UNCERTAINTY_METRICS:
        fn = _METRIC_FNS[name]
        values: List[float] = []
        for idx in draws:
            v = fn([preds[i] for i in idx], [labels[i] for i in idx])
            if v is not None:
                values.append(v)
        lo, hi = _interval(values, level)
        out.append(
            MetricInterval(
                metric=name,
                point=_r(fn(preds, labels)),
                lower=_r(lo),
                upper=_r(hi),
                defined=len(values),
                excluded=replicates - len(values),
            )
        )
    return out


def paired_bootstrap_comparison(
    samples: Sequence[LabeledSample],
    primary: WeightsByGroup,
    reference: WeightsByGroup,
    *,
    replicates: int,
    level: float,
    seed: int,
    primary_source: str = "primary",
    reference_source: str = "reference",
) -> PairedComparison:
    """Paired bootstrap of ``metric(primary) − metric(reference)`` on the same rows.

    Each replicate applies the *same* resampled indices to both tables, so the
    interval is for the difference itself rather than two independent intervals.
    A replicate where the metric is undefined for either table is excluded and
    counted for that metric.
    """
    _validate_bootstrap_params(len(samples), replicates, level)
    p_preds = predict_scores(samples, primary)
    r_preds = predict_scores(samples, reference)
    labels = [s.label for s in samples]
    draws = _bootstrap_indices(len(samples), replicates, seed)
    rows: List[MetricDifference] = []
    for name in UNCERTAINTY_METRICS:
        fn = _METRIC_FNS[name]
        diffs: List[float] = []
        for idx in draws:
            lab = [labels[i] for i in idx]
            a = fn([p_preds[i] for i in idx], lab)
            b = fn([r_preds[i] for i in idx], lab)
            if a is not None and b is not None:
                diffs.append(a - b)
        pa, pb = fn(p_preds, labels), fn(r_preds, labels)
        lo, hi = _interval(diffs, level)
        rows.append(
            MetricDifference(
                metric=name,
                primary=_r(pa),
                reference=_r(pb),
                point_difference=_r(pa - pb) if pa is not None and pb is not None else None,
                lower=_r(lo),
                upper=_r(hi),
                defined=len(diffs),
                excluded=replicates - len(diffs),
            )
        )
    return PairedComparison(primary_weights=primary_source, reference_weights=reference_source, metrics=rows)


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
    unc = parser.add_argument_group(
        "uncertainty (optional)",
        "percentile bootstrap over dataset rows; --bootstrap-replicates and --bootstrap-level have no "
        "default and are both required as soon as any of these options is given",
    )
    unc.add_argument("--bootstrap-replicates", type=int, default=None, help="number of bootstrap replicates (>= 1)")
    unc.add_argument(
        "--bootstrap-level", type=float, default=None, help="interval level, strictly between 0 and 1 (e.g. 0.9)"
    )
    unc.add_argument("--bootstrap-seed", type=int, default=None, help="RNG seed for the resampling (default 0)")
    unc.add_argument(
        "--compare-weights",
        default=None,
        metavar="PATH|static",
        help="second weights table for a paired comparison (difference = --weights table minus this one); "
        f"'{STATIC_WEIGHTS_LITERAL}' means the static WP 4.1 estimates",
    )
    args = parser.parse_args(argv)

    want_uncertainty = any(
        v is not None
        for v in (args.bootstrap_replicates, args.bootstrap_level, args.bootstrap_seed, args.compare_weights)
    )
    if want_uncertainty:
        if args.bootstrap_replicates is None or args.bootstrap_level is None:
            parser.error("uncertainty requires both --bootstrap-replicates and --bootstrap-level (no defaults)")
        if args.bootstrap_replicates < 1:
            parser.error("--bootstrap-replicates must be >= 1")
        if not 0.0 < args.bootstrap_level < 1.0:
            parser.error("--bootstrap-level must be strictly between 0 and 1")

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
    if not want_uncertainty:
        print(report.to_json() if args.json else report.render())
        return 0

    seed = args.bootstrap_seed if args.bootstrap_seed is not None else 0
    uncertainty = UncertaintyReport(
        method=BOOTSTRAP_METHOD,
        resampling_unit=RESAMPLING_UNIT,
        replicates=args.bootstrap_replicates,
        seed=seed,
        level=args.bootstrap_level,
        metrics=bootstrap_metrics(
            samples, weights, replicates=args.bootstrap_replicates, level=args.bootstrap_level, seed=seed
        ),
    )
    if args.compare_weights is not None:
        if args.compare_weights == STATIC_WEIGHTS_LITERAL:
            ref_weights = static_weights_for(groups)
            ref_source = "static (WP 4.1 estimates)"
        else:
            ref_path = Path(args.compare_weights)
            if not ref_path.exists():
                parser.error(f"compare weights file not found: {ref_path}")
            ref_weights = load_weights_file(ref_path, groups)
            ref_source = str(ref_path)
        uncertainty.paired_comparison = paired_bootstrap_comparison(
            samples,
            weights,
            ref_weights,
            replicates=args.bootstrap_replicates,
            level=args.bootstrap_level,
            seed=seed,
            primary_source=source,
            reference_source=ref_source,
        )

    if args.json:
        payload = report.to_dict()
        payload["uncertainty"] = uncertainty.to_dict()
        print(json.dumps(payload, indent=2))
    else:
        print(report.render() + "\n\n" + uncertainty.render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
