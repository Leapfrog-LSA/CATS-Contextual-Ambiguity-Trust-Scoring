import json

import pytest

from cats.calibration.human_labels import ValidationError, append, load, validate, validate_record

_VALID_RECORD = {
    "source_url": "https://example-news-outlet.it/rss",
    "domain": "example-news-outlet.it",
    "cats_score": 67.3,
    "cats_band": "medium_high",
    "engine_version": "1.4",
    "cats_version": "1.7.0",
    "human_band": "high",
    "reason": "Consistent daily cadence, no clone domain flags.",
    "date": "2026-09-16",
    "provenance": "issue",
    "issue_url": "https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring/issues/123",
}


def test_valid_record_has_no_errors():
    assert validate_record(_VALID_RECORD) == []


def test_missing_required_field():
    record = dict(_VALID_RECORD)
    del record["reason"]
    errors = validate_record(record)
    assert any("reason" in e for e in errors)


@pytest.mark.parametrize("field", list(_VALID_RECORD))
def test_missing_each_required_field_except_issue_url(field):
    record = dict(_VALID_RECORD)
    if field == "issue_url":
        pytest.skip("issue_url is conditionally required, checked separately")
    del record[field]
    assert validate_record(record) != []


def test_cats_score_out_of_range():
    record = dict(_VALID_RECORD)
    record["cats_score"] = 142.0
    errors = validate_record(record)
    assert any("cats_score" in e for e in errors)


def test_cats_score_bool_rejected():
    record = dict(_VALID_RECORD)
    record["cats_score"] = True
    errors = validate_record(record)
    assert any("cats_score" in e for e in errors)


def test_invalid_band_value():
    record = dict(_VALID_RECORD)
    record["human_band"] = "extremely_high"
    errors = validate_record(record)
    assert any("human_band" in e for e in errors)


def test_cats_band_must_match_determine_band():
    record = dict(_VALID_RECORD)
    record["cats_score"] = 90.0  # -> "high"
    record["cats_band"] = "medium_high"  # mismatched on purpose
    errors = validate_record(record)
    assert any("does not match" in e for e in errors)


def test_invalid_date():
    record = dict(_VALID_RECORD)
    record["date"] = "16/09/2026"
    errors = validate_record(record)
    assert any("date" in e for e in errors)


def test_invalid_provenance():
    record = dict(_VALID_RECORD)
    record["provenance"] = "twitter_dm"
    errors = validate_record(record)
    assert any("provenance" in e for e in errors)


def test_issue_url_required_when_provenance_is_issue():
    record = dict(_VALID_RECORD)
    del record["issue_url"]
    errors = validate_record(record)
    assert any("issue_url" in e for e in errors)


def test_issue_url_not_required_for_demo_provenance():
    record = dict(_VALID_RECORD)
    record["provenance"] = "demo"
    del record["issue_url"]
    assert validate_record(record) == []


def test_domain_rejects_full_url():
    record = dict(_VALID_RECORD)
    record["domain"] = "https://example-news-outlet.it/"
    errors = validate_record(record)
    assert any("domain" in e for e in errors)


def test_reason_must_be_non_empty():
    record = dict(_VALID_RECORD)
    record["reason"] = "   "
    errors = validate_record(record)
    assert any("reason" in e for e in errors)


# ── validate(path) ───────────────────────────────────────────────────────


def test_validate_missing_file(tmp_path):
    violations = validate(tmp_path / "does_not_exist.jsonl")
    assert len(violations) == 1
    assert "not found" in violations[0].message


def test_validate_empty_file_is_valid(tmp_path):
    path = tmp_path / "human_labels.jsonl"
    path.write_text("")
    assert validate(path) == []


def test_validate_file_with_valid_and_invalid_lines(tmp_path):
    path = tmp_path / "human_labels.jsonl"
    bad_record = dict(_VALID_RECORD)
    bad_record["cats_score"] = 999.0
    path.write_text(
        json.dumps(_VALID_RECORD, ensure_ascii=False)
        + "\n"
        + "not json at all\n"
        + json.dumps(bad_record, ensure_ascii=False)
        + "\n"
    )

    violations = validate(path)

    assert len(violations) == 2
    assert violations[0].line == 2
    assert "invalid JSON" in violations[0].message
    assert violations[1].line == 3
    assert "cats_score" in violations[1].message


def test_validation_error_str_includes_line_number():
    err = ValidationError(3, "bad thing")
    assert str(err) == "line 3: bad thing"


# ── append() ─────────────────────────────────────────────────────────────


def test_append_valid_record(tmp_path):
    path = tmp_path / "human_labels.jsonl"
    append(_VALID_RECORD, path=path)

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0]) == _VALID_RECORD


def test_append_invalid_record_raises_and_does_not_write(tmp_path):
    path = tmp_path / "human_labels.jsonl"
    bad_record = dict(_VALID_RECORD)
    bad_record["provenance"] = "carrier_pigeon"

    with pytest.raises(ValueError):
        append(bad_record, path=path)

    assert not path.exists()


def test_append_creates_parent_directories(tmp_path):
    path = tmp_path / "nested" / "dir" / "human_labels.jsonl"
    append(_VALID_RECORD, path=path)
    assert path.exists()


# ── load() ───────────────────────────────────────────────────────────────


def test_load_skips_invalid_lines(tmp_path):
    path = tmp_path / "human_labels.jsonl"
    bad_record = dict(_VALID_RECORD)
    bad_record["cats_score"] = 999.0
    path.write_text(
        json.dumps(_VALID_RECORD, ensure_ascii=False) + "\n" + json.dumps(bad_record, ensure_ascii=False) + "\n"
    )

    records = load(path)

    assert records == [_VALID_RECORD]


def test_load_missing_file_returns_empty_list(tmp_path):
    assert load(tmp_path / "nope.jsonl") == []
