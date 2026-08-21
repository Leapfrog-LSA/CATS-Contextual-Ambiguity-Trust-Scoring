# Recalibration checkpoint — 2026-08-21

Checkpoint requested to answer one question: since 2026-07-25, daily snapshot
collection has grown the merged pool from 59 to 95 sources spanning ~7 weeks
instead of ~3. Does more calendar time alone — same weights, same split
methodology, nothing recalibrated — improve the validated picture?

**Disposition: no weights touched.** `data/calibrated_weights.json` and the
committed train/holdout files are unchanged. This is a checkpoint, not a
recalibration decision.

## Pipeline

Exact sequence from `docs/calibration_findings_2026-07-25.md`, `COHERENCE_BACKEND=sbert`
confirmed active on both builds:

```bash
python -m cats.calibration.merge_snapshots --inputs data/snapshots/*.jsonl --out merged.jsonl
python -m cats.calibration.split --input merged.jsonl              # message axis, default fraction 0.2
python -m cats.calibration.build_dataset --input {train,holdout}_sources.jsonl --out {train,holdout}.jsonl
python -m cats.calibration.evaluate --dataset holdout.jsonl [--weights data/calibrated_weights.json]
```

95 sources / 54 321 messages merged from all snapshots to date. Message-axis
split: 95 train-side / 75 holdout-side source-slices, both label-diverse
(train: {10:13, 30:4, 50:17, 70:22, 85:37, 95:2}; holdout: {10:3, 30:4, 50:15,
70:18, 85:34, 95:1}).

## Result — same sign, smaller edge

| Metric (holdout, message axis, fraction 0.2) | 07-25 (n=45, 59 src) | **08-21 (n=75, 95 src)** |
|---|---:|---:|
| Static WP 4.1 — Spearman | +0.043 | +0.033 |
| Static WP 4.1 — concordance | 0.515 | 0.515 |
| Static WP 4.1 — band agreement (exact / within-1) | — | 17.3% / 66.7% |
| **Production (shipped) — Spearman** | **+0.127** | **+0.078** |
| **Production (shipped) — concordance** | **0.563** | **0.537** |
| **Production (shipped) — band agreement (exact / within-1)** | 33.3% / — | 24.0% / 89.3% |

The shipped weights still beat the static baseline — the qualitative finding
from 07-25 replicates, on nearly double the sources and more than twice the
calendar span. But the *edge* is smaller on every axis (Spearman +0.078 vs
+0.127, concordance 0.537 vs 0.563, exact band agreement 24.0% vs 33.3%), not
larger. More calendar time alone did not sharpen the validated picture; if
anything it diluted it slightly. Three candidate explanations, not
distinguished by this run (see *Zombie feeds*, below, for one of them):

1. Larger, more diverse pools are intrinsically harder to rank — the 07-25
   holdout was smaller and may have had an easier label distribution by
   chance.
2. The new snapshots add sources whose signals are less separable (more
   mid-range labels: 50/70 now dominate more of both sides than in 07-25).
3. A meaningful slice of the added history is not "more recent behaviour" at
   all but old, low-information backlog re-surfacing through feed merges (see
   below) — noise added at the same rate as signal.

**A second, separate concern**: predicted-band diversity collapsed for the
shipped weights — 74 of 75 holdout sources land in `medium_high`, only 1 in
`medium`. The static baseline spans two bands more evenly (49 `medium` / 26
`medium_high`). High within-1 agreement (89.3%) is partly an artifact of this:
almost everything is called the same band, so almost nothing can be more than
one band off. This is worth tracking in future checkpoints — a scorer that
stops discriminating between medium and medium-high on real data is a
different failure mode than one that ranks in the wrong order.

