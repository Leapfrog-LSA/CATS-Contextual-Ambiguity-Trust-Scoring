"""Inventory of the third-party texts stored in this repository, per source and by length.

Why. The calibration and snapshot files (`data/*_sources.jsonl`,
`data/labelled_sources.jsonl`, `data/snapshots/*.jsonl`) hold message texts
collected from public RSS feeds. Those texts belong to their publishers, not to
this project. Before the maintainer decides whether raw texts stay public
(roadmap, item 1) — and before anything is purged or relicensed — they need to
know *what* is there: which publishers, how many texts, and how long they are.
A feed item that is a headline plus a one-line summary is a different thing
from a feed that ships the full article body.

What it reports, per ``source_id``:

* the publisher's domain (from the ``url`` homepage, else the ``rss`` URL —
  a feed can sit on a third-party host such as FeedBurner), ``source_type``
  and the files the source appears in;
* message occurrences across all files, and **unique** texts (deduplicated by
  SHA-256 of the text across every input file — the snapshots overlap heavily);
* characters in the unique texts: total, median, maximum;
* unique texts per length bucket (``<=300``, ``301-1000``, ``1001-5000``,
  ``>5000`` characters) and how many carry a ``metadata.link`` back to the
  original;
* first and last message timestamp.

The bucket edges are **descriptive only**. They are not legal thresholds: this
script makes no finding about copyright, quotation or text-and-data-mining
exceptions. That assessment is the maintainer's (see ``DATA_LICENSE``).

It reads files and writes reports; it never modifies or deletes data.

Usage::

    python research/text_inventory.py                       # default file set, Markdown summary
    python research/text_inventory.py --csv inventory.csv --json inventory.json
    python research/text_inventory.py "data/snapshots/*.jsonl" --top 0   # every source
"""

from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple
from urllib.parse import urlparse

DEFAULT_PATTERNS: Tuple[str, ...] = (
    "data/labelled_sources.jsonl",
    "data/train_sources.jsonl",
    "data/holdout_sources.jsonl",
    "data/snapshots/*.jsonl",
)

# (label, inclusive upper bound in characters); the last bucket is open-ended.
BUCKETS: Tuple[Tuple[str, Optional[int]], ...] = (
    ("<=300", 300),
    ("301-1000", 1000),
    ("1001-5000", 5000),
    (">5000", None),
)

CSV_FIELDS = (
    ["source_id", "domain", "source_type", "files", "occurrences", "unique_texts", "unique_chars"]
    + ["median_chars", "max_chars"]
    + [f"bucket_{label}" for label, _ in BUCKETS]
    + ["with_link", "first_timestamp", "last_timestamp"]
)


def bucket_for(length: int) -> str:
    """Return the label of the length bucket ``length`` (in characters) falls in."""
    for label, upper in BUCKETS:
        if upper is None or length <= upper:
            return label
    raise AssertionError("unreachable: the last bucket is open-ended")


def domain_of(record: dict) -> str:
    """Publisher host for a source record: from ``url``, else ``rss``; ``www.`` stripped, lower-cased."""
    for key in ("url", "rss"):
        value = record.get(key)
        if isinstance(value, str) and value:
            host = (urlparse(value).hostname or "").lower()
            if host:
                return host[4:] if host.startswith("www.") else host
    return ""


@dataclass
class SourceInventory:
    source_id: str
    domain: str = ""
    source_type: str = ""
    files: Set[str] = field(default_factory=set)
    occurrences: int = 0
    lengths: Dict[str, int] = field(default_factory=dict)  # text sha256 -> length in characters
    linked: Set[str] = field(default_factory=set)  # sha256 of unique texts that carry metadata.link
    first_timestamp: str = ""
    last_timestamp: str = ""

    def add_message(self, message: dict) -> None:
        text = message.get("text")
        if not isinstance(text, str):
            text = ""
        self.occurrences += 1
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        self.lengths[digest] = len(text)
        metadata = message.get("metadata")
        if isinstance(metadata, dict) and metadata.get("link"):
            self.linked.add(digest)
        timestamp = message.get("timestamp")
        # ISO-8601 UTC strings ("...Z") sort chronologically as plain strings.
        if isinstance(timestamp, str) and timestamp:
            if not self.first_timestamp or timestamp < self.first_timestamp:
                self.first_timestamp = timestamp
            if not self.last_timestamp or timestamp > self.last_timestamp:
                self.last_timestamp = timestamp

    def row(self) -> dict:
        lengths = list(self.lengths.values())
        buckets = {label: 0 for label, _ in BUCKETS}
        for length in lengths:
            buckets[bucket_for(length)] += 1
        row = {
            "source_id": self.source_id,
            "domain": self.domain,
            "source_type": self.source_type,
            "files": len(self.files),
            "occurrences": self.occurrences,
            "unique_texts": len(lengths),
            "unique_chars": sum(lengths),
            "median_chars": int(statistics.median(lengths)) if lengths else 0,
            "max_chars": max(lengths) if lengths else 0,
        }
        row.update({f"bucket_{label}": count for label, count in buckets.items()})
        row.update(
            {
                "with_link": len(self.linked),
                "first_timestamp": self.first_timestamp,
                "last_timestamp": self.last_timestamp,
            }
        )
        return row


