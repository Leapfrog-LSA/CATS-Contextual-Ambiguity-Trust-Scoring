# Feed-health audit — July 2026

Reproducible via [`research/feed_health_audit.py`](../research/feed_health_audit.py)
(read-only; issues the same GET the weekly collector does).

## Why

A dead feed silently drops its source from every collection and biases the
dataset. *Il Corriere della Sera* (label 85, MBFC High — a scarce Italian
high-reliability source) had never been collected because its registered feed
404s. That was found by chance; this audit finds the rest on purpose.

## Result (126 feeds in `data/labels.jsonl`)

| Status | Count | Meaning |
|---|---:|---|
| ok | 64 | 200 + body looks like a feed |
| **dead** | **35** | 404/410 or DNS/connection failure — produces nothing |
| not-xml | 10 | 200 but an HTML page, not a feed |
| blocked | 17 | 403/429/timeout — likely User-Agent/geo blocking (ambiguous) |

**Only ~51% of registered feeds actually return a feed.** This is why ~59
sources appear in the snapshots despite 126 registered feeds, and the loss is
**not random**: the 35 dead feeds cluster at labels 85 (17) and 50 (10), so the
effective dataset is biased relative to the registry.

The dead feeds are overwhelmingly non-Italian international outlets whose feed
URLs have moved.

## Repair progress

Common feed-path probing (scratchpad aid) plus per-source verification —
**every replacement checked for HTTP 200 + valid XML *and* correct
outlet/language** — repaired **14** feeds so far, dropping the registry from
35 dead to 22 (ok 64 → 78, ≈62% working):

- Italian: **Corriere della Sera** (`→ xml2.corriereobjects.it/rss/homepage.xml`),
  **Il Giornale** (`→ ilgiornale.it/feed.xml`).
- Others: Mail & Guardian, Al Jazeera Arabic, Gulf News, Manila Bulletin,
  Göteborgs-Posten, Texas Tribune, Digi24, Le Soir, The Register, Index.hr,
  The Citizen, ZDNet — all `→` a verified working feed of the same outlet.

**Deliberately skipped** (a common pattern resolved but to the wrong
edition/brand — not applied): AFP (pattern gave the French feed; original was
English), WNYC (its `/feed/` serves sister-site Gothamist), Le Parisien
(English edition only). These need the correct per-source URL.

Still dead (22): mostly outlets whose feed URL no pattern found — Bild, Welt,
Sky News UK, Haaretz, ITV News, Jerusalem Post, The National UAE, DPA, and
others — each needs a manual URL lookup.

## Recommendation

Run a **feed-repair pass**: for each `dead`/`not-xml` entry, find the outlet's
current feed (verify HTTP 200 + XML), update both `data/labels.jsonl` and
`data/Fonti_OSINT.csv`, then re-run this audit until only genuine `blocked`
(UA/geo) entries remain. Drop sources whose outlet no longer publishes a feed.
This roughly **doubles** the usable source count before the next calibration —
a bigger, less biased dataset — and is a prerequisite for the ≥100-source
future-holdout target. It needs a network session; the audit tool makes it a
mechanical, verifiable loop. Do not auto-remove `blocked` feeds: they may just
refuse this User-Agent.
