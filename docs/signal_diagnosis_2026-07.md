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

---

## Message-level follow-up (completes roadmap item 7)

The vector-level diagnosis above could not see inside gaming's sub-scores or
sweep volatility/silence thresholds. This second pass recomputes those from
the committed snapshot message histories — reproducible via
[`research/gaming_volatility_diagnosis_spike.py`](../research/gaming_volatility_diagnosis_spike.py)
(same protocol: train = merged 02/03/05-Jul snapshots n=56, holdout = unseen
06-Jul snapshot n=53; no NLP model assets needed).

### Gaming: a duplicated sub-score, and heuristics that fire on journalism

| sub-score (higher=worse) | ρ train | ρ holdout |
|---|---:|---:|
| repetition | +0.15 | −0.00 |
| ttr | +0.08 | −0.09 |
| burst | +0.11 | +0.09 |
| vocab | +0.08 | −0.09 |
| aggregated value | +0.17 | −0.01 |

1. **`vocab_score` ≡ `ttr_score` above the 50-token floor** — both compute
   `1 − unique/total`. Verified: identical in 56/56 train and 52/53 holdout
   sources. The gaming mean is therefore effectively
   `(repetition + burst + 2·TTR)/4`: TTR is silently double-weighted, and the
   four "independent" heuristics are three. A constraint note now sits in
   `signals/gaming.py`; the fix (a genuinely distinct fourth heuristic, or a
   3-term mean) changes signal semantics → next recalibration.
2. **The mild train correlations point the wrong way and don't generalise.**
   Positive ρ means high "manipulation" sub-scores associate with *reliable*
   outlets: professional newsrooms post in bursts (breaking news) and reuse
   templated phrasing (repetition). On the holdout everything collapses to
   |ρ| ≤ 0.09. No re-weighting of these sub-scores rescues gaming — the
   heuristics measure newsroom practice, not manipulation. Redesign or
   removal at the next recalibration.

### Volatility: partially starved, and the 0.4 threshold is the worst setting

| spike threshold | ρ train | ρ holdout |
|---|---:|---:|
| 0.1 | −0.12 | −0.12 |
| 0.3 | −0.14 | −0.15 |
| **0.4 (current)** | **+0.03** | **−0.05** |
| 0.6 | −0.03 | −0.13 |

48.9% of holdout messages have TextBlob polarity exactly 0.0 (Italian text
the sentiment lexicon cannot see), so half the corpus is invisible to the
signal regardless of threshold — a hard ceiling for the default backend. But
within that ceiling the current threshold is locally the *worst* choice
tried: at 0.1–0.3 volatility carries ρ ≈ −0.12…−0.15 **in the semantically
correct direction, consistently on train and holdout** — roughly 3× its
current holdout information. Candidate change for the next recalibration
(threshold change ⇒ full recalibrate + future-holdout revalidation); the BERT
sentiment backend may raise the ceiling further (untested — needs model
weights).

### Silence: the 72 h threshold is close to, but not at, its optimum

| threshold (h) | ρ train | ρ holdout |
|---|---:|---:|
| 24 | −0.38 | −0.46 |
| 48 | −0.39 | −0.35 |
| **72 (current)** | **−0.42** | **−0.43** |
| 96 | −0.47 | −0.47 |
| 120–168 | −0.47 | −0.47 |

Raising the anomaly threshold to ≥ 96 h strengthens silence slightly and
consistently on both splits, and the curve plateaus there. Feeds roadmap
item 13 (threshold validation) — same recalibration discipline applies.

### Updated bottom line for phase C

Item 7 is complete. The evidence ranks the interventions: (a) fix the
volatility threshold (~3× its information, trivial change, needs the
recalibration cycle), (b) silence threshold to 96 h (small consistent gain,
same cycle), (c) gaming needs redesign, not tuning — its heuristics measure
newsroom practice and one of its four terms is a duplicate, (d) coherence:
keep, with the SBERT backend requirement documented above. None of these
ship without recalibrate → future-holdout revalidate (CLAUDE.md).
