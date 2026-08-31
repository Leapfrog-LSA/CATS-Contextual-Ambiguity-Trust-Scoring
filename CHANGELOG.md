# Changelog

All notable changes to CATS are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- **Volatility source-relative (z-score) normalization research spike —
  result: not shipped, promising lead flagged for revisit**
  (`research/volatility_normalization_spike.py`,
  `docs/volatility_source_relative_spike_2026-08.md`). Raised in review:
  the current spike threshold is global (same cutoff for every source
  regardless of its natural tone variance); tested normalizing each
  sentiment delta against the source's own mean/std instead. At one point
  in the sweep (k=1.5) this beats production on both splits (train −0.326,
  holdout −0.210 vs. the shipped −0.141/−0.151) — but one step away in the
  same grid (k=2.0) the sign flips positive and gets stronger positive
  still at k=2.5, the same instability pattern that disqualified
  `claim_density` in the content-credibility spike. A hybrid
  (absolute-floor + z-score) design reaches an even stronger holdout ρ
  (−0.352) at the same k=1.5 but shows the identical flip at k=2.0 across
  every floor tried — the instability is a property of the z-score
  threshold itself, not the near-zero-variance edge case the floor was
  meant to guard against. Not shipped on this evidence; flagged as the
  most promising of the recent spikes (unlike the two rejected below) —
  the sign-flip's consistency across 5 independent floor settings suggests
  a real "grading a source on its own curve" mechanism worth re-testing
  once a larger future holdout can tell a genuine k-dependent effect apart
  from a sample artifact.
- **CRED-1 cross-check reference tools (`research/`), evaluated and not
  integrated into any pipeline.** `data/cred1_current.csv` is a snapshot of
  [CRED-1](https://github.com/aloth/cred-1) (© Alexander Loth, CC BY 4.0,
  aggregating OpenSources.co and the Iffy.news Index). Considered as a
  calibration/watchlist source and rejected for that purpose: its
  category/credibility_score taxonomy doesn't map onto `cats_flag`/
  `evidence_level`, there's no import pipeline, and coverage of domains CATS
  already tracks is thin. Kept only as a manual, read-only reference:
  `research/cred1_lookup.py` looks up one domain by hand;
  `research/compare_satire.py` and `research/compare_all_flags.py` compare
  its labels against `data/disinfo_sources.csv` domain-by-domain. Findings
  from that comparison (14/114 CATS domains covered, 5/14 — 36% — disagree,
  zero coverage of the 50 Doppelganger clone domains) are in
  `data/README.md`.
- **`domain_provenance` popularity corroboration.** A domain already flagged
  by an existing structural rule (free-host/suspicious-TLD/typosquat) that is
  also absent from the Tranco top-1M now gets a +15 corroboration bonus.
  Deliberately never a standalone trigger: a 25-source sample of
  `data/Fonti_OSINT.csv` found 24% of legitimate catalogue sources (government
  subdomains, regional open-data portals, niche outlets) have no Tranco rank
  at all, so "unranked" alone would mislabel real institutional sources.
  The popularity table itself is **not committed** (22 MB, 1M rows) — fetch it
  with the new `make tranco-download` before evaluating URLs, same pattern as
  `make nlp-download` for the spaCy model; without it the signal degrades
  cleanly to pre-corroboration behaviour (unit tests mock the table instead
  of depending on the download). Re-validated through the production path
  (`research/validate_domain_penalty.py` on the 06-Jul future holdout, n=53,
  with the table present): aggregate concordance/Spearman unchanged
  (0.762/0.578, identical with and without the corroboration bonus) — the
  three already-corrected sources get a sharper penalty, no pairwise
  ranking flips on this holdout. `cats/signals/domain_provenance.py`,
  `cats/signals/types.py`, `cats/core/config.py`, `Makefile`.

### Fixed
- **Silence's 72h anomaly threshold was short of its plateau** — a sweep
  (`research/gaming_volatility_diagnosis_spike.py`) found rho strengthens
  monotonically from 24h to 96h then plateaus (96/120/168h identical), so
  96h is the smallest threshold reaching the full available gain.
  `SOURCE_TYPE_THRESHOLDS` changes from 72.0 to 96.0 for every source type
  (`cats/signals/silence.py`, `docs/silence_retune_2026-08.md`).
  `cats/calibration/split.py`'s `silence_blind_sources` picks the new value
  up automatically (reads `threshold_for`), which does mean a split whose
  window was fine at 72h can now be flagged blind at 96h — the diagnostic
  working as intended, not a regression.
- **Volatility's 0.4 spike threshold was locally the worst choice in the
  swept grid** — a finer 9-point sweep (`research/gaming_volatility_diagnosis_spike.py`)
  found 0.4 was the only point where the train-side correlation flipped to
  the semantically wrong sign (+0.028), while 0.3 gives the strongest,
  consistent −0.14/−0.15 on train/holdout. `compute_volatility`'s default
  `spike_threshold` changes from 0.4 to 0.3
  (`cats/signals/volatility.py`, `docs/volatility_retune_2026-08.md`). Does
  not raise the signal's hard ceiling: 48.9% of Italian messages carry
  TextBlob polarity exactly 0.0, invisible to this signal at any threshold.
- **Gaming's `vocab_score` silently double-weighted `ttr_score`** — the two
  sub-scores are mathematically identical above the 50-token floor (both
  compute `1 - unique/total`), diagnosed in `docs/signal_diagnosis_2026-07.md`
  but left in place pending the recalibration cycle it required.
  `compute_gaming`'s `value` is now the mean of the three genuinely distinct
  sub-scores (repetition, ttr, burst); `vocab_score` is still computed and
  returned for introspection, just no longer folded into `value`
  (`cats/signals/gaming.py`, `docs/gaming_redesign_2026-08.md`).
- **Round 12's `Il Corriere della Sera` fix didn't actually work** — caught the
  next morning when the daily collection run logged `feed carries a DTD;
  refusing to parse` for it. The round-12 replacement feed
  (`corriere.it/dynamic-feed/rss/section/cronache.xml`) was verified with an
  HTTP client that confirmed 200 + valid-looking XML with a recent `pubDate`,
  but never checked against the collector's own parser, which deliberately
  rejects any document carrying a `<!DOCTYPE` as an XXE guard
  (`cats/calibration/collect_rss.py`) — every URL under that feed system emits
  one, so the "fix" was permanently unusable regardless of which section was
  picked. Re-registered to the legacy `xml2.corriereobjects.it/rss/cronaca.xml`
  (no DOCTYPE, freshest surviving section on that system, 80 days stale vs the
  830-day-stale `homepage` it replaces) and verified this time by calling
  `cats.calibration.collect_rss.parse_feed` directly, not just an HTTP client.
  **`research/feed_health_audit.py`'s `classify()` now calls `parse_feed`
  itself** instead of a separate XML-shape heuristic, so `ok`/`stale` mean
  "the collector can actually use this" by construction — re-running the full
  registry with the corrected check also caught 5 more feeds (Natural News,
  Sixth Tone, The Hill Tech, Berlingske Business, Le Parisien) the old
  heuristic had been silently over-crediting as `ok`. See
  `docs/feed_health_2026-07.md` → *Round 12 correction*.

