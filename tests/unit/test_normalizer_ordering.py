"""Regression tests for normalize_messages ordering, dedup and input hygiene.

These pin the fixes for the timestamp-ordering and non-string-input bugs found
in the July 2026 repo audit: the pipeline must sort on the real instant (not
the ISO string), dedup the same moment written with different offsets, tolerate
naive timestamps, and skip non-string fields instead of crashing.
"""

from cats.pipeline.normalizer import normalize_messages


def test_mixed_offsets_sort_by_instant_not_string():
    # 10:00+02:00 == 08:00Z, which is BEFORE 09:30Z — lexicographic string
    # sorting would put "10:00+02:00" last and get the order wrong.
    out = normalize_messages(
        [
            {"timestamp": "2026-01-01T10:00:00+02:00", "text": "first (08:00Z)"},
            {"timestamp": "2026-01-01T09:30:00+00:00", "text": "second (09:30Z)"},
        ]
    )
    assert [m.text for m in out] == ["first (08:00Z)", "second (09:30Z)"]


def test_same_instant_different_offset_is_deduped():
    out = normalize_messages(
        [
            {"timestamp": "2026-01-01T10:00:00+02:00", "text": "same"},
            {"timestamp": "2026-01-01T08:00:00Z", "text": "same"},
        ]
    )
    assert len(out) == 1


def test_naive_and_aware_timestamps_do_not_crash():
    # A naive timestamp is treated as UTC; sorting a naive/aware mix must not
    # raise "can't compare offset-naive and offset-aware datetimes".
    out = normalize_messages(
        [
            {"timestamp": "2026-01-01T09:00:00", "text": "naive-09"},
            {"timestamp": "2026-01-01T08:00:00Z", "text": "aware-08"},
        ]
    )
    assert [m.text for m in out] == ["aware-08", "naive-09"]


def test_non_string_fields_are_skipped_not_crash():
    assert normalize_messages([{"timestamp": "2026-01-01T08:00:00Z", "text": 123}]) == []
    assert normalize_messages([{"timestamp": 123, "text": "hi"}]) == []
    assert normalize_messages([{"timestamp": "2026-01-01T08:00:00Z", "text": "   "}]) == []


def test_valid_messages_still_pass_through():
    out = normalize_messages(
        [
            {"timestamp": "2026-01-02T08:00:00Z", "text": "b"},
            {"timestamp": "2026-01-01T08:00:00Z", "text": "a"},
        ]
    )
    assert [m.text for m in out] == ["a", "b"]
