import json

import pytest

from cats.calibration.label_from_ratings import (
    build_label_registry,
    load_ratings,
    main,
    map_label,
    normalize_host,
    source_type_from_category,
)


# ── Scale mapping ──────────────────────────────────────────────────────────
def test_map_label_mbfc_is_ordinal():
    assert map_label("VERY HIGH", "mbfc") > map_label("Mixed", "mbfc") > map_label("very low", "mbfc")


def test_map_label_numeric_clamps():
    assert map_label("150", "numeric") == 100.0
    assert map_label("-5", "numeric") == 0.0
    assert map_label("not-a-number", "numeric") is None


def test_map_label_unknown_value_returns_none():
    assert map_label("bogus", "mbfc") is None


def test_map_label_custom_and_unknown_scale():
    assert map_label("trusted", "custom", {"trusted": 88}) == 88.0
    with pytest.raises(ValueError):
        map_label("x", "weird")


# ── Helpers ────────────────────────────────────────────────────────────────
def test_normalize_host_strips_scheme_and_www():
    assert normalize_host("https://www.Example.com/path") == "example.com"
    assert normalize_host("example.com") == "example.com"
    assert normalize_host("") == ""


def test_source_type_from_category():
    assert source_type_from_category("📰 Media & Testate Giornalistiche") == "news"
    assert source_type_from_category("📡 Social Media & Media Monitoring") == "social"
    assert source_type_from_category("🔐 Cybersecurity & Digital OSINT") == "default"


# ── Loading ratings ────────────────────────────────────────────────────────
def test_load_ratings_json_dict(tmp_path):
    p = tmp_path / "r.json"
    p.write_text(json.dumps({"https://www.abc.com": "High", "xyz.org": "Low"}), encoding="utf-8")
    ratings = load_ratings(p)
    assert ratings["abc.com"] == "High"
    assert ratings["xyz.org"] == "Low"


def test_load_ratings_csv(tmp_path):
    p = tmp_path / "r.csv"
    p.write_text("domain,rating\nwww.abc.com,High\nxyz.org,Mixed\n", encoding="utf-8")
    ratings = load_ratings(p)
    assert ratings == {"abc.com": "High", "xyz.org": "Mixed"}


# ── Join ───────────────────────────────────────────────────────────────────
def _sources():
    return [
        {"Fonte": "ABC", "URL": "https://abc.com", "Macro-categoria": "📰 Media", "RSS Feed": "https://abc.com/rss"},
        {"Fonte": "XYZ", "URL": "http://www.xyz.org", "Macro-categoria": "📡 Social Media"},
        {"Fonte": "NoRating", "URL": "https://unrated.com", "Macro-categoria": "📰 Media"},
    ]


def test_build_label_registry_joins_and_maps():
    ratings = {"abc.com": "High", "xyz.org": "Low"}
    records, stats = build_label_registry(_sources(), ratings, "mbfc")
    assert stats.total_sources == 3
    assert stats.matched == 2  # unrated.com is dropped
    by_id = {r["source_id"]: r for r in records}
    assert by_id["ABC"]["label"] == 85.0 and by_id["ABC"]["source_type"] == "news"
    assert by_id["ABC"]["rss"] == "https://abc.com/rss"
    assert by_id["XYZ"]["label"] == 30.0 and by_id["XYZ"]["source_type"] == "social"
    assert stats.by_source_type == {"news": 1, "social": 1}


def test_build_label_registry_counts_unmapped_rating():
    ratings = {"abc.com": "bogus-rating"}  # host matches but rating won't map
    records, stats = build_label_registry(_sources(), ratings, "mbfc")
    assert records == []
    assert stats.unmapped_rating == 1


# ── CLI ────────────────────────────────────────────────────────────────────
def test_main_end_to_end(tmp_path, capsys):
    sources = tmp_path / "sources.csv"
    sources.write_text(
        "Macro-categoria,Fonte,URL,RSS Feed\n"
        "📰 Media,ABC,https://abc.com,https://abc.com/rss\n"
        "📡 Social,XYZ,https://xyz.org,\n",
        encoding="utf-8",
    )
    ratings = tmp_path / "ratings.csv"
    ratings.write_text("domain,rating\nabc.com,Very High\nxyz.org,Mixed\n", encoding="utf-8")
    out = tmp_path / "labels.jsonl"
    rc = main(["--sources", str(sources), "--ratings", str(ratings), "--scale", "mbfc", "--out", str(out)])
    assert rc == 0
    lines = [json.loads(x) for x in out.read_text(encoding="utf-8").splitlines()]
    assert len(lines) == 2
    assert {r["source_id"] for r in lines} == {"ABC", "XYZ"}
    assert "Wrote 2 labelled source" in capsys.readouterr().out


def test_main_returns_1_when_no_match(tmp_path):
    sources = tmp_path / "s.csv"
    sources.write_text("Macro-categoria,Fonte,URL\n📰 Media,ABC,https://abc.com\n", encoding="utf-8")
    ratings = tmp_path / "r.csv"
    ratings.write_text("domain,rating\nother.com,High\n", encoding="utf-8")
    out = tmp_path / "labels.jsonl"
    rc = main(["--sources", str(sources), "--ratings", str(ratings), "--scale", "mbfc", "--out", str(out)])
    assert rc == 1
    assert not out.exists()
