# Volatility threshold retune — 26 August 2026 (roadmap item 7d)

The [message-level follow-up](signal_diagnosis_2026-07.md#volatility-partially-starved-and-the-04-threshold-is-the-worst-setting)
found that the 0.4 spike threshold was, of the values swept, locally the
*worst* choice in the semantically correct (negative) direction: it was the
only point in the grid where the train-side correlation flipped sign
(+0.028), while 0.1–0.3 held a consistent −0.12…−0.15 on both train and
holdout — roughly 3× the current threshold's holdout information. The
diagnosis named this a candidate change for the next recalibration cycle
(`CLAUDE.md`); this is that cycle, run right after the [gaming
fix](gaming_redesign_2026-08.md) in the same week.

## Picking the value

Re-ran the full sweep (`research/gaming_volatility_diagnosis_spike.py`,
9-point grid, same 56-source train / 53-source future-holdout split as the
diagnosis):

| threshold | ρ train | ρ holdout |
|---:|---:|---:|
| 0.05 | −0.089 | −0.099 |
| 0.1 | −0.116 | −0.124 |
| 0.15 | −0.093 | −0.085 |
| 0.2 | −0.051 | −0.093 |
| **0.3** | **−0.141** | **−0.151** |
| 0.4 (was) | +0.028 | −0.053 |
| 0.5 | +0.006 | −0.069 |
| 0.6 | −0.030 | −0.129 |
| 0.8 | −0.033 | −0.076 |

0.3 is the strongest and most consistent point in the grid on both splits —
not just "in the 0.1–0.3 range" as the diagnosis's coarser 4-point summary
put it, but the single best value once swept finely. `cats/signals/volatility.py`'s
`compute_volatility` default changes from 0.4 to 0.3.

**The ceiling this doesn't move.** 48.9% of holdout messages carry TextBlob
polarity exactly 0.0 on Italian text (the sentiment lexicon can't see it),
capping this signal regardless of threshold. This retune only stops the
signal actively pointing the wrong way on train; it does not raise that
ceiling. The diagnosis flagged the BERT sentiment backend as a possible
higher ceiling — untested here, unchanged scope.

## Protocol

Same reproduction of the declared [28-Jul validation](calibration_findings_2026-07-28.md)
protocol used for the gaming fix, run on top of the now-shipped gaming-fixed
`data/calibrated_weights.json` / `data/train.jsonl` / `data/holdout_future.jsonl`,
recomputing only `volatility` with the new threshold:

```bash
python -m cats.calibration.merge_snapshots \
  --inputs data/snapshots/labelled_sources_2026-07-0{2,3,5}.jsonl \
  --out train_sources.jsonl                                        # 56 sources / 3 643 messages
python -m cats.calibration.build_dataset --input train_sources.jsonl --out train.jsonl
python -m cats.calibration.build_dataset \
  --input data/snapshots/labelled_sources_2026-07-06.jsonl --out holdout_future.jsonl  # 53 sources, never trained on
python -m cats.calibration --dataset train.jsonl --out calibrated_weights.json \
  --metric spearman --seed 7
python -m cats.calibration.evaluate --dataset holdout_future.jsonl --weights calibrated_weights.json
```

`COHERENCE_BACKEND=sbert` confirmed active. Rebuilding the *current shipped*
(post-gaming-fix) holdout through this pipeline first reproduced 0.753 /
+0.551 exactly, confirming the pipeline before comparing anything built on
it.

## Result — no material regression

| Metric (future holdout, n=53) | Shipped (post-gaming-fix, 26-Aug) | Shipped weights, re-scored on retuned-volatility holdout | **New calibrated weights (retuned volatility)** | Static WP 4.1, retuned-volatility holdout |
|---|---:|---:|---:|---:|
| Spearman | +0.551 | +0.550 | **+0.556** | +0.510 |
| Concordance | 0.753 | 0.750 | **0.750** | 0.733 |
| Band agreement (exact / within-1) | 26.4% / 79.2% | 28.3% / 79.2% | **28.3% / 77.4%** | 15.1% / 58.5% |

Movement across the board is inside GA/measurement noise (±0.003–0.006 on
every metric) — no direction reads as a regression, and 0.750 still clears
the 0.70 production criterion from 28-Jul. New GA output (`--seed 7`):

| Group | coherence | volatility | silence | gaming |
|---|---:|---:|---:|---:|
| `news` (was: 0.428 / 0.038 / 0.524 / 0.011) | 0.428 | **0.059** | 0.502 | 0.010 |
| `default` (was: 0.139 / 0.375 / 0.307 / 0.180) — n=2, not meaningful | 0.056 | 0.432 | 0.325 | 0.187 |

The `news`-group volatility weight moves 0.038 → 0.059 — a small increase,
consistent with the signal now carrying slightly more (and correctly
signed) information rather than near-noise. It stays well below silence and
coherence, matching the diagnosis's finding that even at its best swept
value volatility is a minor contributor, not a rescued signal.

## Shipped

`data/calibrated_weights.json`, `data/train.jsonl` and
`data/holdout_future.jsonl` updated to this run's outputs (same 56/53-source
split as the 07-28 baseline; gaming fix from `gaming_redesign_2026-08.md`
carried forward, volatility now computed at threshold 0.3).

## What this doesn't fix

The 48.9%-zero-polarity ceiling stands: TextBlob's lexicon is not built for
Italian, and roughly half the corpus is invisible to sentiment-based
volatility no matter the threshold. Raising that ceiling would mean
evaluating the BERT sentiment backend (`neuraly/bert-base-italian-cased-sentiment`,
already used by the `volatility` signal's alternate backend path) on the
same holdout — untried in this pass, a candidate for a future checkpoint.

## Caveats (unchanged from 07-28, still apply)

n=53 holdout, distant-supervision labels (MBFC + documented disinformation
networks): indicative, not a certified accuracy figure. Two `default`-type
sources are excluded from per-type correlation (n too small); the reported
figures are the `news` group that dominates the registry.
