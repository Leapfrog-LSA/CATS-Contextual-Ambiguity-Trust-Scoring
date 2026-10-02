import json

import pytest
import structlog

from cats import __version__
from cats.cli import main
from cats.lite import FeedFetchError, FeedNotFoundError, UnsafeURLError

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


def test_score_unmeasured_coherence_warning(monkeypatch, capsys):
    result = dict(_RESULT)
    result["requires_human_review"] = True
    result["degraded_signals"] = ["coherence"]
    monkeypatch.setattr("cats.cli.score_feed", lambda *a, **k: result)

    exit_code = main(["score", "https://esempio.it"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Review required: signal(s) not measured: coherence" in captured.out
    assert "python -m spacy download it_core_news_lg" in captured.out


def test_score_measured_coherence_has_no_warning(monkeypatch, capsys):
    monkeypatch.setattr("cats.cli.score_feed", lambda *a, **k: dict(_RESULT))

    main(["score", "https://esempio.it"])

    assert "NOT measured" not in capsys.readouterr().out


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


def _scoring_that_logs(*args, **kwargs):
    """Stand-in for `score_feed` that logs on the way, as the real one does."""
    structlog.get_logger("cats.test").info("feed_fetched", messages=48)
    return dict(_RESULT)


def test_json_output_stays_parseable_when_the_library_logs(monkeypatch, capsys):
    # Regression: structlog is unconfigured by default and prints to STDOUT, so
    # every line the library logged landed in front of the JSON and
    # `cats score <url> --json | jq` died on the first one.
    monkeypatch.setattr("cats.cli.score_feed", _scoring_that_logs)

    assert main(["score", "https://esempio.it", "--json"]) == 0

    captured = capsys.readouterr()
    assert json.loads(captured.out)["trust_score"] == 67.3
    assert "feed_fetched" in captured.err


def test_human_output_is_not_interleaved_with_log_lines(monkeypatch, capsys):
    monkeypatch.setattr("cats.cli.score_feed", _scoring_that_logs)

    assert main(["score", "https://esempio.it"]) == 0

    captured = capsys.readouterr()
    assert captured.out.startswith("Source")
    assert "feed_fetched" not in captured.out


def _scored(score_value, band="medium_high", review=False, degraded=None, domain=0.0):
    result = json.loads(json.dumps(_RESULT))
    result["trust_score"] = score_value
    result["band"] = band
    result["requires_human_review"] = review
    result["degraded_signals"] = degraded or []
    result["signals"]["domain_provenance"] = domain
    return result


def _fake_score_feed(table):
    def fake(url, **kwargs):
        outcome = table[url]
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    return fake


def test_compare_ranks_by_score_and_lists_failures(monkeypatch, capsys):
    table = {
        "https://low.example": _scored(41.3, band="medium"),
        "https://high.example": _scored(78.2),
        "https://gone.example": FeedNotFoundError("no RSS/Atom feed found for https://gone.example"),
        "https://mid.example": _scored(64.7),
    }
    monkeypatch.setattr("cats.lite.score_feed", _fake_score_feed(table))

    exit_code = main(["compare", *table])

    out = capsys.readouterr().out
    assert exit_code == 0
    ranked = [line for line in out.splitlines() if line.lstrip()[:1].isdigit()]
    assert [line.split()[1] for line in ranked] == [
        "https://high.example",
        "https://mid.example",
        "https://low.example",
    ]
    assert "Not scored (1):" in out
    assert "https://gone.example: no RSS/Atom feed found" in out
    assert "not of truthfulness" in out


def test_compare_json_has_ranks_and_errors(monkeypatch, capsys):
    table = {
        "https://a.example": _scored(50.0, band="medium"),
        "https://b.example": _scored(70.0),
        "http://127.0.0.1/": UnsafeURLError("refused 'http://127.0.0.1/'"),
    }
    monkeypatch.setattr("cats.lite.score_feed", _fake_score_feed(table))

    exit_code = main(["compare", *table, "--json"])

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert [(r["rank"], r["url"]) for r in payload["ranked"]] == [(1, "https://b.example"), (2, "https://a.example")]
    assert payload["errors"] == [{"url": "http://127.0.0.1/", "error": "refused 'http://127.0.0.1/'"}]


def test_compare_flags_review_domain_and_missing_model(monkeypatch, capsys):
    table = {
        "https://a.example": _scored(55.0, band="medium", review=True, degraded=["coherence"]),
        "https://b.example": _scored(40.2, band="medium", domain=40.0),
    }
    monkeypatch.setattr("cats.lite.score_feed", _fake_score_feed(table))

    main(["compare", *table])

    out = capsys.readouterr().out
    assert "yes" in out and "domain" in out
    assert "python -m spacy download it_core_news_lg" in out


def test_compare_reads_urls_from_file_and_dedupes(monkeypatch, tmp_path, capsys):
    calls = []

    def fake(url, **kwargs):
        calls.append(url)
        return _scored(60.0)

    monkeypatch.setattr("cats.lite.score_feed", fake)
    url_file = tmp_path / "sources.txt"
    url_file.write_text("# my sources\nhttps://a.example\n\nhttps://b.example  # trailing comment\nhttps://a.example\n")

    exit_code = main(["compare", "--file", str(url_file)])

    assert exit_code == 0
    assert calls == ["https://a.example", "https://b.example"]


def test_compare_needs_two_urls(capsys):
    assert main(["compare", "https://only.example"]) == 2
    assert "at least two URLs" in capsys.readouterr().err


def test_compare_exit_3_when_nothing_scored(monkeypatch, capsys):
    table = {
        "https://a.example": FeedFetchError("could not reach https://a.example"),
        "https://b.example": FeedNotFoundError("no RSS/Atom feed found for https://b.example"),
    }
    monkeypatch.setattr("cats.lite.score_feed", _fake_score_feed(table))

    assert main(["compare", *table]) == 3
    assert "Not scored (2):" in capsys.readouterr().out
