# Calibration input data

Licensing and attribution for every file here: [`DATA_LICENSE`](../DATA_LICENSE)
and [`NOTICE.md`](../NOTICE.md). The message texts in `*_sources.jsonl` and
`snapshots/` belong to their publishers. `python research/text_inventory.py`
lists them per source and by length.

## `Fonti_OSINT.csv`
OSINT source catalogue v5.25, 2026-06-17 (5 275 sources, 311 with an RSS feed at release, 287 after the 2026-11-09 dead-feed cleanup in `docs/feed_health_2026-07.md`;
the human-readable consolidated edition lives in
[`Fonti_OSINT_CONSOLIDATO.md`](Fonti_OSINT_CONSOLIDATO.md)). Input for
`python -m cats.calibration.label_from_ratings --sources data/Fonti_OSINT.csv`.
v5.25 adds three non-RSS data sources (FRED, Finnhub, AISStream) over v5.22 —
the RSS-bearing set is unchanged, so `labels.jsonl` is identical under both.

## `ratings.csv` — distant-supervision reliability ratings
`domain,rating` for **107** of the catalogue's unique RSS-bearing domains (104
at the 2026-07-02 collection plus 3 Italian outlets added later),
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
  the 107 matched domains under-represent the catalogue's Italian long tail.
- The label distribution has **no Low/Very Low** sources (51 High,
  30 Mostly Factual, 24 Mixed, 2 Very High): calibration will mostly learn to
  rank the upper-middle of the scale. Adding a few known-unreliable feeds
  would widen the ordinal spread.
- Domain-level ratings apply to every path under the host, and ratings carry
  MBFC's own editorial perspective — treat results as indicative
  (distant-supervision caveats in `docs/eu_ai_act/data_governance_art10.md`).

## `disinfo_sources.csv` — known low-reliability sources
Curated registry of documented disinformation/fake-news domains (114 rows,
deduplicated): the Russian **Doppelganger** clone network (Qurium 2022-09-27,
DFRLab/DOJ 2024 — forensic attribution) and the Italian *bufale* network plus
known fake-news factories (BUTAC/Bufalopedia, Repubblica). Columns include the
impersonated outlet, attribution, evidence level and a `cats_flag`
(`disinformation_clone | fake_news_site | fake_news_portal | satire_recognizable
| suspect_source`).

Used to widen the ordinal spread of `labels.jsonl`: domains flagged
`fake_news_site | disinformation_clone | fake_news_portal` whose RSS feed is
still alive are appended with label **10.0** (MBFC "Very Low" equivalent —
membership in a documented disinformation network is stronger evidence than a
rating). `satire_recognizable` entries (declared satire, e.g. Lercio, The
Onion) are **excluded** from labels: satire is not disinformation and MBFC does
not place it on the factual-reporting scale. `suspect_source` entries are
people/organisations without feeds and are ignored. Of the 87 probed domains,
11 had a live feed on 2026-07-02 (most Doppelganger clones are seized/offline).