### Changed
- **Weights recalibrated after the silence retune, future-holdout
  revalidated** (`data/calibrated_weights.json`, `data/train.jsonl`,
  `data/holdout_future.jsonl`, `docs/silence_retune_2026-08.md`). Same
  protocol, run on top of the volatility-retune baseline just below:
  concordance 0.750, Spearman +0.554 (was 0.750 / +0.556) — movement inside
  GA noise, still clears the 0.70 criterion. The `news`-group silence weight
  moves 0.502 → 0.543, consistent with the signal now carrying more
  information at the retuned threshold.
- **Weights recalibrated after the volatility retune, future-holdout
  revalidated** (`data/calibrated_weights.json`, `data/train.jsonl`,
  `data/holdout_future.jsonl`, `docs/volatility_retune_2026-08.md`). Same
  protocol, run on top of the gaming-fix baseline just below: concordance
  0.750, Spearman +0.556 (was 0.753 / +0.551) — movement inside GA noise,
  still clears the 0.70 criterion. The `news`-group volatility weight moves
  0.038 → 0.059, a small increase consistent with the signal now carrying
  slightly more, correctly-signed information.
- **Weights recalibrated after the gaming fix, future-holdout revalidated**
  (`data/calibrated_weights.json`, `data/train.jsonl`,
  `data/holdout_future.jsonl`, `docs/gaming_redesign_2026-08.md`). Same
  protocol as the declared 28-Jul validation (train = merged 02/03/05-Jul
  snapshots, holdout = the untouched 06-Jul snapshot, GA `--metric spearman
  --seed 7`), rebuilt with the fixed gaming signal: concordance 0.753,
  Spearman +0.551 (was 0.755 / +0.553) — no material regression, still clears
  the 0.70 production criterion. The `news`-group gaming weight drops from
  0.059 to 0.011: the calibrator now credits gaming close to its true
  near-zero marginal value instead of partially rewarding the duplicated ttr
  term.

### Added
- **Cross-source corroboration research spike (roadmap item 11) — result:
  feasibility check failed, registry not built**
  (`research/cross_source_corroboration_spike.py`,
  `docs/cross_source_corroboration_spike_2026-08.md`). A per-source
  corroboration rate (lexical overlap with another source's message within
  ±48h) initially looked like a real signal — ρ +0.328 train / +0.290
  holdout / +0.316 pooled, stable sign and magnitude, unlike the
  content-credibility spike below. Inspecting the matches found 88%
  (284/321) were **one source pair** (CNET↔Mashable) sharing a daily
  templated puzzle-hint column format, not genuine story corroboration;
  removing it drops the correlation 20-25% and what remains is spread
  across only ~14 of ~5,900 possible source pairs (20 of ~109 sources ever
  register a match). Recommendation: do not build the cross-source
  registry the roadmap flagged as a real data-design cost — the
  feasibility check this item asked for failed, closing the decision
  point. Not wired into scoring; no production code changed.
- **Content-credibility signal research spike (roadmap item 10) — result:
  do not integrate** (`research/content_credibility_spike.py`,
  `docs/content_credibility_spike_2026-08.md`). Tested three EN/IT
  lexicon-based sub-scores named in the roadmap (sensationalism, claim
  density, citation/attribution) against the same train/holdout split used
  for this week's threshold retunes. None clears the noise bar (|ρ| ≤ 0.18
  on the future holdout — the same magnitude as gaming's dead sub-scores);
  `claim_density`, the only one with real magnitude, flips sign between
  train (+0.056) and holdout (−0.179), the same instability pattern that
  flagged volatility's old 0.4 threshold. Lexicons were fixed before any
  correlation was computed (leakage discipline). Recommendation: a real
  content-credibility signal needs model-based features (claim extraction,
  hedging classification, or an LLM judge), not keyword lists — a
  materially bigger investment not justified by this spike alone. Not
  wired into scoring; no production code or calibrated weights changed.
- **10 catalogued-but-feedless registry rows given working feeds, passing the
  ≥100-source calibration target for the first time (round 13 addendum)**
  (`data/labels.jsonl`, `data/Fonti_OSINT.csv`, `docs/feed_health_2026-07.md`).
  49 registry rows carried a label and URL but no `rss`; checked known
  feed-path patterns (`feeds.bbci.co.uk`, RFI's `/rss` suffix, standard CMS
  paths) for the most valuable of them and verified each through
  `collect_rss.fetch_feed` + `parse_feed` directly before writing. **10
  filled in**: `BBC News`, `BBC News World`, `BBC Science & Environment`,
  `BBC Arabic`, `RFI English`, `RFI Français`, `Le Monde`, `France 24`,
  `The Independent`, `The Hill`. **2 candidates found but rejected**: the
  only working Al Jazeera and Foreign Policy feeds found are already
  registered under `Al Jazeera Africa` and `Foreign Policy Africa`
  respectively — assigning either to the bare `Al Jazeera English` /
  `Foreign Policy` rows would have reproduced the round-9 Ukrainska Pravda
  bug (two source_ids double-counting one feed), caught this time by
  checking every candidate against the registry before writing, not after.
  Combined with round 13's 3 curl-recovered sources: 13 net-new reachable
  sources, taking the registry past the roadmap's ≥100-source target for the
  first time — pending confirmation from an actual collection run, since the
  merged-snapshot count is what actually matters.
- **`collect_rss.fetch_feed` retries a 403 via `curl` before giving up,
  recovering 3 of 15 `blocked` feeds (round 13)**
  (`cats/calibration/collect_rss.py`, `research/feed_health_audit.py`,
  `docs/feed_health_2026-07.md`). Three feeds long classified `blocked`
  (`al-monitor.com`, `hrw.org`, `rnz.co.nz`) turned out to be blocking
  httpx's specific TLS/HTTP client fingerprint, not the IP or User-Agent
  string: `curl`, same network, same UA, gets a clean 200. The fallback
  lives in the collector itself, not just the audit script, so every future
  collection run benefits, not only this one; the other 12 `blocked` feeds
  stay 403 under curl too — confirmed IP/geo or JS-challenge blocks, a
  genuinely different class curl can't cross. `RNZ Pacific`'s registered
  `/rss` also turned out to resolve to the homepage, not a feed; corrected
  to `/rss/pacific.xml`, found once curl confirmed the domain wasn't blocked.
  A bug in the first version of this fix was caught before shipping: `curl`
  without `--fail` exits 0 on an HTTP 4xx and returns the WAF's challenge
  page as if it were the feed body, which `parse_feed` was then rejecting
  for the misleading reason "carries a DTD" (an HTML error page's own
  `<!DOCTYPE html>`) instead of correctly staying `blocked` — added `--fail`
  and re-verified all three recoveries plus a sample of the still-blocked 12
  individually before re-running the full audit. `research/feed_health_audit.py`
  inherits the fallback automatically, since it already calls
  `collect_rss.fetch_feed` (round-12-correction pattern). Net:
  `blocked` 15 → 12, `ok` 78 → 79, `stale` 12 → 13 — see
  `docs/feed_health_2026-07.md` → *Round 13*.
