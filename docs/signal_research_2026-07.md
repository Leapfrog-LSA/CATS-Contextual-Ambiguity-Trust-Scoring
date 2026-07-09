# Signal discriminative power — investigation (task #8)

The 6-Jul future-snapshot validation ([findings](calibration_findings_2026-07-28.md))
passed (holdout concordance 0.755) but showed CATS's discrimination rests almost
entirely on **one** of the four signals:

| Signal | ρ vs label (future holdout) |
|---|---:|
| coherence | +0.06 |
| volatility | −0.05 |
| **silence** | **−0.43** |
| gaming | −0.01 |

Silence being the only informative signal is an operational risk: a
disinformation outlet that simply publishes on a **regular cadence** neutralises
silence and collapses CATS toward chance. This document records the
investigation into a complementary signal — reproducible via
[`research/domain_provenance_spike.py`](../research/domain_provenance_spike.py).

## Hypothesis

The behavioural signals all operate on *messages* (timestamps + text). The one
class of unreliable source they are structurally **blind** to is
infrastructure-based impersonation — the Doppelganger clones
(`spiegel.ltd`, `bild.pics`, `ansa.ltd`) are invisible to coherence, volatility,
silence and gaming alike, because their *content* is plausible; the deception is
the *domain*. A signal computed from the source domain should therefore be
orthogonal to the four behavioural ones.

## Prototype

A `domain_provenance_score` (0–100, higher = more clone/impersonation red flags)
from **general domain structure only** — never from membership in
`data/disinfo_sources.csv`, so it generalises to unseen domains:

- **Rare/cheap TLD** used by clone networks (`.pics .ltd .cfd .live .work .fun
  .today …` — the exact Doppelganger set): +40
- **Free-hosting subdomain** (`*.altervista.org`, `*.blogspot.com`,
  `*.wordpress.com`): +45
- **Typo-squat**: Levenshtein distance 1–2 to a fixed major-outlet brand list
  (not equal to it): +50
- **Brand name embedded on a foreign TLD** (e.g. `bild` on `.pics`): +25

## Results

**Registry (n=160):** ρ(domain red-flag, label) = **−0.26** — weaker than
silence, but in the right direction and, crucially, computed from a completely
independent input.

**Precision vs recall.** The signal is **high-precision, low-recall**:

| Label band | n | flagged (score ≥ 40) |
|---|---:|---:|
| low (≤30) | 19 | 4 |
| mid (50–70) | 72 | 0 |
| high (≥85) | 69 | 1 |

Almost no false positives on legitimate outlets, but it catches only the
infrastructure clones (suspicious TLD / free hosting / typo-squat). It **misses**
fake-news content on normal domains (`worldnewsdailyreport.com`,
`empirenews.net`) and established low-quality outlets (`naturalnews.com`,
`rt.com`) — those have ordinary domains and need a content/NLP signal instead.

**The value is where silence fails.** On the future holdout, combining the
behavioural score with a domain penalty:

| Future holdout (n=53) | concordance | Spearman |
|---|---:|---:|
| behavioural (calibrated, silence-driven) | 0.755 | +0.553 |
| domain-provenance alone | 0.560 | — |
| **behavioural + domain penalty** | **0.775** | **+0.595** |

The +0.02 concordance gain is modest because only 3 of 53 holdout sources are
structurally suspicious — but every correction was correct, and one is exactly
the adversarial case:

> **Il Corrispondente** (a `blogspot.com` disinformation site, label 10)
> publishes on a regular cadence, so *silence did not catch it* (behavioural
> score 52.6, i.e. "medium"). The domain penalty pulls it to 25.6 ("low").

That single example is the whole argument: the domain signal fixes precisely the
failure mode that defeats silence.

## Recommendation (decision for the maintainers)

1. **Add domain-provenance as a fifth signal for v2.0.** It is orthogonal to the
   four behavioural signals, high-precision (safe to add — near-zero false
   positives), and it closes the regular-cadence-clone gap. It needs a source
   *URL/domain* at evaluation time, which the API already receives (`source_id`,
   context) but does not currently feed to scoring.
2. **It is not sufficient alone** (recall ~20% on the low tail). The remaining
   low-reliability class — fake-news content on ordinary domains — requires a
   *content-credibility* signal (claim-density, sensationalism, citation
   patterns), which is the larger NLP work item.
3. **Keep the leakage discipline**: score from domain structure and a maintained
   brand list, never from the labelled disinfo set, or the validation numbers
   become circular.

This spike is intentionally **not** wired into the production pipeline: adding a
scoring signal changes band semantics and needs its own calibration and
re-validation. The evidence above is to inform that decision, not pre-empt it.

## Update — integrated (ENGINE 1.4)

The maintainers approved integration. Domain-provenance ships **not** as a fifth
weighted signal but as an **asymmetric post-aggregation penalty**
(`score − 0.6 × domain_red_flag`, clamped at 0) — a symmetric weighted term
would reward clean domains and inflate the low tail, since most fake-news lives
on ordinary domains scoring 0. The four calibrated behavioural weights are
unchanged. Re-validated through the *production* scoring path
(`cats.scoring.engine` + `cats.signals.domain_provenance`) on the same future
holdout: concordance **0.755 → 0.775**, Spearman **+0.553 → +0.595**, all three
corrections low-reliability clones. Reproduce with
`research/validate_domain_penalty.py`. See `docs/architecture.md` →
*Domain-provenance penalty*. The content-credibility signal for the low-recall
tail (fake-news on ordinary domains) remains the open work item.