## `cred1_current.csv` — external reference dataset (not used in any pipeline)
Snapshot of [CRED-1](https://github.com/aloth/cred-1) (© Alexander Loth, CC BY 4.0),
which aggregates OpenSources.co (CC BY 4.0, Melissa Zimdars et al.) and the
Iffy.news Index (MIT, Reynolds Journalism Institute). 2 674 domains with a
`category` (fake/conspiracy/unreliable/satire/mixed/reliable/rumor) and a
0.0–1.0 `credibility_score`, plus enrichment fields (Tranco rank, domain age,
fact-check claim count, Google Safe Browsing flag).

**Not imported into `labels.jsonl`, `disinfo_sources.csv`, or any signal.**
Evaluated as a calibration/watchlist source (2026-08-28) and rejected for that
purpose: `category`/`credibility_score` do not map onto `cats_flag`/
`evidence_level` as used here (see `disinfo_sources.csv` above — different
taxonomy, different axis), there is no import pipeline, and coverage of the
domains CATS actually tracks is thin (12%, see below). Kept only as a
manual cross-check reference — `research/cred1_lookup.py` looks up a single
domain; `research/compare_satire.py` and `research/compare_all_flags.py`
compare its labels against `disinfo_sources.csv` domain-by-domain.

Coverage/agreement against `disinfo_sources.csv` (2026-08-29, re-run
`research/compare_all_flags.py` for a fresh count): only 14 of 114 CATS-known
domains (12%) also appear in CRED-1, and of those 14, 5 (36%) disagree on
category — in both directions. Zero of the 50 Doppelganger-style clone
domains are covered at all (CRED-1 tracks editorial credibility, not
domain/infrastructure impersonation). Treat any single CRED-1 label as a
starting point to check by hand, not a verdict.

## `labels.jsonl`
Output of step 1 (`label_from_ratings`) over the catalogue + ratings above
(141 sources, labels 50–95), **plus** 11 very-low (10.0) sources appended from
`disinfo_sources.csv` as described above, **plus** 8 MBFC-rated Low (30.0) /
Very Low (10.0) outlets with live RSS feeds appended directly (Natural News,
Global Research, Before It's News, Activist Post, WND, Veterans Today, RT News,
David Icke — ratings re-verified on the linked MBFC pages on 2026-07-05, rows
in `ratings_provenance.csv`; they are appended rather than joined because they
are not in the `Fonti_OSINT` catalogue), **plus** 3 more Italian High-rated
outlets added directly to the catalogue+ratings join since (`repubblica.it`,
`open.online`, and `lastampa.it` — the last added 2026-08-30, see
[`dataset_expansion_runbook.md`](../docs/dataset_expansion_runbook.md)) —
**163 total**. Next step:

```bash
python -m cats.calibration.collect_rss --labels data/labels.jsonl --out labelled_sources.jsonl
```

## `human_labels.jsonl` — human score-disagreement labels

Empty at first; grows as reviewers file "score feedback" issues (see
`.github/ISSUE_TEMPLATE/score_feedback.yml`) or use the public demo/API
contest flow. Schema, `validate(path)` and `append(record)` live in
`cats/calibration/human_labels.py`; `research/ingest_score_feedback.py`
turns a saved GitHub issue body into a draft record for review. One JSON
object per line:

```json
{
  "source_url": "https://example-news-outlet.it/rss",
  "domain": "example-news-outlet.it",
  "cats_score": 67.3,
  "cats_band": "medium_high",
  "engine_version": "1.4",
  "cats_version": "1.7.0",
  "human_band": "high",
  "reason": "Consistent daily cadence for 3+ years, no clone domain flags; the silence signal is penalising a source that simply publishes weekly.",
  "date": "2026-09-16",
  "provenance": "issue",
  "issue_url": "https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring/issues/123"
}
```

`cats_band`/`human_band` must be one of the five CATS bands, `cats_band`
must match `determine_band(cats_score)`, and `issue_url` is required when
`provenance` is `"issue"`. `provenance` is one of `issue | demo |
api_contest`.

**Use is validation-only, and always will be: never signal input.** These
are human disagreements with a score, not ground truth — feeding them into
the signals or the weighted aggregation would let the same disagreement both
grade CATS and train it (leakage). The intended use is comparing CATS's
ranking against these human verdicts, the same validation role
`data/labels.jsonl` plays for distant-supervision ratings but sourced from
people instead.

## Pipeline outputs
`data/snapshots/` now holds 67 snapshots (2026-07-02 → 2026-09-30; daily
collection continues in the `cats-snapshots` data repo). The files here come
from two different runs:

- **July 3-snapshot run (merged snapshots 2026-07-02/03/05):**
  `labelled_sources.jsonl` = `merge_snapshots` over those three snapshots
  (50 sources / 3 426 messages), its temporal 80/20 split (`train_sources` /
  `holdout_sources`) and the built `holdout.jsonl` (`COHERENCE_BACKEND=sbert`).
  Numbers and analysis in `docs/calibration_findings_2026-07.md`. Caveat of
  that run: mainstream feeds publish hourly, disinfo sites sporadically, so the
  temporal split put every low-label source in *train*.
- **August 2026 silence-retune cycle:** `train.jsonl` (56 sources),
  `holdout_future.jsonl` (53 sources, a **future** holdout the calibrator never
  saw) and `calibrated_weights.json` (spearman; `news` weights 0.410 / 0.042 /
  0.543 / 0.006 for coherence / volatility / silence / gaming) are this run's
  outputs, on the same 56/53-source split as the 07-28 baseline — see
  [`docs/silence_retune_2026-08.md`](../docs/silence_retune_2026-08.md). The
  future-holdout validation is recorded in
  [`docs/calibration.md`](../docs/calibration.md) §3 (concordance 0.750,
  Spearman +0.554); scores remain **ordinal**, not calibrated probabilities.
  Weights calibrated under ≤ 1.2.x (before the polarity fix) are invalid.