- **Feed-health audit gains a `stale` classification, and 4 stale feeds are
  fixed (round 12)** (`research/feed_health_audit.py`,
  `docs/feed_health_2026-07.md`). Follow-up to the same-day recalibration
  checkpoint's finding that 15 of 95 merged sources hadn't produced a new
  message in 30+ days despite being reachable and `ok`: `classify()` now
  compares each feed's own newest `<pubDate>`/`<updated>` against today
  (>14 days = `stale`, distinct from `ok`), since a feed can return HTTP 200 +
  valid XML forever while silently serving the same cached body — exactly
  what happened to `Il Corriere della Sera`'s registered feed, the source
  that motivated writing this script. Full-registry re-run found 11 `stale`
  feeds; **4 fixed, each verified live before updating the registry**: `Il
  Corriere della Sera` (its feed system moved to
  `dynamic-feed/rss/section/cronache.xml`, frozen since 2024-05-13 under the
  old URL), `The National UAE` (`.../category/uae/` emptied to 0 items,
  `.../category/news/uae/` still live), `Jerusalem Post`
  (`rssfeedsheadlines.aspx` frozen since 2025-06-16, `rssfeedsfrontpage.aspx`
  live), and `World Daily News Report` (feed URL now redirects to an
  unrelated site, `aidesociale.ca` — `rss` nulled rather than guessing a
  replacement, per the round-9 precedent). 7 low-value stale feeds and 2
  borderline cases (including `Crisis Group Alert`, label 95) investigated
  and flagged, not chased further — see `docs/feed_health_2026-07.md` →
  *Round 12*.
- **Recalibration checkpoint (2026-08-21): same-sign edge, smaller magnitude,
  plus two new data-quality findings** (`docs/calibration_findings_2026-08-21.md`).
  Re-ran the exact 07-25 message-axis pipeline on the pool grown from 59 to 95
  sources (~3 to ~7 weeks). The shipped weights still beat the static WP 4.1
  baseline (Spearman +0.078 vs +0.033, concordance 0.537 vs 0.515) — the 07-25
  finding replicates — but every margin shrank rather than grew (07-25:
  +0.127/0.563), and predicted-band diversity for the shipped weights
  collapsed (74/75 holdout sources called `medium_high`). Two contributing
  causes found: (1) two single-record timestamp bugs — a `1970-01-01` epoch
  sentinel (2 CNET messages, a missing-pubDate default, not a real date) and a
  future-dated CMS artifact (`La Repubblica`, stamped two weeks ahead via its
  own pre-scheduled URL) — that make `split.py`'s printed window diagnostic
  unreliable (it takes a plain pooled min/max) though the actual split point
  is essentially unaffected; (2) **15 of the 95 merged sources (16%) have not
  produced a new message in 30+ days**, several not in years, including
  `Il Corriere della Sera` (stale again, 830 days — the exact source that
  motivated writing `research/feed_health_audit.py` in the first place) and 8
  of the label-10 disinformation sources (already the scarcest class). These
  feeds are all audit-`ok` (HTTP 200, valid XML) — the round-11 audit checks
  reachability, not content freshness, so it cannot see this. `data/calibrated_weights.json`
  unchanged — this is a checkpoint, not a recalibration decision.

- **Feed-health audit round 11** (`docs/feed_health_2026-07.md`), prompted
  by the daily/weekly RSS collection sitting at 95 unique sources for weeks
  despite near-daily runs. Confirms the two are the same number: the
  registry's `ok` feed count *is* the calibration source ceiling, not a
  collection bug. No new recoverable feed found (unlike round 10's
  query-parameter fix) — two feeds newly reclassified `not-xml`
  (David Icke, News Examiner) are Cloudflare anti-bot interstitials
  returning 200/202, the same block class as the 15 already-`blocked`
  feeds and ITV News/L'Orient Today's persistent 404s, not a URL-drift case.
  Breaking the 95-source ceiling needs either a different network path for
  the 17 sandboxed feeds or registering genuinely new sources — not more
  collection runs against the current registry.

### Fixed
- **The weekly RSS collection workflow could silently clobber or lose a
  same-day snapshot** (`.github/workflows/collect-rss.yml`). It checks out
  `main` once at job start but can run well past its 06:00 UTC cron target
  if the runner queue is backed up; by commit time, another same-day
  snapshot (a manual or PR collection) may already be on `main`. The old
  script (`git add` + `git commit` + plain `git push`) had no way to notice:
  if its stale checkout still had the file, the eventual push either got
  rejected outright (losing that run's whole collection with nothing but a
  red Actions run to show for it) or, if it landed, replaced the file with
  this run's collection alone rather than the union both runs together
  should have produced — happened for real on 2026-08-10 (harmless only
  because that day's manual collection turned out to be a strict subset of
  the workflow's, verified after the fact with `merge_snapshots`, not by
  design). The commit step now re-syncs to `origin/main` immediately before
  each push attempt and, if a same-day file is already there, unions it with
  this run's collection through `cats.calibration.merge_snapshots` instead
  of overwriting it; a bounded retry (3 attempts) re-syncs and re-merges
  again if the push is rejected because `main` moved in the meantime.

### Added
- **The split now reports each side's observed window against the `silence`
  threshold**, so a holdout too short for that signal to vary is visible where
  it is produced instead of being diagnosed by hand afterwards. `silence` scores
  the share of inter-message gaps longer than 72 h, so a source whose whole
  history spans no more than 72 h scores a flat 0 because of the window it was
  given, not because of how it published. Each side now prints its window and a
  `silence-blind: K/N` count, warns when *no* source can register a gap (the
  signal is constant and any weight on it is unvalidated), and warns when at
  least a quarter of a side is blind (the distribution is compressed toward 0).
  On the seven merged snapshots to date both tiers fire: at the default
  fraction 0.2 the holdout window is 47 h and **64/64** sources are blind; at
  0.5 it is 360 h and 21/78 (27%) are. This is the calendar-time constraint
  from `docs/calibration_findings_2026-07-25.md` showing up as an inert signal.
