# Feed-health audit — July 2026

Reproducible via [`research/feed_health_audit.py`](../research/feed_health_audit.py)
(read-only; issues the same GET the weekly collector does).

## Why

A dead feed silently drops its source from every collection and biases the
dataset. *Il Corriere della Sera* (label 85, MBFC High — a scarce Italian
high-reliability source) had never been collected because its registered feed
404s. That was found by chance; this audit finds the rest on purpose.

## Result (126 feeds in `data/labels.jsonl`)

| Status | At audit | After round 1–3 | Before round 4 (2026-07-22) | After round 4 |
|---|---:|---:|---:|---:|
| ok | 64 | 91 | 90 | **97** |
| dead | 35 | 9 | 10 | **8** |
| not-xml | 10 | 10 | 10 | **5** |
| blocked | 17 | 16 | 16 | 16 |

(The "before round 4" counts drifted slightly from the round 1–3 numbers merged in PR #42 — two days of natural feed flakiness, not a regression.)

At audit only **~51%** of registered feeds returned a feed — why ~59 sources
appear in the snapshots despite 126 registered feeds, and the loss was **not
random** (the dead feeds clustered at labels 85 and 50, biasing the effective
dataset). After the repair passes below (rounds 1–4), **~77%** work.

The dead feeds are overwhelmingly non-Italian international outlets whose feed
URLs have moved.

## Repair progress

**Every replacement checked for HTTP 200 + valid XML *and* correct
outlet/language** before applying. **33 feeds repaired** across four rounds
(35 dead → 8, not-xml 10 → 5; ok 64 → 97, ≈77% working):

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

- **Round 3 (WebSearch per source, 4):** Haaretz English
  (`→ haaretz.com/srv/all-headlines-rss`), Bild (`→ bild.de/feed/alles.xml`),
  The Conversation AU (`→ theconversation.com/au/articles.atom`), The National
  UAE (`→ thenationalnews.com/arc/outboundfeeds/rss/category/uae/…`).

**Deliberately skipped** where the only feed found was the wrong
edition/brand/section: AFP (every English path still serves French), WNYC
(serves sister-site Gothamist), Geo TV (only a Bollywood section feed —
fixed in round 4, see below), Business Day (no working feed found — fixed
in round 4), ITV News / USA Today (no valid feed).

Still broken (~9 dead + not-xml/blocked): outlets with no discoverable clean
feed or that block scraping — TRT Africa, Jakarta Globe, DPA, Mediazona,
L'Orient Today, Taiwan News, Iran International, Rudaw, Caixin, Jordan Times,
B92, SF Gate, and the like. These are the hard tail; some no longer publish a
usable public feed at all.

### Round 4 (WebSearch + curl probing per source, 5 fixed)

- **B92** (`→ b92.net/rss/latest`; the old `/rss/` path now serves an HTML
  index of category feeds — found the "Najnovije"/latest feed in that index).
- **Iran International** (`→ iranintl.com/en/feed`; `/en/rss` now 404s/HTML,
  WebSearch found the current WordPress `/feed` alias).
- **SF Gate** (`→ sfgate.com/bayarea/feed/bay-area-news-429.php`; `/rss/`
  is now an HTML index of per-topic Hearst feeds — took the general Bay Area
  local-news one, matching the "Bay Area" registry note, over the narrower
  business/sports/culture feeds also listed there).
- **Geo TV** (`→ geo.tv/rss/1/1`; the MSN-syndication widget on the old
  `/rss` HTML index page linked the numeric category feed IDs).
- **Business Day** (`→ businessday.co.za/arc/outboundfeeds/rss/`; the
  `businesslive.co.za` domain now redirects internally to the
  `businessday.co.za` Arc XP site, which exposes the standard Arc outbound
  feed — round 1–3 had marked this "no working feed found").

Two more resolved themselves without any edit (confirmed by re-audit, not
touched): **The Citizen** (dead → ok) and **David Icke** (not-xml/HTTP 202 →
ok) — both were transient (rate-limit/WAF hiccup at audit time), not broken
feeds.

**Investigated and confirmed *not* fixable from this session** (13 — the hard
tail is now largely outlets that have dropped public RSS entirely, not just
moved it):

- **No public feed exists any more** (site checked for autodiscovery tags,
  common `/feed`, `/rss`, `/rss.xml`, category-feed patterns — all either
  404 or resolve to the app shell / homepage): TRT Africa, Mediazona,
  Jakarta Globe (its old category feeds now return `410 Gone`, i.e.
  deliberately retired, not moved), AFP News (corporate wire site, no
  article feed), WNYC (redesigned around podcast RSS only, no general news
  feed), DPA International (`/rss` and `/feed` both `404`, wire agency,
  subscription-only), Jordan Times (feed directories independently confirm
  it now 404s), Rudaw (an `rss-categories` page is advertised but renders
  only the client-side app shell, no static links), Caixin China (`/rss/`,
  `/rss.xml` all redirect to a dead page; the alternate
  `gateway.caixin.com` API feed exists but is for `caixinglobal.com`, the
  English edition — wrong language for this ZH-language registry entry, so
  not used), USA Today (`rss.usatoday.com` now redirects straight to the
  homepage), Taiwan News (every feed path renders the Next.js app shell,
  HTTP 200 with no feed content).
- **Domain blocks this environment's network entirely** (every path on the
  domain, not just `/rss`, times out or returns a WAF challenge/`INTERNAL_ERROR`
  regardless of protocol) — cannot verify a replacement from here, so none was
  applied: **ITV News**, **L'Orient Today** (Cloudflare "Just a moment…" JS
  challenge on every page including the homepage).

## Recommendation

The remaining 13 `dead`/`not-xml` entries (listed above under round 4) are
the genuine hard tail: outlets that have discontinued public RSS entirely, or
whose domain blocks this environment's network outright (not just the
`/rss` path). Further WebSearch/curl probing from a session with this same
network profile is unlikely to find anything new — the marginal fixes per
round have gone 14 → 10 → 4 → 5, each round more effort for less yield.
Two paths forward, not mutually exclusive:

- **Drop** the outlets confirmed to have no public feed at all (Mediazona,
  Jakarta Globe, AFP News, WNYC, DPA International, Jordan Times, Rudaw,
  Caixin China, USA Today, Taiwan News, TRT Africa) from the registry rather
  than leaving them permanently dead — a source with a 404 feed contributes
  nothing to collection either way.
- **Retry ITV News / L'Orient Today** from a session on a different network
  path (their block looks environment-specific — Cloudflare/WAF challenge,
  not a genuinely dead feed) before dropping them.

Do not auto-remove genuine `blocked` (403/429/timeout) feeds: they may just
refuse this User-Agent, not be dead. This round brought the registry to
**~77% working** (97/126) — a prerequisite for the ≥100-source future-holdout
target, alongside the content-credibility signal work, both still blocked on
a full-network + spaCy-model session (see `docs/dataset_expansion_runbook.md`).
