"""Run weight calibration and emit a reusable weights file.

CLI::

    python -m cats.calibration.calibrate --dataset data.jsonl --out calibrated_weights.json

The emitted JSON is consumable by ``cats.scoring.weights``: point the
``CATS_WEIGHTS_FILE`` setting at it to serve calibrated weights in production.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Sequence

from cats.calibration.dataset import LabeledSample, load_dataset
from cats.calibration.ga import GAConfig, GeneticOptimizer
from cats.calibration.objective import (
    METRICS,
    WeightsByGroup,
    bounds_for,
    build_fitness,
    decode,
    predict_scores,
)

# Source-type group -> the context a CATS caller would send for it.
_GROUP_CONTEXT = {"social": {"source_type": "social"}, "news": {"source_type": "news"}, "default": {}}


@dataclass
class CalibrationOutput:
    weights: WeightsByGroup
    metric: str
    score: float
    baseline_score: float
    groups: List[str]
    generations: int
    history: List[float] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "metric": self.metric,
            "score": round(self.score, 6),
            "baseline_score": round(self.baseline_score, 6),
            "improvement": round(self.score - self.baseline_score, 6),
            "groups": self.groups,
            "generations": self.generations,
            "weights": {g: {k: round(v, 6) for k, v in w.items()} for g, w in self.weights.items()},
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


def _baseline_weights(groups: Sequence[str]) -> WeightsByGroup:
    # Imported lazily so calibration does not require app settings/env to be set.
    from cats.scoring.weights import get_dynamic_weights

    return {g: dict(get_dynamic_weights(_GROUP_CONTEXT.get(g, {}))) for g in groups}


def calibrate(
    samples: Sequence[LabeledSample],
    metric: str = "spearman",
    config: Optional[GAConfig] = None,
) -> CalibrationOutput:
    fitness, groups = build_fitness(samples, metric)
    optimizer = GeneticOptimizer(bounds_for(groups), fitness, config)
    result = optimizer.run()

    labels = [s.label for s in samples]
    metric_fn = METRICS[metric]
    baseline = metric_fn(predict_scores(samples, _baseline_weights(groups)), labels)

    return CalibrationOutput(
        weights=decode(result.best_genome, groups),
        metric=metric,
        score=result.best_fitness,
        baseline_score=baseline,
        groups=groups,
        generations=len(result.history),
        history=result.history,
    )


def main(argv: Optional[List[str]] = None) -> CalibrationOutput:
    parser = argparse.ArgumentParser(description="Calibrate CATS signal weights via genetic search.")
    parser.add_argument("--dataset", required=True, help="Path to a .jsonl or .json labelled dataset")
    parser.add_argument("--metric", default="spearman", choices=sorted(METRICS), help="Fitness metric")
    parser.add_argument("--out", default="calibrated_weights.json", help="Output weights file")
    parser.add_argument("--generations", type=int, default=80)
    parser.add_argument("--pop-size", type=int, default=60)
    parser.add_argument("--seed", type=int, default=None, help="RNG seed for reproducible runs")
    args = parser.parse_args(argv)

    samples = load_dataset(args.dataset)
    config = GAConfig(generations=args.generations, pop_size=args.pop_size, seed=args.seed)
    output = calibrate(samples, metric=args.metric, config=config)

    Path(args.out).write_text(output.to_json(), encoding="utf-8")
    print(
        f"Calibrated {len(samples)} samples over groups {output.groups}\n"
        f"  metric         : {output.metric}\n"
        f"  baseline score : {output.baseline_score:.4f}\n"
        f"  calibrated     : {output.score:.4f}  (Δ {output.score - output.baseline_score:+.4f})\n"
        f"  written to     : {args.out}"
    )
    return output


if __name__ == "__main__":  # pragma: no cover
    main()
