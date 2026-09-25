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

Timestamp sanity filter (opt-in)
--------------------------------
Some feeds mix old or mis-dated items into their "recent" window: evergreen
content, a literal ``1970-01-01`` parser default, a feed serving 2022-2024
archive items. Merged into a history, these create multi-year fake gaps that
distort ``silence`` and ``volatility`` (see
``docs/snapshot_history_audit_2026-09.md``). ``--not-before`` / ``--not-after``
keep only messages dated inside ``[not_before, not_after]`` (whole UTC days,
both inclusive). Once a bound is set, messages with an unparseable timestamp
are dropped as well.

* The filter is off by default, so a merge without the flags is byte-for-byte
  what it was. The shipped July calibration inputs stay reproducible.
* The bounds are explicit, never "today". A build must give the same output
  whenever it is re-run.
* A source the filter empties is left out of the output, because the temporal
  split cannot place a source that has no timestamp. It is always named in the
  report, never dropped silently.
* A source that loses more than half its messages is flagged for a feed-health
  check, since its feed is not surfacing current activity. It is kept.

The filter only touches the calibration dataset. Live scoring is unchanged.

Usage::

    python -m cats.calibration.merge_snapshots \\
        --inputs data/snapshots/*.jsonl --out data/labelled_sources.jsonl

    # with the sanity filter (the audit's data-driven floor; pick the ceiling
    # as the date of the newest snapshot in the build)
    python -m cats.calibration.merge_snapshots \\
        --inputs data/snapshots/*.jsonl --out data/labelled_sources.jsonl \\
        --not-before 2026-06-01 --not-after 2026-09-25

Then split/build as usual — with multi-snapshot histories the temporal split
regains meaning, because every source now spans the same collection window.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

import structlog

logger = structlog.get_logger()

# A source that loses more than this share of its messages to the timestamp
# filter is flagged: its feed is not surfacing current activity and needs a
# feed-health check (docs/feed_health_2026-07.md), not only a quiet trim.
HEAVY_LOSS_FRACTION = 0.5


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


@dataclass
class TimestampFilterReport:
    """What :func:`filter_by_timestamp` removed, and which sources it hit hard."""

    kept: int = 0
    dropped_before: int = 0
    dropped_after: int = 0
    dropped_unparseable: int = 0
    # (source_id, messages before, messages after) for sources that lost more
    # than HEAVY_LOSS_FRACTION but kept at least one message.
    heavy_loss: List[Tuple[str, int, int]] = field(default_factory=list)
    # (source_id, messages before) for sources left with none: excluded.
    emptied: List[Tuple[str, int]] = field(default_factory=list)

    @property
    def dropped(self) -> int:
        return self.dropped_before + self.dropped_after + self.dropped_unparseable


def _parse_timestamp(value: object) -> Optional[datetime]:
    """ISO-8601 → aware UTC datetime; ``None`` if missing or unparseable.

    A timestamp without an offset is read as UTC, so naive and aware values
    compare instead of raising ``TypeError``.
    """
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def filter_by_timestamp(
    records: Sequence[dict],
    not_before: Optional[date] = None,
    not_after: Optional[date] = None,
    heavy_loss_fraction: float = HEAVY_LOSS_FRACTION,
) -> Tuple[List[dict], TimestampFilterReport]:
    """Keep only messages dated within ``[not_before, not_after]`` (UTC days, inclusive).

    Either bound may be ``None`` (open on that side). With both ``None`` this is
    a no-op that returns the records unchanged. Otherwise a message whose
    timestamp is missing or unparseable is dropped too, because its position
    in time cannot be checked.

    A source the filter empties is excluded from the result and listed in
    ``report.emptied``. A source whose history was already empty is passed
    through untouched: the filter has nothing to say about it. Input records
    are not mutated.
    """
    report = TimestampFilterReport()
    if not_before is None and not_after is None:
        report.kept = sum(len(r.get("messages") or []) for r in records)
        return list(records), report
    if not_before is not None and not_after is not None and not_before > not_after:
        raise ValueError(f"not_before ({not_before}) is after not_after ({not_after})")

    floor = datetime.combine(not_before, time.min, tzinfo=timezone.utc) if not_before else None
    # Inclusive whole day: anything before the next UTC midnight is in range.
    ceiling = datetime.combine(not_after + timedelta(days=1), time.min, tzinfo=timezone.utc) if not_after else None

    out: List[dict] = []
    for record in records:
        messages = record.get("messages") or []
        if not messages:
            out.append(record)
            continue
        kept = []
        for message in messages:
            ts = _parse_timestamp(message.get("timestamp") if isinstance(message, dict) else None)
            if ts is None:
                report.dropped_unparseable += 1
            elif floor is not None and ts < floor:
                report.dropped_before += 1
            elif ceiling is not None and ts >= ceiling:
                report.dropped_after += 1
            else:
                kept.append(message)
        report.kept += len(kept)
        source_id = str(record.get("source_id"))
        if not kept:
            report.emptied.append((source_id, len(messages)))
            continue
        if (len(messages) - len(kept)) / len(messages) > heavy_loss_fraction:
            report.heavy_loss.append((source_id, len(messages), len(kept)))
        filtered = dict(record)
        filtered["messages"] = kept
        out.append(filtered)
    return out, report


def _parse_day(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected a date as YYYY-MM-DD, got {value!r}") from None


def _read_jsonl(path: Path) -> List[dict]:
    records = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def _print_filter_report(
    report: TimestampFilterReport,
    not_before: Optional[date],
    not_after: Optional[date],
    total_messages: int,
    sources_written: int,
) -> None:
    window = f"[{not_before or '-inf'}, {not_after or '+inf'}]"
    share = report.dropped / total_messages if total_messages else 0.0
    print(f"\nTimestamp filter {window}: dropped {report.dropped} message(s) ({share:.2%})")
    print(
        f"  {report.dropped_before} before the window, {report.dropped_after} after it, "
        f"{report.dropped_unparseable} with a missing/unparseable timestamp"
    )
    print(f"  wrote {sources_written} source(s), {report.kept} message(s)")
    if report.emptied:
        print(f"\n  {len(report.emptied)} source(s) had no message in range and were EXCLUDED:")
        for source_id, before in report.emptied:
            print(f"    {source_id}: {before} -> 0 messages")
    if report.heavy_loss:
        print(
            f"\n  {len(report.heavy_loss)} source(s) lost more than {HEAVY_LOSS_FRACTION:.0%} "
            "of their messages (kept; check feed health):"
        )
        for source_id, before, after in report.heavy_loss:
            print(f"    {source_id}: {before} -> {after} messages")


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
    parser.add_argument(
        "--not-before",
        type=_parse_day,
        default=None,
        metavar="YYYY-MM-DD",
        help="drop messages dated before this UTC day (sanity filter; off by default)",
    )
    parser.add_argument(
        "--not-after",
        type=_parse_day,
        default=None,
        metavar="YYYY-MM-DD",
        help="drop messages dated after this UTC day, e.g. the newest snapshot's date (off by default)",
    )
    args = parser.parse_args(argv)

    for path in args.inputs:
        if not path.exists():
            parser.error(f"snapshot not found: {path}")
    if args.not_before and args.not_after and args.not_before > args.not_after:
        parser.error(f"--not-before {args.not_before} is after --not-after {args.not_after}")

    snapshots = [_read_jsonl(path) for path in args.inputs]
    records, total_messages, duplicates = merge_records(snapshots)
    if not records:
        print("No records found in the given snapshots; nothing written.")
        return 1

    filtering = args.not_before is not None or args.not_after is not None
    merged_sources = len(records)
    records, report = filter_by_timestamp(records, args.not_before, args.not_after)
    if not records:
        print("The timestamp filter left no source with a message in range; nothing written.")
        return 1

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Merged {len(args.inputs)} snapshot(s) -> {merged_sources} source(s), {total_messages} message(s)")
    print(f"  {duplicates} duplicate message(s) skipped (feed overlap between runs)")
    if filtering:
        _print_filter_report(report, args.not_before, args.not_after, total_messages, len(records))
    print(
        "\nNext: temporal split, then build the dataset:\n"
        f"  python -m cats.calibration.split --input {args.out} --holdout-fraction 0.2"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