- **Recalibration on the corrected split (2026-07-25): not shipped, but the
  production weights are now validated** (`docs/calibration_findings_2026-07-25.md`).
  With the message-axis holdout the 2026-07-24 blocker is gone, and the shipped
  weights beat the static WP 4.1 baseline on a holdout with real label spread at
  both split fractions tried (Spearman +0.127/+0.141 vs +0.043/+0.053;
  concordance 0.563/0.565 vs 0.515/0.527) — the evidence that was missing last
  time. The *candidate* weights were not shipped: they beat production at
  fraction 0.2 and tie at 0.5, with band agreement reversing between the two, so
  the sign of the difference depends on a split parameter and is noise at n≈46.
  `data/calibrated_weights.json` and the committed datasets are unchanged.
- **`build_dataset` now reports the active coherence backend** and warns when it
  is not `sbert`. The shipped weights assume SBERT; under the default `ner` the
  coherence signal is close to inert (mean 1.7 / sd 5.3 against 23.3 / 11.6 on
  the same sources) and its distribution collapses in the holdout, which
  silently inverts the conclusion of a weight comparison — every set scored at
  or below chance under `ner` and above it under `sbert`. `sentence-transformers`
  is an optional extra, so this degradation is the default state of a fresh
  environment and nothing previously surfaced it at runtime.

### Changed
- **The temporal calibration split now cuts message histories, not sources**
  (`cats/calibration/split.py`, new default `--axis message`). The previous
  axis ranked *sources* by their most recent message and held out the newest
  slice — degenerate on RSS data, because every live feed's newest message is
  hours old at collection time, so the ranking is really by publishing
  frequency, which is close to a proxy for the label:
  Spearman(recency, label) = **+0.539** on the 2026-07-20 snapshot. On the
  merged 59-source pool it produced a 12-source holdout of which 11 were
  labels 70/85, with the disinfo tail exiled to train because such sources
  publish irregularly — a holdout that cannot rank anything, and the reason
  the 2026-07-24 recalibration could not validate. The same pool on the
  message axis gives a 45-source holdout spanning five labels including four
  at label 10. The old behaviour is kept as `--axis source` (the right
  question once the pool's newest slice is label-diverse on its own), and both
  axes now print each side's label distribution and warn when a holdout has
  fewer than three distinct labels. **No weights were recalibrated here** —
  that is a separate change, gated on its own re-validation per `CLAUDE.md`.

### Fixed
- **The Citizen's registered RSS feed went dead** (`thecitizen.co.tz/rss.xml`,
  404). Found by a fresh feed-health re-audit (round 10,
  `docs/feed_health_2026-07.md`) run specifically to check whether the 15
  hosts flagged `blocked` in round 7 had quietly gone dead — they hadn't
  (still a clean HTTP 403, no ambiguity), but this previously-unflagged feed
  had. The site's own RSS autodiscovery link and the common `/feed/`, `/rss/`
  paths all dead-end or soft-404; the working endpoint takes the section as a
  query parameter instead of a path segment
  (`rss.xml?section=tanzania`). Verified live before updating
  `data/labels.jsonl` and `data/Fonti_OSINT.csv` (byte-exact, CRLF preserved
  on the CSV). Registry unchanged at 114 feeds — a URL correction, not a row
  added or removed.
- **`collect_rss` silently destroyed an existing snapshot at `--out`.** Snapshots
  are written to a dated filename, so two runs on the same day collided and the
  second truncated the first. That loses every source the earlier run reached
  and the later one could not, and the loss is irrecoverable: a feed exposes
  only its recent window. It cost a real source on 2026-08-01 — a manual
  collection at 08:49 UTC (90 sources / 3 341 messages) was replaced by a
  routine run at 09:11 (89 / 3 330) when **David Icke**'s feed happened to
  serve malformed XML on the second pass. Writing to an existing `--out` now
  **merges** into it through `merge_snapshots.merge_records`: messages unioned
  and deduplicated on `(timestamp, text)`, fresh metadata winning, and sources
  present in only one side retained. Replayed on that collision the merge keeps
  David Icke and yields 90 sources / 3 428 messages — 98 more than what landed.
  `--overwrite` restores the truncating behaviour deliberately, and an existing
  file that cannot be parsed is left untouched while the new run is written
  alongside as `.partial` rather than either one being lost.
- **The `SessionStart` hook reported success while installing nothing.**
  `.claude/hooks/session-start.sh` ran `pip install -e . -r requirements-dev.txt
  || true` and then printed `environment ready` unconditionally. On the current
  cloud base image that install aborts — the image ships a Debian-packaged
  `PyJWT` with no `RECORD` file, which pip cannot uninstall to satisfy the
  resolved version (`Cannot uninstall PyJWT 2.7.0, RECORD file not found`) — and
  `|| true` swallowed it, so sessions started with no `pytest`, no `httpx` and
  no `pydantic` while being told the environment was ready. The install now
  passes `--ignore-installed PyJWT`, prints the pip error when it still fails,
  and the closing line reports the *verified* state rather than the attempted
  one. The Setup script in `docs/cloud_setup.md` carried the same defect and
  gets the same flag plus an explicit post-install check.
- **Corrected the test-environment instructions in `CLAUDE.md` and
  `docs/cloud_setup.md`**, which told every session that `pytest` fails at
  collection without `CATS_API_KEY` / `DATABASE_URL` / `REDIS_URL` /
  `AUDIT_ENCRYPTION_KEY`. It does not: the test modules that import `Settings`
  supply their own via `os.environ.setdefault`, so with no env vars at all the
  full suite collects (225) and `tests/unit/` passes 208/208. The real hazard is
  the opposite one, and the docs said nothing about it — `setdefault` means an
  exported variable overrides the test's, so a `DATABASE_URL` without the
  `+asyncpg` driver makes SQLAlchemy demand `psycopg2` (not a dependency of this
  project) and collection fails with a `ModuleNotFoundError` that reads as a
  missing package rather than a malformed URL.
- **A source was counted twice in every calibration pass.**
  `Ukrainska Pravda` and `Ukrainska Pravda English` carried the same `rss`
  URL, so both collected the same Ukrainian feed: in the `2026-07-13` and
  `2026-07-20` snapshots the two rows hold byte-identical message payloads
  under two `source_id`s at the same label (70). `merge_snapshots`
  deduplicates messages *within* a `source_id`, which is the wrong axis to
  catch this, so nothing downstream noticed. The English row's `rss` is now
  blanked in `data/labels.jsonl` and `data/Fonti_OSINT.csv` — the source stays
  catalogued and labelled (feedless rows are kept by `label_from_ratings.py`
  and skipped by `collect_rss`), it simply stops collecting a duplicate.
  The real English-edition feed URL could not be verified — Cloudflare 403s
  every `pravda.com.ua` path from this network — so none was guessed.
  Registry: 115 → 114 feeds, no source or label removed.
  See `docs/feed_health_2026-07.md` → *Round 9*.

