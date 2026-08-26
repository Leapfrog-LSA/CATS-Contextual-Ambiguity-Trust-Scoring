"""Temporal train/holdout split for labelled sources.

Calibrating on the past and validating on the future prevents leakage and
surfaces drift — a random split would let a calibrator "see the future". The
split operates on **labelled sources** (the ``build_dataset`` input: records with
timestamped messages + a ``label``), because that is where the time information
lives; the post-build ``{source_type, signals, label}`` records carry none.

There are two ways to cut "past" from "future", and they behave very
differently on RSS data:

``message`` axis (**default**)
    Cut every source's *message history* at a shared cutoff: earlier messages
    train, later messages validate. A source appears on both sides with
    different behaviour, so the holdout keeps the label spread of the pool by
    construction. This answers "do weights fitted on past behaviour still
    predict labels from future behaviour" — drift over time.

``source`` axis (legacy)
    Order *sources* by their most recent message and hold out the newest slice,
    so holdout sources are unseen during calibration. This answers "do the
    weights generalise to sources never calibrated on".

The default is ``message`` because the ``source`` axis is **degenerate on this
dataset**, not as a matter of taste. Every live RSS feed's newest message is a
few hours old at collection time, so ordering sources by that timestamp ranks
them by *how often they publish* — which is close to a proxy for the label.
Measured on the 2026-07-20 snapshot: Spearman(recency, label) = **+0.539**, and
the resulting 11-source holdout was entirely labels 70/85, with every label-10
disinfo source exiled to train because such sources publish irregularly. A
holdout with no label spread cannot validate anything, which is what stopped the
2026-07-24 recalibration (``docs/calibration_findings_2026-07-24.md``).

The ``source`` axis is kept, not deleted: it is the right question to ask once
the pool is large enough that its newest slice is label-diverse on its own.

Both axes report the label distribution of each side, so a degenerate split is
visible at the point it is produced rather than three pipeline stages later.
For the same reason each side also reports its **observed window** against the
``silence`` threshold: a source whose history spans no more than the
threshold (96 h as of 2026-08-26, ``docs/silence_retune_2026-08.md``) cannot
contain a gap longer than it, so its silence is 0 because the window was cut
short, not because the source published steadily. Cutting a three-week
collection in two can put a large share of a side below that line, which is
invisible in the label spread and only surfaces as an inert signal during
calibration.

Usage::

    python -m cats.calibration.split --input sources.jsonl --holdout-fraction 0.2
    python -m cats.calibration.split --input sources.jsonl --cutoff 2026-01-01T00:00:00Z
    python -m cats.calibration.split --input sources.jsonl --axis source
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from cats.calibration.collect_rss import DEFAULT_MIN_MESSAGES
from cats.signals.silence import threshold_for

# Share of a side's sources that may be silence-blind before it is called out.
# A judgement call, not a derived constant: below it the signal still varies
# across enough sources to rank them, above it most of the distribution is
# structural zeros. The all-blind case is reported separately and is not a
# matter of degree — there the signal is constant.
SILENCE_BLIND_WARN_FRACTION = 0.25


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


def message_times(record: dict) -> List[datetime]:
    """Every parseable message timestamp in a record, ascending.

    Unlike :func:`record_time` this tolerates a record with none — the caller
    decides whether an untimed source is fatal or simply unsplittable.
    """
    times: List[datetime] = []
    for m in record.get("messages") or []:
        ts = m.get("timestamp") if isinstance(m, dict) else None
        if ts:
            try:
                times.append(_parse_ts(str(ts)))
            except ValueError:
                continue
    return sorted(times)


def message_quantile_cutoff(records: List[dict], holdout_fraction: float) -> datetime:
    """Timestamp with ``holdout_fraction`` of all messages at or after it.

    Pooled across sources, so the cutoff is a single moment in wall-clock time
    rather than a per-source one — the point is that both sides describe the
    same period for every source.
    """
    if not 0.0 < holdout_fraction < 1.0:
        raise ValueError("holdout_fraction must be between 0 and 1 (exclusive)")
    pooled: List[datetime] = []
    for r in records:
        pooled.extend(message_times(r))
    if not pooled:
        raise ValueError("no parseable message timestamps in any record")
    pooled.sort()
    idx = int(len(pooled) * (1.0 - holdout_fraction))
    idx = min(max(idx, 0), len(pooled) - 1)
    return pooled[idx]


def message_split(
    records: List[dict],
    holdout_fraction: float = 0.2,
    cutoff: Optional[datetime] = None,
    min_messages: int = DEFAULT_MIN_MESSAGES,
) -> Tuple[List[dict], List[dict]]:
    """Split each source's *messages* at a shared cutoff into (train, holdout).

    A source contributes to a side only if it has at least ``min_messages``
    there — below that the behavioural signals are not meaningfully estimable
    (the same floor ``collect_rss`` applies), so a thin side is dropped rather
    than passed on as noise. Messages whose timestamp will not parse cannot be
    placed in time and are dropped from both sides.
    """
    if not records:
        raise ValueError("no records to split")
    if cutoff is None:
        cutoff = message_quantile_cutoff(records, holdout_fraction)

    train: List[dict] = []
    holdout: List[dict] = []
    for r in records:
        before: List[dict] = []
        after: List[dict] = []
        for m in r.get("messages") or []:
            ts = m.get("timestamp") if isinstance(m, dict) else None
            if not ts:
                continue
            try:
                when = _parse_ts(str(ts))
            except ValueError:
                continue
            (after if when >= cutoff else before).append(m)
        if len(before) >= min_messages:
            train.append({**r, "messages": before})
        if len(after) >= min_messages:
            holdout.append({**r, "messages": after})
    return train, holdout


def record_span_hours(record: dict) -> Optional[float]:
    """Hours between a record's first and last parseable message, if it has two."""
    times = message_times(record)
    if len(times) < 2:
        return None
    return (times[-1] - times[0]).total_seconds() / 3600.0


