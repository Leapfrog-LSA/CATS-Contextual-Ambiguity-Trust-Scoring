# Volatility source-relative normalization — research spike, 31 August 2026

Raised in a methodological review of CATS (31 Aug 2026): `compute_volatility`'s
spike threshold is **global** — the same absolute sentiment-delta cutoff
(0.3, see [volatility_retune_2026-08.md](volatility_retune_2026-08.md)) for
a naturally expressive source and a naturally flat one. The review's
suggestion — flag a delta as anomalous only relative to *that source's own*
historical tone variance, not a fixed number applied to everyone — is a
real, previously-unaddressed gap. This spike tests it, reproducible via
[`research/volatility_normalization_spike.py`](../research/volatility_normalization_spike.py)
(stdlib + TextBlob only, no NLP model assets).

## Hypothesis

A tabloid and a wire service have different natural ranges of sentiment
swing. A fixed global threshold either over-flags the expressive-but-legitimate
source or under-flags genuine anomalies in the flat one. Normalizing each
delta against the source's own mean/std (a z-score) should separate
*anomalous-for-this-source* swings from *normal-for-this-source* ones,
regardless of the source's baseline expressiveness.

## Method

Per source: z-score each sentiment delta against that source's own
mean/std of deltas; flag a "spike" when `|delta − mean| > k · max(std, floor)`.
Swept `k ∈ {1.0, 1.5, 2.0, 2.5, 3.0}` and `floor ∈ {0.0, 0.05, 0.1, 0.15, 0.2}`
— the floor exists to probe a known failure mode explicitly: a source with
near-constant sentiment (std → 0, plausible given 48.9% of holdout messages
carry TextBlob polarity exactly 0.0 on Italian text) would flag *every*
nonzero delta as a huge z-score outlier with no floor. Same train/holdout
protocol as every other spike this week (56-source train / 53-source
future holdout, parameters fixed before running against any label).

## Diagnostic: is the near-zero-variance failure mode actually common?

Only 4 of 53 holdout sources (8%) have delta std < 0.05 — most sources do
have meaningful natural tone variance to normalize against (std range
0.000–0.350, median 0.142). The failure mode the floor is meant to guard
against is real but not the dominant pattern in this dataset.

## Result — a promising number that does not survive scrutiny

| k | floor | train ρ | holdout ρ |
|--:|--:|--:|--:|
| 1.0 | 0.00 | −0.152 | −0.083 |
| 1.5 | 0.00 | −0.326 | **−0.210** |
| 2.0 | 0.00 | **+0.124** | **+0.099** |
| 2.5 | 0.00 | +0.443 | +0.380 |
| 3.0 | 0.00 | +0.280 | +0.141 |

(Full 5×5 grid in the script output; every floor row repeats this same
pattern — the floor barely moves the numbers, confirming the near-zero-variance
edge case is not what's driving this.)

At `k=1.5` the design beats the current production baseline on both splits
(train −0.326, holdout −0.210, vs. the shipped threshold's −0.141/−0.151) —
genuinely stronger, correct sign, consistent between train and holdout. That
would normally be the profile of a real signal (the standard this project
uses, e.g. in the [gaming](gaming_redesign_2026-08.md) and
[silence](silence_retune_2026-08.md) fixes).

**But one step away in the same grid, at `k=2.0`, the sign flips to
positive on both splits — and gets *stronger* positive at `k=2.5`
(+0.44 train, +0.38 holdout).** A parameter whose sign depends on which
narrow window of the same hyperparameter you land in is not evidence of a
stable relationship — it is the same instability pattern that disqualified
`claim_density` in the [content-credibility spike](content_credibility_spike_2026-08.md)
and that flagged the pre-fix volatility threshold itself as untrustworthy.

## A hybrid design does not fix it

Tested whether pairing the z-score with an absolute delta floor (both
conditions must fire) stabilises the flip — same rationale as the existing
global threshold, just gated by the relative z-score too:

| abs_floor | k=0.5 | k=1.0 | k=1.5 | k=2.0 |
|--:|--:|--:|--:|--:|
| 0.10 | −0.176 | −0.057 | **−0.272** | +0.099 |
| 0.15 | −0.153 | −0.116 | **−0.319** | +0.099 |
| 0.20 | −0.102 | −0.106 | **−0.352** | +0.015 |
| 0.30 | −0.145 | −0.087 | **−0.249** | −0.023 |

(holdout ρ shown; full train+holdout table in the script output.) The
`k=1.5` column is the strongest result across the entire spike —
`abs_floor=0.2, k=1.5` reaches holdout ρ **−0.352**, more than double the
current production number. But the identical flip at `k=2.0` persists at
*every* absolute floor tried. The absolute floor does not fix the
instability; it is a property of the z-score threshold itself, not the
near-zero-variance edge case the floor was designed to guard against.

## A theoretical read on why this might be more than noise

The flip is too consistent — same boundary (between k=1.5 and k=2.0),
repeated across five independent floor settings — to dismiss purely as
sampling noise on 53 holdout sources. A candidate mechanism: pure
self-relative normalization can "grade a source on its own curve." A
chronically volatile source's large everyday swings become *its own
normal* (large std), so only a truly extreme event registers as a z-score
outlier for it — the design can end up rewarding chronic volatility rather
than penalising it, the opposite of the intended effect. A normally calm
source reacting once to real news would, by contrast, register a strong
z-score spike for a single legitimate event. If real, this would explain
a threshold-dependent sign flip: at low k the design still mostly tracks
raw variance (correct direction, similar to the global threshold); at high
k it increasingly rewards sources whose *entire distribution* is
anomalous, inverting the semantics. This is a hypothesis the data are
consistent with, not a proven mechanism — distinguishing it from
sample-specific noise needs more sources than 53 provides.

## Recommendation — do not ship; the most promising lead of the three tried, not a result

This is the same disposition as the [content-credibility](content_credibility_spike_2026-08.md)
and [cross-source-corroboration](cross_source_corroboration_spike_2026-08.md)
spikes, for a related reason: a numerically better result that is not
stable across a narrow hyperparameter window is not trustworthy evidence,
regardless of how good the best single point looks.

1. **Do not replace the global threshold with source-relative z-score
   normalization**, pure or hybrid, on this evidence.
2. **This is not a dead end like the other two spikes**, though — the
   sign-flip's consistency across five floor settings, and the plausible
   "grading on a curve" mechanism, are a specific, well-formed hypothesis
   worth re-testing once the pool supports it: with today's 53-source
   holdout there is no way to tell a real k-dependent mechanism from a
   coincidence of which particular sources happen to be in this sample.
   Revisit when the ≥100-source future holdout with multi-month history
   (the Fase D gate) exists — a genuine effect should replicate at a
   similar k on an independently-drawn holdout; a sample artifact should
   move around unpredictably.
3. **If revisited, test the mechanism directly**: rank holdout sources by
   their own delta std and check whether the "grading on a curve" theory
   predicts which specific sources flip between low-k and high-k
   classification, rather than only looking at the aggregate correlation.

## Caveats

n=53 holdout, distant-supervision labels, same caveats as every other
spike this week. `sentiment_polarity` is TextBlob, same 48.9%-zero-polarity
ceiling on Italian text as the global-threshold design — this spike changes
how deltas are *thresholded*, not the polarity signal feeding them, so
that ceiling is unaffected either way.
