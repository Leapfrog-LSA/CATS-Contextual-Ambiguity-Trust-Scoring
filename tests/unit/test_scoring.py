import pytest

from cats.scoring.engine import aggregate_score, determine_band, requires_human_review
from cats.scoring.weights import DEFAULT_WEIGHTS, get_dynamic_weights
from cats.signals.types import SignalResult


def _signal(name, value, confidence=0.5):
    return SignalResult(name=name, value=value, confidence=confidence)


class TestAggregateScore:
    def test_weighted_average(self):
        signals = [_signal("coherence", 80), _signal("volatility", 60)]
        weights = {"coherence": 0.6, "volatility": 0.4}
        score = aggregate_score(signals, weights)
        assert abs(score - 72.0) < 0.01

    def test_missing_weight_uses_default(self):
        signals = [_signal("coherence", 100)]
        score = aggregate_score(signals, {})
        assert abs(score - 100.0) < 0.01

    def test_empty_signals(self):
        assert aggregate_score([], {}) == 50.0


class TestDetermineBand:
    @pytest.mark.parametrize(
        "score,expected",
        [
            (95, "high"),
            (80, "high"),
            (72, "medium_high"),
            (60, "medium_high"),
            (50, "medium"),
            (40, "medium"),
            (30, "low"),
            (20, "low"),
            (10, "very_low"),
            (0, "very_low"),
        ],
    )
    def test_band_thresholds(self, score, expected):
        assert determine_band(score) == expected


class TestRequiresHumanReview:
    def test_low_band_requires_review(self):
        assert requires_human_review(15, "very_low", []) is True
        assert requires_human_review(25, "low", []) is True

    def test_low_confidence_low_score(self):
        signals = [_signal("coherence", 40, confidence=0.2)]
        assert requires_human_review(45, "medium", signals) is True

    def test_high_score_no_review(self):
        signals = [_signal("coherence", 85, confidence=0.8)]
        assert requires_human_review(85, "high", signals) is False


class TestWeights:
    def test_default_weights_sum_to_one(self):
        assert abs(sum(DEFAULT_WEIGHTS.values()) - 1.0) < 1e-6

    def test_social_weights(self):
        w = get_dynamic_weights({"source_type": "social"})
        assert abs(sum(w.values()) - 1.0) < 1e-6
        assert w["volatility"] == 0.30

    def test_news_weights(self):
        w = get_dynamic_weights({"source_type": "news"})
        assert abs(sum(w.values()) - 1.0) < 1e-6
        assert w["coherence"] == 0.35

    def test_unknown_source_uses_defaults(self):
        w = get_dynamic_weights({"source_type": "blog"})
        assert w == DEFAULT_WEIGHTS
