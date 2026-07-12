from cats.pipeline.normalizer import normalize_messages


def test_normalize_sorts_by_timestamp():
    raw = [
        {"timestamp": "2026-01-01T10:00:00Z", "text": "Second"},
        {"timestamp": "2026-01-01T08:00:00Z", "text": "First"},
    ]
    result = normalize_messages(raw)
    assert len(result) == 2
    assert result[0].text == "First"
    assert result[1].text == "Second"


def test_normalize_deduplicates():
    raw = [
        {"timestamp": "2026-01-01T08:00:00Z", "text": "Same message"},
        {"timestamp": "2026-01-01T08:00:00Z", "text": "Same message"},
    ]
    result = normalize_messages(raw)
    assert len(result) == 1


def test_normalize_skips_invalid():
    raw = [
        {"timestamp": "2026-01-01T08:00:00Z", "text": "Valid"},
        {"timestamp": "not-a-date", "text": "Invalid timestamp"},
        {"timestamp": "2026-01-01T09:00:00Z", "text": ""},
        {"text": "Missing timestamp"},
        {"timestamp": "2026-01-01T10:00:00Z"},
    ]
    result = normalize_messages(raw)
    assert len(result) == 1
    assert result[0].text == "Valid"


def test_normalize_strips_whitespace():
    raw = [{"timestamp": "2026-01-01T08:00:00Z", "text": "  Hello world  "}]
    result = normalize_messages(raw)
    assert result[0].text == "Hello world"


def test_normalize_empty_input():
    assert normalize_messages([]) == []


def test_normalize_sorts_chronologically_across_timezones():
    # 10:00+05:00 is 05:00 UTC — chronologically FIRST, although a naive
    # string sort would place it after 08:00+00:00.
    raw = [
        {"timestamp": "2026-01-01T08:00:00+00:00", "text": "Second"},
        {"timestamp": "2026-01-01T10:00:00+05:00", "text": "First"},
    ]
    result = normalize_messages(raw)
    assert [m.text for m in result] == ["First", "Second"]
    assert all(m.timestamp.endswith("+00:00") for m in result)  # stored as UTC


def test_normalize_naive_timestamp_taken_as_utc():
    raw = [
        {"timestamp": "2026-01-01T08:00:00", "text": "Naive"},
        {"timestamp": "2026-01-01T09:00:00Z", "text": "Aware"},
    ]
    result = normalize_messages(raw)
    assert [m.text for m in result] == ["Naive", "Aware"]
    assert result[0].timestamp == "2026-01-01T08:00:00+00:00"


def test_normalize_dedups_same_instant_different_offsets():
    raw = [
        {"timestamp": "2026-01-01T08:00:00+00:00", "text": "Same message"},
        {"timestamp": "2026-01-01T09:00:00+01:00", "text": "Same message"},
    ]
    assert len(normalize_messages(raw)) == 1


def test_normalize_skips_non_text_input_without_crashing():
    raw = [
        {"timestamp": "2026-01-01T08:00:00Z", "text": "Valid"},
        {"timestamp": "2026-01-01T09:00:00Z", "text": 12345},
        {"timestamp": "2026-01-01T10:00:00Z", "text": ["not", "a", "string"]},
        {"timestamp": 1735718400, "text": "Numeric timestamp"},
        {"timestamp": None, "text": "None timestamp"},
        "not-a-dict",
        None,
    ]
    result = normalize_messages(raw)
    assert len(result) == 1
    assert result[0].text == "Valid"
