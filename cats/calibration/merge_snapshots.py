"""Merge labelled-source snapshots into cumulative message histories.

An RSS feed only exposes the *recent* window of a source's activity (typically
10-50 entries), so a single :mod:`cats.calibration.collect_rss` run yields
short histories — too short for silence/volatility to mean much, and too
synchronous for a temporal split to separate slow-publishing sources from
fast ones. The remedy is to run the collector periodically and **merge** the
snapshots: this module unions the messages of each source across any number of
labelled-source files, so histories grow with every run.

Merge semantics
---------------
* Records are keyed by ``source_id``; inputs are processed in the order given.
* ``messages`` are unioned and deduplicated on ``(timestamp, text)`` — feeds
  overlap between runs by design — then sorted by timestamp ascending.
* For every other field (``label``, ``source_type``, ``url``, ``rss``, …) the
  **last** input wins, so relabelled or re-typed sources take the newest
  metadata. A label change is logged: it usually means the ratings file was
  updated between snapshots.
* Sources present in only some snapshots are kept (dead feeds stop
  contributing new messages but their history remains usable).

Usage::

    python -m cats.calibration.merge_snapshots \\
        --inputs data/snapshots/*.jsonl --out data/labelled_sources.jsonl

Then split/build as usual — with multi-snapshot histories the temporal split
regains meaning, because every source now spans the same collection window.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import structlog

logger = structlog.get_logger()


def merge_records(snapshots: Sequence[List[dict]]) -> Tuple[List[dict], int, int]:
    """Merge labelled-source snapshots; returns (records, total_msgs, dupes).

    ``snapshots`` is ordered oldest → newest; the newest occurrence of a source
    supplies its metadata, while messages accumulate across all of them.
    """
    merged: Dict[str, dict] = {}
    seen: Dict[str, set] = {}
    duplicates = 0

    for snapshot in snapshots:
        for record in snapshot:
            source_id = str(record.get("source_id") or "")
            if not source_id:
                logger.warning("merge_record_missing_source_id")
                continue
            messages = [m for m in record.get("messages") or [] if isinstance(m, dict)]
            if source_id not in merged:
                merged[source_id] = {k: v for k, v in record.items() if k != "messages"}
                merged[source_id]["messages"] = []
                seen[source_id] = set()
            else:
                previous = merged[source_id]
                if "label" in record and record.get("label") != previous.get("label"):
                    logger.info(
                        "merge_label_updated",
                        source=source_id,
                        old=previous.get("label"),
                        new=record.get("label"),
                    )
                for key, value in record.items():
                    if key != "messages":
                        previous[key] = value
            for message in messages:
                key = (str(message.get("timestamp")), str(message.get("text")))
                if key in seen[source_id]:
                    duplicates += 1
                    continue
                seen[source_id].add(key)
                merged[source_id]["messages"].append(message)

    records = []
    total_messages = 0
    for record in merged.values():
        record["messages"].sort(key=lambda m: str(m.get("timestamp")))
        total_messages += len(record["messages"])
        records.append(record)
    return records, total_messages, duplicates


def _read_jsonl(path: Path) -> List[dict]:
    records = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m cats.calibration.merge_snapshots",
        description="Merge labelled-source snapshots into cumulative message histories.",
    )
    parser.add_argument(
        "--inputs",
        type=Path,
        nargs="+",
        required=True,
        help="snapshot .jsonl files, oldest first (newest metadata wins)",
    )
    parser.add_argument("--out", type=Path, required=True, help="merged labelled sources (.jsonl)")
    args = parser.parse_args(argv)

    for path in args.inputs:
        if not path.exists():
            parser.error(f"snapshot not found: {path}")

    snapshots = [_read_jsonl(path) for path in args.inputs]
    records, total_messages, duplicates = merge_records(snapshots)
    if not records:
        print("No records found in the given snapshots; nothing written.")
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Merged {len(args.inputs)} snapshot(s) -> {len(records)} source(s), {total_messages} message(s)")
    print(f"  {duplicates} duplicate message(s) skipped (feed overlap between runs)")
    print(
        "\nNext: temporal split, then build the dataset:\n"
        f"  python -m cats.calibration.split --input {args.out} --holdout-fraction 0.2"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
