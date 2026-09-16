import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "research"))

from ingest_score_feedback import build_record, parse_issue_body  # noqa: E402

_ISSUE_BODY = """### Source URL

https://example-news-outlet.it

### Command / call used

cats score https://example-news-outlet.it --source-type news

### CATS version

cats-scoring 1.7.0

### Score / band you got

67.3 / medium_high

### Score / band you expected

should be high

### Why do you think the score is wrong?

Consistent daily cadence for 3+ years, no clone domain flags.

### Consent

- [X] I consent to this case being added anonymised to `data/human_labels.jsonl`.
"""

_ISSUE_URL = "https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring/issues/123"


def test_parse_issue_body_extracts_all_fields():
    fields = parse_issue_body(_ISSUE_BODY)

    assert fields["Source URL"] == "https://example-news-outlet.it"
    assert fields["Score / band you got"] == "67.3 / medium_high"
    assert "Consistent daily cadence" in fields["Why do you think the score is wrong?"]


def test_build_record_parses_score_band_and_consent():
    record = build_record(_ISSUE_BODY, issue_url=_ISSUE_URL, cats_version="1.7.0")

    assert record["source_url"] == "https://example-news-outlet.it"
    assert record["domain"] == "example-news-outlet.it"
    assert record["cats_score"] == 67.3
    assert record["cats_band"] == "medium_high"
    assert record["human_band"] == "high"
    assert record["provenance"] == "issue"
    assert record["issue_url"] == _ISSUE_URL
    assert record["_consent_given"] is True
    assert "_warning_band_mismatch" not in record


def test_build_record_detects_score_band_mismatch():
    body = _ISSUE_BODY.replace("67.3 / medium_high", "90.0 / medium_high")

    record = build_record(body, issue_url=_ISSUE_URL)

    assert record["cats_score"] == 90.0
    assert "_warning_band_mismatch" in record


def test_build_record_no_consent_when_unchecked():
    body = _ISSUE_BODY.replace("- [X] I consent", "- [ ] I consent")

    record = build_record(body, issue_url=_ISSUE_URL)

    assert record["_consent_given"] is False


def test_build_record_ambiguous_human_band_is_none():
    body = _ISSUE_BODY.replace(
        "should be high",
        "somewhere between low and high, not sure",
    )

    record = build_record(body, issue_url=_ISSUE_URL)

    assert record["human_band"] is None
