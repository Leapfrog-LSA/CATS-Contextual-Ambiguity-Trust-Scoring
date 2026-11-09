# Coverage probe on the OSINT watchlist catalogue — 2026-11-09

A one-off run of CATS over every RSS feed in the public catalogue of
[`Leapfrog-LSA/osint-sources-disinfo-watchlist`](https://github.com/Leapfrog-LSA/osint-sources-disinfo-watchlist)
(`Fonti_OSINT.csv`, commit `0fee456`, 6,028 sources, 1,105 with a feed).

> **What this is, and is not.** It is a **coverage and robustness** test:
> whether CATS runs at eight times the size of its labelled registry, how many
> feeds give it usable evidence, and how scores spread across languages. It is
> **not** an accuracy test. These feeds have no reliability labels, so no score
> here can be called right or wrong. Scores are **ordinal**, not calibrated
> probabilities (WP 4.1/4.3).
>
> **Aggregates only.** Per the rule set for the observatory
> (`research/observatory_aggregate.py`), this report names no source. No message
> text was stored: each feed was fetched, parsed and scored in memory.

## Method

- **Feeds:** the 1,088 unique feed URLs of the catalogue. 236 of them are
  also in CATS's `data/Fonti_OSINT.csv`, and 852 are not.
- **Fetching:** one fetch per feed on 2026-11-09, from a cloud egress, with
  the collector's own code (`cats.calibration.collect_rss.fetch_feed` and
  `parse_feed`). The status rules are those of `research/feed_health_audit.py`:
  `stale` means the newest item is more than 14 days old, `dead` means 404/410
  or a connection failure, and `blocked` means 403/429 or a timeout.
- **Scoring:** `cats.lite.score` on CATS `main` (ENGINE 1.4, calibrated
  weights, default NER coherence backend), with the outlet's homepage passed
  for the domain-provenance check. `source_type` was `news` for the media
  category and `default` for the rest.
- **No Tranco table:** `data/tranco_top1m.csv` was absent, as in a default
  install.
- **Not used:** the watchlist's `disinfo_sources_master.csv`. It is almost the
  same list as CATS's `data/disinfo_sources.csv` (107 of 108 domains), which
  CATS already uses for its labels. Scoring it would be circular (leakage
  discipline, `CLAUDE.md`).

## Reachability (1,088 feeds)

| Status | All | Also in CATS catalogue (236) | New to CATS (852) |
|---|---:|---:|---:|
| ok | 777 | 148 | 629 |
| stale | 75 | 1 | 74 |
| blocked | 82 | 24 | 58 |
| not-xml | 82 | 27 | 55 |
| dead | 72 | 36 | 36 |

`blocked` results depend on the egress and are not evidence that a feed is
dead.

## Scoring (852 feeds that returned messages)

| Measure | Value |
|---|---|
| Scoring errors | 0 |
| Degraded signals (NLP unavailable) | 0 |
| Messages per feed (median) | 15 |
| Sufficient evidence (≥ 3 messages) | 845 |
| Language detected | other 737 (86%), italian 110, unknown 5 |
| Bands | medium 704 (83%), low 89, medium_high 51, high 6, very_low 2 |
| Score, median (10th–90th percentile) | 51.3 (39.1–58.9) |
| `requires_human_review` | 194 |

## Findings

1. **Scores bunch in the middle.** 83% of feeds land in `medium`, and 80% of
   scores fall between 39 and 59. There are two causes, both known limits:
   - **One fetch is not a history.** `silence` is 0 for most feeds, because a
     single feed snapshot has no long gap to detect.
   - **Coherence is mostly inert outside Italian.** The default backend
     compares spaCy Italian named entities across messages. Coherence was
     above 0 in 65% of the Italian feeds but only 37% of the others.

   A more informative spread needs a multi-day collection, and better
   non-Italian support (2027 roadmap). Coherence is near-inert on the NER
   backend even in Italian, as the README says.
2. **All 6 `high` scores are artefacts of a one-message feed.** Each had
   exactly one message, and 5 of the 6 were stale (one since 2010). With fewer
   than two messages, `coherence` returns 100 at zero confidence
   (`reason: insufficient_messages`), and the weighted mean still counts that
   100 at full weight.
   - **Already caught by the evidence guardrail:** CATS already reports these
     as `evidence.sufficient = false` and forces `requires_human_review`.
   - **But the score is still shown:** it reads as "high". This is the open
     residual of risk R5 in `docs/eu_ai_act/risk_management_art9.md`.
     Changing the score is a signal change, so it waits for the recalibration
     cycle. Until then the behaviour is documented in the README and
     `docs/api.md`.
3. **The `low` band mostly reflects silence and language, not unreliability.**
   Of the 91 feeds in `low` / `very_low`, 47% were stale (median `silence`
   73.7), and 93% were not Italian.
4. **Without the Tranco table, the domain-provenance penalty hits 6 legitimate
   outlets out of 852 (0.7%).**
   - **The flags:** two typo-squat flags (short distance from a brand domain),
     three `suspicious_tld` flags on `.online`, and one `free_host` flag
     (blogspot).
   - **Already known:** these are the cases in
     `docs/domain_provenance_maintenance_2026-09.md` and `-2026-10.md`. With
     the Tranco table loaded, the ranked `.online` outlets are exempt.
   - **Depends on a decision:** shipping that table depends on the Tranco
     licence check, which is open for the maintainer.
5. **CATS's own catalogue has stale feed URLs.** Of the 236 feeds shared with
   CATS's `data/Fonti_OSINT.csv`, 36 were `dead` and 27 `not-xml` on this
   egress.
   - **No effect on collection:** these are catalogue rows outside the labelled
     registry, so they don't affect daily collection. The feed-health rounds
     cover the registry only.
   - **Before any fix:** a cleanup should re-check each feed from another
     network, and first decide which of the two diverging catalogue copies is
     the source of truth.

## Reproducing

The probe script was not committed. It was a single-use run, and keeping it
out avoided any risk of storing texts. To repeat the run:
- for each catalogue feed, call `fetch_feed` + `parse_feed`, then
  `cats.lite.score(messages, source_type=…, explain=False, url=homepage)`;
- keep only the status, message count and score fields, never the texts.