### Added
- **Shared-feed detection in the feed-health audit**
  (`research/feed_health_audit.py`): reports registry rows pointing at the
  same feed URL, offline and before any network call, normalising scheme /
  `www.` / trailing slash so the same feed written two ways still collapses.
  This is a dataset defect rather than a health one — the feed answers fine,
  it is the double-counting that hurts — and the previous audits had no way
  to surface it. Only one case existed (see *Fixed*).
- **Draft (non-binding) EU AI Act classification recommendation**
  (`docs/eu_ai_act/draft_recommendation_2026-07-24.md`): reasoned Annex III
  screening and a proposed conditional determination — not high-risk as
  currently distributed, with explicit re-assessment triggers for
  law-enforcement/migration/judicial deployers (Annex III points 6-8) and for
  any deployer treating a CATS score as determinative of a natural person's
  access to credit or essential services (point 5). Per CLAUDE.md this does
  **not** fill in `classification.md`'s Outcome table — that stays a TODO for
  a human/legal sign-off; the draft is linked from it as a starting point.
- **Recalibration re-attempted (2026-07-24): pipeline unblocked, not shipped.**
  The 2026-07-23 spaCy/`explosion-models` GitHub-scope block did not
  reproduce this session — `it_core_news_lg` downloads under the default
  *Trusted* network level with no `add_repo` grant needed. With full-fidelity
  NER available, the full merge → temporal-split → build → calibrate →
  validate pipeline ran end-to-end for the first time since 2026-07-06
  (folding in the two RSS snapshots collected post feed-repair that had never
  been merged), but the resulting candidate weights scored *worse* than both
  the static baseline and current production on the future holdout — traced
  to the 59-source pool's most-recent 20% clustering at label 70/85 with no
  mid-range spread, not a signal regression. Not shipped;
  `data/calibrated_weights.json` and the committed train/holdout files are
  unchanged. Findings and full numbers in
  `docs/calibration_findings_2026-07-24.md`; `docs/dataset_expansion_runbook.md`
  updated accordingly.
- **Feed-health audit tool** (`research/feed_health_audit.py`, findings in
  `docs/feed_health_2026-07.md`): checks every RSS feed in the label registry
  (read-only, the same GET the weekly collector issues) and classifies each
  ok / dead / not-xml / blocked. The first audit found only **64 of 126**
  registered feeds actually returned a feed — 35 dead (404/410), 10 HTML, so a
  third of the registry was silently producing nothing, biased toward the
  labels where the dead feeds clustered.
- **Two verified Italian high-reliability sources** — `repubblica.it` and
  `open.online`, both MBFC **High** read directly from the MBFC pages (feeds
  verified reachable): `data/ratings.csv`, `data/ratings_provenance.csv`,
  `data/labels.jsonl`. This is the scarce cell (Italian high tail).
- **Dataset-maintenance runbook** (`docs/dataset_expansion_runbook.md`): the
  verified pipeline sequence to add sources and keep the collection healthy,
  with a data-safety warning (see Fixed).
- **Community health files**: `CODE_OF_CONDUCT.md` (Contributor Covenant
  2.1), `.github/ISSUE_TEMPLATE/` (bug report, feature request), and
  `.github/pull_request_template.md` — `CONTRIBUTING.md` already referenced
  issue templates that didn't exist yet.

