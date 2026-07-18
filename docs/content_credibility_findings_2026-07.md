# Content-credibility signal — spike findings (July 2026)

Reproducible via [`research/content_credibility_spike.py`](../research/content_credibility_spike.py)
(reads only committed data: the 06-Jul snapshot messages + the aligned
`data/holdout_future.jsonl` labels).

## Why this signal was tried

The [domain-provenance work](signal_research_2026-07.md) closed the
regular-cadence-clone gap but explicitly left one class uncovered: **fake-news
content on ordinary domains** — plausible-looking text on an unremarkable
domain, invisible to the four behavioural signals *and* to the domain penalty.
The candidate signal reads the message **text**: a style red-flag from
capital-letter shouting, clickbait punctuation, a bilingual hyperbole/absolutist
lexicon, minus an attribution-verb credit. Leakage discipline as everywhere
else — general text style only, never membership in `data/disinfo_sources.csv`.

## Method note that decides the result

In the July 2026 registry the low tail (label 10) is **Italian** and the high
tail (label 85) is **mostly English** international outlets. So any feature that
merely separates Italian from English scores a spurious correlation with the
label. The spike therefore reports the raw correlation **and** the
within-Italian correlation (language detected with `cats.pipeline.language`);
only the latter is evidence of a real content signal.

Aggregation is **per message** (mean of per-message style scores), not over the
concatenated history: a disinfo outlet is characterised by *consistent*
sensationalism, and blob-averaging dilutes a shouty headline among many clean
sentences. Per-message aggregation is ~2–3× more discriminative on the raw axis.

## Results (future holdout, n=53)

| Measure | ρ vs label |
|---|---:|
| Raw content red-flag | **−0.331** |
| **Within-Italian (n=8)** | **+0.082** |
| Within-non-Italian (n=45) | −0.317 |

Orthogonality (rho vs the behavioural signals): coherence −0.06, gaming −0.11
(independent), but volatility +0.14 and silence +0.21 (partial overlap).

Low vs high tail mean red-flag: low (≤30) 2.7 vs high (≥70) 1.0; within Italian
4.0 vs 1.7.

## Honest read — the signal is NOT validated on this data

1. **The raw −0.331 is the language confound, not credibility.** Within the
   Italian sources — where the actual low tail lives — the correlation
   collapses to **+0.082** (noise, and n=8 is far too small to conclude
   anything). The number looks good only because Italian tabloid-style RSS uses
   more caps/punctuation than English wire copy.
2. **The feature barely fires.** Even low-tail Italian sources score ~0.6–4.0
   out of 100; the within-Italian low>high separation rests almost entirely on
   a single overt-ALL-CAPS outlet (*Il Corrispondente*, 12.7). Modern
   disinformation RSS text is mostly clean prose — fabricated-but-plausible
   claims (the `worldnewsdailyreport` class) are not caught by surface style.
3. **The committed registry cannot test this signal.** n=8 Italian (n=5 low
   tail) makes the one number that matters uninterpretable.

## Recommendation (decision for the maintainers)

**Do not wire content-credibility into scoring yet.** Surface style is
directionally plausible but unproven here, and its apparent value on the current
data is a language artefact. This is a hard block on the dataset work
(roadmap: a larger, **language-balanced** labelled set with a real low tail):
until Italian low-reliability and Italian high-reliability sources both exist in
quantity, the confound cannot be removed and the signal cannot be calibrated or
validated. Two directions for when that data exists:

- keep the surface-style features but treat them as one input among several;
- add a genuine content dimension surface style misses — claim/fact structure,
  which needs real NLP (entailment / claim detection), the larger work item.

As with every candidate signal, wiring it changes band semantics and requires
its own calibration + future-holdout re-validation (`CLAUDE.md`). This spike is
evidence for that decision, not a pre-emption of it.

## The dataset gap, quantified — what to collect

The confound above is not specific to the 53-source holdout. Measured across
**all** sources that have collected text (every snapshot merged, n=59) via
[`research/dataset_language_balance.py`](../research/dataset_language_balance.py):

| Language | low (≤30) | mid (31–69) | high (≥70) | total |
|---|---:|---:|---:|---:|
| Italian | 5 | 1 | 3 | 9 |
| non-Italian | 11 | 4 | 35 | 50 |

ρ(is_italian, label) = **−0.265**: "being Italian" alone predicts a low label,
because Italian sources cluster in the low band while the high band is almost
entirely English. Any content feature is therefore contaminated until the set
is balanced.

**Concrete collection target** (to make language roughly independent of the
label): add **~41 Italian sources**, overwhelmingly **high-reliability** ones
(~32 — the scarcest cell: only 3 today vs 35 English), plus ~6 low and ~3 mid.
This is also the path to the ≥100-source future holdout the v2.0 accuracy
target needs. It requires a **network session** (RSS/MBFC access) — the
existing pipeline (`collect_rss` → `label_from_ratings` → `merge_snapshots` →
`split` → `build_dataset`) already does the collection; only the source list
and a network-enabled run are missing. No feeds are invented here.
