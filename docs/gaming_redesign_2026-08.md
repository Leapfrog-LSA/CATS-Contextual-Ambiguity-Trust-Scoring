# Gaming signal fix and revalidation — 26 August 2026 (roadmap item 7c)

The [message-level follow-up](signal_diagnosis_2026-07.md#gaming-a-duplicated-sub-score-and-heuristics-that-fire-on-journalism)
found that `gaming`'s `vocab_score` sub-score is mathematically identical to
`ttr_score` above the 50-token floor (both compute `1 - unique/total`),
so the unweighted 4-term mean in `compute_gaming` silently counted `ttr`
twice. The diagnosis named two valid fixes — "a genuinely distinct fourth
heuristic, or a 3-term mean" — and left the choice, and the required
recalibration + future-holdout revalidation (`CLAUDE.md`), for a later pass.
This is that pass.

## The fix

`cats/signals/gaming.py`: `compute_gaming`'s `value` is now the mean of the
three genuinely distinct sub-scores (`repetition`, `ttr`, `burst`) instead of
four. `vocab_score` is still computed and returned on `GamingResult` — for
introspection, and so the original diagnosis spike
(`research/gaming_volatility_diagnosis_spike.py`) stays reproducible — it is
just no longer folded into `value`.

**Chosen over a new fourth heuristic deliberately.** The same diagnosis found
that *all three* remaining sub-scores carry ~0 rank information on the future
holdout (|ρ| ≤ 0.09) and that their mild train-only correlations point the
wrong way — professional newsrooms post in bursts and reuse templated
phrasing, so the heuristics track newsroom practice, not manipulation.
Inventing a new heuristic under a one-week budget would add untested logic
with no stronger claim to generalising than the ones it replaced. Removing
the diagnosed double-count is the change the evidence actually supports;
redesigning gaming into something that detects manipulation rather than
newsroom cadence is a separate, larger decision left open below.

## Protocol

Exact reproduction of the declared [28-Jul validation](calibration_findings_2026-07-28.md)'s
protocol, only recomputing the `gaming` signal with the fix:

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

`COHERENCE_BACKEND=sbert` confirmed active (required — see
[signal diagnosis](signal_diagnosis_2026-07.md#operational-implication--the-coherence-backend-matters)).
Rebuilding the *old* (pre-fix) `data/holdout_future.jsonl` through this exact
pipeline reproduced 0.755 / +0.553 exactly, confirming the pipeline itself
matches the declared run before comparing anything.

## Result — no material regression, and the weight gets more honest

| Metric (future holdout, n=53) | Shipped, pre-fix (07-28) | Shipped weights, re-scored on fixed-gaming holdout | **New calibrated weights (fixed gaming)** | Static WP 4.1, fixed-gaming holdout |
|---|---:|---:|---:|---:|
| Spearman | +0.553 | +0.542 | **+0.551** | +0.480 |
| Concordance | 0.755 | 0.750 | **0.753** | 0.721 |
| Band agreement (exact / within-1) | 26.4% / 79.2% | 26.4% / 79.2% | **26.4% / 79.2%** | 18.9% / 62.3% |

0.753 still clears the 0.70 production criterion from the 28-Jul validation;
the ±0.002-0.005 movement is within what GA re-runs and the small honest
change to gaming's values would be expected to produce, not a regression.
Predicted-band counts are unchanged (`very_low` 1, `low` 4, `medium` 5,
`medium_high` 42, `high` 1) — the fix does not reshuffle which sources land
where.

What *does* move is the weight itself. New GA output (`--seed 7`):

| Group | coherence | volatility | silence | gaming |
|---|---:|---:|---:|---:|
| `news` (was: 0.395 / 0.077 / 0.469 / **0.059**) | 0.428 | 0.038 | 0.524 | **0.011** |
| `default` (was: 0.143 / 0.428 / 0.268 / 0.161) — n=2, not meaningful | 0.139 | 0.375 | 0.307 | 0.180 |

The `news`-group gaming weight drops from 0.059 to 0.011: with the duplicate
`ttr` term gone, the calibrator now credits gaming close to its true
near-zero marginal value (LOSO Δ −0.005 in the original diagnosis) instead of
partially rewarding it for double-counting `ttr`. This is the expected,
correct effect of removing a measurement bug — a signal that was carrying
spurious weight because of an arithmetic accident now carries less.

## Shipped

`data/calibrated_weights.json`, `data/train.jsonl` and
`data/holdout_future.jsonl` are updated to this run's outputs (same 56/53
sources and split as the 07-28 baseline, gaming recomputed with the fix).

## What this doesn't fix

This closes the diagnosed *bug* (duplicate sub-score), not the deeper
redesign-or-removal question the diagnosis raised. Per the message-level
follow-up, gaming's three remaining sub-scores still carry ~0 rank
information on the future holdout and measure newsroom publishing practice
more than manipulation. A signal that actually discriminates gaming/spam
from professional publishing would need new heuristics validated from
scratch through their own spike → calibrate → revalidate cycle — a larger,
riskier piece of work than a bug fix, and explicitly out of scope here.
Candidate directions (unevaluated): cross-message near-duplicate/templating
detection distinct from bigram repetition, engagement-manipulation signals
(if such metadata is ever available), or folding gaming into the
content-credibility signal (roadmap item 10) rather than keeping it separate.

## Caveats (unchanged from 07-28, still apply)

n=53 holdout, distant-supervision labels (MBFC + documented disinformation
networks): indicative, not a certified accuracy figure. Two `default`-type
sources are excluded from per-type correlation (n too small); the reported
figures are the `news` group that dominates the registry.
