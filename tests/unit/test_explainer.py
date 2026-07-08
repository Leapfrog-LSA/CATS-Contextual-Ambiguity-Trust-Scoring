from cats.scoring.explainer import generate_explanation
from cats.signals.types import SignalResult


def test_explanation_structure():
    signals = [
        SignalResult(name="coherence", value=70.0, confidence=0.8),
        SignalResult(name="volatility", value=30.0, confidence=0.5),
    ]
    weights = {"coherence": 0.6, "volatility": 0.4}
    result = generate_explanation(65.0, "medium_high", signals, weights)

    assert result["trust_score"] == 65.0
    assert result["band"] == "medium_high"
    assert len(result["signals"]) == 2
    assert "disclaimer" in result
    assert "ordinal" in result["disclaimer"].lower()


def test_explanation_signal_details():
    signals = [SignalResult(name="coherence", value=80.0, confidence=0.9, metadata={"pairs": 5})]
    weights = {"coherence": 1.0}
    result = generate_explanation(80.0, "high", signals, weights)

    detail = result["signals"][0]
    assert detail["signal"] == "coherence"
    assert detail["value"] == 80.0
    assert detail["weight"] == 1.0
    assert detail["contribution"] == 80.0
    assert detail["metadata"] == {"pairs": 5}


def test_score_share_and_primary_driver():
    signals = [
        SignalResult(name="coherence", value=80.0, confidence=0.9),
        SignalResult(name="gaming", value=20.0, confidence=0.5),
    ]
    weights = {"coherence": 0.5, "gaming": 0.5}
    result = generate_explanation(50.0, "medium", signals, weights)

    shares = {d["signal"]: d["score_share_pct"] for d in result["signals"]}
    # coherence: 80*0.5=40; gaming is negative-polarity: (100-20)*0.5=40 -> 50% / 50%
    assert shares["coherence"] == 50.0
    assert shares["gaming"] == 50.0
    assert sum(shares.values()) == 100.0


def test_negative_polarity_signal_contributes_on_reliability_axis():
    signals = [
        SignalResult(name="coherence", value=50.0, confidence=0.9),
        SignalResult(name="silence", value=90.0, confidence=0.9),  # very silent -> unreliable
    ]
    weights = {"coherence": 0.5, "silence": 0.5}
    result = generate_explanation(30.0, "low", signals, weights)

    details = {d["signal"]: d for d in result["signals"]}
    assert details["silence"]["polarity"] == "negative"
    assert details["silence"]["value"] == 90.0
    assert details["silence"]["reliability_value"] == 10.0
    assert details["silence"]["contribution"] == 5.0
    assert details["coherence"]["polarity"] == "positive"
    assert details["coherence"]["reliability_value"] == 50.0
    # High silence must NOT drive the score up: coherence dominates.
    assert result["primary_driver"] == "coherence"


def test_score_share_zero_total_is_safe():
    signals = [SignalResult(name="coherence", value=0.0, confidence=0.0)]
    weights = {"coherence": 0.3}
    result = generate_explanation(0.0, "very_low", signals, weights)
    assert result["signals"][0]["score_share_pct"] == 0.0
    assert result["primary_driver"] == "coherence"


def test_domain_penalty_is_reported_separately():
    signals = [
        SignalResult(name="coherence", value=70.0, confidence=0.8),
        SignalResult(name="domain_provenance", value=65.0, confidence=1.0, metadata={"reasons": ["suspicious_tld"]}),
    ]
    weights = {"coherence": 1.0}
    result = generate_explanation(30.0, "low", signals, weights)

    # domain-provenance is a penalty, not a weighted signal: it must NOT appear
    # in the behavioural decomposition.
    assert [d["signal"] for d in result["signals"]] == ["coherence"]
    penalty = result["domain_penalty"]
    assert penalty["domain_red_flag_score"] == 65.0
    assert penalty["penalty_applied"] == 39.0  # 0.6 * 65
    assert penalty["metadata"]["reasons"] == ["suspicious_tld"]


def test_no_domain_penalty_block_without_domain_signal():
    signals = [SignalResult(name="coherence", value=70.0, confidence=0.8)]
    result = generate_explanation(70.0, "medium_high", signals, {"coherence": 1.0})
    assert "domain_penalty" not in result