### Fixed
- **Closed the sibling-repo cross-check of the 11 nulled "no longer
  publishing RSS" sources** (round 8): compared `data/Fonti_OSINT.csv` and
  `data/disinfo_sources.csv` against `Leapfrog-LSA/osint-sources-disinfo-watchlist`
  (a public "v0.1" snapshot of the same underlying catalogue). No new sources
  either way — the disinfo watchlist is byte-identical (114/114), and the
  sibling's OSINT catalogue is a strict subset of this one. It did carry
  candidate RSS URLs for the 11 round-5-nulled sources; live-checked all 11
  and found nothing usable — 9 confirm dead, and the one that returned valid
  XML (TRT Africa's candidate) turned out to be TRT World's feed, a
  different outlet under the same broadcaster. No registry changes; this
  line of investigation is closed. Full findings in
  `docs/feed_health_2026-07.md` round 8.
- **Daily Maverick's dead feed fixed** (`https://www.dailymaverick.co.za/feed/`
  → `/rss/`): the round-7 flakiness between `403` and `404` across UA variants
  turned out to be two different signals colliding in one concurrent run, not
  one ambiguous host — a clean single-request recheck showed the homepage is
  reachable (unlike the 15 IP-blocked feeds) while the *registered* feed path
  is a genuine `404` (moved/renamed, confirmed by a real "not found" page, not
  a WAF challenge). Found the working replacement (`/rss/`, redirects to
  `/dmrss/`, verified with a same-day `pubDate` and live content across all
  four UA variants) and updated `data/labels.jsonl` + `data/Fonti_OSINT.csv`.
  Registry now **15 `blocked`** (all IP-level, none dead), **2 `dead`**
  (ITV News, L'Orient Today, environment-specific), **98 `ok`**.
- **Manually verified the 16 `blocked` feeds (round 7)**, each with four
  User-Agent variants (collector's own UA, Chrome desktop, a legitimate
  feed-reader/bot UA, no UA at all): 15 of 16 return an identical `403`
  regardless of UA, which is evidence of an IP/ASN-level block on this
  sandboxed session class (same conclusion already reached for ITV
  News/L'Orient Today), not a UA-string filter — left as-is, no registry
  changes, since nothing here distinguishes a genuinely dead feed from an
  IP block. Also fixed a **false positive found in the process**: Strafatti
  Quotidiani was flagged `blocked` on a transient WordPress.com `429` caused
  by the diagnostic script's own concurrent burst, not a real block —
  `research/feed_health_audit.py` now retries a `429` (with backoff) before
  classifying, which moved it back to `ok`. Also surfaced (not fixed — needs
  an editorial call, and the source is itself in the blocked set so can't be
  re-verified from here) a **registry duplicate**: Ukrainska Pravda and
  Ukrainska Pravda English share the identical `rss` URL, so the "English"
  row is not actually collecting English content. Full findings in
  `docs/feed_health_2026-07.md` round 7.
- **34 dead/mislabelled RSS feeds repaired across five verification rounds**
  (registry **35 dead / 64 ok → 2 dead / 97 ok**, ~84% of the 115 feeds still
  registered), each replacement checked for HTTP 200 + valid XML *and*
  correct outlet/language before applying — most notably **Il Corriere della
  Sera** (label 85, a scarce Italian high-reliability source) whose
  registered feed 404'd, so it had *never* been collected (the only
  "corriere" in the snapshots was the disinfo clone *Corriere del Corsaro*,
  label 10). Also Il Giornale (fixed twice — it regressed between rounds),
  Bild, Welt, Haaretz, Sky News UK, Jerusalem Post, Le Parisien, Al Jazeera
  Arabic, Business Day, B92, Iran International, Geo TV, SF Gate, and
  others. Byte-exact edits to `data/labels.jsonl` and `data/Fonti_OSINT.csv`
  (CRLF preserved); no label record lost.
- **11 outlets confirmed to have discontinued public RSS entirely**
  (TRT Africa, Mediazona, Jakarta Globe, AFP News, WNYC, DPA International,
  Jordan Times, Rudaw, Caixin China, USA Today, Taiwan News) had their `rss`
  field set to `null` rather than being deleted — the label record is kept
  so the weekly collector stops hitting a confirmed-dead URL without losing
  the ground truth. Two more (ITV News, L'Orient Today) block this
  environment's network on every path and were deliberately left as-is
  rather than nulled, since that looks environment-specific, not a genuinely
  dead feed. See `docs/feed_health_2026-07.md`.
- **Documented a data-destroying maintenance step.** `data/labels.jsonl` is a
  curated **merge** of MBFC ratings and the documented-disinfo registry, *not*
  reproducible from `ratings.csv` alone: regenerating it with
  `label_from_ratings --scale mbfc` drops 160→141 records, deleting the entire
  ground-truth low tail (Corriere del Corsaro label 10, etc.). The runbook now
  writes MBFC output to a separate file to merge, never overwriting the curated
  registry.
- **Documented the spaCy-model recalibration blocker precisely.** A
  *Full*-network session still can't fetch `it_core_news_lg`: the download
  hits `github.com/explosion/spacy-models`, and that repo isn't in the
  session's GitHub scope — a per-repo grant, not a network-level setting.
  `docs/dataset_expansion_runbook.md` now documents the exact failure, the
  `SessionStart` hook's silent `|| true` swallow of it, and the two mirrors
  checked and ruled out (Hugging Face needs auth, PyPI doesn't host spaCy
  pipelines), so recalibration isn't attempted from a degraded NER run by
  mistake.
- `CHANGELOG.md`'s `[1.0.0]` entry was out of Keep-a-Changelog order (listed
  before `[Unreleased]` instead of last); moved to the bottom.
- `SECURITY.md`'s supported-versions table still said `1.0.x`; updated to
  the current `1.6.x`.

### Planned
- Content-credibility signal for fake-news on ordinary domains (the low-tail
  class domain structure cannot catch).
- Full EU AI Act Annex IX documentation
- v2.0 (2027): recalibration with the diagnosis inputs, concordance/AUC ≥ 0.78
  on a ≥ 100-source future holdout

---

## [1.6.0] — 2026-07-12

### Added
- **Input-language flag (risk R3, roadmap item 8).** Evaluations now assess
  whether the message corpus is Italian (`cats/pipeline/language.py`: a
  dependency-free script check + Italian function-word ratio, 205/205 correct
  on the July snapshot registry, thresholds with a >4× margin). `cats.lite`
  results and `/evaluate` responses carry a `language` block
  (`italian`/`other`/`unknown` + confidence), and explanations warn when the
  Italian-optimised NLP stack is scoring non-Italian text. Flag-only: scores
  and bands never change. Not persisted — `/explain` does not report it.
- **Minimum-evidence guardrail (risk R5, roadmap item 9).** New
  `CATS_MIN_EVIDENCE_MESSAGES` setting (default 3): evaluations on fewer
  messages report `evidence.sufficient=false` and force
  `requires_review`/`requires_human_review` — previously a single message
  aggregated to a "high" band with zero confidence and *no* flag. The
  `evidence` block (message count, minimum, mean behavioural confidence) is
  returned by `cats.lite` and `/evaluate`. Flag-only: scores and bands never
  change (penalising them needs the recalibration cycle). The API schema
  floor stays 1 message for backwards compatibility.

- Repo analysis, development plan and numbered roadmap
  (`docs/piano_sviluppo_roadmap_2026-07.md`): state of the project at
  v1.5.0/ENGINE 1.4, strengths, open risks (single-signal discrimination,
  small validation set, unvalidated thresholds, pending legal TODOs, minor
  repo inconsistencies) and a 15-point phased roadmap.
- The `SessionStart` hook promised by `docs/cloud_setup.md` now actually ships
  (`.claude/hooks/session-start.sh` + `.claude/settings.json`): cloud-only,
  idempotent fallback for the environment setup script — installs the dev/test
  stack and the Italian NLP assets on a cold container, fast no-op on a warm one.
- Adversarial robustness regression suite (`tests/unit/test_adversarial.py`)
  turning the Art. 9 risk-register TODOs for R3/R4/R5 into executable tests:
  regular publishing cadence neutralises `silence` and is only caught via the
  domain penalty (R4); a single message currently aggregates to a "high" band
  at zero confidence, and the API schema floor is one message (R5); non-Italian
  input degrades silently with nothing flagging the language mismatch (R3).
  The tests pin current behaviour — weaknesses included — so signal-hardening
  work or accidental regressions must surface as deliberate test changes.
  Risk register §2/§7 updated to reference the suite.
- Signal ablation/LOSO diagnosis (`research/signal_ablation_spike.py`,
  findings in `docs/signal_diagnosis_2026-07.md`): on the future holdout,
  coherence — a near-chance solo ranker (0.528) — is the second-largest
  contributor to the calibrated aggregate (LOSO −0.139 concordance, it breaks
  the ties silence leaves), overturning the earlier "likely overfitting"
  reading; volatility (−0.013) and gaming (−0.005, solo at chance) are the
  real redesign candidates. Operational note: the calibrated weights assume
  the SBERT coherence backend — degraded/NER coherence forfeits that
  contribution.
- Message-level follow-up diagnosis
  (`research/gaming_volatility_diagnosis_spike.py`, findings appended to
  `docs/signal_diagnosis_2026-07.md`): gaming's `vocab` sub-score is
  arithmetically identical to `ttr` above the 50-token floor (TTR silently
  double-weighted; constraint note added in `signals/gaming.py`) and its
  heuristics correlate with newsroom practice, not manipulation — redesign
  candidate; volatility's 0.4 spike threshold is locally the worst setting
  tried (0.1–0.3 give ρ ≈ −0.12…−0.15 in the correct direction on both
  splits, ~3× current information, ceiling: 48.9% of messages have TextBlob
  polarity exactly 0); silence strengthens slightly and consistently at
  ≥ 96 h (ρ −0.47 vs −0.43, plateau from 96 h). All candidate changes are
  gated on the recalibrate → future-holdout revalidate cycle.

### Changed
- `requires_human_review` / `requires_review` is now `true` for evaluations
  below the evidence minimum, regardless of score or band (see the
  minimum-evidence guardrail above).

### Security
- The bundled nginx now **overwrites** `X-Forwarded-For` with `$remote_addr`
  instead of appending to it (`$proxy_add_x_forwarded_for`): the app takes the
  *first* entry of the header and records it in the GDPR audit log, so a
  client-supplied header could forge the audited IP even behind the proxy.
  Regression-tested (`tests/unit/test_security.py`).
- Failed API-key attempts are now rate-limited per client IP (429 beyond the
  sliding window). Previously the limiter only ran after successful
  verification, leaving key brute-forcing unthrottled at the app layer.
- `docker-compose.yml` no longer publishes the app's port 8000 on the host:
  the API is reachable only through nginx, so the proxy's rate limiting,
  security headers and `X-Forwarded-For` rewrite cannot be bypassed.

### Fixed
- The API now starts when the spaCy model is missing: `lifespan` crashed on a
  missing/broken `it_core_news_lg`; it now logs `spacy_model_unavailable` and
  serves in the documented degraded mode (neutral zero-confidence NER
  coherence, `/health` reports `nlp: "not_loaded"`).
- The Docker image now ships `data/calibrated_weights.json`. Pointing
  `CATS_WEIGHTS_FILE` at it inside the container hit the missing-file fallback
  and silently scored with the static, unvalidated weight estimates.
- `normalize_messages` sorts chronologically under mixed UTC offsets:
  timestamps are normalised to UTC before sort/dedup (the previous ISO-string
  sort mis-ordered mixed-timezone histories, skewing the temporal signals;
  naive timestamps are taken as UTC). Non-string `text`/`timestamp` entries
  and non-dict records are now counted and skipped instead of raising
  `AttributeError` from `cats.lite` on non-text input.
- `make split` no longer litters the repo root with `train.jsonl` /
  `holdout.jsonl`: outputs go to the gitignored `data/splits/`, and the CLI's
  default output names are gitignored at the root as a safety net. Missing
  `.PHONY` declarations (`docker-logs`, `db-downgrade`, `generate-key`) added.
- `docs/compliance.md` asserted CATS is a "Limited Risk AI System" under the
  EU AI Act — a legal determination that contradicts the *pending*
  classification decision tracked in `docs/eu_ai_act/classification.md`.
  Softened to "pending legal decision" with a pointer to the classification
  prerequisite; the same doc's stale accuracy rows (weights described as
  uncalibrated) and version roadmap were brought up to the v1.5.0 state.
