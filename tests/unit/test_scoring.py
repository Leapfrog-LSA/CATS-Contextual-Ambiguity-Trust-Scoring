import pytest

from cats.scoring.engine import (
    DOMAIN_PENALTY_WEIGHT,
    aggregate_score,
    apply_domain_penalty,
    determine_band,
    requires_human_review,
)
from cats.scoring.weights import DEFAULT_WEIGHTS, get_dynamic_weights
from cats.signals.types import SignalResult


def _signal(name, value, confidence=0.5):
    return SignalResult(name=name, value=value, confidence=confidence)


class TestAggregateScore:
    def test_weighted_average(self):
        # volatility is negative-polarity: 60 enters as 100-60=40.
        signals = [_signal("coherence", 80), _signal("volatility", 60)]
        weights = {"coherence": 0.6, "volatility": 0.4}
        score = aggregate_score(signals, weights)
        assert abs(score - 64.0) < 0.01

    def test_missing_weight_uses_default(self):
        signals = [_signal("coherence", 100)]
        score = aggregate_score(signals, {})
        assert abs(score - 100.0) < 0.01

    def test_empty_signals(self):
        assert aggregate_score([], {}) == 50.0

    def test_negative_polarity_signals_are_inverted(self):
        # A pathological source: silent, volatile, gamed. High raw values on
        # the negative signals must LOWER the score, not raise it.
        bad = [_signal("silence", 90), _signal("volatility", 90), _signal("gaming", 90)]
        good = [_signal("silence", 5), _signal("volatility", 5), _signal("gaming", 5)]
        weights = {"silence": 0.4, "volatility": 0.3, "gaming": 0.3}
        assert aggregate_score(bad, weights) < 20.0
        assert aggregate_score(good, weights) > 80.0

    def test_all_neutral_signals_score_neutral(self):
        signals = [
            _signal("coherence", 50),
            _signal("volatility", 50),
            _signal("silence", 50),
            _signal("gaming", 50),
        ]
        assert abs(aggregate_score(signals, DEFAULT_WEIGHTS) - 50.0) < 0.01


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


class TestValidateWeights:
    def test_rounded_calibrated_weights_accepted_and_normalised(self):
        # A calibrated file rounds each weight independently, so a valid table
        # can sum to 1.000001. The loader must accept it (not fall back to
        # static) and renormalise to an exact sum.
        from cats.scoring.weights import _validate_weights

        w = _validate_weights({"coherence": 0.395030, "volatility": 0.076897, "silence": 0.469124, "gaming": 0.058949})
        assert abs(sum(w.values()) - 1.0) < 1e-9

    def test_genuinely_malformed_weights_rejected(self):
        import pytest

        from cats.scoring.weights import _validate_weights

        with pytest.raises(ValueError):
            _validate_weights({"coherence": 0.5, "volatility": 0.9})  # sums to 1.4
        with pytest.raises(ValueError):
            _validate_weights({"coherence": 0.0, "volatility": 0.0})  # sums to 0


class TestApplyDomainPenalty:
    def _domain(self, value, confidence=1.0):
        return SignalResult(name="domain_provenance", value=value, confidence=confidence)

    def test_clean_domain_is_no_op(self):
        # A clean domain (value 0) must never change the score — the penalty is
        # asymmetric and only lowers scores for red-flag domains.
        assert apply_domain_penalty(73.0, self._domain(0.0)) == 73.0

    def test_clone_domain_is_penalised(self):
        # spiegel.ltd scores 65 -> penalty 0.6*65 = 39.
        assert abs(apply_domain_penalty(73.0, self._domain(65.0)) - (73.0 - DOMAIN_PENALTY_WEIGHT * 65.0)) < 1e-9

    def test_penalty_clamps_at_zero(self):
        assert apply_domain_penalty(10.0, self._domain(100.0)) == 0.0

    def test_no_domain_passthrough(self):
        assert apply_domain_penalty(55.0, None) == 55.0

    def test_zero_confidence_domain_passthrough(self):
        # No URL supplied -> zero confidence -> score unchanged.
        assert apply_domain_penalty(55.0, self._domain(0.0, confidence=0.0)) == 55.0
