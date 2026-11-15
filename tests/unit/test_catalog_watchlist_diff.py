import json

import pytest

from research.catalog_watchlist_diff import (
    DATA_DIR,
    HeaderError,
    classify_registry,
    compare_catalogs,
    count_definitions,
    feed_key,
    index_catalog,
    load_catalog,
    load_registry,
    main,
    roadmap_check,
    safe_host,
)

HEADER = "Macro-categoria,Sottosezione,Fonte,URL,RSS Feed,Lingua\n"


def _write(path, text):
    path.write_text(text, encoding="utf-8")
    return path


def _catalog(path, rows):
    lines = [HEADER] + [f"M,S,{name},{url},{rss},EN\n" for name, url, rss in rows]
    return _write(path, "".join(lines))


def _registry(path, records):
    return _write(path, "".join(json.dumps(r) + "\n" for r in records))


def test_host_and_feed_normalisation():
    assert safe_host("https://www.Example.org/path") == "example.org"
    assert safe_host("example.org") == "example.org"
    assert safe_host("") == ""
    assert safe_host("http://[bad") is None  # normalize_host raises ValueError here
    assert feed_key("https://www.example.org/feed/") == feed_key("http://example.org/feed")
    assert feed_key("") == "" and feed_key(None) == ""


def test_load_catalog_reads_bom_and_rejects_wrong_header(tmp_path):
    good = tmp_path / "good.csv"
    good.write_bytes(("﻿" + HEADER + "M,S,A,https://a.example,,EN\n").encode("utf-8"))
    rows = load_catalog(good)
    assert rows[0]["URL"] == "https://a.example"

    bad = _write(tmp_path / "bad.csv", "Name,Homepage,Feed\nA,https://a.example,\n")
    with pytest.raises(HeaderError, match="URL"):
        load_catalog(bad)


def test_load_registry_drops_label(tmp_path):
    path = _registry(
        tmp_path / "labels.jsonl",
        [{"source_id": "A", "source_type": "news", "label": 70, "url": "https://a.example", "rss": None}],
    )
    (row,) = load_registry(path)
    assert "label" not in row
    assert row["source_id"] == "A"


def test_compare_catalogs_counts_hosts_feeds_duplicates_and_bad_urls(tmp_path):
    cats = index_catalog(
        load_catalog(
            _catalog(
                tmp_path / "cats.csv",
                [
                    ("A", "https://www.a.example", "https://a.example/feed/"),
                    ("A bis", "http://a.example", ""),  # duplicate host, empty feed
                    ("B", "https://b.example", "https://b.example/rss"),
                    ("C", "https://c.example", ""),
                    ("OnlyCats", "https://cats-only.example", ""),
                    ("Bad", "http://[bad", ""),
                ],
            )
        )
    )
    watchlist = index_catalog(
        load_catalog(
            _catalog(
                tmp_path / "wl.csv",
                [
                    ("A", "https://a.example", "http://www.a.example/feed"),  # same feed, other spelling
                    ("B", "https://b.example", "https://b.example/other"),
                    ("C", "https://c.example", "https://c.example/feed"),
                    ("C2", "https://www.c.example", ""),
                    ("New", "https://wl-only.example", "https://wl-only.example/feed"),
                ],
            )
        )
    )
    diff = compare_catalogs(cats, watchlist)
    assert diff["hosts_only_cats"] == ["cats-only.example"]
    assert diff["hosts_only_watchlist"] == ["wl-only.example"]
    assert diff["hosts_common"] == ["a.example", "b.example", "c.example"]
    assert diff["feeds_common"] == ["a.example/feed"]
    assert diff["feeds_only_cats"] == ["b.example/rss"]
    assert diff["feeds_only_watchlist"] == ["b.example/other", "c.example/feed", "wl-only.example/feed"]
    assert diff["multi_row_hosts_cats"] == ["a.example"]
    assert diff["multi_row_hosts_watchlist"] == ["c.example"]
    assert diff["common_hosts_feed_differs"] == ["b.example"]
    assert diff["common_hosts_feed_disjoint"] == ["b.example"]
    assert diff["common_hosts_feed_only_watchlist"] == ["c.example"]
    assert diff["common_hosts_feed_only_cats"] == []
    assert diff["unparseable_host_rows_cats"] == ["row 7: Bad"]
    assert diff["unparseable_host_rows_watchlist"] == []