- Documentation state sync: `docs/README.md` was an empty stub (now a full
  index), `CITATION.cff` still cited version 1.3.0 (now 1.5.0),
  `SUMMARY.md`/README lacked `docs/cloud_setup.md`, the README roadmap was
  frozen at v1.3.1, and `docs/architecture.md`/`docs/api.md` did not describe
  the response-time guardrail blocks.
- Alembic migrations now honour the `DATABASE_URL` environment variable
  (falling back to `alembic.ini`): `alembic upgrade head` / `make db-migrate`
  previously always targeted the hardcoded localhost `cats` database and
  failed in the CI/cloud test environments, which configure `cats_test`.
- `CONTRIBUTING.md` no longer directs pull requests at the non-existent
  `develop` branch (PRs target `main`); the inert `develop` push trigger was
  removed from CI.
- README license links pointed at `LICENSE/` (404 on GitHub); now `LICENSE`.
- The future-snapshot validation was misdated "28 July 2026" in the findings
  title and its citations — it ran on **6 July 2026** (commit `2b41982`).
  Living docs and code comments now carry the correct date; the findings
  filename and released changelog entries are kept for link stability.

---

## [1.5.0] — 2026-07-08

### Added
- **Domain-provenance penalty (ENGINE 1.4).** Signal-hardening so discriminative
  power no longer rests on `silence` alone: impersonation/clone domains
  (rare/cheap TLDs, free-hosting subdomains, brand typo-squats) now lower a
  source's score via an asymmetric post-aggregation penalty
  (`score − 0.6 × domain_red_flag`, clamped at 0), applied when a source URL is
  supplied (`context["url"]`, `cats.lite.score(url=…)`). Red-flags come from
  general domain structure only, never the labelled disinfo set. Validated on
  the 28 Jul 2026 future holdout: pairwise concordance **0.755 → 0.775**, every
  correction a low-reliability clone (reproduce via
  `research/validate_domain_penalty.py`). The four calibrated behavioural weights
  are unchanged; `/explain` reports the penalty separately. Not a weighted fifth
  signal — a symmetric term would reward clean domains and inflate the low tail
  (fake-news on ordinary domains). See `docs/architecture.md`,
  `docs/signal_research_2026-07.md`.

### Changed
- **`ENGINE_VERSION` 1.3 → 1.4.** Scores of sources evaluated with a red-flagged
  URL are not comparable with earlier engines; `/explain` flags rows scored
  under a previous engine. Sources evaluated without a URL are unaffected.

---

## [1.4.0] — 2026-07-07

### Added
- Validated calibrated weights shipped as the recommended production table in
  `data/calibrated_weights.json` — point `CATS_WEIGHTS_FILE` at it.
- Cloud setup guide for Claude Code on the web (`docs/cloud_setup.md`):
  environment setup script, CI-mirrored test env vars, and per-phase network
  access for running linters and the test suite in a fresh cloud session.

### Changed
- **Calibrated weights validated on a future snapshot (28 Jul 2026).**
  Calibrated on the merged 02/03/05-Jul snapshots, evaluated on the unseen
  06-Jul snapshot: pairwise concordance **0.755** (> 0.70 target), Spearman
  **+0.553**, 79.2% band agreement within one band, low tail discriminating
  correctly. Accuracy declaration and `docs/calibration_findings_2026-07-28.md`
  updated.

### Fixed
- Calibrated weight files whose independently-rounded entries summed to just off
  1.0 (e.g. 1.000001) were rejected by `_validate_weights`, silently falling
  back to the static table so the calibrated weights never loaded. The check now
  accepts a loose tolerance and renormalises, and rejects only genuinely
  malformed tables (sum ≤ 0 or off by > 1e-3).
- Audit purge reads the deleted-row count defensively (`getattr`) — the DELETE
  `CursorResult` exposes `rowcount`, but the base `Result` type does not, which
  broke the mypy CI check.

---

## [1.3.1] — 2026-07-05

### Fixed
- **`CATS_WEIGHTS_FILE` and `CATS_API_KEYS` were silently ignored** — the
  settings fields only matched the bare `WEIGHTS_FILE`/`API_KEYS` names, so
  calibrated weights and multi-tenant keys configured as documented never
  loaded. Both documented spellings are now accepted (validation aliases).
- Gaming: corpora under 50 tokens no longer receive a spurious maximum
  vocabulary-uniformity sub-score (+25 points); the sub-score is neutral (0).
- `/health` no longer returns raw exception strings (could leak DSNs/internal
  hostnames on an unauthenticated endpoint); details are logged instead.
  The payload now includes the running version.
- Audit purge uses a single `DELETE` statement instead of loading and deleting
  expired rows one by one.
