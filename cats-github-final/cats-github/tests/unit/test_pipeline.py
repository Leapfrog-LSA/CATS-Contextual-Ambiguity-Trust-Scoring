"""Unit tests — pipeline normalizer."""
import pytest
from cats.pipeline.normalizer import normalize_messages


def test_normalize_sorts_by_timestamp():
    raw = [
        {"timestamp": "2026-01-01T12:00:00Z", "text": "second"},
        {"timestamp": "2026-01-01T10:00:00Z", "text": "first"},
    ]
    result = normalize_messages(raw)
    assert result[0].text == "first"
    assert result[1].text == "second"


def test_normalize_deduplicates():
    raw = [
        {"timestamp": "2026-01-01T10:00:00Z", "text": "duplicato"},
        {"timestamp": "2026-01-01T10:00:00Z", "text": "duplicato"},
    ]
    result = normalize_messages(raw)
    assert len(result) == 1


def test_normalize_skips_missing_fields():
    raw = [
        {"timestamp": "2026-01-01T10:00:00Z"},        # missing text
        {"text": "missing timestamp"},                 # missing timestamp
        {"timestamp": "2026-01-01T10:00:00Z", "text": "valid"},
    ]
    result = normalize_messages(raw)
    assert len(result) == 1
    assert result[0].text == "valid"


def test_normalize_skips_invalid_timestamps():
    raw = [
        {"timestamp": "not-a-date", "text": "invalid"},
        {"timestamp": "2026-01-01T10:00:00Z", "text": "valid"},
    ]
    result = normalize_messages(raw)
    assert len(result) == 1


def test_normalize_strips_whitespace():
    raw = [{"timestamp": "2026-01-01T10:00:00Z", "text": "  spazi  "}]
    result = normalize_messages(raw)
    assert result[0].text == "spazi"


def test_normalize_empty_input():
    assert normalize_messages([]) == []