def expand_patterns(patterns: Iterable[str]) -> List[Path]:
    """Expand globs to a sorted, de-duplicated list of existing files."""
    found: Set[Path] = set()
    for pattern in patterns:
        matches = glob.glob(pattern)
        if not matches and Path(pattern).is_file():
            matches = [pattern]
        found.update(Path(match) for match in matches if Path(match).is_file())
    return sorted(found)


def build_inventory(paths: Sequence[Path]) -> Tuple[Dict[str, SourceInventory], List[dict]]:
    """Read every JSONL file; return per-source inventories and per-file summaries."""
    sources: Dict[str, SourceInventory] = {}
    file_rows: List[dict] = []
    for path in paths:
        records = messages = 0
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{line_number}: not valid JSON ({exc.msg})") from exc
                if not isinstance(record, dict) or not record.get("source_id"):
                    continue
                records += 1
                source_id = str(record["source_id"])
                inventory = sources.setdefault(source_id, SourceInventory(source_id=source_id))
                inventory.files.add(str(path))
                inventory.domain = inventory.domain or domain_of(record)
                inventory.source_type = inventory.source_type or str(record.get("source_type") or "")
                for message in record.get("messages") or []:
                    if isinstance(message, dict):
                        inventory.add_message(message)
                        messages += 1
        file_rows.append({"file": str(path), "bytes": path.stat().st_size, "sources": records, "messages": messages})
    return sources, file_rows


def summarize(rows: Sequence[dict], file_rows: Sequence[dict]) -> dict:
    """Totals across all sources and files."""
    totals = {
        "files": len(file_rows),
        "file_bytes": sum(row["bytes"] for row in file_rows),
        "sources": len(rows),
        "domains": len({row["domain"] for row in rows if row["domain"]}),
        "occurrences": sum(row["occurrences"] for row in rows),
        "unique_texts": sum(row["unique_texts"] for row in rows),
        "unique_chars": sum(row["unique_chars"] for row in rows),
        "with_link": sum(row["with_link"] for row in rows),
    }
    totals.update({f"bucket_{label}": sum(row[f"bucket_{label}"] for row in rows) for label, _ in BUCKETS})
    return totals


def render_markdown(rows: Sequence[dict], totals: dict, *, top: int) -> str:
    bucket_labels = [label for label, _ in BUCKETS]
    lines = [
        "# Text inventory",
        "",
        f"- Files read: {totals['files']} ({totals['file_bytes'] / 1_000_000:.1f} MB on disk)",
        f"- Sources: {totals['sources']} ({totals['domains']} distinct publisher domains)",
        f"- Message occurrences: {totals['occurrences']:,}; unique texts: {totals['unique_texts']:,}"
        f" ({totals['unique_chars']:,} characters)",
        f"- Unique texts with a link to the original: {totals['with_link']:,}",
        "- Unique texts by length (characters): "
        + ", ".join(f"{label}: {totals[f'bucket_{label}']:,}" for label in bucket_labels),
        "",
        "Length buckets are descriptive, not legal thresholds.",
        "",
    ]
    shown = list(rows) if top <= 0 else list(rows)[:top]
    heading = "All sources" if top <= 0 or top >= len(rows) else f"Top {len(shown)} of {len(rows)} sources"
    lines += [
        f"## {heading}, by characters in unique texts",
        "",
        "| source_id | domain | unique texts | characters | median | max | " + " | ".join(bucket_labels) + " |",
        "|---|---|---:|---:|---:|---:|" + "---:|" * len(bucket_labels),
    ]
    for row in shown:
        cells = [
            str(row["source_id"]).replace("|", "\\|"),
            row["domain"],
            f"{row['unique_texts']:,}",
            f"{row['unique_chars']:,}",
            f"{row['median_chars']:,}",
            f"{row['max_chars']:,}",
        ] + [f"{row[f'bucket_{label}']:,}" for label in bucket_labels]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("patterns", nargs="*", help="JSONL files or globs (default: the repository's text-bearing set)")
    parser.add_argument("--csv", type=Path, help="write one row per source to this CSV file")
    parser.add_argument("--json", type=Path, help="write totals, per-file and per-source rows to this JSON file")
    parser.add_argument("--top", type=int, default=25, help="sources listed in the Markdown table (0 = all)")
    args = parser.parse_args(argv)

    paths = expand_patterns(args.patterns or DEFAULT_PATTERNS)
    if not paths:
        sys.stderr.write("No input files found.\n")
        return 1

    sources, file_rows = build_inventory(paths)
    rows = sorted((inv.row() for inv in sources.values()), key=lambda r: (-r["unique_chars"], r["source_id"]))
    totals = summarize(rows, file_rows)

    if args.csv:
        with args.csv.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
    if args.json:
        payload = {"totals": totals, "files": file_rows, "sources": rows}
        args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sys.stdout.write(render_markdown(rows, totals, top=args.top))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
