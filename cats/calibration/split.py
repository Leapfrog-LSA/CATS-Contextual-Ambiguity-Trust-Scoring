"""Temporal train/holdout split for labelled sources.

Calibrating on the past and validating on the future prevents leakage and
surfaces drift — a random split would let a calibrator "see the future". The
split operates on **labelled sources** (the ``build_dataset`` input: records with
timestamped messages + a ``label``), because that is where the time information
lives; the post-build ``{source_type, signals, label}`` records carry none.

Each record's time is its **most recent message** (latest activity). Records are
ordered by that time and the holdout is the most-recent slice — either a fraction
(``--holdout-fraction``) or everything at/after an explicit ``--cutoff``.

Usage::

    python -m cats.calibration.split --input sources.jsonl --holdout-fraction 0.2
    python -m cats.calibration.split --input sources.jsonl --cutoff 2026-01-01T00:00:00Z
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple


def _parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def record_time(record: dict) -> datetime:
    """Most recent message timestamp in a labelled-source record.

    Raises ``ValueError`` if the record has no message with a parseable
    ISO-8601 timestamp — temporal correctness must not silently degrade.
    """
    times: List[datetime] = []
    for m in record.get("messages") or []:
        ts = m.get("timestamp") if isinstance(m, dict) else None
        if ts:
            try:
                times.append(_parse_ts(str(ts)))
            except ValueError:
                continue
    if not times:
        raise ValueError(f"record {record.get('source_id', '?')!r} has no parseable message timestamp")
    return max(times)


def temporal_split(
    records: List[dict],
    holdout_fraction: float = 0.2,
    cutoff: Optional[datetime] = None,
) -> Tuple[List[dict], List[dict]]:
    """Split records into (train, holdout) by recency.

    With ``cutoff``, records whose latest message is at/after it form the
    holdout. Otherwise the most-recent ``holdout_fraction`` of records do.
    """
    if not records:
        raise ValueError("no records to split")
    timed = sorted(records, key=record_time)  # ascending: oldest first

    if cutoff is not None:
        train = [r for r in timed if record_time(r) < cutoff]
        holdout = [r for r in timed if record_time(r) >= cutoff]
        return train, holdout

    if not 0.0 < holdout_fraction < 1.0:
        raise ValueError("holdout_fraction must be between 0 and 1 (exclusive)")
    n_holdout = max(1, round(len(timed) * holdout_fraction))
    n_holdout = min(n_holdout, len(timed) - 1)  # always leave at least one for train
    split_at = len(timed) - n_holdout
    return timed[:split_at], timed[split_at:]


def _read_records(path: Path) -> List[dict]:
    raw = path.read_text(encoding="utf-8").strip()
    if not raw:
        return []
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in raw.splitlines() if line.strip()]
    data = json.loads(raw)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("sources"), list):
        return data["sources"]
    raise ValueError("JSON input must be a list or an object with a 'sources' list")


def _write_jsonl(records: List[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m cats.calibration.split",
        description="Temporal train/holdout split of labelled sources (calibrate on the past, validate on the future).",
    )
    parser.add_argument("--input", required=True, type=Path, help="labelled sources (.jsonl/.json)")
    parser.add_argument(
        "--train-out", type=Path, default=Path("train.jsonl"), help="train output (default train.jsonl)"
    )
    parser.add_argument(
        "--holdout-out", type=Path, default=Path("holdout.jsonl"), help="holdout output (default holdout.jsonl)"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--holdout-fraction", type=float, default=0.2, help="most-recent fraction for holdout (def 0.2)")
    group.add_argument(
        "--cutoff", type=str, default=None, help="ISO-8601; records at/after the cutoff form the holdout"
    )
    args = parser.parse_args(argv)

    if not args.input.exists():
        parser.error(f"input file not found: {args.input}")
    cutoff = None
    if args.cutoff:
        try:
            cutoff = _parse_ts(args.cutoff)
        except ValueError:
            parser.error(f"invalid --cutoff (expected ISO-8601): {args.cutoff}")

    records = _read_records(args.input)
    try:
        train, holdout = temporal_split(records, holdout_fraction=args.holdout_fraction, cutoff=cutoff)
    except ValueError as exc:
        parser.error(str(exc))

    _write_jsonl(train, args.train_out)
    _write_jsonl(holdout, args.holdout_out)
    print(
        f"Split {len(records)} record(s): {len(train)} train -> {args.train_out}, "
        f"{len(holdout)} holdout -> {args.holdout_out}"
    )
    if not holdout or not train:
        print("WARNING: one side is empty; adjust --cutoff/--holdout-fraction for a usable split.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
