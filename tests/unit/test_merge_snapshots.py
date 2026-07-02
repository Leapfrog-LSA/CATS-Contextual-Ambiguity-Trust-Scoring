import json

from cats.calibration.merge_snapshots import main, merge_records


def _msg(ts: str, text: str) -> dict:
    return {"timestamp": ts, "text": text}


_OLD = {
    "source_id": "news:acme",
    "source_type": "news",
    "label": 85.0,
    "messages": [_msg("2026-01-01T08:00:00Z", "a"), _msg("2026-01-01T09:00:00Z", "b")],
}
_NEW = {
    "source_id": "news:acme",
    "source_type": "news",
    "label": 70.0,
    "messages": [_msg("2026-01-01T09:00:00Z", "b"), _msg("2026-02-01T08:00:00Z", "c")],
}


def test_merge_unions_and_dedupes_messages():
    records, total, dupes = merge_records([[_OLD], [_NEW]])
    assert len(records) == 1
    assert total == 3
    assert dupes == 1
    texts = [m["text"] for m in records[0]["messages"]]
    assert texts == ["a", "b", "c"]  # sorted by timestamp


def test_merge_newest_metadata_wins():
    records, _, _ = merge_records([[_OLD], [_NEW]])
    assert records[0]["label"] == 70.0


def test_merge_keeps_sources_missing_from_later_snapshots():
    other = {"source_id": "news:dead", "label": 10.0, "messages": [_msg("2025-01-01T00:00:00Z", "x")]}
    records, total, _ = merge_records([[_OLD, other], [_NEW]])
    assert {r["source_id"] for r in records} == {"news:acme", "news:dead"}
    assert total == 4


def test_merge_skips_records_without_source_id():
    records, _, _ = merge_records([[{"label": 1.0, "messages": []}]])
    assert records == []


def test_main_roundtrip(tmp_path):
    first = tmp_path / "s1.jsonl"
    second = tmp_path / "s2.jsonl"
    out = tmp_path / "merged.jsonl"
    first.write_text(json.dumps(_OLD) + "\n", encoding="utf-8")
    second.write_text(json.dumps(_NEW) + "\n", encoding="utf-8")

    assert main(["--inputs", str(first), str(second), "--out", str(out)]) == 0

    merged = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
    assert len(merged) == 1
    assert len(merged[0]["messages"]) == 3
