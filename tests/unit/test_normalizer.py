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