For context, neither number here is directly comparable to the production
weights' *shipped* validation in `docs/calibration_findings_2026-07-28.md`
(concordance 0.755, Spearman +0.553, single held-out future snapshot,
n=53) — that used a different protocol (one whole snapshot never trained on,
not a pooled message-axis cut) on an earlier, smaller pool. The two protocols
answer related but different questions and should not be read as a
regression from 0.755 to 0.537; they were never the same measurement.

## Two timestamp bugs, found while explaining an anomalous split window

The split step reported implausible window bounds:

```
train window:   1970-01-01T05:00:00+00:00 -> 2026-08-14T14:48:03+00:00 (496306 h)
holdout window: 2026-08-14T14:48:11+00:00 -> 2026-09-04T23:00:00+00:00 (512 h)
```

Both ends are wrong, and both trace to single bad messages, not to a
systematic clock or timezone bug:

- **Epoch sentinel (train side).** Two CNET messages carry the identical
  timestamp `1970-01-01T05:00:00Z`. This is a classic missing/failed-parse
  sentinel, not a real publish date — almost certainly `collect_rss` (or the
  upstream feed parser) defaulting a message with no usable `<pubDate>` to
  `datetime.fromtimestamp(0)` instead of dropping it. Worth a fix:
  `collect_rss` should drop a message it cannot date rather than stamp it at
  the epoch, the same way `cats/calibration/split.py` already drops messages
  whose timestamp won't parse at all.
- **Future embargo date (holdout side).** One `La Repubblica` message
  ("Caldo, domani il picco record…") is stamped `2026-09-04T23:00:00Z`, two
  weeks past the actual collection date — and its own URL contains
  `/2026/09/05/...`. This is the source's own CMS pre-scheduling artifact
  (a weather-forecast piece slotted into the RSS feed under a future
  publish date), not a parsing bug on our side.

**Practical impact is small but real.** `split.py`'s `window_bounds()` takes a
plain pooled min/max, so either single record fully determines the printed
window — that diagnostic line is unreliable whenever any one message in 54 321
has a bad timestamp, which is why it read almost 57 years wide. The actual
split point is unaffected (`message_quantile_cutoff` uses a rank position, and
2–3 outliers among 54 321 pooled messages cannot move an 80th-percentile index
by more than a few slots). The two carrier sources (CNET, `La Repubblica`,
both label 85) do carry a spurious multi-year/multi-week "gap" in their own
message history, which `silence` scores from inter-message gaps — that gap
will register as far past the 72 h threshold and likely pushes each source's
own `silence` value toward the maximum for a reason that has nothing to do
with how they actually publish. That is at most a 2-of-95-row effect on this
run's aggregate numbers, not something that would flip the table above, but
it is worth fixing rather than accumulating: `merge_snapshots` or
`build_dataset` could reject/flag a message timestamped before some floor
(e.g. 2020) or more than ~48 h ahead of collection time, so one bad record
can't silently distort a source's own signal history the way this one does
today.

## The bigger finding: audit-`ok` is not the same as *live*

Cross-checking every source's most recent (non-outlier) message age against
today turned up a pattern the feed-health audit (`docs/feed_health_2026-07.md`)
cannot see, because it only checks that a feed *answers* (HTTP 200 + XML
shape), never whether its content is *current*:

**15 of the 95 merged sources (16%) have not contributed a single new message
in 30+ days**, several not in years:

| Days stale | Label | Source | Last message | Messages held |
|---:|---:|---|---|---:|
| 3524 | 10 | Strafatti Quotidiani | 2016-12-27 | 10 |
| 2265 | 10 | World Daily News Report | 2020-06-08 | 6 |
| 1365 | 10 | Corriere del Corsaro | 2022-11-24 | 10 |
| 1004 | 10 | Daily Buzz Live | 2023-11-20 | 5 |
| 858 | 10 | Empire Sports News | 2024-04-14 | 4 |
| 830 | **85** | **Il Corriere della Sera** | 2024-05-13 | 69 |
| 797 | 10 | Il Corrispondente | 2024-06-15 | 25 |
| 760 | 10 | Veterans Today | 2024-07-21 | 10 |
| 758 | 10 | Empire News | 2024-07-24 | 10 |
| 430 | 70 | Jerusalem Post | 2025-06-16 | 30 |
| 413 | 50 | The National UAE | 2025-07-04 | 172 |
| 40 | 50 | Arab News | 2026-07-12 | 40 |
| 39 | 70 | Times of Israel | 2026-07-13 | 42 |
| 32 | 70 | Ukrainska Pravda English | 2026-07-20 | 40 |
| 32 | 70 | Ukrainska Pravda | 2026-07-20 | 40 |

