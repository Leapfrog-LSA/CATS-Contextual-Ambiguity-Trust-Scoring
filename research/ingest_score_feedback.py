"""Turn a "Score feedback" GitHub issue into a draft data/human_labels.jsonl record.

Reads the *rendered* body of an issue filed with
``.github/ISSUE_TEMPLATE/score_feedback.yml`` (save it locally, e.g. via
``gh issue view <n> --json body -q .body > issue.md``) and parses the
form's fields into a candidate record matching
``cats.calibration.human_labels``'s schema.

This never appends silently. Two fields the issue form doesn't ask for
in a schema-ready shape have to be resolved by a human before the record is
usable:

* **cats_score / cats_band** — parsed from the free-text "Score / band you
  got" answer (e.g. ``"67.3 / medium_high"``); if it doesn't parse cleanly,
  the record is left incomplete and flagged.
* **human_band** — the "Score / band you expected" answer is free text (a
  reporter may write "should be high, not medium"); this script tries to
  pull out a recognised band keyword but does **not** guess when none is
  found or more than one is present.
* **engine_version** — not asked on the form at all (a reporter can't be
  expected to know it); defaults to the *currently installed*
  ``cats.scoring.engine.ENGINE_VERSION`` unless overridden with
  ``--engine-version``. Verify this matches what the engine actually was
  when the issue's score was produced (check the CATS version reported).

By default the script prints the draft record as JSON for review — it never
touches ``data/human_labels.jsonl`` unless you pass ``--append``, and the
consent checkbox in the issue must be checked (``--force`` overrides this,
for a maintainer who has separately confirmed consent).

Usage::

    python research/ingest_score_feedback.py issue.md --issue-url \\
        https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring/issues/123
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Dict, Optional

from cats import __version__ as _CATS_VERSION
from cats.calibration.human_labels import append, validate_record
from cats.calibration.label_from_ratings import normalize_host
from cats.scoring.engine import ENGINE_VERSION, determine_band

_VALID_BANDS = ("high", "medium_high", "medium", "low", "very_low")

# Issue-form field label -> internal key. Must track the `label:` values in
# .github/ISSUE_TEMPLATE/score_feedback.yml.
_FIELD_LABELS = {
    "Source URL": "source_url",
    "Command / call used": "command",
    "CATS version": "cats_version_raw",
    "Score / band you got": "score_got",
    "Score / band you expected": "score_expected",
    "Why do you think the score is wrong?": "reason",
    "Consent": "consent",
}

_SECTION_RE = re.compile(r"^### (.+?)\s*$", re.MULTILINE)


def parse_issue_body(body: str) -> Dict[str, str]:
    """Split a rendered GitHub issue-form body into {field label: answer}."""
    matches = list(_SECTION_RE.finditer(body))
    fields: Dict[str, str] = {}
    for i, m in enumerate(matches):
        label = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        value = body[start:end].strip()
        fields[label] = value
    return fields


def _parse_score_band(text: str) -> tuple[Optional[float], Optional[str]]:
    """Parse a "67.3 / medium_high" style answer into (score, band)."""
    score = None
    band = None
    m = re.search(r"(\d+(?:\.\d+)?)", text)
    if m:
        try:
            value = float(m.group(1))
            if 0.0 <= value <= 100.0:
                score = value
        except ValueError:
            pass
    found = _find_bands(text)
    if len(found) == 1:
        band = found.pop()
    return score, band


def _find_bands(text: str) -> set:
    """Bands mentioned in free text, matched on whole words/tokens only.

    ``\\b`` treats ``_`` as a word character, so ``\\bhigh\\b`` does not match
    the "high" inside "medium_high" -- each band is only counted once even
    when one band name is a substring of another (high / medium_high).
    """
    lowered = text.lower()
    found = set()
    for band in _VALID_BANDS:
        underscored = re.compile(rf"\b{re.escape(band)}\b")
        spaced = re.compile(rf"\b{re.escape(band.replace('_', ' '))}\b")
        if underscored.search(lowered) or spaced.search(lowered):
            found.add(band)
    return found


def _parse_human_band(text: str) -> Optional[str]:
    found = _find_bands(text)
    return found.pop() if len(found) == 1 else None


def _is_checked(consent_text: str) -> bool:
    return bool(re.search(r"^\s*- \[[xX]\]", consent_text, re.MULTILINE))


def build_record(
    body: str,
    issue_url: str,
    engine_version: str = ENGINE_VERSION,
    cats_version: Optional[str] = None,
    date: Optional[str] = None,
) -> Dict:
    """Build a (possibly incomplete) candidate record from an issue body."""
    fields = parse_issue_body(body)

    source_url = fields.get("Source URL", "").strip()
    score, cats_band = _parse_score_band(fields.get("Score / band you got", ""))
    human_band = _parse_human_band(fields.get("Score / band you expected", ""))
    reason = fields.get("Why do you think the score is wrong?", "").strip()

    record: Dict = {
        "source_url": source_url,
        "domain": normalize_host(source_url) if source_url else "",
        "cats_score": score,
        "cats_band": cats_band,
        "engine_version": engine_version,
        "cats_version": cats_version or _CATS_VERSION,
        "human_band": human_band,
        "reason": reason,
        "date": date or dt.date.today().isoformat(),
        "provenance": "issue",
        "issue_url": issue_url,
    }
    # Cross-check the parsed band against the parsed score when both parsed.
    if score is not None and cats_band is not None and determine_band(score) != cats_band:
        record["_warning_band_mismatch"] = (
            f"parsed cats_band {cats_band!r} disagrees with determine_band({score}) "
            f"= {determine_band(score)!r} -- check the 'Score / band you got' answer by hand"
        )
    record["_consent_given"] = _is_checked(fields.get("Consent", ""))
    return record


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("body_file", type=Path, help="path to the saved issue body (markdown)")
    parser.add_argument("--issue-url", required=True, help="permalink to the source issue")
    parser.add_argument("--engine-version", default=ENGINE_VERSION, help="override the detected ENGINE_VERSION")
    parser.add_argument("--cats-version", default=None, help="override cats.__version__")
    parser.add_argument("--date", default=None, help="override the record date (ISO-8601); default: today")
    parser.add_argument("--append", action="store_true", help="append to data/human_labels.jsonl if it validates")
    parser.add_argument(
        "--force",
        action="store_true",
        help="append even if the issue's consent checkbox wasn't ticked (maintainer confirmed consent separately)",
    )
    args = parser.parse_args(argv)

    body = args.body_file.read_text(encoding="utf-8")
    record = build_record(
        body,
        issue_url=args.issue_url,
        engine_version=args.engine_version,
        cats_version=args.cats_version,
        date=args.date,
    )

    consent_given = record.pop("_consent_given")
    warning = record.pop("_warning_band_mismatch", None)
    if warning:
        print(f"WARNING: {warning}", file=sys.stderr)

    clean_record = {k: v for k, v in record.items() if v is not None}
    print(json.dumps(clean_record, indent=2, ensure_ascii=False))

    if not args.append:
        return 0

    if not consent_given and not args.force:
        print(
            "\nNot appending: the issue's consent checkbox wasn't ticked. Pass --force "
            "only if consent was confirmed separately.",
            file=sys.stderr,
        )
        return 1

    errors = validate_record(clean_record)
    if errors:
        print("\nNot appending: record is incomplete/invalid:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print("\nComplete the missing fields by hand and use cats.calibration.human_labels.append().", file=sys.stderr)
        return 1

    append(clean_record)
    print(f"\nAppended to {Path('data/human_labels.jsonl').resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
