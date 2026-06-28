import json

import pytest

from cats.calibration.calibrate import calibrate
from cats.calibration.dataset import LabeledSample, load_dataset
from cats.calibration.ga import GAConfig, GeneticOptimizer
from cats.calibration.objective import bounds_for, canonical_source_type, decode, pairwise_concordance, spearman


# ── GA engine ─────────────────────────────────────────────────────────────
def test_ga_maximises_simple_objective():
    # Fitness rewards genes close to their upper bound -> optimum at (1, 1, 1).
    opt = GeneticOptimizer(
        bounds=[(0.0, 1.0)] * 3,
        fitness_fn=lambda g: sum(g),
        config=GAConfig(pop_size=40, generations=60, seed=7),
    )
    result = opt.run()
    assert result.best_fitness > 2.7
    assert all(0.0 <= x <= 1.0 for x in result.best_genome)


def test_ga_is_reproducible_with_seed():
    cfg = GAConfig(pop_size=20, generations=15, seed=123)
    fit = lambda g: -((g[0] - 0.3) ** 2)  # noqa: E731
    a = GeneticOptimizer([(0.0, 1.0)], fit, cfg).run()
    b = GeneticOptimizer([(0.0, 1.0)], fit, GAConfig(pop_size=20, generations=15, seed=123)).run()
    assert a.best_genome == b.best_genome


def test_ga_rejects_empty_bounds():
    with pytest.raises(ValueError):
        GeneticOptimizer(bounds=[], fitness_fn=lambda g: 0.0)


# ── Encoding ──────────────────────────────────────────────────────────────
def test_canonical_source_type():
    assert canonical_source_type("social") == "social"
    assert canonical_source_type("news") == "news"
    assert canonical_source_type("blog") == "default"
    assert canonical_source_type("whatever") == "default"


def test_decode_normalises_to_one():
    weights = decode([2.0, 2.0, 2.0, 2.0], ["social"])
    assert set(weights["social"]) == {"coherence", "volatility", "silence", "gaming"}
    assert abs(sum(weights["social"].values()) - 1.0) < 1e-9
    assert all(abs(v - 0.25) < 1e-9 for v in weights["social"].values())


def test_decode_handles_multiple_groups():
    groups = ["default", "news"]
    assert len(bounds_for(groups)) == 8
    weights = decode([1, 1, 1, 1, 3, 1, 0, 0], groups)
    assert set(weights) == {"default", "news"}
    assert abs(sum(weights["news"].values()) - 1.0) < 1e-9


# ── Metrics ───────────────────────────────────────────────────────────────
def test_spearman_perfect_and_inverse():
    assert spearman([1, 2, 3, 4], [10, 20, 30, 40]) == pytest.approx(1.0)
    assert spearman([1, 2, 3, 4], [40, 30, 20, 10]) == pytest.approx(-1.0)


def test_pairwise_concordance():
    assert pairwise_concordance([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)
    assert pairwise_concordance([3, 2, 1], [1, 2, 3]) == pytest.approx(0.0)


# ── Dataset ───────────────────────────────────────────────────────────────
def test_load_dataset_jsonl(tmp_path):
    p = tmp_path / "d.jsonl"
    p.write_text(
        '{"source_type": "news", "signals": {"coherence": 1, "volatility": 2, '
        '"silence": 3, "gaming": 4}, "label": 50}\n',
        encoding="utf-8",
    )
    samples = load_dataset(p)
    assert len(samples) == 1
    assert samples[0].signals["coherence"] == 1.0


def test_load_dataset_json_array(tmp_path):
    p = tmp_path / "d.json"
    record = {
        "source_type": "social",
        "signals": {"coherence": 5, "volatility": 5, "silence": 5, "gaming": 5},
        "label": 1,
    }
    p.write_text(json.dumps([record]), encoding="utf-8")
    assert len(load_dataset(p)) == 1


def test_sample_missing_signal_raises():
    with pytest.raises(ValueError):
        LabeledSample(source_type="news", signals={"coherence": 1.0}, label=10.0)


def test_load_dataset_empty_raises(tmp_path):
    p = tmp_path / "empty.jsonl"
    p.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        load_dataset(p)


# ── End-to-end calibration ────────────────────────────────────────────────
def _synthetic_samples():
    # Ground-truth reliability is driven mostly by coherence and (inverse) gaming,
    # so a good calibration should load weight onto those two signals.
    rows = [
        (90, 20, 30, 10),
        (80, 40, 10, 20),
        (70, 60, 50, 25),
        (60, 30, 20, 40),
        (50, 70, 40, 55),
        (40, 50, 60, 60),
        (30, 80, 30, 75),
        (20, 45, 70, 85),
    ]
    samples = []
    for coh, vol, sil, gam in rows:
        label = 0.7 * coh + 0.3 * (100 - gam)  # monotone in coherence, anti-gaming
        samples.append(
            LabeledSample(
                source_type="news",
                signals={"coherence": coh, "volatility": vol, "silence": sil, "gaming": gam},
                label=label,
            )
        )
    return samples


def test_calibrate_beats_baseline_on_synthetic_data():
    samples = _synthetic_samples()
    out = calibrate(samples, metric="spearman", config=GAConfig(generations=120, pop_size=60, seed=42))
    assert out.groups == ["news"]
    assert abs(sum(out.weights["news"].values()) - 1.0) < 1e-9
    # Calibration should achieve strong rank agreement and not regress vs. baseline.
    assert out.score > 0.9
    assert out.score >= out.baseline_score


def test_calibration_output_serialises():
    samples = _synthetic_samples()
    out = calibrate(samples, metric="concordance", config=GAConfig(generations=20, pop_size=20, seed=1))
    payload = json.loads(out.to_json())
    assert payload["metric"] == "concordance"
    assert "news" in payload["weights"]
    assert "improvement" in payload