Two things stand out:

1. **`Il Corriere della Sera` is stale again.** This is the exact source
   named in `research/feed_health_audit.py`'s own docstring as the reason the
   script exists — "never collected for months because its registered feed
   404s — found by chance." It is presumably no longer 404ing (it has 69
   collected messages, and it did not appear in the round-11 audit's `dead`
   list), but it has not produced a new item since 2024-05-13. A feed can move
   from *dead* to *reachable-but-frozen* and the audit's `ok`/`dead`/`blocked`/
   `not-xml` classes have no way to tell the difference — both look identical
   from the outside (200, valid XML), and only content age exposes it.
2. **8 of the 15 are label-10 disinformation sources** — already the scarcest,
   most valuable class for calibration (the low tail). A disinfo source truly
   going dark is itself meaningful behaviour, but here it means roughly a
   third of the pool's label-10 rows (8 of ~20–25) are calibrating against
   history that is one to nine-plus years old, not current behaviour, while
   the rest of the pool (mainstream `news` sources) is dominated by messages
   from the last few weeks. That asymmetry — old data concentrated in exactly
   the class the signals most need to separate — is a plausible contributor
   to the smaller validated edge above: growing the pool added sources, but a
   chunk of that growth is backlog, not new signal.

This refines, rather than contradicts, the round-11 feed-health finding
(`docs/feed_health_2026-07.md`): the near-exact match between the audit's 95
`ok` feeds and the calibration dataset's 95-source count is still real, but
"ok" measures *reachability*, not *liveness* — some fraction of those 95 are
feeds that answer correctly and simply have nothing new to say. Growing
snapshot count further will not grow usable content from these 15 sources; it
will keep re-collecting the same stale bodies (`merge_snapshots` already
dedupes them away silently, which is why they were invisible until checked
directly).

**Not done in this session** (would need explicit go-ahead, per the pattern
for prior audit/pipeline changes): adding a staleness class to
`feed_health_audit.py` (compare each feed's newest item date against today,
distinct from the existing `ok`/`dead`/`blocked`/`not-xml`); adding the
timestamp sanity floor/ceiling described above to `collect_rss` or
`merge_snapshots`; and specifically re-verifying `Il Corriere della Sera`'s
current registered feed URL, since it is both the audit's motivating case and
a scarce high-reliability Italian source.

## What would change the answer

Unchanged from 07-25 in kind, sharpened in degree by this run:

1. **More calendar time still helps, but not unconditionally** — only from
   sources that are actually publishing. 15 of 95 aren't; a "more data" story
   has to net that out.
2. **Fix or replace the 15 stale feeds**, starting with `Il Corriere della
   Sera` (flagship high-reliability Italian source) and the 8 stale label-10
   sources (the scarcest class). This likely matters more for the validated
   edge than accumulating further snapshots at the current registry.
3. **Investigate the predicted-band collapse** (74/75 at `medium_high`)
   before treating within-1 band agreement as informative — it may mostly
   reflect a scorer that has stopped discriminating in the middle of the
   scale, not one that agrees with ground truth.
4. Re-run this exact checkpoint after (2) and (3), before any weight change,
   so the next comparison isolates "did fixing the pool help" from "did more
   time alone help" — this run answered the second question and the answer is
   "not by itself."
