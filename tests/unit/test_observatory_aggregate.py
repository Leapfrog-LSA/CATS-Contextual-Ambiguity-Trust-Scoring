import json

import pytest

from research.observatory_aggregate import (
    _check_no_identifiers,
    _country_from_url,
    build_aggregates,
    collect_source_stats,
    render_markdown,
)

_SECRET_SOURCE_ID = "TopSecretDisinfoOutlet"
_SECRET_DOMAIN = "topsecretdisinfooutlet.example"
_SECRET_URL = f"https://{_SECRET_DOMAIN}/rss"

_ITALIAN_MESSAGES = [
    {"timestamp": f"2026-01-0{i}T08:00:00Z", "text": "Il governo annuncia un piano economico per la crescita."}
    for i in range(1, 6)
]
_ENGLISH_MESSAGES = [
    {"timestamp": f"2026-02-0{i}T08:00:00Z", "text": "The government announced a new economic plan today."}
    for i in range(1, 6)
]


def _write_snapshot(tmp_path, name, records):
    path = tmp_path / name
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record) + "\n")
    return path


@pytest.fixture
def snapshot_dir(tmp_path):
    records = [
        {
            "source_id": _SECRET_SOURCE_ID,
            "source_type": "news",
            "label": 10.0,
            "url": _SECRET_URL,
            "rss": _SECRET_URL,
            "messages": _ITALIAN_MESSAGES,
        },
        {
            "source_id": "AnotherOutlet",
            "source_type": "news",
            "label": 85.0,
            "url": "https://another-outlet.co.uk/rss",
            "rss": "https://another-outlet.co.uk/rss",
            "messages": _ENGLISH_MESSAGES,
        },
        {
            "source_id": "ThirdOutlet",
            "source_type": "default",
            "label": 55.0,
            "url": "https://third-outlet.fr/rss",
            "rss": "https://third-outlet.fr/rss",
            "messages": _ITALIAN_MESSAGES,
        },
    ]
    _write_snapshot(tmp_path, "labelled_sources_2026-09-01.jsonl", records)
    return tmp_path


def test_country_from_url_generic_tld_is_unknown():
    assert _country_from_url("https://example.com/rss") == "unknown (generic TLD)"


def test_country_from_url_known_cctld():
    assert _country_from_url("https://example.it/rss") == "Italy"


def test_country_from_url_unmapped_cctld():
    assert _country_from_url("https://example.xy/rss") == "unknown (unmapped TLD)"


def test_country_from_url_none():
    assert _country_from_url(None) == "unknown (no URL)"


def test_collect_source_stats_never_carries_identifiers(snapshot_dir):
    stats = collect_source_stats(str(snapshot_dir / "*.jsonl"), load_nlp=False)

    assert len(stats) == 3
    for entry in stats:
        assert set(entry) == {"source_type", "language", "country", "band", "signals"}
        assert set(entry["signals"]) == {"coherence", "volatility", "silence", "gaming"}


def test_build_aggregates_groups_by_source_type_language_country(snapshot_dir):
    stats = collect_source_stats(str(snapshot_dir / "*.jsonl"), load_nlp=False)
    aggregates = build_aggregates(stats)

    assert set(aggregates) == {"source_type", "language", "country"}
    assert aggregates["source_type"]["news"]["n"] == 2
    assert aggregates["source_type"]["default"]["n"] == 1
    assert sum(bucket["n"] for bucket in aggregates["country"].values()) == 3


def test_check_no_identifiers_passes_on_clean_aggregates(snapshot_dir):
    stats = collect_source_stats(str(snapshot_dir / "*.jsonl"), load_nlp=False)
    aggregates = build_aggregates(stats)

    _check_no_identifiers(aggregates)  # must not raise


def test_check_no_identifiers_catches_a_leaked_identifier_key():
    leaked = {"news": {"n": 1, "source_id": _SECRET_SOURCE_ID}}

    with pytest.raises(AssertionError):
        _check_no_identifiers(leaked)


def test_rendered_markdown_never_contains_source_identifiers(snapshot_dir):
    stats = collect_source_stats(str(snapshot_dir / "*.jsonl"), load_nlp=False)
    aggregates = build_aggregates(stats)
    markdown = render_markdown(aggregates, report_date="2026-09-17", total_sources=len(stats))

    assert _SECRET_SOURCE_ID not in markdown
    assert _SECRET_DOMAIN not in markdown
    assert "another-outlet" not in markdown
    assert "third-outlet" not in markdown
    assert ".fr" not in markdown and ".co.uk" not in markdown  # no leftover feed-url fragments
    assert "Total scored sources: 3" in markdown
    assert "news" in markdown  # the group label itself is not an identifier


def test_collect_source_stats_empty_pattern_returns_empty(tmp_path):
    assert collect_source_stats(str(tmp_path / "*.jsonl")) == []
