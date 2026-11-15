"""Composition of a calibration dataset: label x language, signal confidence, volume.

Why. A holdout is only as informative as its mix. Before adding sources (see
``docs/dataset_expansion_runbook.md``) the maintainer needs to see, per label,
how many sources are Italian vs. not, how many had at least one signal computed
on thin evidence, and how much text each source contributed. This script counts
that from the ``diagnostics`` block that :mod:`cats.calibration.build_dataset`
writes next to ``source_type`` / ``signals`` / ``label``.

What it prints, for one ``.jsonl`` dataset:

* a table of record counts per ``label`` x language (``italian`` / ``other`` /
  ``unknown``);
* how many sources have at least one per-signal confidence below 1;
* minimum / median / maximum of ``n_messages``.

Limits.

* The language is the ``detected`` field of
  :func:`cats.pipeline.language.detect_language`, a function-word heuristic
  that only separates **Italian** from **other** and **uncertain**
  (``unknown``). It does not identify which non-Italian language a source uses.
* Records without ``diagnostics`` — every dataset committed before this block
  existed, e.g. ``data/train.jsonl``, ``data/holdout_future.jsonl``,
  ``data/holdout.jsonl`` — are counted as language ``unknown`` and excluded
  from the confidence / message-count statistics. Their number is stated in
  the output; it is not an error.
* Purely descriptive: it never changes a score, band, weight or dataset, and
  the counts must not be used to weight, filter or exclude samples.

It reads one file, makes no network call and writes nothing.

Usage::

    python research/holdout_composition.py --dataset data/holdout_future.jsonl
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path
from typing import Dict, List, Optional, Sequence

LANGUAGES = ("italian", "other", "unknown")


def read_jsonl(path: Path) -> List[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _label_key(record: dict) -> str:
    label = record.get("label")
    if isinstance(label, (int, float)):
        return f"{float(label):g}"
    return "missing"


def _label_sort_key(key: str) -> tuple:
    try:
        return (0, float(key))
    except ValueError:
        return (1, 0.0)


def composition(records: List[dict]) -> dict:
    """Count label x language, low-confidence sources and message volume."""
    table: Dict[str, Dict[str, int]] = {}
    without_diagnostics = 0
    low_confidence = 0
    n_messages: List[int] = []
    for r in records:
        diag = r.get("diagnostics")
        if isinstance(diag, dict):
            lang = diag.get("language")
            if lang not in LANGUAGES:
                lang = "unknown"
            conf = diag.get("signal_confidence") or {}
            if any(isinstance(c, (int, float)) and c < 1.0 for c in conf.values()):
                low_confidence += 1
            n = diag.get("n_messages")
            if isinstance(n, int):
                n_messages.append(n)
        else:
            without_diagnostics += 1
            lang = "unknown"
        row = table.setdefault(_label_key(r), {lg: 0 for lg in LANGUAGES})
        row[lang] += 1
    return {
        "records": len(records),
        "without_diagnostics": without_diagnostics,
        "table": {k: table[k] for k in sorted(table, key=_label_sort_key)},
        "low_confidence_sources": low_confidence,
        "n_messages": (
            {"min": min(n_messages), "median": statistics.median(n_messages), "max": max(n_messages)}
            if n_messages
            else None
        ),
    }


def render(path: Path, comp: dict) -> str:
    lines = [f"Dataset: {path}", f"Records: {comp['records']}"]
    lines.append(
        f"Records without diagnostics: {comp['without_diagnostics']} (counted as language 'unknown', "
        "excluded from the confidence and n_messages statistics)"
    )
    lines.append("")
    header = f"{'label':>8}  " + "  ".join(f"{lg:>8}" for lg in LANGUAGES) + f"  {'total':>6}"
    lines.append(header)
    lines.append("-" * len(header))
    totals = {lg: 0 for lg in LANGUAGES}
    for label, row in comp["table"].items():
        for lg in LANGUAGES:
            totals[lg] += row[lg]
        lines.append(f"{label:>8}  " + "  ".join(f"{row[lg]:>8}" for lg in LANGUAGES) + f"  {sum(row.values()):>6}")
    lines.append("-" * len(header))
    lines.append(f"{'total':>8}  " + "  ".join(f"{totals[lg]:>8}" for lg in LANGUAGES) + f"  {comp['records']:>6}")
    lines.append("")
    with_diag = comp["records"] - comp["without_diagnostics"]
    lines.append(f"Sources with at least one signal confidence < 1: {comp['low_confidence_sources']} of {with_diag}")
    nm = comp["n_messages"]
    if nm is None:
        lines.append("n_messages: n/a (no record carries diagnostics)")
    else:
        lines.append(f"n_messages: min {nm['min']}  median {nm['median']:g}  max {nm['max']}")
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dataset", required=True, type=Path, help="calibration dataset (.jsonl)")
    args = parser.parse_args(argv)
    if not args.dataset.exists():
        parser.error(f"dataset not found: {args.dataset}")
    print(render(args.dataset, composition(read_jsonl(args.dataset))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
