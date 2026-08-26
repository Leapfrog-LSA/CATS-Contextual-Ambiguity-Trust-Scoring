# Silence threshold retune — 26 August 2026 (roadmap item 13, partial)

The [message-level follow-up](signal_diagnosis_2026-07.md#silence-the-72-h-threshold-is-close-to-but-not-at-its-optimum)
found the 72 h anomaly threshold close to, but not at, its optimum: rho
strengthens monotonically from 24 h to 96 h and then plateaus (96/120/168 h
identical). This closes that recommendation, third of the three candidates
the diagnosis named for "the next recalibration" — after the [gaming
fix](gaming_redesign_2026-08.md) and the [volatility
retune](volatility_retune_2026-08.md), both shipped earlier this week.

## Picking the value

Re-ran the sweep (`research/gaming_volatility_diagnosis_spike.py`, same
56-source train / 53-source future-holdout split):

| threshold (h) | ρ train | ρ holdout |
|---:|---:|---:|
| 24 | −0.376 | −0.461 |
| 48 | −0.386 | −0.353 |
| 72 (was) | −0.423 | −0.430 |
| **96** | **−0.468** | **−0.474** |
| 120 | −0.468 | −0.474 |
| 168 | −0.468 | −0.474 |

96 h is the smallest threshold that reaches the plateau on both splits —
raising it further (120 h, 168 h) buys nothing, so 96 h is the natural
choice: the full available gain, no unnecessary extra slack.
`cats/signals/silence.py`'s `SOURCE_TYPE_THRESHOLDS` changes from 72.0 to
96.0 for all three source types (kept uniform, matching how the sweep itself
was run — a single override applied across all source types, not a
per-type value).

## A structural side effect: `silence_blind_sources`

`cats/calibration/split.py`'s `silence_blind_sources` (used by
`cats.calibration.split` to warn when a holdout side's window is too short
for `silence` to register any anomaly at all) reads the threshold via
`threshold_for`, so it picked up 96 h automatically — no separate bug. But
this raises the bar for what counts as "long enough": a source whose
observed window is, say, 80 h was fine under the old 72 h threshold and is
now classified `silence`-blind under 96 h. This is not a regression, it is
the diagnostic doing its job with the corrected threshold — but it does mean
a data-quality warning that was silent before may now fire on splits that
previously looked clean. Updated `tests/unit/test_split.py` fixtures
accordingly (the exact-threshold-boundary tests were pinned to 72 h/96 h
spans and needed new boundary values to keep testing "at/under" vs. "over"
the *current* threshold rather than the old one).

## Protocol

Same reproduction as the two earlier fixes, run on top of the currently
shipped (post-gaming-fix, post-volatility-retune) baseline, recomputing only
`silence` at the new threshold:

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

`COHERENCE_BACKEND=sbert` confirmed active. Rebuilding the current shipped
holdout through this pipeline first reproduced 0.750 / +0.556 exactly,
confirming the pipeline before comparing anything built on it.

## Result — no material regression

| Metric (future holdout, n=53) | Shipped (pre-this-fix) | Shipped weights, re-scored on retuned-silence holdout | **New calibrated weights (retuned silence)** | Static WP 4.1, retuned-silence holdout |
|---|---:|---:|---:|---:|
| Spearman | +0.556 | +0.562 | **+0.554** | +0.511 |
| Concordance | 0.750 | 0.753 | **0.750** | 0.734 |
| Band agreement (exact / within-1) | 28.3% / 77.4% | 28.3% / 77.4% | **26.4% / 79.2%** | 15.1% / 56.6% |

Movement stays inside the same GA/measurement noise band as the two earlier
fixes this week (±0.003–0.008); 0.750 still clears the 0.70 production
criterion. New GA output (`--seed 7`):

| Group | coherence | volatility | silence | gaming |
|---|---:|---:|---:|---:|
| `news` (was: 0.428 / 0.059 / 0.502 / 0.010) | 0.410 | 0.042 | **0.543** | 0.006 |
| `default` (was: 0.056 / 0.432 / 0.325 / 0.187) — n=2, not meaningful | 0.129 | 0.341 | 0.404 | 0.126 |

The `news`-group silence weight moves 0.502 → 0.543, consistent with the
signal now carrying more information (ρ −0.474 vs −0.430 on the holdout) —
the same pattern as the volatility retune: fixing a threshold makes the
calibrator trust the signal more, not less.

## Shipped

`data/calibrated_weights.json`, `data/train.jsonl` and
`data/holdout_future.jsonl` updated to this run's outputs (same 56/53-source
split as the 07-28 baseline; gaming fix and volatility retune carried
forward, silence now computed at threshold 96 h for every source type).

## What this doesn't fix

Item 13's remaining scope — full recalibration on the ≥100-source holdout,
band-cutoff validation (80/60/40/20), and the domain-penalty coefficient —
is untouched; this closes only the silence-threshold piece the July
diagnosis specifically measured. Per-source-type differentiation of the
threshold (today still uniform 96 h across `social`/`news`/`default`) was
not attempted: the sweep that produced this number applied one override
across all types, so a per-type value would need its own sweep, not a
reuse of this one.

## Caveats (unchanged from 07-28, still apply)

n=53 holdout, distant-supervision labels (MBFC + documented disinformation
networks): indicative, not a certified accuracy figure. Two `default`-type
sources are excluded from per-type correlation (n too small); the reported
figures are the `news` group that dominates the registry.
