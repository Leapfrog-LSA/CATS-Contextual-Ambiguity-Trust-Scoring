"""CATS weight calibration.

Tooling to empirically calibrate the signal weight matrix against a labelled
dataset, replacing the initial hand-picked estimates flagged in WP 4.1.

The optimisation uses a small, dependency-free genetic algorithm (see
``cats.calibration.ga``). Because CATS scores are *ordinal* rankings (WP 4.3),
the objective maximises a rank-agreement metric (Spearman / pairwise
concordance) rather than absolute error.
"""

from cats.calibration.calibrate import CalibrationOutput, calibrate
from cats.calibration.dataset import LabeledSample, load_dataset
from cats.calibration.ga import GAConfig, GAResult, GeneticOptimizer

__all__ = [
    "calibrate",
    "CalibrationOutput",
    "load_dataset",
    "LabeledSample",
    "GeneticOptimizer",
    "GAConfig",
    "GAResult",
]
