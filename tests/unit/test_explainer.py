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
    # coherence: 80*0.5=40, gaming: 20*0.5=10 -> total 50 -> 80% / 20%
    assert shares["coherence"] == 80.0
    assert shares["gaming"] == 20.0
    assert sum(shares.values()) == 100.0
    assert result["primary_driver"] == "coherence"


def test_score_share_zero_total_is_safe():
    signals = [SignalResult(name="coherence", value=0.0, confidence=0.0)]
    weights = {"coherence": 0.3}
    result = generate_explanation(0.0, "very_low", signals, weights)
    assert result["signals"][0]["score_share_pct"] == 0.0
    assert result["primary_driver"] == "coherence"
