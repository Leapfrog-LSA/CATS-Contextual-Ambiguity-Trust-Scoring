# Calibration input data

## `Fonti_OSINT.csv`
OSINT source catalogue v5.25, 2026-06-17 (5 275 sources, 311 with an RSS feed;
the human-readable consolidated edition lives in
[`Fonti_OSINT_CONSOLIDATO.md`](Fonti_OSINT_CONSOLIDATO.md)). Input for
`python -m cats.calibration.label_from_ratings --sources data/Fonti_OSINT.csv`.
v5.25 adds three non-RSS data sources (FRED, Finnhub, AISStream) over v5.22 —
the RSS-bearing set is unchanged, so `labels.jsonl` is identical under both.

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

## Pipeline outputs (merged snapshots 2026-07-02/03/05)
`labelled_sources.jsonl` = `merge_snapshots` over the three snapshots in
`data/snapshots/` (50 sources / 3 426 messages), temporal 80/20 split
(`train_sources` / `holdout_sources`), built datasets (`train.jsonl` /
`holdout.jsonl`, `COHERENCE_BACKEND=sbert`) and `calibrated_weights.json`
(spearman, seed 7, **v1.3.0 polarity-corrected engine** — weights calibrated
under ≤ 1.2.x are invalid). Numbers and analysis in
`docs/calibration_findings_2026-07.md`. ⚠️ Caveat: mainstream feeds publish
hourly, disinfo sites sporadically, so the temporal split puts every low-label
source in *train* — low-end discrimination is currently measured on the
full-dataset diagnostic; validate against a **future** snapshot (tracked).
