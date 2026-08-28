# Cross-source corroboration — research spike, 28 August 2026 (roadmap item 11)

The [28-Jul findings](calibration_findings_2026-07-28.md) named cross-source
corroboration as a candidate direction, and the roadmap flagged it
explicitly as needing a feasibility check before any commitment to a shared
cross-source registry (a real data-design change): "verificare fattibilità e
valore incrementale prima di impegnarsi." This is that check, reproducible
via
[`research/cross_source_corroboration_spike.py`](../research/cross_source_corroboration_spike.py)
(stdlib only, no NLP model assets).

## Hypothesis

A story that genuinely happened gets reported by more than one outlet within
hours; a source fabricating its own narrative has nothing else corroborating
it. A per-source "corroboration rate" — the share of its messages that
overlap lexically with some other source's message in a nearby time window —
should therefore correlate positively with reliability, independent of the
four behavioural signals (which look at one source's own timing/text) and of
domain-provenance (which looks at one source's own URL).

## Prototype

Per-message "distinctive word set" (lowercased alphabetic tokens, length ≥5,
minus a small EN/IT stopword list) matched via an inverted index against
every other source's messages within ±48h; a match counts if
Jaccard(word sets) ≥ 0.3. Per source, `corroboration_rate` = share of its
messages with ≥1 such match from a *different* source_id. Design (window,
threshold, word-length floor) was fixed before this script was run against
any label — same discipline as the other two spikes this week.

## First result — looked promising

| split | n | ρ | mean rate | all-zero |
|---|---:|---:|---:|---:|
| train (merged 02/03/05-Jul) | 55 | **+0.328** | 0.015 | 37/55 (67%) |
| holdout (06-Jul, unseen) | 52 | **+0.290** | 0.019 | 43/52 (83%) |
| pooled (train ∪ holdout) | 55 | +0.316 | 0.017 | 35/55 (64%) |

Unlike the [content-credibility spike](content_credibility_spike_2026-08.md)
(|ρ| ≤ 0.18, sign-flipping), this held the same sign and a similar magnitude
across train, holdout, *and* a pooled cross-check — the profile of a real
signal, not noise. Label-extreme means told the same story: `label≤30`
sources average 0.000 corroboration, `label≥70` average 0.030.

## Second look — it doesn't survive inspection

Before trusting a sparse signal (67-83% of sources score exactly 0), the
matches themselves were inspected. The top-8 by match strength, and 284 of
321 deduplicated matches overall (88%), are **one single source pair**:
CNET ↔ Mashable, both publishing daily video-game/puzzle-hint columns
("Today's Wordle Hints, Answer and Help for July 2, #1839" / "Wordle today:
Answer, hints for July 3, 2026") with near-identical templated phrasing.
This is a **recurring-content-genre artifact**, not independent
verification of a news event — both outlets happen to run the same daily
filler feature, so their headlines share distinctive words regardless of
any real-world story. Across the full pool, matches concentrate in just
**16 distinct source pairs** (out of ~5,900 possible pairs among the ~109
merged sources), and 20 of ~109 sources ever register a single corroborated
message.

Removing the CNET↔Mashable and LA Times↔Mashable pairs (both tech/lifestyle
outlets sharing the puzzle-column genre) weakens the correlation but does
not zero it out — a residual signal remains from the other ~14 pairs:

| split | ρ (excl. puzzle-genre pairs) | mean rate | all-zero |
|---|---:|---:|---:|
| train | +0.282 (was +0.328) | 0.0077 | 38/55 |
| holdout | +0.215 (was +0.290) | 0.0101 | 45/52 |

A ~20-25% relative drop in correlation from excluding two source pairs, on a
signal that only 20 of ~109 sources register at all, is not evidence of a
mechanism that generalises — it is evidence that the *specific outlets
present in this corpus* happen to produce a handful of coincidental lexical
overlaps, some genre-driven, some possibly genuine, too few to distinguish
from each other or to trust as a reproducible property of "how reliable
sources behave."

## Recommendation — do not build the shared registry; feasibility check failed

This closes the roadmap's own decision point (verify feasibility and
incremental value before committing to a new cross-source data design):

1. **Don't build a cross-source registry on this evidence.** The naive
   lexical-Jaccard proxy for "corroboration" is dominated by a recurring
   templated-content-genre false positive (daily puzzle/game-hint columns),
   not genuine independent story verification — the opposite of what the
   hypothesis needed to be true.
2. **The residual signal after removing that artifact is too sparse to
   trust**: ~20 corroborating sources out of ~109, concentrated in ~14
   pairs. Whatever real signal remains cannot currently be told apart from
   more incidental content-genre overlap without a much better
   story-matching method (named-entity/event extraction, or embedding
   similarity robust to templated boilerplate) — the same "needs
   model-based features, not lexical heuristics" conclusion the
   content-credibility spike reached, for a related reason.
3. **Value proposition of item 11 itself is now in question, not just this
   prototype.** Even a "successful" cheap lexical-overlap corroboration
   signal would have covered only a small fraction of sources (most RSS
   outlets in this pool simply don't share verbatim-adjacent phrasing with
   each other on the same day, syndicated puzzle columns aside) — a
   fundamentally low-recall signal even before the artifact was found. A
   real corroboration system's incremental value over domain-provenance
   (already the "high-precision, low-recall" case in this codebase) would
   need to be re-argued from scratch with better matching, not assumed.
4. **Caught by inspecting matches before trusting a correlation number** —
   the same practice that caught the curl `--fail` bug and gaming's
   vocab/ttr duplicate this project has relied on before. A promising ρ is
   a reason to look closer, not a reason to ship.

## Caveats

n=53-56 per split, distant-supervision labels. The stopword/word-length
proxy for "distinctive word" is crude; a better content-matching method
might avoid the puzzle-column false positive while still finding genuine
corroboration — but that is precisely the "model-based features" investment
flagged as out of scope for a spike, not something to iterate into this
lexical approach.
