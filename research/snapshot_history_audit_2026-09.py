"""Research spike (13 Sep 2026): does the full accumulated snapshot pool
(2026-07-02 through today) already meet the Fase B roadmap bar ("holdout
futuro >= 100 sorgenti con storia multi-mese")? And is that pool actually
trustworthy as collected?

Motivation: 50 daily/weekly snapshots have piled up as separate files under
data/snapshots/. Nobody had yet run `cats.calibration.merge_snapshots` across
the FULL accumulated set (only ever done for same-day collision pairs) to see
the real per-source message depth and calendar span. Doing that here surfaced
a genuine data-quality problem: some sources' RSS feeds intersperse
old/mis-dated items (evergreen content, or outright parser bugs -- a literal
1970-01-01 epoch default on CNET) into their "recent" window. Left in, these
create multi-year fake gaps in an otherwise-continuous timeline -- exactly
the kind of corruption that would poison `silence`/`volatility`'s temporal-gap
math on any future recalibration built from this pool.

Method: merge every committed snapshot (`data/snapshots/*.jsonl`) via the
production `cats.calibration.merge_snapshots` code (not a reimplementation,
so the real dedup-on-(timestamp,text) semantics apply), then look at the
actual per-source message-count and calendar-span distribution before and
after a timestamp sanity filter. The filter's cutoff (2026-06-01) is
data-driven, not a guess: a monthly histogram of all 107 976 deduplicated
messages shows a sharp, unambiguous break -- January-May 2026 combined
contribute only 109 messages across all 109 sources (obvious trace-level
noise), June 2026 jumps to 458 (consistent with a normal RSS window
surfacing a few weeks-old items on first fetch, since real daily collection
only started 2026-07-02), and July onward is 106 864. There is no smooth
curve to pick a threshold from -- the break IS the signal.

Run from the repo root:  python research/snapshot_history_audit_2026-09.py
Reads only committed data (data/snapshots/*.jsonl). No NLP model assets
needed. Writes its cleaned output to data/snapshots_merged_clean_2026-09.jsonl
(a NEW, clearly-dated artifact -- this script never touches the production
data/labelled_sources.jsonl or the shipped train/holdout split, which remain
the July 56/53-source calibration inputs until a full Fase D recalibration
cycle is explicitly run and validated).
"""

from __future__ import annotations

import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# Inert placeholders so cats.core.config imports outside the API deployment.
os.environ.setdefault("CATS_API_KEY", "spike-unused")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost:1/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:1/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTAwMzI=")

from cats.calibration.merge_snapshots import _read_jsonl, merge_records  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SNAP_DIR = ROOT / "data" / "snapshots"
OUT_PATH = ROOT / "data" / "snapshots_merged_clean_2026-09.jsonl"

# Data-driven, not a guess -- see module docstring for the monthly-histogram
# break that motivates this specific date.
SANITY_FLOOR = datetime(2026, 6, 1, tzinfo=timezone.utc)
# The collector never runs from the future; anything after "now" is a bug.
SANITY_CEILING = datetime(2026, 9, 13, 23, 59, 59, tzinfo=timezone.utc)

# A source loses more than this fraction of its messages to the filter -> its
# feed is not actually surfacing current activity and needs separate
# feed-health attention (docs/feed_health_2026-07.md precedent), not just a
# quiet drop.
FEED_HEALTH_LOSS_THRESHOLD = 0.5


def _parse(ts: str) -> datetime | None:
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


def _span_days(messages: list[dict]) -> int | None:
    times = sorted(_parse(m["timestamp"]) for m in messages if m.get("timestamp"))
    times = [t for t in times if t is not None]
    if len(times) < 2:
        return None
    return (times[-1] - times[0]).days


def _percentile(sorted_vals: list[int], p: float) -> int:
    if not sorted_vals:
        return 0
    idx = min(len(sorted_vals) - 1, int(len(sorted_vals) * p))
    return sorted_vals[idx]


