import json
from datetime import date

import pytest

from cats.calibration.merge_snapshots import filter_by_timestamp, main, merge_records


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


# --- timestamp sanity filter -------------------------------------------------


def _src(source_id: str, *timestamps: str) -> dict:
    return {
        "source_id": source_id,
        "label": 50.0,
        "messages": [_msg(ts, f"{source_id}-{i}") for i, ts in enumerate(timestamps)],
    }


def test_filter_without_bounds_is_a_noop():
    records = [_src("a", "1970-01-01T00:00:00Z", "not a date")]
    out, report = filter_by_timestamp(records)
    assert out == records
    assert report.dropped == 0 and report.kept == 2


def test_filter_bounds_are_whole_utc_days_inclusive():
    records = [
        _src(
            "a",
            "2026-05-31T23:59:59Z",  # before the floor
            "2026-06-01T00:00:00Z",  # first instant of the floor day: kept
            "2026-07-15T12:00:00+02:00",
            "2026-09-13T23:59:59Z",  # last second of the ceiling day: kept
            "2026-09-14T00:00:00Z",  # after the ceiling
        )
    ]
    out, report = filter_by_timestamp(records, date(2026, 6, 1), date(2026, 9, 13))
    assert [m["timestamp"] for m in out[0]["messages"]] == [
        "2026-06-01T00:00:00Z",
        "2026-07-15T12:00:00+02:00",
        "2026-09-13T23:59:59Z",
    ]
    assert (report.dropped_before, report.dropped_after, report.kept) == (1, 1, 3)


def test_filter_compares_offsets_in_utc_and_reads_naive_as_utc():
    # 2026-06-01T01:00+02:00 is 2026-05-31T23:00Z: before a 06-01 floor.
    records = [_src("a", "2026-06-01T01:00:00+02:00", "2026-06-01T00:30:00")]
    out, report = filter_by_timestamp(records, not_before=date(2026, 6, 1))
    assert [m["timestamp"] for m in out[0]["messages"]] == ["2026-06-01T00:30:00"]
    assert report.dropped_before == 1


def test_filter_drops_unparseable_timestamps_once_a_bound_is_set():
    records = [_src("a", "2026-07-01T00:00:00Z", "yesterday", "")]
    out, report = filter_by_timestamp(records, not_before=date(2026, 6, 1))
    assert len(out[0]["messages"]) == 1
    assert report.dropped_unparseable == 2


def test_filter_open_ceiling_keeps_future_dates():
    records = [_src("a", "2026-07-01T00:00:00Z", "2099-01-01T00:00:00Z")]
    out, report = filter_by_timestamp(records, not_before=date(2026, 6, 1))
    assert len(out[0]["messages"]) == 2 and report.dropped == 0


def test_filter_excludes_emptied_sources_and_names_them():
    # A source with no message in range cannot be placed by the temporal split,
    # so it is left out, but it is always reported, never dropped silently.
    records = [
        _src("dormant", "2022-03-01T00:00:00Z", "1970-01-01T00:00:00Z"),
        _src("live", "2026-07-01T00:00:00Z"),
    ]
    out, report = filter_by_timestamp(records, date(2026, 6, 1), date(2026, 9, 30))
    assert [r["source_id"] for r in out] == ["live"]
    assert report.emptied == [("dormant", 2)]


def test_filter_passes_through_sources_that_were_already_empty():
    records = [{"source_id": "none", "label": 1.0, "messages": []}]
    out, report = filter_by_timestamp(records, not_before=date(2026, 6, 1))
    assert out == records
    assert report.emptied == []


def test_filter_flags_heavy_loss_but_keeps_the_source():
    records = [_src("stale", "2023-01-01T00:00:00Z", "2023-01-02T00:00:00Z", "2026-07-01T00:00:00Z")]
    out, report = filter_by_timestamp(records, not_before=date(2026, 6, 1))
    assert len(out) == 1 and len(out[0]["messages"]) == 1
    assert report.heavy_loss == [("stale", 3, 1)]


def test_filter_exactly_half_lost_is_not_flagged():
    records = [_src("half", "2023-01-01T00:00:00Z", "2026-07-01T00:00:00Z")]
    _, report = filter_by_timestamp(records, not_before=date(2026, 6, 1))
    assert report.heavy_loss == []


def test_filter_does_not_mutate_its_input():
    records = [_src("a", "2023-01-01T00:00:00Z", "2026-07-01T00:00:00Z")]
    before = json.dumps(records)
    filter_by_timestamp(records, not_before=date(2026, 6, 1))
    assert json.dumps(records) == before


def test_filter_rejects_inverted_bounds():
    with pytest.raises(ValueError):
        filter_by_timestamp([_src("a", "2026-07-01T00:00:00Z")], date(2026, 9, 1), date(2026, 6, 1))


def _write_snapshot(tmp_path, name, records):
    path = tmp_path / name
    path.write_text("".join(json.dumps(r) + "\n" for r in records), encoding="utf-8")
    return path


def test_main_without_filter_flags_keeps_everything(tmp_path):
    snap = _write_snapshot(tmp_path, "s.jsonl", [_src("a", "1970-01-01T00:00:00Z", "2026-07-01T00:00:00Z")])
    out = tmp_path / "merged.jsonl"
    assert main(["--inputs", str(snap), "--out", str(out)]) == 0
    merged = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
    assert len(merged[0]["messages"]) == 2


def test_main_with_filter_writes_only_in_range_and_reports(tmp_path, capsys):
    snap = _write_snapshot(
        tmp_path,
        "s.jsonl",
        [
            _src("live", "1970-01-01T00:00:00Z", "2026-07-01T00:00:00Z"),
            _src("dormant", "2022-01-01T00:00:00Z"),
        ],
    )
    out = tmp_path / "merged.jsonl"
    rc = main(["--inputs", str(snap), "--out", str(out), "--not-before", "2026-06-01", "--not-after", "2026-09-25"])
    assert rc == 0
    merged = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
    assert [r["source_id"] for r in merged] == ["live"]
    assert [m["timestamp"] for m in merged[0]["messages"]] == ["2026-07-01T00:00:00Z"]
    printed = capsys.readouterr().out
    assert "EXCLUDED" in printed and "dormant: 1 -> 0" in printed
    # "live" lost exactly half (1 of 2): not "more than half", so no heavy-loss line.
    assert "live: 2 -> 1" not in printed


def test_main_returns_1_when_filter_leaves_nothing(tmp_path):
    snap = _write_snapshot(tmp_path, "s.jsonl", [_src("dormant", "2022-01-01T00:00:00Z")])
    out = tmp_path / "merged.jsonl"
    assert main(["--inputs", str(snap), "--out", str(out), "--not-before", "2026-06-01"]) == 1
    assert not out.exists()


@pytest.mark.parametrize(
    "extra",
    [
        ["--not-before", "2026-13-01"],  # not a date
        ["--not-after", "yesterday"],
        ["--not-before", "2026-09-01", "--not-after", "2026-06-01"],  # inverted
    ],
)
def test_main_rejects_bad_filter_dates(tmp_path, extra):
    snap = _write_snapshot(tmp_path, "s.jsonl", [_src("a", "2026-07-01T00:00:00Z")])
    with pytest.raises(SystemExit) as exc:
        main(["--inputs", str(snap), "--out", str(tmp_path / "m.jsonl"), *extra])
    assert exc.value.code == 2
