# CATS catalogue vs watchlist catalogue — 2026-11-15

A read-only comparison of CATS's `data/Fonti_OSINT.csv` and `data/labels.jsonl`
with a local copy of the `Fonti_OSINT.csv` of
[`Leapfrog-LSA/osint-sources-disinfo-watchlist`](https://github.com/Leapfrog-LSA/osint-sources-disinfo-watchlist),
made with `research/catalog_watchlist_diff.py`.

> **What this is, and is not.** It describes *where* the two catalogue copies
> differ, by normalised host and by normalised feed URL. It changes no data
> file, computes no score, and does not use or report the registry's `label`
> field. It proposes no alignment rule: those stay with the maintainer
> (see *Not decided*, below).
>
> **Aggregates only.** Like `docs/watchlist_probe_2026-11.md`, this report
> names no source. The per-source detail comes from the script's `--out` file,
> which is not committed.

## Run

- **Date:** 2026-11-15.
- **Watchlist copy:** commit `7a79ac0970f2ffce7dddf302d3ae275b48339ef4`,
  `Fonti_OSINT.csv` sha256
  `596d3fde299e405d7154f3ee1c073ee4aa83f78ba75132e887cfa882bf36f577`.
- **CATS:** commit `f336f26c66e7f02623cff5c10aa9fb8f8f5d6ad7` (`main`).
- **Not read:** the watchlist's `disinfo_sources_master.csv` and CATS's
  `data/disinfo_sources.csv`.
- **Command** (from the repository root, no network):

  ```
  python -m research.catalog_watchlist_diff \
      --watchlist <copy>/Fonti_OSINT.csv \
      --watchlist-commit 7a79ac0970f2ffce7dddf302d3ae275b48339ef4
  ```

## Definitions

- **Host:** the `URL` column (registry: `url`) through
  `cats.calibration.label_from_ratings.normalize_host`: lower case, leading
  `www.` removed. A URL it cannot parse counts as "host not parseable".
- **Feed / homepage URL:** the `RSS Feed` column (registry: `rss`) or the
  homepage through `research.feed_health_audit.normalise_feed`: lower case,
  scheme, `www.` and trailing slash removed. An empty cell is "no feed".
- **Feeds of a host:** the set of normalised feeds over all rows of that host
  in one copy (a host can have several rows).
- **Registry feed "same":** the registry feed equals any watchlist feed of the
  same host.

Every figure below was produced by that run. None is copied from an earlier
document. The 2026-11-09 probe and the July Round 8 used older copies of
both catalogues, so their figures are not comparable.

## Results

- watchlist commit: `7a79ac0970f2ffce7dddf302d3ae275b48339ef4`
- watchlist sha256: `596d3fde299e405d7154f3ee1c073ee4aa83f78ba75132e887cfa882bf36f577`
- CATS catalogue sha256: `bcb9ab9c8161a3ef2198f9076f5bba1b944669a70a3ab9c9368ffebd04cd8d12`
- CATS registry sha256: `eb4398244edc20ddc888af034bfe0068ff386b74180bcbef27dddc262f8ef085`

### Inputs

| Input | Rows |
|---|---:|
| CATS catalogue rows | 5,275 |
| watchlist rows | 6,028 |
| registry rows | 163 |
| registry distinct source_id | 163 |

### Catalogue vs catalogue

| Count | Value | Definition |
|---|---:|---|
| hosts_only_cats | 246 | normalised hosts present in the CATS catalogue and absent from the watchlist |
| hosts_only_watchlist | 1,002 | normalised hosts present in the watchlist and absent from the CATS catalogue |
| hosts_common | 4,807 | normalised hosts present in both copies |
| feeds_only_cats | 83 | normalised feed URLs present in the CATS catalogue and absent from the watchlist |
| feeds_only_watchlist | 884 | normalised feed URLs present in the watchlist and absent from the CATS catalogue |
| feeds_common | 204 | normalised feed URLs present in both copies |
| multi_row_hosts_cats | 133 | hosts with more than one row in the CATS catalogue |
| multi_row_hosts_watchlist | 115 | hosts with more than one row in the watchlist |
| common_hosts_feed_differs | 77 | common hosts where both copies list at least one feed and the two sets of normalised feeds differ |
| common_hosts_feed_disjoint | 71 | subset of the previous: common hosts whose two non-empty feed sets share no feed at all |
| common_hosts_feed_only_cats | 0 | common hosts with a feed in the CATS catalogue and no feed in the watchlist |
| common_hosts_feed_only_watchlist | 773 | common hosts with a feed in the watchlist and no feed in the CATS catalogue |
| unparseable_host_rows_cats | 0 | CATS catalogue rows whose URL cannot be parsed into a host |
| unparseable_host_rows_watchlist | 0 | watchlist rows whose URL cannot be parsed into a host |
| empty_url_rows_cats | 0 | CATS catalogue rows with an empty URL |
| empty_url_rows_watchlist | 0 | watchlist rows with an empty URL |

### Registry vs watchlist

| Host status | Rows |
|---|---:|
| in_watchlist | 143 |
| absent | 20 |
| no_host | 0 |
| unparseable | 0 |

| Feed status (host in watchlist) | Rows |
|---|---:|
| same | 65 |
| different | 41 |
| registry_only | 1 |
| watchlist_only | 36 |
| both_empty | 0 |

Homepage differs at the same host: 7 rows.

### Candidate definitions of a diverging registry source (roadmap figure: 55)

| Definition | Rows | Meaning |
|---|---:|---|
| D1_host_absent | 20 | registry rows whose homepage host is not in the watchlist (or has no parseable host) |
| D2_feed_different | 41 | host in the watchlist, both sides have a feed, and the registry feed matches none of the watchlist feeds for that host |
| D3a_feed_watchlist_only | 36 | host in the watchlist, the registry has no feed, the watchlist has one for that host |
| D3b_feed_registry_only | 1 | host in the watchlist, the registry has a feed, the watchlist has none for that host |
| D4_feed_mismatch | 78 | D2 or D3a or D3b: host in the watchlist and the feed is not the same on both sides (rows where both sides have no feed are not counted) |
| D5_homepage_differs | 7 | host in the watchlist, but the registry homepage (normalised URL) matches none of the watchlist homepages for that host |
| D6_absent_or_feed_mismatch | 98 | D1 or D4 |
| D7_feed_mismatch_or_homepage | 78 | D4 or D5 |
| D8_any_divergence | 98 | D1 or D4 or D5 |
| D9_feed_not_in_watchlist | 59 | registry rows with a feed that appears nowhere among the watchlist feeds, whatever the host |

55: not reproducible with any candidate definition on this copy.

## The figure of 55 in the roadmap

`docs/piano_sviluppo_roadmap_2026-09.md` says the two copies diverge on
55 sources of the labelled registry. The method behind that figure is not
documented in the repository.

**55 is not reproducible on this copy with any of the ten candidate
definitions above** (D1–D9, D3 split into D3a/D3b). The definitions were not
adjusted to reach it. The figure may come from another watchlist commit, an
earlier state of the CATS files, or a definition not listed here.

## Not decided (maintainer)

These choices stay open. This report makes no recommendation on any of them.

- **Definition of "diverging registry source":** which definition, if any,
  the roadmap figure should use.
- **Watchlist commit:** which commit to pin for future comparisons, and how
  the copy is obtained.
- **Alignment direction and method:** how the watchlist, which the roadmap
  names as the original, is applied to CATS.
- **The 2026-11-09 catalogue corrections:** what happens to the CATS feed
  fixes from *Catalogue cleanup* in `docs/feed_health_2026-07.md`.
- **Duplicate hosts:** whether and how hosts with several rows are deduplicated
  in either copy.
- **`data/labels.jsonl`:** whether it stays as it is or gets feeds updated by
  hand. It is curated and must never be regenerated destructively (SAFETY
  section of `docs/dataset_expansion_runbook.md`).
- **Naming sources:** whether a committed report may name individual sources.
  This one gives counts only.
- **Licence and terms of the watchlist catalogue:** not reviewed here. They
  must be checked by the maintainer or counsel before any row is copied into
  CATS. No row was copied.