def main() -> None:
    files = sorted(SNAP_DIR.glob("labelled_sources_*.jsonl"))
    print(f"Merging {len(files)} snapshot file(s) from {SNAP_DIR}\n")

    records, total_messages, duplicates = merge_records([_read_jsonl(p) for p in files])
    print(f"Merged -> {len(records)} source(s), {total_messages} message(s), {duplicates} duplicate(s) skipped\n")

    print("=== Monthly histogram, all messages (the data-driven cutoff evidence) ===")
    months: Counter = Counter()
    future = 0
    for r in records:
        for m in r.get("messages") or []:
            dt = _parse(m.get("timestamp", ""))
            if dt is None:
                continue
            if dt > SANITY_CEILING:
                future += 1
            key = f"{dt.year}-{dt.month:02d}" if dt.year >= 2026 else f"<{dt.year}"
            months[key] += 1
    for k in sorted(months, key=lambda x: (x.startswith("<"), x)):
        print(f"  {k:>8s}: {months[k]}")
    print(f"  future-dated (after {SANITY_CEILING.date()}): {future}")

    print(f"\n=== Before filter: per-source message count / calendar span (n={len(records)}) ===")
    counts_before = sorted(len(r.get("messages") or []) for r in records)
    spans_before = sorted(s for s in (_span_days(r.get("messages") or []) for r in records) if s is not None)
    print(
        f"  messages/source: min={counts_before[0]} p25={_percentile(counts_before, .25)} "
        f"median={_percentile(counts_before, .5)} p75={_percentile(counts_before, .75)} max={counts_before[-1]}"
    )
    print(
        f"  span days/source: min={spans_before[0]} p25={_percentile(spans_before, .25)} "
        f"median={_percentile(spans_before, .5)} p75={_percentile(spans_before, .75)} max={spans_before[-1]}"
    )

    print(f"\n=== Applying sanity filter: drop messages outside [{SANITY_FLOOR.date()}, {SANITY_CEILING.date()}] ===")
    cleaned = []
    total_dropped = 0
    feed_health_flags = []
    for r in records:
        msgs = r.get("messages") or []
        kept = [m for m in msgs if (dt := _parse(m.get("timestamp", ""))) and SANITY_FLOOR <= dt <= SANITY_CEILING]
        dropped = len(msgs) - len(kept)
        total_dropped += dropped
        if msgs and dropped / len(msgs) > FEED_HEALTH_LOSS_THRESHOLD:
            feed_health_flags.append((r["source_id"], len(msgs), dropped, len(kept)))
        new_r = dict(r)
        new_r["messages"] = kept
        cleaned.append(new_r)

    print(f"  dropped {total_dropped} message(s) ({total_dropped / total_messages:.2%} of the merged total)")

    print(f"\n=== Feed-health flags: sources losing >{FEED_HEALTH_LOSS_THRESHOLD:.0%} of messages to the filter ===")
    if not feed_health_flags:
        print("  none")
    for source_id, before, dropped, after in feed_health_flags:
        print(f"  {source_id}: {before} -> {after} messages ({dropped/before:.1%} dropped)")

    print(f"\n=== After filter: per-source message count / calendar span (n={len(cleaned)}) ===")
    counts_after = sorted(len(r.get("messages") or []) for r in cleaned)
    spans_after = sorted(s for s in (_span_days(r.get("messages") or []) for r in cleaned) if s is not None)
    print(
        f"  messages/source: min={counts_after[0]} p25={_percentile(counts_after, .25)} "
        f"median={_percentile(counts_after, .5)} p75={_percentile(counts_after, .75)} max={counts_after[-1]}"
    )
    print(
        f"  span days/source: min={spans_after[0]} p25={_percentile(spans_after, .25)} "
        f"median={_percentile(spans_after, .5)} p75={_percentile(spans_after, .75)} max={spans_after[-1]}"
    )
    over_60 = sum(1 for s in spans_after if s >= 60)
    print(f"  sources with span >= 60 days: {over_60}/{len(spans_after)}")

    with OUT_PATH.open("w", encoding="utf-8") as handle:
        for r in cleaned:
            handle.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\nWrote cleaned merged history -> {OUT_PATH}")
    print(
        "\nThis is a DERIVED, dated artifact for future Fase D preparation -- it does\n"
        "NOT replace data/labelled_sources.jsonl or the shipped train/holdout split.\n"
        "See docs/snapshot_history_audit_2026-09.md for the full write-up."
    )


if __name__ == "__main__":
    main()
