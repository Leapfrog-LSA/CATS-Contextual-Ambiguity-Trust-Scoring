# Snapshot history audit — 13 September 2026

Prompted by a simple question during the daily check-in: after ~50 snapshots
accumulated since 2026-07-02, are we close to Fase B's exit bar ("holdout
futuro ≥ 100 sorgenti con storia multi-mese")? Nobody had actually merged the
full accumulated pool to check — `merge_snapshots` has only ever been run on
same-day collision pairs. Doing that here (reproducible via
[`research/snapshot_history_audit_2026-09.py`](../research/snapshot_history_audit_2026-09.py))
answers the question, and surfaces a real data-quality problem along the way.

## Method

Merged all 50 committed `data/snapshots/*.jsonl` files with the production
`cats.calibration.merge_snapshots` code (real dedup-on-`(timestamp, text)`
semantics, not a reimplementation), then looked at the actual per-source
message-count and calendar-span distribution.

## Finding 1 — raw numbers look like a pass

50 snapshots → **109 distinct sources**, **107 976** deduplicated messages
(172 067 raw, 64 091 duplicates from RSS-window overlap between runs — as
designed). Before any cleanup: median 72 days of calendar span per source,
71/109 sources (65%) span ≥60 days. On paper, ≥100 sources with multi-month
history — Fase B's bar, met.

## Finding 2 — some feeds interleave old/mis-dated content into their "recent" window

A monthly histogram of every deduplicated message's timestamp shows a sharp,
unambiguous break:

| period | messages |
|---|--:|
| all years < 2026 | 545 |
| 2026-01 | 5 |
| 2026-02 | 7 |
| 2026-03 | 15 |
| 2026-04 | 28 |
| 2026-05 | 54 |
| 2026-06 | 458 |
| 2026-07 | 14 565 |
| 2026-08 | 63 518 |
| 2026-09 (partial) | 28 781 |

January–May 2026 combined contribute 109 messages across all 109 sources —
trace-level noise, not real recent activity. June 2026 (458) is consistent
with a normal RSS window surfacing a few-weeks-old items on first fetch,
since real daily collection only started 2026-07-02. Everything before June
is a different population: individually implausible dates including a
literal `1970-01-01` epoch-default on CNET (a parser bug), a `1994-07-10`
item on LA Times, a `2001-01-01` item on Il Giornale, and — the worst case —
**Il Corriere della Sera**, where 86 of its 88 collected messages (97.7%)
date from 2022–2024 and only 2 are genuinely from 2026. That source's feed
is not surfacing current activity at all; it has been serving stale/archival
content this entire collection window.

Left uncleaned, these create multi-year fake gaps in an otherwise-continuous
per-source timeline — exactly the corruption that would poison
`silence`/`volatility`'s temporal-gap math in any future recalibration built
from this pool.

## Finding 3 — a data-driven sanity filter, and what it costs

Filter: drop any message outside `[2026-06-01, 2026-09-13]` (the floor is the
break identified above; the ceiling rules out 1 single future-dated message,
also a bug). This drops 655 of 107 976 messages (0.61%) — small and
targeted.

But 10 sources lose the great majority of their history to this filter,
because their entire recent-looking collected content turns out to be stale:

| source | before | after | dropped |
|---|--:|--:|--:|
| Corriere del Corsaro | 10 | 0 | 100% |
| Il Corrispondente | 25 | 0 | 100% |
| Strafatti Quotidiani | 10 | 0 | 100% |
| Daily Buzz Live | 5 | 0 | 100% |
| Empire News | 10 | 0 | 100% |
| Empire Sports News | 4 | 0 | 100% |
| World Daily News Report | 6 | 0 | 100% |
| Veterans Today | 10 | 0 | 100% |
| Diretta News.it | 52 | 3 | 94.2% |
| Il Corriere della Sera | 88 | 2 | 97.7% |

All eight 100%-loss sources are known low-reliability/disinfo-labelled
sources already familiar from this week's domain-provenance work (several
are the exact free-hosting clone sites `notiziepericolose.blogspot.com` /
`strafattiquotidiani.wordpress.com` and siblings caught earlier). This reads
as a real, separate finding, not a filter artifact: these sources' RSS feeds
are effectively dormant — everything they've "shown" as recent this whole
window is recycled old content, not genuine fresh activity. That is itself
informative behaviour (worth a future look, e.g. whether `silence` already
catches it or needs a "feed never actually updates" case), but it means
there is currently no fresh 2026 message history to score them on at all —
they cannot contribute to a new calibration or holdout until their feeds
(if still monitored) start actually publishing, or they get pruned from the
registry.

## Where this leaves Fase B

After the sanity filter **and** excluding sources with fewer than 10
remaining usable messages (the two near-zero cases above included): **99
sources** with genuinely current, clean 2026 history — one short of the
"≥100 sources" bar, not comfortably past it. Median clean span per source:
71 days (~2.3 months); 60/101 sources with any valid span still reach ≥60
days. So: closer to "multi-month" than not, but not yet a comfortable margin
on either the source-count or the depth criterion, and the raw 109-source
count that looked like a pass was flattered by 10 sources whose real
contribution is zero.

## Output

[`research/snapshot_history_audit_2026-09.py`](../research/snapshot_history_audit_2026-09.py)
reproduces all of the above and writes the cleaned, deduplicated merge to
`data/snapshots_merged_clean_2026-09.jsonl` — **not committed** (≈83MB of
full message bodies, gitignored; regenerate on demand by re-running the
script against the then-current `data/snapshots/`). This file is a DERIVED,
dated preparation artifact for a future Fase D recalibration attempt — it
does **not** replace `data/labelled_sources.jsonl` or the shipped
July 56/53-source train/holdout split, which remain the production
calibration inputs. Building a new dataset/calibration from this pool is a
separate, larger decision (the full spike → calibrate → future-holdout
re-validate cycle CLAUDE.md requires) that has not been done here.

## Recommendation

1. **Do not yet treat Fase B as satisfied.** 99 usable sources is one short
   of the stated bar, and collection needs to keep running — the daily
   check-in already does this, no change needed there.
2. **Apply this same sanity floor going forward** when any future session
   does build a new calibration dataset from the accumulated snapshots —
   don't let this one-off audit be the only place this check happens.
   Worth considering (not done here, a separate decision): should
   `collect_rss` or `merge_snapshots` itself warn on messages outside a
   plausible recency window, so this doesn't require a manual audit next
   time?
3. **The 8 fully-dead sources are worth a human/roadmap decision**, not a
   silent drop: either their feeds get re-verified (same style as
   `docs/feed_health_2026-07.md`), or they're flagged as structurally
   dormant and excluded from future dataset builds until proven otherwise.
