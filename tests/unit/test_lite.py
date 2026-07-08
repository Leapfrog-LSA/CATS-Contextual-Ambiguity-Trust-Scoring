import pytest

from cats.lite import score

_MESSAGES = [
    {"timestamp": "2026-01-01T08:00:00Z", "text": "Il governo annuncia un piano economico."},
    {"timestamp": "2026-01-01T12:00:00Z", "text": "I sindacati commentano il piano del governo."},
    {"timestamp": "2026-01-02T09:00:00Z", "text": "Il parlamento discute la legge di bilancio."},
]


def test_score_returns_full_result():
    result = score(_MESSAGES, source_type="news", load_nlp=False)
    assert 0.0 <= result["trust_score"] <= 100.0
    assert result["band"] in {"very_low", "low", "medium", "medium_high", "high"}
    assert isinstance(result["requires_human_review"], bool)
    assert set(result["signals"]) == {"coherence", "volatility", "silence", "gaming"}
    assert result["explanation"]["trust_score"] == result["trust_score"]
    assert "disclaimer" in result["explanation"]


def test_score_without_explanation():
    result = score(_MESSAGES, source_type="social", load_nlp=False, explain=False)
    assert "explanation" not in result


def test_score_with_weight_override():
    weights = {"coherence": 0.7, "volatility": 0.1, "silence": 0.1, "gaming": 0.1}
    result = score(_MESSAGES, weights=weights, load_nlp=False)
    assert result["explanation"]["signals"][0]["weight"] in {0.7, 0.1}


def test_score_rejects_empty_messages():
    with pytest.raises(ValueError):
        score([], load_nlp=False)
    with pytest.raises(ValueError):
        score([{"timestamp": "", "text": ""}], load_nlp=False)


def test_clone_url_penalises_and_reports_domain():
    base = score(_MESSAGES, source_type="news", load_nlp=False, explain=False)
    clone = score(_MESSAGES, source_type="news", load_nlp=False, url="https://spiegel.ltd")
    assert clone["trust_score"] < base["trust_score"]
    assert "domain_provenance" in clone["signals"]
    assert "domain_penalty" in clone["explanation"]
    assert clone["explanation"]["domain_penalty"]["domain_red_flag_score"] == 65.0


def test_clean_url_does_not_change_score():
    base = score(_MESSAGES, source_type="news", load_nlp=False, explain=False)
    clean = score(_MESSAGES, source_type="news", load_nlp=False, explain=False, url="https://www.corriere.it")
    assert clean["trust_score"] == base["trust_score"]


def test_no_url_keeps_four_signals():
    result = score(_MESSAGES, source_type="news", load_nlp=False, explain=False)
    assert set(result["signals"]) == {"coherence", "volatility", "silence", "gaming"}
