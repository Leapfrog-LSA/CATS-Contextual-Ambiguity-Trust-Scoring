"""Unit tests — scoring engine and weight logic."""
import pytest
from cats.signals.types import SignalResult
from cats.scoring.engine import aggregate_score, determine_band, requires_human_review
from cats.scoring.weights import DEFAULT_WEIGHTS, get_dynamic_weights
from cats.scoring.explainer import generate_explanation


def _sig(name: str, value: float, conf: float = 0.8) -> SignalResult:
    return SignalResult(name=name, value=value, confidence=conf)


# ── aggregate_score ─────────────────────────────────────────────────────────────

def test_aggregate_score_in_range():
    signals = [_sig("coherence", 80), _sig("volatility", 60), _sig("silence", 70), _sig("gaming", 50)]
    s = aggregate_score(signals, DEFAULT_WEIGHTS)
    assert 0.0 <= s <= 100.0


def test_aggregate_score_weighted_correctly():
    # Only coherence contributes (weight 0.30), rest are 0
    signals = [_sig("coherence", 100), _sig("volatility", 0), _sig("silence", 0), _sig("gaming", 0)]
    s = aggregate_score(signals, DEFAULT_WEIGHTS)
    assert abs(s - 30.0) < 0.01


def test_aggregate_score_empty_signals_returns_default():
    assert aggregate_score([], {}) == 50.0


def test_aggregate_score_all_perfect():
    signals = [_sig(n, 100) for n in ["coherence", "volatility", "silence", "gaming"]]
    assert aggregate_score(signals, DEFAULT_WEIGHTS) == pytest.approx(100.0)


# ── determine_band ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("score,expected", [
    (100, "high"), (80, "high"), (79.9, "medium_high"),
    (60, "medium_high"), (59.9, "medium"), (40, "medium"),
    (39.9, "low"), (20, "low"), (19.9, "very_low"), (0, "very_low"),
])
def test_determine_band_boundaries(score, expected):
    assert determine_band(score) == expected


# ── requires_human_review ───────────────────────────────────────────────────────

def test_review_required_for_low_band():
    assert requires_human_review(35, "low", [_sig("x", 35)]) is True


def test_review_required_for_very_low_band():
    assert requires_human_review(5, "very_low", [_sig("x", 5)]) is True


def test_no_review_for_high_band():
    signals = [_sig(n, 90) for n in ["coherence", "volatility", "silence", "gaming"]]
    assert requires_human_review(90, "high", signals) is False


def test_review_required_low_confidence_and_score():
    signals = [_sig("x", 45, conf=0.2)]  # low confidence
    assert requires_human_review(45, "medium", signals) is True


# ── weights ────────────────────────────────────────────────────────────────────

def test_default_weights_sum_to_one():
    assert abs(sum(DEFAULT_WEIGHTS.values()) - 1.0) < 1e-6


@pytest.mark.parametrize("ctx", [
    {"source_type": "social"},
    {"source_type": "news"},
    {"source_type": "unknown"},
    {},
])
def test_dynamic_weights_always_sum_to_one(ctx):
    w = get_dynamic_weights(ctx)
    assert abs(sum(w.values()) - 1.0) < 1e-6


def test_social_source_weights_emphasise_volatility():
    w = get_dynamic_weights({"source_type": "social"})
    assert w["volatility"] >= w["coherence"]


def test_news_source_weights_emphasise_coherence():
    w = get_dynamic_weights({"source_type": "news"})
    assert w["coherence"] >= w["volatility"]


# ── explainer ──────────────────────────────────────────────────────────────────

def test_explainer_contains_required_keys():
    signals = [_sig("coherence", 70), _sig("volatility", 40)]
    exp = generate_explanation(65.0, "medium_high", signals, DEFAULT_WEIGHTS)
    assert "trust_score" in exp
    assert "band" in exp
    assert "signals" in exp
    assert "disclaimer" in exp


def test_explainer_disclaimer_present():
    signals = [_sig("coherence", 70)]
    exp = generate_explanation(70, "medium_high", signals, DEFAULT_WEIGHTS)
    assert len(exp["disclaimer"]) > 20
