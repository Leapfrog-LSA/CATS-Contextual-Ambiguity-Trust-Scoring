# Future-snapshot validation — 6 July 2026

> **Dating note.** This validation was run on **6 July 2026** (commit
> `2b41982`, on the 2026-07-06 holdout snapshot). The original title and this
> file's name said "28 July" — a dating slip that propagated into other
> documents before it was caught. The filename (and the released CHANGELOG
> entries that cite it) are kept as-is for link stability.

This is the honest temporal validation the earlier findings deferred: calibrate
on **past** snapshots only, then evaluate on a **later snapshot the calibrator
never saw**. It is the first CATS result that is *declarative* rather than
merely diagnostic, because the holdout is genuinely out-of-sample in time.

## Protocol

- **Train**: `merge_snapshots` over the three earliest weekly snapshots
  (`data/snapshots/labelled_sources_2026-07-02/03/05.jsonl`) → 56 sources /
  3 643 messages (1 320 feed-overlap duplicates dropped). SBERT coherence
  backend, GA calibration `--metric spearman --seed 7`.
- **Holdout**: the 2026-07-06 snapshot **only** (53 sources / 1 753 messages),
  built independently and never merged into training. Full label spread,
  including a real low tail: 12 sources at label 10 and 3 at 30.
- Weights validated this way ship in `data/calibrated_weights.json`; datasets
  in `data/train.jsonl` / `data/holdout_future.jsonl`.

## Result — the criterion is met

| Metric (future holdout, n=53) | Static WP 4.1 | **Calibrated (validated)** |
|---|---:|---:|
| Pairwise concordance (AUC-like) | 0.731 | **0.755** |
| Spearman ρ | +0.505 | **+0.553** |
| Band agreement (within 1) | 62.3% | **79.2%** |
| Band agreement (exact) | 18.9% | **26.4%** |

Pairwise concordance **0.755 > 0.70** on a snapshot the calibrator never saw:
the calibrated weights **generalise forward in time**. The low tail now
discriminates — the five lowest-predicted sources are all label-10
disinformation sources, and the single `high` prediction is the label-95
source. This closes the open validation work item: the weights are usable in
production (see below).

## The caveat the same data forces us to state

The validation passes almost entirely on the strength of **one signal**.
Per-signal rank correlation against the ground-truth label on the *future
holdout*:

| Signal | ρ vs label | mean @ label ≤ 30 | mean @ label ≥ 70 |
|---|---:|---:|---:|
| coherence | +0.06 | 25.2 | 25.0 |
| volatility | −0.05 | 13.3 | 8.6 |
| **silence** | **−0.43** | **32.7** | **1.3** |
| gaming | −0.01 | 51.9 | 51.7 |

Silence remains the only informative signal, and its polarity is semantically
correct (disinformation feeds publish sporadically; mainstream outlets
continuously). Coherence, volatility and gaming carry essentially **no rank
information even on four weeks of accumulated history** — the extra span did
not rescue them. The calibrated news weights (silence 0.47, coherence 0.40,
volatility 0.08, gaming 0.06) load coherence more than its holdout ρ (0.06)
justifies: that is likely mild overfitting of the SBERT coherence signal on the
training split, and it is why the calibrated edge over the static weights is
real but modest (Δ concordance +0.024).

**Implication for the roadmap (open item — signal discriminative power).** A
system that scores well on one signal is a system that an adversary defeats by
managing that one signal: a disinformation outlet that simply publishes on a
regular cadence would neutralise silence and collapse CATS toward chance. The
v2.0 signal-hardening work should therefore prioritise making at least one of
coherence/volatility/gaming carry independent rank information — candidate
directions: domain/impersonation features (the Doppelganger case is invisible
to all four current signals), cross-source corroboration, and longer per-source
spans than a monthly RSS window affords.

## Caveats (unchanged, still apply)

- n=53 holdout, distant-supervision labels (MBFC + documented disinformation
  networks): indicative, not a certified accuracy figure. The Art. 15
  declaration states the measured metrics and their conditions.
- Two `default`-type sources are excluded from the per-type correlation (n too
  small); the reported figures are the `news` group that dominates the registry.