def window_bounds(records: List[dict]) -> Optional[Tuple[datetime, datetime]]:
    """(earliest, latest) message timestamp across a side, or None if untimed."""
    pooled: List[datetime] = []
    for r in records:
        pooled.extend(message_times(r))
    if not pooled:
        return None
    return min(pooled), max(pooled)


def silence_blind_sources(records: List[dict]) -> Tuple[int, int]:
    """(blind, total) — sources whose window is too short for ``silence`` to fire.

    ``compute_silence`` scores the share of inter-message gaps longer than the
    source-type threshold (96 h for every type today). A source whose whole
    observed history spans no more than that threshold cannot contain such a
    gap, and one with fewer than two messages has no gaps at all: both score a
    flat 0. That zero is a property of the window the split handed them, not of
    how the source behaved, so counting them says how much of a side carries
    real silence information.
    """
    blind = 0
    for r in records:
        span = record_span_hours(r)
        if span is None or span <= threshold_for(str(r.get("source_type") or "default")):
            blind += 1
    return blind, len(records)


def label_spread(records: List[dict]) -> Dict[float, int]:
    """Label → count, for reporting whether a split side can validate at all."""
    counts: Dict[float, int] = {}
    for r in records:
        label = r.get("label")
        if label is None:
            continue
        counts[float(label)] = counts.get(float(label), 0) + 1
    return dict(sorted(counts.items()))


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


def _report_silence_window(side_name: str, records: List[dict]) -> None:
    """Print a side's observed window and how much of it ``silence`` can see."""
    if not records:
        return
    threshold = threshold_for("default")
    bounds = window_bounds(records)
    if bounds is not None:
        span_h = (bounds[1] - bounds[0]).total_seconds() / 3600.0
        print(f"  {side_name} window: {bounds[0].isoformat()} -> {bounds[1].isoformat()} ({span_h:.0f} h)")

    blind, total = silence_blind_sources(records)
    print(f"  {side_name} silence-blind: {blind}/{total} source(s) span <= the {threshold:.0f} h threshold")
    if not total:
        return
    if blind == total:
        print(
            f"WARNING: no {side_name} source spans more than the {threshold:.0f} h silence threshold, so "
            "silence is identically 0 on this side. It is constant, cannot rank anything, and any weight "
            "on it is unvalidated — the fix is a longer collection window, not a different split fraction."
        )
    elif blind / total >= SILENCE_BLIND_WARN_FRACTION:
        print(
            f"WARNING: {blind}/{total} {side_name} sources ({blind / total:.0%}) span <= the "
            f"{threshold:.0f} h silence threshold, so their silence is 0 by construction rather than by "
            "behaviour. The signal is compressed toward 0 here and comparisons that lean on it are weak."
        )


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
    parser.add_argument(
        "--axis",
        choices=("message", "source"),
        default="message",
        help="split each source's messages at a shared cutoff (default), or hold out whole unseen sources",
    )
    parser.add_argument(
        "--min-messages",
        type=int,
        default=DEFAULT_MIN_MESSAGES,
        help=f"message axis: drop a side with fewer messages than this (def {DEFAULT_MIN_MESSAGES})",
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
        if args.axis == "message":
            train, holdout = message_split(
                records,
                holdout_fraction=args.holdout_fraction,
                cutoff=cutoff,
                min_messages=args.min_messages,
            )
        else:
            train, holdout = temporal_split(records, holdout_fraction=args.holdout_fraction, cutoff=cutoff)
    except ValueError as exc:
        parser.error(str(exc))

    _write_jsonl(train, args.train_out)
    _write_jsonl(holdout, args.holdout_out)
    print(
        f"Split {len(records)} record(s) on the {args.axis} axis: {len(train)} train -> {args.train_out}, "
        f"{len(holdout)} holdout -> {args.holdout_out}"
    )

    train_spread, holdout_spread = label_spread(train), label_spread(holdout)
    print(f"  train labels:   {train_spread}")
    print(f"  holdout labels: {holdout_spread}")
    if not holdout or not train:
        print("WARNING: one side is empty; adjust --cutoff/--holdout-fraction for a usable split.")
    elif len(holdout_spread) < 3:
        print(
            f"WARNING: the holdout carries only {len(holdout_spread)} distinct label(s) — it cannot rank "
            "sources it never varies over, so validation on it is not meaningful. Widen the pool, or "
            "check whether the axis is selecting on something correlated with the label."
        )

    _report_silence_window("train", train)
    _report_silence_window("holdout", holdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
