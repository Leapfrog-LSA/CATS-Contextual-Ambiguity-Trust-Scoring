import json

import pytest

from cats.calibration.split import (
    _parse_ts,
    label_spread,
    main,
    message_quantile_cutoff,
    message_split,
    record_span_hours,
    record_time,
    silence_blind_sources,
    temporal_split,
    window_bounds,
)


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
            "--axis",
            "source",
            "--holdout-fraction",
            "0.2",
        ]
    )
    assert rc == 0
    assert len(train_out.read_text().splitlines()) == 4
    assert len(holdout_out.read_text().splitlines()) == 1
    assert "Split 5 record(s)" in capsys.readouterr().out


# ── message axis ───────────────────────────────────────────────────────────
def test_message_split_keeps_a_source_on_both_sides():
    """The point of the axis: one source contributes past *and* future behaviour."""
    rec = _rec("a", *[f"2026-01-{d:02d}T00:00:00Z" for d in range(1, 11)])
    train, holdout = message_split([rec], cutoff=_parse_ts("2026-01-06T00:00:00Z"), min_messages=3)
    assert [r["source_id"] for r in train] == ["a"]
    assert [r["source_id"] for r in holdout] == ["a"]
    assert len(train[0]["messages"]) == 5
    assert len(holdout[0]["messages"]) == 5


def test_message_split_drops_a_side_below_min_messages():
    rec = _rec(
        "a", "2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z", *[f"2026-02-{d:02d}T00:00:00Z" for d in range(1, 5)]
    )
    train, holdout = message_split([rec], cutoff=_parse_ts("2026-01-15T00:00:00Z"), min_messages=3)
    assert train == []  # only 2 messages before the cutoff
    assert len(holdout) == 1 and len(holdout[0]["messages"]) == 4


def test_message_split_preserves_label_spread_the_source_axis_loses():
    """Regression pin for the 2026-07-24 failure.

    Both groups publish across the *same* period — the sporadic ones just post
    less often, so their newest message is always a little older. That alone is
    enough for the source axis to hand the whole holdout to the frequent
    publishers, taking the label with it.
    """
    daily = [f"2026-01-{d:02d}T00:00:00Z" for d in range(1, 32)] + [f"2026-02-{d:02d}T00:00:00Z" for d in range(1, 29)]
    occasional = ["2026-01-05T00:00:00Z", "2026-01-15T00:00:00Z", "2026-01-25T00:00:00Z"] + [
        "2026-02-05T00:00:00Z",
        "2026-02-15T00:00:00Z",
        "2026-02-25T00:00:00Z",
    ]
    frequent = [_rec(f"hi{i}", *daily, label=85) for i in range(3)]
    sporadic = [_rec(f"lo{i}", *occasional, label=10) for i in range(3)]
    records = frequent + sporadic

    _, src_holdout = temporal_split(records, holdout_fraction=0.5)
    assert set(label_spread(src_holdout)) == {85.0}  # low tail exiled to train

    _, msg_holdout = message_split(records, cutoff=_parse_ts("2026-02-01T00:00:00Z"), min_messages=3)
    assert set(label_spread(msg_holdout)) == {10.0, 85.0}  # both bands validated


def test_message_quantile_cutoff_splits_messages_not_sources():
    recs = [_rec("a", *[f"2026-01-{d:02d}T00:00:00Z" for d in range(1, 11)])]
    cutoff = message_quantile_cutoff(recs, holdout_fraction=0.2)
    assert cutoff == _parse_ts("2026-01-09T00:00:00Z")


def test_message_quantile_cutoff_rejects_untimed_records():
    with pytest.raises(ValueError):
        message_quantile_cutoff([{"source_id": "a", "messages": [{"text": "no ts"}]}], 0.2)


def test_message_split_ignores_unparseable_timestamps():
    rec = {
        "source_id": "a",
        "label": 50,
        "messages": [{"timestamp": "not-a-date", "text": "x"}]
        + [{"timestamp": f"2026-01-{d:02d}T00:00:00Z", "text": "x"} for d in range(1, 5)],
    }
    train, holdout = message_split([rec], cutoff=_parse_ts("2026-01-03T00:00:00Z"), min_messages=2)
    kept = sum(len(r["messages"]) for r in train + holdout)
    assert kept == 4  # the untimed message is placed on neither side


