"""Dependency-free genetic algorithm for parameter calibration.

The pluggable-fitness design — a swappable ``FitnessFn`` plugged into a generic
generate -> evaluate -> select -> repeat loop — is inspired by the public
SantanderAI/genetic-algorithm project (Apache-2.0). This is an independent,
self-contained reimplementation: no third-party code is copied and there are no
runtime dependencies, so CATS stays MIT-licensed and dependency-light.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Sequence, Tuple

Genome = List[float]
# A fitness function maps a genome to a score; higher is better.
FitnessFn = Callable[[Sequence[float]], float]


@dataclass
class GAConfig:
    """Hyper-parameters for the genetic optimiser."""

    pop_size: int = 60
    generations: int = 80
    crossover_rate: float = 0.9
    mutation_rate: float = 0.15
    mutation_sigma: float = 0.15  # gaussian step, as a fraction of each gene's range
    elitism: int = 2
    tournament_k: int = 3
    seed: Optional[int] = None


@dataclass
class GAResult:
    best_genome: Genome
    best_fitness: float
    history: List[float] = field(default_factory=list)  # best fitness per generation


def _clamp(x: float, lo: float, hi: float) -> float:
    return lo if x < lo else hi if x > hi else x


class GeneticOptimizer:
    """Real-valued genetic algorithm over bounded genes.

    Parameters
    ----------
    bounds:
        One ``(low, high)`` tuple per gene. Genes are kept inside these bounds.
    fitness_fn:
        Callable scoring a genome (higher is better).
    config:
        Optional :class:`GAConfig`; sensible defaults are used otherwise.
    """

    def __init__(
        self,
        bounds: Sequence[Tuple[float, float]],
        fitness_fn: FitnessFn,
        config: Optional[GAConfig] = None,
    ) -> None:
        if not bounds:
            raise ValueError("bounds must contain at least one gene")
        for lo, hi in bounds:
            if hi < lo:
                raise ValueError(f"invalid bound: ({lo}, {hi})")
        self.bounds: List[Tuple[float, float]] = [(float(lo), float(hi)) for lo, hi in bounds]
        self.fitness_fn = fitness_fn
        self.cfg = config or GAConfig()
        self._rng = random.Random(self.cfg.seed)

    def _random_genome(self) -> Genome:
        return [self._rng.uniform(lo, hi) for lo, hi in self.bounds]

    def _mutate(self, genome: Genome) -> Genome:
        out = list(genome)
        for i, (lo, hi) in enumerate(self.bounds):
            if self._rng.random() < self.cfg.mutation_rate:
                span = hi - lo
                out[i] = _clamp(out[i] + self._rng.gauss(0.0, self.cfg.mutation_sigma * span), lo, hi)
        return out

    def _crossover(self, a: Genome, b: Genome) -> Genome:
        if self._rng.random() > self.cfg.crossover_rate:
            return list(a)
        # Per-gene blend: pick parent A, parent B, or their midpoint.
        return [self._rng.choice((ga, gb, (ga + gb) / 2.0)) for ga, gb in zip(a, b)]

    def _tournament(self, scored: List[Tuple[Genome, float]]) -> Genome:
        best: Optional[Tuple[Genome, float]] = None
        for _ in range(self.cfg.tournament_k):
            cand = self._rng.choice(scored)
            if best is None or cand[1] > best[1]:
                best = cand
        assert best is not None
        return best[0]

    def run(self) -> GAResult:
        pop = [self._random_genome() for _ in range(self.cfg.pop_size)]
        best_genome: Optional[Genome] = None
        best_fit = float("-inf")
        history: List[float] = []

        for _ in range(self.cfg.generations):
            scored = [(g, self.fitness_fn(g)) for g in pop]
            scored.sort(key=lambda t: t[1], reverse=True)

            if scored[0][1] > best_fit:
                best_genome, best_fit = list(scored[0][0]), scored[0][1]
            history.append(best_fit)

            elites = min(self.cfg.elitism, len(scored))
            nxt: List[Genome] = [list(scored[i][0]) for i in range(elites)]
            while len(nxt) < self.cfg.pop_size:
                p1 = self._tournament(scored)
                p2 = self._tournament(scored)
                nxt.append(self._mutate(self._crossover(p1, p2)))
            pop = nxt

        assert best_genome is not None
        return GAResult(best_genome=best_genome, best_fitness=best_fit, history=history)
