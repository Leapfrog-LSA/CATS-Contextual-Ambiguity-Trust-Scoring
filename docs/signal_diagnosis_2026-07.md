# Signal diagnosis — ablation & leave-one-out (July 2026, roadmap item 7)

The [6-Jul future-snapshot validation](calibration_findings_2026-07-28.md)
showed per-signal rank correlation concentrated in `silence` and concluded the
calibrated coherence weight was "likely mild overfitting". Before any signal
redesign (roadmap phase C) that hypothesis deserved a test. This document
records a quantitative diagnosis of the four behavioural signals on the
committed calibration datasets — reproducible via
[`research/signal_ablation_spike.py`](../research/signal_ablation_spike.py)
(pure math on the precomputed signal vectors in `data/train.jsonl` /
`data/holdout_future.jsonl`; no NLP assets needed).

## Method

Four views on the same data (train n=56, future holdout n=53, shipped
calibrated weights):

1. **Per-signal ρ** vs label — marginal rank information.
2. **Inter-signal ρ** — redundancy check.
3. **Solo ranker** — each signal alone (all weight on it), holdout
   concordance/Spearman.
4. **Leave-one-signal-out (LOSO)** — calibrated weights with one signal zeroed
   and the rest renormalised: each signal's *marginal contribution to the
   aggregate*, which is not the same thing as its solo strength.

## Results (future holdout, n=53)

| signal | ρ vs label | solo concordance | LOSO Δ concordance | mean @ label ≤30 | mean @ label ≥70 |
|---|---:|---:|---:|---:|---:|
| coherence | +0.06 | 0.528 | **−0.139** | 25.2 | 25.0 |
| volatility | −0.05 | 0.518 | −0.013 | 13.3 | 8.6 |
| **silence** | **−0.43** | **0.636** | **−0.184** | 32.7 | 1.3 |
| gaming | −0.01 | 0.498 | −0.005 | 51.9 | 51.7 |

Full calibrated aggregate: concordance 0.755, Spearman +0.553. Inter-signal
rank correlations are all ≤ 0.27 — the signals are near-orthogonal; the
problem is lack of signal, not collinearity.

## What this changes in the received wisdom

1. **Coherence is load-bearing, not (only) overfit.** Solo it is barely above
   chance (0.528), but removing it from the calibrated mix costs −0.139
   concordance — the second-largest drop after silence. Mechanism: most
   sources tie on silence (the high tail averages 1.3), and concordance counts
   tied pairs as coin-flips; coherence breaks those ties in the right
   direction on the *future* holdout, which overfitting would not survive. The
   "likely mild overfitting" reading in the 6-Jul findings is therefore too
   pessimistic: the GA put 0.395 on coherence because it earns it in
   combination.
2. **Volatility and gaming are the actual dead weight.** Marginal contribution
   −0.013 / −0.005 concordance; gaming solo is *at chance* (0.498) and
   separates the tails by 0.2 points. These two — not coherence — are the
   redesign candidates of roadmap item 7.
3. **Silence remains the single point of failure, slightly softened.**
   Dropping it leaves 0.572, above chance but weak; with the ENGINE 1.4 domain
   penalty the full path reaches 0.775. An adversary managing cadence
   *and* publishing on a clean domain still collapses most of the margin —
   the content-credibility work item stands.

## Operational implication — the coherence backend matters

The dataset signal values were computed with the **SBERT** coherence backend.
The deployment default is NER (spaCy `it_core_news_lg`), which degrades to a
neutral constant when the model is absent — a neutral constant breaks no ties,
so **a deployment running degraded/NER coherence does not get the +0.139 that
the calibrated weights assume**. Until backend-specific calibration exists,
production deployments relying on `data/calibrated_weights.json` should run
the SBERT backend (`COHERENCE_BACKEND=sbert`), or expect holdout-style
concordance closer to the LOSO-coherence figure (≈0.62) than to 0.755.

## Recommendations (decisions for the maintainers, not pre-empted)

1. **Keep coherence; document the SBERT requirement** wherever the calibrated
   weights are recommended (done in this doc; consider `.env.example` /
   README).
2. **Target volatility and gaming for redesign or down-weighting** at the next
   recalibration (roadmap item 13). The remaining diagnosis they need —
   sub-score ablation for gaming (repetition/TTR/burst/vocab are only stored
   aggregated) and a spike-threshold sweep for volatility — requires
   recomputing signals from message histories with the NLP assets installed;
   this spike could not do it from the stored vectors alone.
3. **No roster or weight change without the full cycle** (recalibrate →
   re-validate on a future holdout), per `CLAUDE.md`. Removing gaming looks
   free (−0.005) but that is an n=53 estimate.

Caveats: single future holdout, n=53, distant-supervision labels (MBFC);
`default`-group sources are 2 of 53. Indicative, not certified.
