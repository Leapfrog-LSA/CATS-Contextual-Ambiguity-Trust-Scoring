import csv
import json

import pytest

from research.text_inventory import bucket_for, build_inventory, domain_of, expand_patterns, main, summarize


def _write_jsonl(path, records):
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record) + "\n")
    return path


def _message(text, timestamp="2026-07-01T08:00:00Z", link=True):
    message = {"timestamp": timestamp, "text": text}
    if link:
        message["metadata"] = {"link": "https://publisher.example/article"}
    return message


@pytest.mark.parametrize(
    "length, expected",
    [(0, "<=300"), (300, "<=300"), (301, "301-1000"), (1000, "301-1000"), (1001, "1001-5000"), (5001, ">5000")],
)
def test_bucket_edges_are_inclusive_upper_bounds(length, expected):
    assert bucket_for(length) == expected


def test_domain_prefers_homepage_over_feed_host():
    record = {"url": "https://www.Publisher.example/", "rss": "https://feeds.feedburner.com/publisher"}
    assert domain_of(record) == "publisher.example"
    assert domain_of({"rss": "https://www.feed-only.example/rss"}) == "feed-only.example"
    assert domain_of({}) == ""


def test_texts_are_deduplicated_across_files(tmp_path):
    shared = _message("Same headline. Same summary.")
    first = _write_jsonl(
        tmp_path / "a.jsonl",
        [{"source_id": "Pub", "source_type": "news", "url": "https://pub.example", "messages": [shared]}],
    )
    second = _write_jsonl(
        tmp_path / "b.jsonl",
        [
            {
                "source_id": "Pub",
                "source_type": "news",
                "url": "https://pub.example",
                "messages": [shared, _message("x" * 6000, "2026-07-03T08:00:00Z", link=False)],
            }
        ],
    )

    sources, files = build_inventory([first, second])
    row = sources["Pub"].row()

    assert row["occurrences"] == 3
    assert row["unique_texts"] == 2
    assert row["unique_chars"] == len("Same headline. Same summary.") + 6000
    assert row["max_chars"] == 6000
    assert row["bucket_<=300"] == 1 and row["bucket_>5000"] == 1
    assert row["with_link"] == 1
    assert row["files"] == 2
    assert (row["first_timestamp"], row["last_timestamp"]) == ("2026-07-01T08:00:00Z", "2026-07-03T08:00:00Z")
    assert [f["messages"] for f in files] == [1, 2]

    totals = summarize([row], files, sources)
    assert totals["unique_texts"] == 2 and totals["domains"] == 1 and totals["distinct_texts"] == 2


def test_distinct_total_counts_a_text_shared_by_two_sources_once(tmp_path):
    shared = _message("Wire copy republished by two outlets.")
    path = _write_jsonl(
        tmp_path / "s.jsonl",
        [{"source_id": "A", "messages": [shared]}, {"source_id": "B", "messages": [shared]}],
    )
    sources, files = build_inventory([path])
    totals = summarize([inv.row() for inv in sources.values()], files, sources)
    assert totals["unique_texts"] == 2
    assert totals["distinct_texts"] == 1
    assert totals["distinct_chars"] == len(shared["text"])


def test_invalid_json_names_the_file_and_line(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_text('{"source_id": "ok", "messages": []}\n{not json\n', encoding="utf-8")
    with pytest.raises(ValueError, match=r"bad\.jsonl:2"):
        build_inventory([path])


def test_main_writes_csv_and_json_and_never_touches_inputs(tmp_path, capsys):
    data = _write_jsonl(
        tmp_path / "snap.jsonl",
        [
            {"source_id": "Big", "url": "https://big.example", "messages": [_message("y" * 2000)]},
            {"source_id": "Small", "url": "https://small.example", "messages": [_message("short")]},
        ],
    )
    before = data.read_bytes()
    csv_path, json_path = tmp_path / "out.csv", tmp_path / "out.json"

    assert main([str(tmp_path / "*.jsonl"), "--csv", str(csv_path), "--json", str(json_path), "--top", "1"]) == 0

    assert data.read_bytes() == before
    with csv_path.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert [r["source_id"] for r in rows] == ["Big", "Small"]  # sorted by characters, largest first
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["totals"]["sources"] == 2
    out = capsys.readouterr().out
    assert "Top 1 of 2 sources" in out and "| Big |" in out and "| Small |" not in out


def test_main_without_inputs_fails(tmp_path):
    assert main([str(tmp_path / "missing-*.jsonl")]) == 1
    assert expand_patterns([str(tmp_path / "nothing")]) == []
