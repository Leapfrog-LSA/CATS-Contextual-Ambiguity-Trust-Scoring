# Calibration input data

## `Fonti_OSINT.csv`
OSINT source catalogue v5.22 (5 272 sources, 311 with an RSS feed). Input for
`python -m cats.calibration.label_from_ratings --sources data/Fonti_OSINT.csv`.

## `ratings.csv` — distant-supervision reliability ratings
`domain,rating` for **104 of the 310** unique RSS-bearing catalogue domains,
on the Media Bias/Fact Check *Factual Reporting* scale
(`Very High | High | Mostly Factual | Mixed | Low | Very Low`) — use
`--ratings data/ratings.csv --scale mbfc`.

### Provenance and method
- Every rating is the **Factual Reporting** level assigned by
  [Media Bias/Fact Check](https://mediabiasfactcheck.com) (MBFC) to that outlet;
  the per-domain MBFC page and retrieval date are recorded in
  [`ratings_provenance.csv`](ratings_provenance.csv). Ratings were collected on
  2026-07-02 via web search over MBFC's public pages (one query per domain;
  low-probability long-tail domains — mostly Italian regional/trade press —
  were probed with grouped/sampled queries). No rating was invented: domains
  MBFC does not cover are simply absent and are dropped by the joiner.
- **Attribution:** ratings are © Media Bias/Fact Check and are used here as
  factual reference data for research/calibration with attribution. Re-verify
  against the linked MBFC pages before any redistribution; MBFC updates
  ratings over time.

### Caveats (see also `docs/calibration.md`)
- MBFC coverage skews to English-language and major international outlets:
  the 104 matched domains under-represent the catalogue's Italian long tail.
- The label distribution has **no Low/Very Low** sources (48 High,
  30 Mostly Factual, 24 Mixed, 2 Very High): calibration will mostly learn to
  rank the upper-middle of the scale. Adding a few known-unreliable feeds
  would widen the ordinal spread.
- Domain-level ratings apply to every path under the host, and ratings carry
  MBFC's own editorial perspective — treat results as indicative
  (distant-supervision caveats in `docs/eu_ai_act/data_governance_art10.md`).

## `labels.jsonl`
Output of step 1 (`label_from_ratings`) over the two files above: one
`{source_id, source_type, label, url, rss}` per matched source. Next step:

```bash
python -m cats.calibration.collect_rss --labels data/labels.jsonl --out labelled_sources.jsonl
```
