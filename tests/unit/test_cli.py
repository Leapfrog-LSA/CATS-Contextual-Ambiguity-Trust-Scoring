import json

import pytest

from cats import __version__
from cats.cli import main
from cats.lite import FeedFetchError, FeedNotFoundError

_RESULT = {
    "trust_score": 67.3,
    "band": "medium_high",
    "requires_human_review": False,
    "signals": {"coherence": 71.2, "volatility": 55.0, "silence": 12.0, "gaming": 8.5},
    "language": {"detected": "italian", "confidence": 0.31, "marker_ratio": 0.2, "latin_script_ratio": 1.0},
    "evidence": {"messages": 48, "min_messages": 3, "sufficient": True, "mean_signal_confidence": 0.8},
    "explanation": {
        "trust_score": 67.3,
        "band": "medium_high",
        "signals": [
            {"signal": "silence", "score_share_pct": 46.0},
            {"signal": "coherence", "score_share_pct": 30.0},
        ],
        "primary_driver": "silence",
        "disclaimer": "Ordinal ranking, not a probability.",
    },
    "source": {
        "url": "https://esempio.it",
        "feed_url": "https://esempio.it/feed",
        "messages": 48,
        "first_timestamp": "2026-07-01T00:00:00Z",
        "last_timestamp": "2026-09-15T00:00:00Z",
        "discovery": "html_link",
    },
}


def test_version(capsys):
    exit_code = main(["--version"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert __version__ in captured.out


def test_score_human_output_contains_score_and_band(monkeypatch, capsys):
    monkeypatch.setattr("cats.cli.score_feed", lambda *a, **k: dict(_RESULT))

    exit_code = main(["score", "https://esempio.it"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Score" in captured.out
    assert "medium_high" in captured.out
    assert "Driver     silence (share 46.0%)" in captured.out


def test_score_json_is_valid_and_has_trust_score(monkeypatch, capsys):
    monkeypatch.setattr("cats.cli.score_feed", lambda *a, **k: dict(_RESULT))

    exit_code = main(["score", "https://esempio.it", "--json"])

    captured = capsys.readouterr()
    assert exit_code == 0
    parsed = json.loads(captured.out)
    assert parsed["trust_score"] == 67.3


def test_score_review_required_line(monkeypatch, capsys):
    result = dict(_RESULT)
    result["requires_human_review"] = True
    result["band"] = "low"
    monkeypatch.setattr("cats.cli.score_feed", lambda *a, **k: result)

    exit_code = main(["score", "https://esempio.it"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Review required: band low" in captured.out


def test_score_clean_domain_no_red_flags_line(monkeypatch, capsys):
    result = dict(_RESULT)
    result["signals"] = dict(_RESULT["signals"])
    result["signals"]["domain_provenance"] = 0.0
    monkeypatch.setattr("cats.cli.score_feed", lambda *a, **k: result)

    exit_code = main(["score", "https://esempio.it"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Domain red flags" not in captured.out


def test_score_domain_red_flag_line(monkeypatch, capsys):
    result = dict(_RESULT)
    result["signals"] = dict(_RESULT["signals"])
    result["signals"]["domain_provenance"] = 42.0
    result["explanation"] = dict(_RESULT["explanation"])
    result["explanation"]["domain_penalty"] = {"metadata": {"reasons": ["suspicious_tld"]}}
    monkeypatch.setattr("cats.cli.score_feed", lambda *a, **k: result)

    exit_code = main(["score", "https://esempio.it"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Domain red flags: suspicious_tld" in captured.out


def test_score_feed_not_found_exit_code_3(monkeypatch, capsys):
    def _raise(*a, **k):
        raise FeedNotFoundError("no feed found")

    monkeypatch.setattr("cats.cli.score_feed", _raise)

    exit_code = main(["score", "https://esempio.it"])

    captured = capsys.readouterr()
    assert exit_code == 3
    assert "no feed found" in captured.err


def test_score_feed_unreachable_exit_code_3(monkeypatch, capsys):
    def _raise(*a, **k):
        raise FeedFetchError("unreachable")

    monkeypatch.setattr("cats.cli.score_feed", _raise)

    exit_code = main(["score", "https://esempio.it"])

    assert exit_code == 3


def test_score_no_valid_messages_exit_code_4(monkeypatch, capsys):
    def _raise(*a, **k):
        raise ValueError("no valid messages after normalisation")

    monkeypatch.setattr("cats.cli.score_feed", _raise)

    exit_code = main(["score", "https://esempio.it"])

    captured = capsys.readouterr()
    assert exit_code == 4
    assert "no valid messages" in captured.err


def test_score_no_url_or_messages_exit_code_2(capsys):
    exit_code = main(["score"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "error" in captured.err


def test_score_messages_reads_jsonl(monkeypatch, tmp_path, capsys):
    messages_file = tmp_path / "messages.jsonl"
    messages_file.write_text(
        '{"timestamp": "2026-01-01T08:00:00Z", "text": "Il governo annuncia un piano."}\n'
        '{"timestamp": "2026-01-02T09:00:00Z", "text": "Il parlamento discute il piano."}\n'
    )

    captured_messages = {}

    def _fake_score(messages, **kwargs):
        captured_messages["messages"] = messages
        result = dict(_RESULT)
        del result["source"]
        return result

    monkeypatch.setattr("cats.cli.score", _fake_score)

    exit_code = main(["score", "--messages", str(messages_file)])

    assert exit_code == 0
    assert len(captured_messages["messages"]) == 2


def test_no_nlp_passes_load_nlp_false(monkeypatch):
    captured_kwargs = {}

    def _fake_score_feed(url, **kwargs):
        captured_kwargs.update(kwargs)
        return dict(_RESULT)

    monkeypatch.setattr("cats.cli.score_feed", _fake_score_feed)

    main(["score", "https://esempio.it", "--no-nlp"])

    assert captured_kwargs["load_nlp"] is False


@pytest.mark.parametrize("argv", [["score", "https://esempio.it", "--weights", "/does/not/exist.json"]])
def test_score_bad_weights_file_exit_code_2(argv, capsys):
    exit_code = main(argv)

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "error" in captured.err
