import json

import pytest

from cats.calibration.split import _parse_ts, main, record_time, temporal_split


def _rec(sid, *timestamps, label=50):
    return {
        "source_id": sid,
        "label": label,
        "messages": [{"timestamp": ts, "text": "x"} for ts in timestamps],
    }


def test_record_time_is_latest_message():
    rec = _rec("a", "2026-01-01T00:00:00Z", "2026-03-01T00:00:00Z", "2026-02-01T00:00:00Z")
    assert record_time(rec) == _parse_ts("2026-03-01T00:00:00Z")


def test_record_time_raises_without_timestamp():
    with pytest.raises(ValueError):
        record_time({"source_id": "a", "messages": [{"text": "no ts"}]})


def test_temporal_split_by_fraction_takes_most_recent():
    recs = [_rec(f"s{i}", f"2026-0{i}-01T00:00:00Z") for i in range(1, 6)]  # Jan..May
    train, holdout = temporal_split(recs, holdout_fraction=0.4)
    assert [r["source_id"] for r in holdout] == ["s4", "s5"]  # most recent 40%
    assert [r["source_id"] for r in train] == ["s1", "s2", "s3"]


def test_temporal_split_leaves_at_least_one_each_side():
    recs = [_rec("a", "2026-01-01T00:00:00Z"), _rec("b", "2026-02-01T00:00:00Z")]
    train, holdout = temporal_split(recs, holdout_fraction=0.9)
    assert len(train) == 1 and len(holdout) == 1


def test_temporal_split_by_cutoff():
    recs = [
        _rec("old", "2025-12-01T00:00:00Z"),
        _rec("edge", "2026-01-01T00:00:00Z"),
        _rec("new", "2026-02-01T00:00:00Z"),
    ]
    train, holdout = temporal_split(recs, cutoff=_parse_ts("2026-01-01T00:00:00Z"))
    assert [r["source_id"] for r in train] == ["old"]
    assert [r["source_id"] for r in holdout] == ["edge", "new"]  # at/after cutoff


def test_temporal_split_rejects_bad_fraction():
    with pytest.raises(ValueError):
        temporal_split([_rec("a", "2026-01-01T00:00:00Z")], holdout_fraction=1.5)


def test_main_writes_both_files(tmp_path, capsys):
    src = tmp_path / "sources.jsonl"
    src.write_text(
        "\n".join(json.dumps(_rec(f"s{i}", f"2026-0{i}-01T00:00:00Z")) for i in range(1, 6)),
        encoding="utf-8",
    )
    train_out = tmp_path / "train.jsonl"
    holdout_out = tmp_path / "holdout.jsonl"
    rc = main(
        [
            "--input",
            str(src),
            "--train-out",
            str(train_out),
            "--holdout-out",
            str(holdout_out),
            "--holdout-fraction",
            "0.2",
        ]
    )
    assert rc == 0
    assert len(train_out.read_text().splitlines()) == 4
    assert len(holdout_out.read_text().splitlines()) == 1
    assert "Split 5 record(s)" in capsys.readouterr().out
