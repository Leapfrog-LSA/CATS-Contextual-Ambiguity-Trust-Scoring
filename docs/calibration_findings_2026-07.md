# Calibration findings — July 2026 snapshots

Empirical findings from the first real calibration runs (snapshots
2026-07-02/03, 49 labelled sources, labels 10–95 including 10 documented
disinformation sources — see `data/README.md`). They motivated the
signal-polarity fix shipped in v1.3.0 (§3) and the still-open
future-snapshot validation.

## 1. Per-signal discriminative power

Spearman rank correlation of each raw signal against the ground-truth label,
full dataset (n=49, merged 2-day histories, SBERT coherence backend):

| Signal | ρ vs label | mean @ label 10 | mean @ label ≥ 70 |
|---|---:|---:|---:|
| coherence | +0.08 | 26.5 | 24.2 |
| volatility | −0.03 | 17.0 | 11.1 |
| **silence** | **−0.44** | **42.4** | **1.2** |
| gaming | +0.05 | 52.8 | 55.1 |

**Silence is currently the only informative signal** on this dataset, and its
polarity is semantically correct: disinformation sites publish sporadically
(mean silence 42) while mainstream outlets publish continuously (1.2).
Coherence, volatility and gaming carry essentially no rank information on
single-feed histories this short.

## 2. The polarity defect dominates everything else

`aggregate_score` is a non-negative weighted average — every signal is treated
as "higher = better" (recorded design decision, see
`architecture.md → Signal Polarity & Scoring`). But the one informative signal
(silence) is "higher = worse". The consequences are measurable:

- The GA, maximising train Spearman, loads weight onto silence — and thereby
  ranks *silent* (disinformation) sources **above** mainstream outlets at
  evaluation time. On the merged-history holdout the label-10 source received
  the **highest** predicted score (29.7 vs ≈6 for the real outlets):
  Spearman −0.42, concordance 0.28.
- Re-running the identical calibration with volatility/silence/gaming
  inverted (`x → 100 − x`) before aggregation:

| | current architecture | polarity-corrected (experiment) |
|---|---:|---:|
| Train Spearman (calibrated) | 0.19 | **0.64** |
| Holdout Spearman | −0.42 | **+0.32** |
| Holdout concordance | 0.28 | **0.66** |
| Holdout band agreement | 0% exact | **40% exact, 90% within 1** |

The experiment changes no signal algorithm and no data — only the direction in
which three signals enter the average. **Fixing polarity (inverting
higher-is-worse signals before aggregation, or allowing signed weights) is the
single highest-leverage change available**, worth more than any recalibration
under the current architecture.

## 3. Resolution — polarity fix shipped in v1.3.0 (2026-07-05)

The experiment above was promoted to the engine: since v1.3.0
`aggregate_score` inverts volatility/silence/gaming (`100 − value`) before the
weighted mean (see `architecture.md → Signal Polarity & Scoring` and the
CHANGELOG). Re-running the full pipeline on the three merged snapshots
(2026-07-02/03/05; 50 sources, 3 426 messages) with the corrected engine,
SBERT coherence, temporal 80/20 split, seed 7:

| | pre-fix (merged 2-day) | v1.3.0 (merged 3-day) |
|---|---:|---:|
| Train Spearman — static baseline | −0.18 … 0.19 | **+0.56** |
| Train Spearman — calibrated | 0.19 | **+0.66** |
| Holdout Spearman (calibrated) | −0.42 | **+0.36** |
| Holdout concordance | 0.28 | **0.71** |
| Holdout band agreement | 0% exact | **40% exact, 100% within 1** |
| Full-dataset Spearman (diagnostic) | 0.14 | **+0.58** |
| Full-dataset concordance (diagnostic) | 0.57 | **0.78** |

The full-dataset band table is now semantically coherent: all four sources
predicted `very_low`/`low` are label-10 disinformation sources, and the single
`high` prediction is the label-95 source. The static weights are positively
correlated for the first time (+0.56 train) — with a common reliability axis
they behave as sensible priors instead of ranking backwards.

Calibrated weights (news group): silence 0.48, coherence 0.36, gaming 0.13,
volatility 0.03 — consistent with §1: silence carries most of the signal,
coherence adds rank information under the SBERT backend.

## 4. Remaining caveats

- n=49 with a 10-source holdout: all numbers are indicative, not declarative.
  The scheduled snapshot collection (`.github/workflows/collect-rss.yml`) plus
  `merge_snapshots` will grow both histories and holdout over the coming weeks;
  re-run the validation then (tracked work item).
- Labels are distant supervision (MBFC + documented disinformation networks);
  the usual leakage/bias caveats in `docs/calibration.md` apply.
- Even polarity-corrected, coherence/volatility/gaming contribute little on
  short histories — whether they become informative with longer spans is
  exactly what the future-snapshot validation will show.