def test_registry_classification_and_definitions(tmp_path):
    watchlist = index_catalog(
        load_catalog(
            _catalog(
                tmp_path / "wl.csv",
                [
                    ("A", "https://a.example", "https://a.example/feed"),
                    ("B", "https://b.example", "https://b.example/other"),
                    ("C", "https://c.example", "https://c.example/feed"),
                    ("D", "https://d.example/it", ""),
                ],
            )
        )
    )
    registry = [
        {"source_id": "A", "source_type": "news", "url": "https://www.a.example/", "rss": "http://a.example/feed/"},
        {"source_id": "B", "source_type": "news", "url": "https://b.example", "rss": "https://b.example/rss"},
        {"source_id": "C", "source_type": "news", "url": "https://c.example", "rss": None},
        {"source_id": "D", "source_type": "news", "url": "https://d.example", "rss": "https://d.example/feed"},
        {"source_id": "E", "source_type": "news", "url": "https://e.example", "rss": "https://c.example/feed"},
        {"source_id": "F", "source_type": "news", "url": "http://[bad", "rss": None},
    ]
    rows = classify_registry(registry, watchlist)
    by_id = {r.source_id: r for r in rows}
    assert by_id["A"].feed_status == "same" and not by_id["A"].homepage_differs
    assert by_id["B"].feed_status == "different"
    assert by_id["C"].feed_status == "watchlist_only"
    assert by_id["D"].feed_status == "registry_only" and by_id["D"].homepage_differs
    assert by_id["E"].host_status == "absent" and by_id["E"].feed_anywhere_in_watchlist
    assert by_id["F"].host_status == "unparseable"

    counts = {key: total for key, _text, total in count_definitions(rows)}
    assert counts["D1_host_absent"] == 2
    assert counts["D2_feed_different"] == 1
    assert counts["D3a_feed_watchlist_only"] == 1
    assert counts["D3b_feed_registry_only"] == 1
    assert counts["D4_feed_mismatch"] == 3
    assert counts["D5_homepage_differs"] == 1
    assert counts["D8_any_divergence"] == 5
    assert counts["D9_feed_not_in_watchlist"] == 2  # B and D; E's feed is in the watchlist under another host


def test_roadmap_check_never_picks_a_definition_that_does_not_match():
    counts = [("X", "x", 54), ("Y", "y", 55), ("Z", "z", 55)]
    assert roadmap_check(counts) == ["Y", "Z"]
    assert roadmap_check([("X", "x", 54)]) == []


def _inputs(tmp_path):
    catalog = _catalog(tmp_path / "cats.csv", [("A", "https://a.example", "https://a.example/feed")])
    watchlist = _catalog(tmp_path / "wl.csv", [("A", "https://www.a.example", ""), ("Bad", "http://[bad", "")])
    labels = _registry(
        tmp_path / "labels.jsonl",
        [{"source_id": "A", "source_type": "news", "label": 70, "url": "https://a.example", "rss": None}],
    )
    return catalog, watchlist, labels


def test_main_leaves_inputs_byte_identical_and_writes_detail(tmp_path, capsys):
    catalog, watchlist, labels = _inputs(tmp_path)
    before = {p: p.read_bytes() for p in (catalog, watchlist, labels)}
    out = tmp_path / "detail.json"
    argv = ["--watchlist", str(watchlist), "--watchlist-commit", "abc123", "--catalog", str(catalog)]
    rc = main(argv + ["--labels", str(labels), "--out", str(out)])
    assert rc == 0
    assert {p: p.read_bytes() for p in before} == before
    stdout = capsys.readouterr().out
    assert "abc123" in stdout and "not reproducible" in stdout
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["roadmap_figure_matches"] == []
    assert payload["catalog"]["unparseable_host_rows_watchlist"] == ["row 3: Bad"]
    assert all("label" not in row for row in payload["registry"])


def test_main_fails_on_wrong_header_and_refuses_out_under_data(tmp_path, capsys):
    catalog, _watchlist, labels = _inputs(tmp_path)
    bad = _write(tmp_path / "bad.csv", "Name,Homepage\nA,https://a.example\n")
    base = ["--watchlist-commit", "abc", "--catalog", str(catalog), "--labels", str(labels)]
    assert main(["--watchlist", str(bad)] + base) == 2
    assert "missing column" in capsys.readouterr().err

    target = DATA_DIR / "should_not_exist.json"
    assert main(["--watchlist", str(catalog), "--out", str(target)] + base) == 2
    assert not target.exists()