def test_main_message_axis_is_the_default(tmp_path, capsys):
    src = tmp_path / "sources.jsonl"
    src.write_text(
        json.dumps(_rec("a", *[f"2026-01-{d:02d}T00:00:00Z" for d in range(1, 11)])),
        encoding="utf-8",
    )
    rc = main(
        [
            "--input",
            str(src),
            "--train-out",
            str(tmp_path / "train.jsonl"),
            "--holdout-out",
            str(tmp_path / "holdout.jsonl"),
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "on the message axis" in out
    assert "holdout labels:" in out


# ── silence window ─────────────────────────────────────────────────────────
def test_record_span_hours_measures_first_to_last():
    rec = _rec("a", "2026-01-01T00:00:00Z", "2026-01-04T12:00:00Z", "2026-01-02T00:00:00Z")
    assert record_span_hours(rec) == 84.0


def test_record_span_hours_is_none_below_two_messages():
    assert record_span_hours(_rec("a", "2026-01-01T00:00:00Z")) is None


def test_window_bounds_spans_every_source():
    recs = [_rec("a", "2026-01-05T00:00:00Z", "2026-01-06T00:00:00Z"), _rec("b", "2026-01-01T00:00:00Z")]
    first, last = window_bounds(recs)
    assert first == _parse_ts("2026-01-01T00:00:00Z")
    assert last == _parse_ts("2026-01-06T00:00:00Z")


def test_window_bounds_is_none_without_timestamps():
    assert window_bounds([{"source_id": "a", "messages": [{"text": "no ts"}]}]) is None


def test_silence_blind_counts_windows_at_or_under_the_threshold():
    """72 h is the threshold: a 72 h window cannot hold a gap *longer* than 72 h."""
    exactly_72h = _rec("edge", "2026-01-01T00:00:00Z", "2026-01-04T00:00:00Z")
    over_72h = _rec("wide", "2026-01-01T00:00:00Z", "2026-01-05T00:00:00Z")
    single = _rec("thin", "2026-01-01T00:00:00Z")
    assert silence_blind_sources([exactly_72h, over_72h, single]) == (2, 3)


def test_silence_blind_respects_the_source_type_threshold():
    rec = {**_rec("a", "2026-01-01T00:00:00Z", "2026-01-05T00:00:00Z"), "source_type": "news"}
    assert silence_blind_sources([rec]) == (0, 1)  # 96 h > the 72 h news threshold


def test_main_warns_when_no_holdout_source_can_register_a_gap(tmp_path, capsys):
    """The three-week-collection trap: a short holdout pins silence at 0."""
    src = tmp_path / "sources.jsonl"
    # Four hours apart over two days, so each half stays well under 72 h while
    # keeping enough messages per side to clear min_messages.
    stamps = [f"2026-01-0{d}T{h:02d}:00:00Z" for d in (1, 2) for h in range(0, 24, 4)]
    src.write_text(
        "\n".join(json.dumps(_rec(f"s{i}", *stamps, label=10 * i)) for i in range(1, 5)),
        encoding="utf-8",
    )
    rc = main(
        [
            "--input",
            str(src),
            "--train-out",
            str(tmp_path / "train.jsonl"),
            "--holdout-out",
            str(tmp_path / "holdout.jsonl"),
            "--holdout-fraction",
            "0.5",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "holdout silence-blind: 4/4" in out
    assert "silence is identically 0 on this side" in out


def test_main_warns_when_a_quarter_of_the_holdout_is_silence_blind(tmp_path, capsys):
    src = tmp_path / "sources.jsonl"
    # Three sources publish across five weeks, one only inside a single day.
    wide = [f"2026-01-{d:02d}T00:00:00Z" for d in range(1, 32, 3)]
    narrow = [f"2026-01-31T{h:02d}:00:00Z" for h in range(0, 24, 4)]
    src.write_text(
        "\n".join(
            [json.dumps(_rec(f"w{i}", *wide, label=10 * i)) for i in range(1, 4)] + [json.dumps(_rec("n", *narrow))]
        ),
        encoding="utf-8",
    )
    rc = main(
        [
            "--input",
            str(src),
            "--train-out",
            str(tmp_path / "train.jsonl"),
            "--holdout-out",
            str(tmp_path / "holdout.jsonl"),
            "--axis",
            "source",
            "--holdout-fraction",
            "0.5",
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "span <= the 72 h silence threshold" in out
    assert "by construction rather than by" in out


def test_main_stays_quiet_when_the_window_is_long_enough(tmp_path, capsys):
    src = tmp_path / "sources.jsonl"
    stamps = [f"2026-0{m}-{d:02d}T00:00:00Z" for m in (1, 2) for d in range(1, 28, 2)]
    src.write_text(
        "\n".join(json.dumps(_rec(f"s{i}", *stamps, label=10 * i)) for i in range(1, 5)),
        encoding="utf-8",
    )
    rc = main(
        [
            "--input",
            str(src),
            "--train-out",
            str(tmp_path / "train.jsonl"),
            "--holdout-out",
            str(tmp_path / "holdout.jsonl"),
        ]
    )
    assert rc == 0
    out = capsys.readouterr().out
    assert "holdout silence-blind: 0/4" in out
    assert "silence threshold" not in out  # reported, not warned about


def test_main_warns_when_the_holdout_cannot_validate(tmp_path, capsys):
    src = tmp_path / "sources.jsonl"
    src.write_text(
        "\n".join(
            json.dumps(_rec(f"s{i}", *[f"2026-01-{d:02d}T00:00:00Z" for d in range(1, 21)], label=70)) for i in range(4)
        ),
        encoding="utf-8",
    )
    rc = main(
        [
            "--input",
            str(src),
            "--train-out",
            str(tmp_path / "train.jsonl"),
            "--holdout-out",
            str(tmp_path / "holdout.jsonl"),
        ]
    )
    assert rc == 0
    assert "cannot rank sources it never varies over" in capsys.readouterr().out
