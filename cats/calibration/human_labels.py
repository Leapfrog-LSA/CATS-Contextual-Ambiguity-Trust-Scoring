"""Human-provided score labels: schema, validation, and safe appending.

Human labels are external verdicts on a CATS score ("the band should be X,
not Y") collected from GitHub issues (the ``score_feedback`` template), the
public demo, or an API-contest channel. **Validation-only** — a human label
is never fed into a signal or the weighted aggregation. Doing so would be
leakage: the same disagreement would both grade the model and train it. The
allowed use is measuring agreement between CATS and human verdicts (e.g. on
a holdout), the same role ``data/labels.jsonl`` plays for calibration but
sourced from people instead of distant supervision.

Schema — one JSON object per line in ``data/human_labels.jsonl``::

    {
      "source_url":     str,            # the URL that was scored
      "domain":         str,            # normalised hostname (no scheme, no www.)
      "cats_score":     float,          # 0-100, the score CATS returned
      "cats_band":      str,            # the band CATS returned for cats_score
      "engine_version": str,            # cats.scoring.engine.ENGINE_VERSION at scoring time
      "cats_version":   str,            # cats.__version__ at scoring time
      "human_band":     str,            # the band a human says is correct
      "reason":         str,            # free-text justification
      "date":           str,            # ISO-8601 date (YYYY-MM-DD)
      "provenance":     str,            # "issue" | "demo" | "api_contest"
      "issue_url":      str | None,     # required when provenance == "issue"
    }

Both ``cats_band``/``human_band`` must be one of the five CATS bands, and
``cats_band`` must match ``determine_band(cats_score)`` — this module never
invents a band, it only checks internal consistency of what was reported.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date as _date
from pathlib import Path
from typing import Dict, List, Optional, Union

from cats.scoring.engine import determine_band

_VALID_BANDS = {"high", "medium_high", "medium", "low", "very_low"}
_VALID_PROVENANCE = {"issue", "demo", "api_contest"}

_REQUIRED_FIELDS = (
    "source_url",
    "domain",
    "cats_score",
    "cats_band",
    "engine_version",
    "cats_version",
    "human_band",
    "reason",
    "date",
    "provenance",
)

DEFAULT_PATH = Path(__file__).resolve().parents[2] / "data" / "human_labels.jsonl"

PathLike = Union[str, Path]


@dataclass
class ValidationError:
    line: int  # 0 for file-level errors (e.g. file not found)
    message: str

    def __str__(self) -> str:
        return f"line {self.line}: {self.message}" if self.line else self.message


def validate_record(record: Dict) -> List[str]:
    """Return every schema violation in one record; ``[]`` means it's valid."""
    errors: List[str] = []

    for field_name in _REQUIRED_FIELDS:
        if field_name not in record or record[field_name] in (None, ""):
            errors.append(f"missing required field '{field_name}'")
    if errors:
        return errors  # remaining checks assume the fields are present

    if not isinstance(record["source_url"], str) or "://" not in record["source_url"]:
        errors.append("'source_url' must be a full URL (scheme://host/...)")

    domain = record["domain"]
    if not isinstance(domain, str) or "://" in domain or "/" in domain:
        errors.append("'domain' must be a bare hostname, not a URL")

    score = record["cats_score"]
    if isinstance(score, bool) or not isinstance(score, (int, float)) or not (0.0 <= float(score) <= 100.0):
        errors.append("'cats_score' must be a number in [0, 100]")

    for band_field in ("cats_band", "human_band"):
        if record[band_field] not in _VALID_BANDS:
            errors.append(f"'{band_field}' must be one of {sorted(_VALID_BANDS)}, got {record[band_field]!r}")

    if not errors and record["cats_band"] != determine_band(float(score)):
        errors.append(
            f"'cats_band' ({record['cats_band']!r}) does not match "
            f"determine_band(cats_score) ({determine_band(float(score))!r})"
        )

    try:
        _date.fromisoformat(str(record["date"]))
    except ValueError:
        errors.append("'date' must be an ISO-8601 date (YYYY-MM-DD)")

    provenance = record["provenance"]
    if provenance not in _VALID_PROVENANCE:
        errors.append(f"'provenance' must be one of {sorted(_VALID_PROVENANCE)}, got {provenance!r}")
    if provenance == "issue" and not record.get("issue_url"):
        errors.append("'issue_url' is required when provenance is 'issue'")

    if not isinstance(record["reason"], str) or not record["reason"].strip():
        errors.append("'reason' must be non-empty text")

    return errors


def validate(path: PathLike = DEFAULT_PATH) -> List[ValidationError]:
    """Validate every record in a ``human_labels.jsonl`` file.

    Returns all violations found; an empty list means every line is valid
    (an empty or all-blank file is valid — there's nothing to violate).
    """
    path = Path(path)
    if not path.exists():
        return [ValidationError(0, f"file not found: {path}")]

    violations: List[ValidationError] = []
    with path.open(encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            raw = raw.strip()
            if not raw:
                continue
            try:
                record = json.loads(raw)
            except json.JSONDecodeError as exc:
                violations.append(ValidationError(lineno, f"invalid JSON: {exc}"))
                continue
            if not isinstance(record, dict):
                violations.append(ValidationError(lineno, "record must be a JSON object"))
                continue
            violations.extend(ValidationError(lineno, msg) for msg in validate_record(record))
    return violations


def append(record: Dict, path: PathLike = DEFAULT_PATH) -> None:
    """Validate and append one record to a ``human_labels.jsonl`` file.

    Raises ``ValueError`` (listing every violation) instead of writing
    anything if the record doesn't match the schema.
    """
    errors = validate_record(record)
    if errors:
        raise ValueError("invalid human_labels record:\n" + "\n".join(f"  - {e}" for e in errors))

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load(path: PathLike = DEFAULT_PATH) -> List[Dict]:
    """Load every valid record from a ``human_labels.jsonl`` file (skips invalid/blank lines)."""
    path = Path(path)
    if not path.exists():
        return []
    records: List[Dict] = []
    with path.open(encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                record = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict) and not validate_record(record):
                records.append(record)
    return records


def _format_report(violations: List[ValidationError]) -> str:
    if not violations:
        return "OK"
    return "\n".join(str(v) for v in violations)


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        prog="python -m cats.calibration.human_labels",
        description="Validate a human_labels.jsonl file against the schema.",
    )
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_PATH, help="path to human_labels.jsonl")
    args = parser.parse_args(argv)

    violations = validate(args.path)
    print(_format_report(violations))
    return 1 if violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
