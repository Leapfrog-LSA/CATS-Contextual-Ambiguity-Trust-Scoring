# Feed-health audit — July 2026

Reproducible via [`research/feed_health_audit.py`](../research/feed_health_audit.py)
(read-only; issues the same GET the weekly collector does).

## Why

A dead feed silently drops its source from every collection and biases the
dataset. *Il Corriere della Sera* (label 85, MBFC High — a scarce Italian
high-reliability source) had never been collected because its registered feed
404s. That was found by chance; this audit finds the rest on purpose.

## Result (126 feeds in `data/labels.jsonl`)

| Status | At audit | After repair |
|---|---:|---:|
| ok | 64 | **88** |
| dead | 35 | **13** |
| not-xml | 10 | 9 |
| blocked | 17 | 16 |

At audit only **~51%** of registered feeds returned a feed — why ~59 sources
appear in the snapshots despite 126 registered feeds, and the loss was **not
random** (the dead feeds clustered at labels 85 and 50, biasing the effective
dataset). After the repair passes below, **~70%** work.

The dead feeds are overwhelmingly non-Italian international outlets whose feed
URLs have moved.

## Repair progress

**Every replacement checked for HTTP 200 + valid XML *and* correct
outlet/language** before applying. **24 feeds repaired** across two rounds
(35 dead → 13; ok 64 → 88):

- **Round 1 (common-path probing, 14):** Corriere della Sera
  (`→ xml2.corriereobjects.it/rss/homepage.xml`), Il Giornale
  (`→ ilgiornale.it/feed.xml`), Mail & Guardian, Al Jazeera Arabic, Gulf News,
  Manila Bulletin, Göteborgs-Posten, Texas Tribune, Digi24, Le Soir,
  The Register, Index.hr, The Citizen, ZDNet.
- **Round 2 (homepage RSS-autodiscovery + verified known URLs, 10):**
  BioBio Chile, Hindu Business Line, Irish Examiner, **Le Parisien** (the
  correct French feed `feeds.leparisien.fr/leparisien/rss` — round 1 had only
  found its English edition, so it was skipped then), Welt, Sky News UK,
  Jerusalem Post, The Standard, Defense News, Firstpost.

**Deliberately skipped** where a pattern resolved to the wrong edition/brand:
AFP (French vs original English), WNYC (its `/feed/` serves sister-site
Gothamist). These need the correct per-source URL.

Still broken (~22): outlets whose feed URL neither probing nor autodiscovery
found — Bild, The National UAE, ITV News, Haaretz, DPA, TRT Africa, Mediazona,
Jakarta Globe, L'Orient Today, The Conversation AU, USA Today, and the
`not-xml`/`blocked` ones — each needs a manual per-source lookup (WebSearch).

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