- API version string was hardcoded at 1.2.0; now read from `cats.__version__`.

### Added
- `POST /v1/cats/contest/{contest_id}/resolve` — close a pending contest
  (`upheld`/`rejected` + response, tenant-scoped, audit-logged): the GDPR
  Art. 22 appeal flow now has its human-decision endpoint. Migration `003`
  adds `trust_scores.engine_version`.
- `/explain` flags rows scored under an older aggregation engine
  (`engine_mismatch`) instead of silently re-decomposing them with current
  semantics.
- `TRUST_PROXY_HEADERS` setting: `X-Forwarded-For` is honoured only when
  enabled (default true, matching the bundled nginx); rate limiting is now
  keyed per API key (hashed) instead of per client IP.
- Per-source-type silence thresholds table
  (`signals/silence.py:SOURCE_TYPE_THRESHOLDS`; all defaults remain 72 h —
  changing values requires recalibration).
- Docker image now downloads the TextBlob corpora (world-readable
  `NLTK_DATA`), so container sentiment matches `make nlp-download` installs.

### Removed
- Unused JWT machinery (`create_access_token`/`verify_token`/`init_jwt_keys`)
  and the `python-jose` dependency: no route ever consumed tokens — auth is
  API-key based. `cryptography` unpinned to `<50`.

---

## [1.3.0] — 2026-07-05

### Added
- **`cats.lite`** — zero-infrastructure scoring: `from cats.lite import score`
  runs the 4-signal pipeline + aggregation as a plain library call (no
  PostgreSQL, no Redis, no API keys). Same signals, same explainability,
  same caveats as `/evaluate`.
- `CITATION.cff` for academic citation.
- PyPI-ready packaging: the project builds as **`cats-scoring`** with the
  library-surface dependencies only (`pip install cats-scoring[sbert]` for the
  multilingual coherence backend); the API deployment stack stays in
  `requirements.txt`. Colab demo notebook in `examples/cats_lite_demo.ipynb`.

### Changed
- **Signal polarity fix in `aggregate_score`** — the higher-is-worse signals
  (volatility, silence, gaming) are now inverted (`100 − value`) before the
  weighted average, so every signal enters the score as a reliability
  contribution. On ≤ 1.2.x the one empirically informative signal (silence)
  entered the average backwards, making calibrated weights rank a documented
  disinformation source *highest* on the July 2026 holdout (Spearman −0.42 →
  +0.32 with the fix; band agreement 0% → 90% within one band). See
  `docs/calibration_findings_2026-07.md` and the updated design decision in
  `docs/architecture.md`.
- `/explain` signal details now include `polarity` and `reliability_value`
  (the inverted value actually aggregated); `contribution`/`score_share_pct`
  are computed on the reliability axis so they decompose the real score.

### Breaking
- Trust scores are **not comparable** with scores produced by ≤ 1.2.x.
- Weights calibrated under the pre-1.3 engine are invalid — recalibrate with
  `python -m cats.calibration` (recalibrated weights for the July 2026
  snapshots ship in `data/calibrated_weights.json`).

---

## [1.2.0] — 2026-06-29

### Added
- Optional Sentence-BERT coherence backend (`COHERENCE_BACKEND=sbert`, model via
  `COHERENCE_MODEL`): mean cosine similarity of consecutive message embeddings.
  `sentence-transformers` is optional (`requirements-sbert.txt`); falls back to
  the spaCy NER backend when unavailable, so the default stays light.
- Per-signal attribution in `/explain`: `score_share_pct` (each signal's share
  of the weighted score) and `primary_driver` — a dependency-free, SHAP-style
  breakdown of *why* a source got its score.

---

## [1.1.0] — 2026-06-29

### Added
- Optional BERT Italian sentiment backend for the volatility signal
  (`SENTIMENT_BACKEND=bert`, model configurable via `SENTIMENT_MODEL`).
  `transformers`/`torch` are optional (`requirements-bert.txt`); the backend
  falls back to TextBlob when they are unavailable, so the default stays light.
- Row-level multi-tenancy: a `tenant_id` (bound to the API key via the optional
  `CATS_API_KEYS` "key:tenant" map, never client-supplied) is stored on every
  `TrustScore` / `AuditLog` / `Contest`, and all reads (`/explain`, `/contest`,
  `/review`, `/stats`) are scoped to the caller's tenant. Backwards compatible:
  unlisted keys resolve to the `default` tenant. Migration `002`.
- `POST /v1/cats/batch` endpoint: evaluate multiple sources in one request
  (1–50 items), persisted atomically in a single transaction.
- Prometheus metrics at `GET /metrics` (`prometheus-client`): HTTP request
  count/latency (labelled by route template) plus `cats_evaluations_total`
  (by band) and a `cats_trust_score` histogram.
- nginx reverse-proxy config (`deploy/nginx.conf`) wired into `docker-compose`:
  per-IP rate limiting (30 req/min), security headers, correct
  `X-Forwarded-For`, and a documented TLS 1.3 server block.
- Weight calibration toolkit (`cats.calibration`): dependency-free genetic
  search that tunes per-source-type signal weights against a labelled dataset,
  optimising rank-agreement (Spearman / pairwise concordance). Calibrated
  weights are served via the `CATS_WEIGHTS_FILE` setting. See
  [docs/calibration.md](docs/calibration.md). GA design inspired by
  SantanderAI/genetic-algorithm (Apache-2.0).

### Fixed
- `compute_coherence` no longer crashes when the spaCy model is not loaded
  (`nlp is None`): it degrades gracefully to a neutral, zero-confidence signal,
  consistent with `/health` reporting `nlp: not_loaded`.
- CI is green again: applied black/isort across the codebase and fixed the
  remaining flake8/mypy errors plus structlog-config and test-isolation bugs
  that had been failing every run.

---

## [1.0.0] — 2026-03-06

### Added
- 4-signal scoring pipeline: coherence, volatility, silence, gaming
- FastAPI REST API with 9-phase evaluation pipeline
- GDPR Art. 13–22 endpoints: `/explain`, `/contest`, `/review`
- AES-256-GCM encrypted audit log (PostgreSQL)
- Redis sliding-window rate limiting (Lua, 30 req/min)
- JWT RS256 authentication with dual API-key rotation
- APScheduler nightly audit purge with distributed Redis lock
- Docker multi-stage build with non-root user
- GitHub Actions CI: lint, unit tests, integration tests, Docker build
- spaCy `it_core_news_lg` for Italian NER
- RFC 7807 Problem Details error responses
- Deep `/health` endpoint (API + Redis + PostgreSQL + NLP)
- WP 4.1/4.3 compliance disclaimer on all explanation responses
- Dynamic weight matrix by source type (social/news)

### Known Limitations
- NLP accuracy ~55–62% (rule-based; see WP 4.1)
- Parameters not empirically calibrated
- Italian-only NLP pipeline
