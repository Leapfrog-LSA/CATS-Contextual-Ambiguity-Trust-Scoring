# Feed-health audit — July 2026

Reproducible via [`research/feed_health_audit.py`](../research/feed_health_audit.py)
(read-only; issues the same GET the weekly collector does).

## Why

A dead feed silently drops its source from every collection and biases the
dataset. *Il Corriere della Sera* (label 85, MBFC High — a scarce Italian
high-reliability source) had never been collected because its registered feed
404s. That was found by chance; this audit finds the rest on purpose.

## Result

| Status | At audit (126 feeds) | After round 1–3 | Before round 4 (2026-07-22) | After round 4 | After round 5 (2026-07-23, 115 feeds) |
|---|---:|---:|---:|---:|---:|
| ok | 64 | 91 | 90 | 97 | **97** |
| dead | 35 | 9 | 10 | 8 | **2** |
| not-xml | 10 | 10 | 10 | 5 | **0** |
| blocked | 17 | 16 | 16 | 16 | **16** |

(The "before round 4" counts drifted slightly from the round 1–3 numbers merged
in PR #42 — two days of natural feed flakiness, not a regression. The feed
count drops from 126 to 115 in round 5 because 11 entries with no recoverable
feed had their `rss` nulled rather than being fixed — see below; the *label*
record is kept, only the dead feed pointer is removed.)

At audit only **~51%** of registered feeds returned a feed — why ~59 sources
appear in the snapshots despite 126 registered feeds, and the loss was **not
random** (the dead feeds clustered at labels 85 and 50, biasing the effective
dataset). After the repair passes below (rounds 1–5), **97/115 (~84%) of
still-registered feeds work**, and the only two `dead` left are outlets that
block this session's network entirely, not a URL problem.

The dead feeds are overwhelmingly non-Italian international outlets whose feed
URLs have moved.

## Repair progress

**Every replacement checked for HTTP 200 + valid XML *and* correct
outlet/language** before applying. **34 feeds repaired** across five rounds
(35 dead → 2, not-xml 10 → 0; ok 64 → 97, ≈84% of the 115 feeds still
registered):

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

### Round 5 (regression fix + execute the round-4 drop recommendation)

**Regression found and fixed:** re-running the audit at the start of round 5
turned up a new dead feed not present at the end of round 4 — **Il Giornale**
(`feed.xml` from round 1 now 404s). The `businessday.co.za` fix in round 4
was a clue: **Il Giornale runs on the same Arc XP CMS**, so the fix was the
same standard outbound path — `→ ilgiornale.it/arc/outboundfeeds/rss/`,
verified HTTP 200 + valid XML + current Italian content. A reminder that
"fixed" feeds need re-auditing periodically, not just once.

**Retried the two network-blocked outlets** (ITV News, L'Orient Today) from
this session — both still time out / WAF-challenge on every path, unchanged
from round 4. **Left as-is** (not nulled): the block looks specific to this
environment's egress (Cloudflare JS challenge, HTTP/2 `INTERNAL_ERROR`), not
evidence the feed is actually dead for the production collector. Nulling
these would risk permanently dropping two legitimate high/mid-reliability
sources over an artifact of the dev sandbox.

**Re-investigated the 11 "no public feed" outlets** from round 4 (WebSearch
per source, one more pass) — no new leads on any of them; every search
independently re-confirmed round 4's finding (e.g. a SitePoint piece
confirming AFP deliberately turned off RSS; WNYC's only remaining feeds are
podcast-specific, some already retired). Round 4 → round 5 yield: 5 → 0 new
fixes, the expected floor for this line of attack.

**Executed the round-4 recommendation:** for the 11 confirmed
no-longer-published feeds (TRT Africa, Mediazona, Jakarta Globe, AFP News,
WNYC, DPA International, Jordan Times, Rudaw, Caixin China, USA Today,
Taiwan News), set `"rss": null` in `data/labels.jsonl` and cleared the `RSS
Feed` column in `data/Fonti_OSINT.csv` — **the label record itself is kept**
(source_id, label, url), only the dead feed pointer is removed, following
the file's existing convention (many sources, e.g. RFI, BBC News, Foreign
Policy, already carry `rss: null`). This was a deliberate choice over
deleting the rows outright: it stops the weekly collector from repeatedly
hitting a confirmed-dead URL while preserving the ground-truth label in case
one of these outlets relaunches a feed later (re-adding a URL is a one-line
diff; re-establishing a lost label is not).

Net effect: **dead 8 → 2, not-xml 5 → 0**. The two remaining `dead` entries
(ITV News, L'Orient Today) are believed environment-specific, not genuinely
broken — worth one more retry from a session with a different network path,
otherwise leave them as-is rather than null them.

### Round 6 (retry from a fresh session, 2026-07-24)

**Retried both network-blocked outlets again**, from a different, freshly
provisioned cloud session (not the one that produced rounds 4-5) — same
result. ITV News: HTTP/2 `INTERNAL_ERROR` on `/news/rss`, and forcing
HTTP/1.1 just times out after 20s, on the homepage too, not only `/rss`.
L'Orient Today: now a flat `403` on every path tried (`/`, `/rss.xml`, `/rss`,
`/feed`) rather than the earlier Cloudflare JS-challenge page — same practical
effect (no feed content reachable), different surface error, which is itself
evidence this is upstream WAF/anti-bot behaviour reacting to the sandbox's
egress IP/UA rather than a stable "this URL is gone" signal. **Left as-is
again** (not nulled) — three independent sessions now agree the domains are
unreachable from this collector's environment while the feed status itself
remains unverified either way. Not worth a fourth retry from *this* class of
session; the next productive step is verifying from a genuinely different
network path (a contributor's machine, or a *Full*-network session with a
different egress) rather than re-running the same probe again.

## Recommendation

After round 5 the registry is close to clean: **0 `not-xml`, 2 `dead`** (both
believed environment-specific — see above), and **16 `blocked`** that are
ambiguous by design (403/429/timeout could be UA/geo refusal, not a dead
feed) and should not be auto-removed.

Remaining work, roughly in order of value:

- **Re-audit periodically, not just once.** Round 5 caught a fresh regression
  (Il Giornale) that round 4 had left working — feed URLs drift over time
  even after being "fixed." Re-run `research/feed_health_audit.py` before
  each calibration pass, not just when chasing dead feeds.
- **ITV News / L'Orient Today**: retried three times now (rounds 4, 5, 6),
  always from this class of sandboxed cloud session, always blocked. Further
  retries from the same kind of session aren't informative — next step is a
  genuinely different network path (contributor's own machine, or otherwise
  outside this sandboxing) before concluding they're genuinely dead and
  nulling them too.
- **Manually verify the 16 `blocked`** (403/429/timeout) with a browser or a
  different UA/IP — some may be genuinely dead, most are probably just
  refusing this collector's User-Agent.
- The 11 nulled sources (label kept, `rss: null`) are permanently out of
  weekly collection until someone finds a working feed again — no further
  action needed unless one of them relaunches RSS.

This round's real prerequisite work — the ≥100-source future-holdout target
and the content-credibility signal — is still blocked on a full-network +
spaCy-model session (see `docs/dataset_expansion_runbook.md`), not on feed
health, which is now in a stable, near-maximal state for this line of effort.
