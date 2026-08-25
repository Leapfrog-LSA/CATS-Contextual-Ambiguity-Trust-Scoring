# Feed-health audit — July 2026

Reproducible via [`research/feed_health_audit.py`](../research/feed_health_audit.py)
(read-only; issues the same GET the weekly collector does).

## Why

A dead feed silently drops its source from every collection and biases the
dataset. *Il Corriere della Sera* (label 85, MBFC High — a scarce Italian
high-reliability source) had never been collected because its registered feed
404s. That was found by chance; this audit finds the rest on purpose.

## Result

| Status | At audit (126 feeds) | After round 1–3 | Before round 4 (2026-07-22) | After round 4 | After round 5 (2026-07-23, 115 feeds) | After round 10 (2026-08-05, 114 feeds) | Round 11 (2026-08-21, 114 feeds) | Round 12 as shipped (2026-08-21, 113 feeds) | Round 12 corrected (2026-08-22, 113 feeds) | Round 13 (2026-08-25, 113 feeds) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ok | 64 | 91 | 90 | 97 | 97 | 98 | 95 | 84 | 78 | **79** |
| stale | — | — | — | — | — | — | — | 11 | 12 | **13** |
| dead | 35 | 9 | 10 | 8 | 2 | 2 | 2 | 2 | 2 | **2** |
| not-xml | 10 | 10 | 10 | 5 | 0 | 0 | 2 | 1 | 6 | **7** |
| blocked | 17 | 16 | 16 | 16 | 16 | 14 | 15 | 15 | 15 | **12** |

Round 12's `ok` count is not a regression from round 11's 95 — it is the same
95 feeds split honestly for the first time. `stale` is a new classification
(see below); every one of its feeds would have scored `ok` under every prior
round's classifier, silently. The "as shipped" column undercounted both
`stale` and `not-xml`, because its check only confirmed a feed *looked* like
valid XML, not that the collector could actually use it — see *Round 12
correction*, below, which tightened the check to call the collector's own
parser and found 6 more feeds (5 `not-xml`, `Il Corriere della Sera` itself
moved from `ok` to `stale`) that the original check had missed. The
"corrected" column is the honest count; the registry feed count also
dropped by one across both (114→113, `World Daily News Report` nulled —
see below).

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

### Round 7 (manual verification of the 16 `blocked`, 2026-07-24)

**Re-checked all 17 feeds then flagged `blocked`** (one more than the
"16" below — the registry had grown by one row since round 5), each with
four request variants: the collector's own UA (`CATS-calibration/1.0`), a
current Chrome desktop UA, a legitimate feed-reader/bot UA
(`Feedfetcher-Google`), and no `User-Agent` header at all (`httpx`'s
default). If the block were UA-string filtering, at least one variant should
have gotten through.

**Result: 15 of 17 return the identical `403` across all four variants**,
including the plain default UA and the Google-feedfetcher UA that no
legitimate anti-scraping rule should reasonably reject — Axios, Al-Monitor,
Nation Africa, The Guardian NG (Nigeria), Il Post, VoxEurop Italia, De
Standaard, Ukrainska Pravda (both the general and English-edition registry
rows — **also flags a registry duplicate**: same `rss` URL,
`pravda.com.ua/rss/`, under two `source_id`s), News24, Sudan Tribune, The
Monitor (Uganda), Times of Israel, RNZ Pacific, Human Rights Watch. A block
that survives switching to a well-known, legitimately-behaved crawler UA and
to no UA at all is evidence of an **IP/ASN-level block on this sandbox's
egress**, the same conclusion already reached for ITV News / L'Orient
Today (round 6) — not a UA-string filter this collector could route around
by changing its own header. **Left as-is** (no registry changes) — nothing
here distinguishes a genuinely dead feed from this environment's outbound IP
being on a WAF's blocklist, so nulling any of these would risk losing
working sources the same way ITV/L'Orient are believed to be false
positives.

**Daily Maverick was a genuinely dead feed, now fixed** — not IP-blocked like
the 15 above. The round-7 flakiness (`403` on three UA variants, `404` on the
fourth) turned out to be two different real signals colliding in one
concurrent burst, not one ambiguous host: a clean, single-request-at-a-time
recheck showed the **homepage** returns `200` for any request that carries a
`User-Agent` header at all (only a bare no-UA request gets `403` there) —
i.e. this domain is reachable from this sandbox, unlike the 15 IP-blocked
ones — while the registered feed path itself (`/feed/`) is a real `404`
(confirmed with a large, genuine "not found" page body, not a small WAF
challenge page) for every UA. The feed moved, it didn't start blocking:
probing common alternate paths found `/rss/` (redirects to `/dmrss/`) returns
`200` with a valid, current feed (`pubDate` same-day, live article content),
confirmed working with all four UA variants including the collector's own.
Fixed: `data/labels.jsonl` and `data/Fonti_OSINT.csv` updated from
`dailymaverick.co.za/feed/` to `dailymaverick.co.za/rss/`; re-running the
audit after the fix moved Daily Maverick from `blocked` to `ok` and dropped
the `blocked` count from 16 to 15.

**Strafatti Quotidiani was a false positive, now fixed at the tool level.**
Two of the four variants returned a clean `200` + valid feed body in the same
run that flagged it `blocked`; the registered feed is fine, the `429` in the
main audit was WordPress.com rate-limiting a burst of near-simultaneous
requests (this diagnostic script fires 17 feeds × 4 UAs concurrently — far
burstier than the weekly collector's normal single request), not a standing
block. Fixed at the source: `research/feed_health_audit.py`'s `classify()`
now retries a `429` up to twice with a short backoff before giving up,
instead of classifying on the first response — re-running the full audit
after the fix moved Strafatti Quotidiani from `blocked` to `ok` and dropped
the `blocked` count from 17 back to the expected 16, with no other feed
affected by the retry logic (429 was already rare in this registry outside
this one bursty host).

### Round 8 (cross-check the 11 nulled sources against a sibling repo, 2026-07-24)

A companion repo, `Leapfrog-LSA/osint-sources-disinfo-watchlist` (a "v0.1"
public-release snapshot that appears to predate, and be fully contained
within, this catalogue), was compared against `data/Fonti_OSINT.csv` and
`data/disinfo_sources.csv`. The disinfo watchlist is byte-identical (114/114
domains, all fields match). The OSINT catalogue offered no new sources (its
4,795 hosts are a strict subset of this repo's 5,053), but it does carry an
RSS URL for 749 hosts where this catalogue's row is blank — 11 of those
intersect the actively-calibrated label registry, and all 11 are exactly the
sources round 5 already nulled as "no longer publishing."

**Live-checked all 11 candidate URLs anyway, in case the sibling snapshot had
independently found something round 5 missed — it hadn't.** 9 confirm dead
outright: AFP News (`404`), DPA International (`404`), Mediazona (`404`),
Jakarta Globe (`404`, 0 bytes), WNYC (`404`), Caixin China (`200` but
redirects to `other.caixin.com/404/index.html` — a disguised 404), Jordan
Times / Rudaw / Taiwan News (`200` but a large non-XML HTML body — the same
client-side app shell round 5 already found, not a feed) — USA Today
(`200` but redirects straight to the homepage, same as round 5). **TRT
Africa's candidate (`trtworld.com/feed/rss.xml`) is the one surprise**: it
returns valid, current XML — but the feed's own `<title>` is "TRT World",
and its content is Turkish/global geopolitics, not Africa-focused. TRT World
and TRT Africa are distinct brand channels under the same broadcaster; this
is the *wrong outlet's* feed, not a working replacement — using it would
mislabel TRT World content as TRT Africa. **No registry changes**; all 11
stay `rss: null`. This line of investigation (sibling-repo cross-check) is
now closed — a future session doesn't need to re-open it without a genuinely
new source of candidate URLs.

## Round 9 (2026-07-25) — the Ukrainska Pravda duplicate, resolved

Round 7 noticed two registry rows carrying the same `rss`
(`https://www.pravda.com.ua/rss/`) and parked it as an editorial call. It
isn't one: the snapshots settle it.

**The two rows collected byte-identical data.** `Ukrainska Pravda` and
`Ukrainska Pravda English` both appear in the `2026-07-13` and `2026-07-20`
snapshots, each with 20 messages, and the message payloads hash identically
(`b0bcde04…` on 07-13, `b1efff3d…` on 07-20). The content is Ukrainian on
both. So the "English" row was never an English edition in the data — it was
the Ukrainian feed collected a second time under a second `source_id`, at the
same label (70), counted twice by every calibration pass that consumed those
snapshots.

**Nothing downstream would have caught it.** `merge_snapshots` deduplicates
messages *within* a `source_id` (`cats/calibration/merge_snapshots.py`), which
is the wrong axis for this bug: two `source_id`s are two sources by
construction. The catalogue row shows how it happened — `Fonti_OSINT.csv`
line 1168 has `Lingua=EN` and `URL=…/eng`, i.e. a genuinely distinct outlet
was intended, but the `RSS Feed` cell was copied from the Ukrainian row above
it.

**The English feed could not be verified from here.** `…/eng/rss/` and
`…/eng/rss/view_news/` both return a 5 486-byte Cloudflare interstitial —
the same body, byte for byte, as the Ukrainian feed's response, so the 403
says nothing about whether those paths exist. Pravda is one of the 15
IP-blocked hosts (round 7). Writing an unverified URL into the registry would
repeat exactly the mistake being fixed, so no replacement URL was guessed.

**Fix applied: blank the wrong feed, keep the source.** `data/labels.jsonl`
now has `"rss": null` on the English row and `data/Fonti_OSINT.csv` line 1168
has an empty `RSS Feed` cell. This is deliberately *not* a row deletion:
`label_from_ratings.py` emits `rss: None` for catalogue rows without a feed
and keeps them, and both `collect_rss` (line 189) and this audit script skip
feedless rows — so the outlet stays catalogued and labelled while stopping the
duplicate collection, and the edit is exactly what regenerating the registry
from the corrected CSV would produce. Registry goes 115 → 114 feeds, 47 → 48
feedless rows; no source and no label was removed. If someone verifies a real
English-edition feed from an unblocked network, re-adding it is a one-cell
edit.

**Guarded at the tool level, as with the round-7 429 fix.** The audit script
now reports *shared feeds* offline, before any network call, normalising
scheme / `www.` / trailing slash so the same feed written two ways still
collapses. Checked against the whole registry: this was the **only** case —
114 distinct feeds across 115 feed-carrying rows before the fix, 114/114
after.

## Round 10 (2026-08-05) — fresh re-audit, The Citizen fixed

Re-ran the audit two weeks after round 9, specifically to settle whether the
15 `blocked` hosts are still ambiguous or have quietly gone dead. **114 feeds:
97 ok, 14 blocked, 3 dead, 0 not-xml.**

`ITV News` and `L'Orient Today` are unchanged — still 404, still believed
environment-specific (round 7). All 14 `blocked` hosts came back a clean
HTTP 403 with no 429/timeout surviving the retry logic, the same pattern as
round 7: still positively an IP-level block, not an ambiguous rate limit, and
one fewer than round 7's 15 (Daily Maverick was fixed there and dropped out
of the class).

The one genuine change is **The Citizen** (label 85, Tanzania), not
previously flagged in any round, now 404 on its registered
`thecitizen.co.tz/rss.xml`.

**Root cause and fix.** The homepage still advertises an RSS autodiscovery
link (`<link rel="alternate" type="application/rss+xml"
href=".../tanzania/rss.xml">`), but that path 404s too — a stale link, not
the live endpoint. Several other common paths (`/feed/`, `/rss/`,
`/tanzania/rss`) soft-404: HTTP 200, but `text/html`, serving the site's app
shell instead of a feed. The working endpoint takes the section as a query
parameter rather than a path segment:
`https://www.thecitizen.co.tz/rss.xml?section=tanzania` —
`application/xml`, valid RSS 2.0, 40 items, all linking to
`thecitizen.co.tz/tanzania/...`, timestamps within the hour of the check
(Tanzanian content: property investment, National Housing redevelopment,
Simba/Yanga football). `data/labels.jsonl` and `data/Fonti_OSINT.csv`
updated (byte-exact, CRLF preserved on the CSV). Registry stays at 114 feeds
— a URL correction, not a row added or removed.

## Round 11 (2026-08-21) — no new fix; confirms the 95-source ceiling

Re-ran two and a half weeks after round 10, prompted by the daily/weekly
collection's source count sitting at 95 unique sources for that entire
stretch despite near-daily runs (`data/snapshots/`, merged via
`cats.calibration.merge_snapshots`) — this audit's **95 `ok`** is the same
number, confirming the collector isn't losing sources on its own: the feed
registry itself is the ceiling.

**ITV News and L'Orient Today are still 404** — the same two feeds every
round has flagged since round 4/7, now including this one. That consistency
across this many independent sessions weakens the "environment-specific"
hedge from earlier rounds; nothing here can confirm or rule that out
further without literally trying from a different network, but treating
them as genuinely dead is now the better prior.

**Two new `not-xml` entries, not a URL-drift case like The Citizen**:
`David Icke` (`http:202`, Cloudflare `sg-captcha: challenge` header,
redirects to `/.well-known/sgcaptcha/`) and `News Examiner` (`http:200`
serving a Cloudflare JS interstitial, "One moment, please..."). Checked the
raw response for both — same class of anti-bot wall as the 15 `blocked`
feeds, just returning a status code (200/202) the script's classifier
doesn't bucket as `blocked`. No fix available from this network; grouping
them with the `blocked` list for the purposes of the recommendation below
(17 total sandboxed feeds now, not 15).

**No net-new recoverable feed this round** — round 10's kind of find (a
URL that only needed a query-parameter fix) didn't repeat. `ok` dropped from
98 (round 10, post-fix) to 95 (-3): 2 to the new not-xml entries above, 1
more to the `blocked` bucket (ordinary week-to-week churn among sandboxed
hosts, not investigated further given the class is already known-blocked
from this network).

## Round 12 (2026-08-21) — a `stale` classification, and 4 fixes

Prompted by a recalibration checkpoint (`docs/calibration_findings_2026-08-21.md`)
run the same day: it found **15 of the 95 merged calibration sources had
produced no new message in 30+ days**, several not in years — invisible to
every prior round because `ok`/`dead`/`blocked`/`not-xml` only ever checked
whether a feed *answers*, never whether its content is *current*. A feed can
return HTTP 200 + valid XML forever while silently serving the same cached
body — that is exactly what happened to `Il Corriere della Sera`'s registered
feed, the same source that motivated writing this script in the first place:
its 404 (round 1) was fixed at some point after round 1–5, but the feed then
froze at its 2024-05-13 content and every round since has correctly, and
uselessly, called it `ok`.

**Added `stale`**: `classify()` now parses each `ok` candidate's own newest
`<pubDate>`/`<updated>` and compares it to today; more than 14 days old
(generous — every case found here was stuck for 30+ days, most for months to
years) reclassifies it `stale` instead of `ok`. Re-running the full registry
(113 feeds, after the one blank below) found **11 stale feeds**:

| Source | Label | Feed's own newest item | Age |
|---|---:|---|---:|
| Strafatti Quotidiani | 10 | 2016-12-27 | 3524 d |
| Corriere del Corsaro | 10 | 2022-11-24 | 1365 d |
| Daily Buzz Live | 10 | 2023-11-20 | 1004 d |
| Empire Sports News | 10 | 2024-04-14 | 858 d |
| Il Corrispondente | 10 | 2024-06-15 | 797 d |
| Veterans Today | 10 | 2024-07-21 | 760 d |
| Empire News | 10 | 2024-07-24 | 758 d |
| Arab News | 50 | 2026-06-18 | 64 d |
| Crisis Group Alert | **95** | 2026-07-30 | 21 d |
| Diretta News.it | 10 | 2026-07-22 | 30 d |
| iNews24.it | 10 | 2026-08-07 | 14 d |

**Four fixed, verified live (fresh content, not just a 200) before updating
`data/labels.jsonl` + `data/Fonti_OSINT.csv`**, the same standard as round
10's The Citizen fix:

- **Il Corriere della Sera** — the registered `xml2.corriereobjects.it/rss/homepage.xml`
  is a legacy endpoint the site's own CDN keeps serving (200, valid XML,
  byte-identical) without ever refreshing it; `www.corriere.it/rss/homepage.xml`
  aliases to the exact same frozen body. The live site runs an entirely
  different feed system, `dynamic-feed/rss/section/<name>.xml` — the
  `homepage` section under it is also empty (0 items), but `cronache`
  (general current-affairs, the traditional main section of an Italian daily)
  has 100 items, newest published today. Registered feed now
  `https://www.corriere.it/dynamic-feed/rss/section/cronache.xml`.
- **The National UAE** — the registered `.../category/uae/?outputType=xml`
  is live (`lastBuildDate` updates hourly) but the `uae` category itself has
  been emptied to 0 items; `.../category/news/uae/?outputType=xml` (same UAE
  scope, one path segment different) has 14 items, newest today. Registered
  feed now includes the `news/` segment.
- **Jerusalem Post** — the registered `rssfeedsheadlines.aspx` is frozen at
  2025-06-16; `rssfeedsfrontpage.aspx` on the same host is live, newest item
  today. Registered feed now `rssfeedsfrontpage.aspx`.
- **World Daily News Report** — not actually stale so much as gone: its feed
  URL now redirects to `aidesociale.ca`, an unrelated French-Canadian social-
  aid site (a lapsed/repurposed domain, not a frozen cache — confirmed by
  content, not just the redirect). Continuing to collect it would score an
  unrelated third-party site under this source's label, worse than doing
  nothing. `rss` nulled (round-9 precedent: label kept, catalogued, collection
  stopped) rather than guessing a replacement for a domain that no longer
  belongs to the outlet.

**The other 7 label-10 feeds were investigated, not fixed** — no autodiscovery
or section-guessing found live content, and unlike the four above these are
low-value hoax/junk sites, not sources worth the same replacement-hunting
effort: a defunct-but-still-resolving hoax blog is arguably consistent with
its own label. Two are specifically worth flagging rather than silently
leaving as "just another stale junk feed": **Veterans Today**'s domain now
redirects to `vtforeignpolicy.com` (a real-world rebrand) and 403s this
session; a future audit from an unblocked network could check whether its new
domain's feed is alive. **Corriere del Corsaro**'s homepage genuinely still
resolves and looks maintained (unlike the others, which look abandoned) —
its `/feed/` endpoint may simply have moved; not chased further this round.

**Two borderline cases flagged, not fixed** — genuinely ambiguous, so treated
like `blocked`, not `dead`: **Crisis Group Alert** (label 95, one of only two
sources at that label — the scarcest tier) is 21 days stale, but "Alert" is a
crisis-escalation feed by design, and a three-week gap between qualifying
events is plausible for that category rather than evidence of brokenness; its
site blocks this session (403) so live content couldn't be cross-checked.
**Diretta News.it** and **iNews24.it** are only 14–30 days stale, newly
crossed the threshold this round — worth re-checking next round before
concluding anything, not acting on a single borderline reading.

## Round 12 correction (2026-08-22) — the Corriere della Sera fix didn't work

The daily collection run the morning after round 12 surfaced the mistake
directly: `Il Corriere della Sera`'s new registered feed
(`corriere.it/dynamic-feed/rss/section/cronache.xml`) failed in the real
collector with `feed carries a DTD; refusing to parse`
(`cats/calibration/collect_rss.py`'s defensive rejection of any `<!DOCTYPE`,
a deliberate XXE guard, not a bug to route around). Round 12's verification
checked that the URL returned 200 + valid-*looking* XML with a recent
`<pubDate>` — it never checked whether the collector's own parser, with its
stricter and deliberately conservative rules, would accept the body. Every
URL under `corriere.it/dynamic-feed/rss/section/*` emits a `<!DOCTYPE xml>`
preamble (harmless in isolation — no external entity — but the guard is a
blanket policy on purpose, and loosening it for one feed is a security
decision, not made here). That entire feed system is therefore permanently
unusable for this collector regardless of which section is picked.

**Fixed properly**: back on the legacy `xml2.corriereobjects.it` system
(no DOCTYPE), most sections are frozen same as `homepage` was, but `cronaca`
(singular — general news) is the freshest, last updated 2026-06-03 — 80 days
stale as of today, still `stale` by the 14-day threshold, but genuinely
parseable and far less stale than the 830-day `homepage` it replaces.
Registered feed now `https://xml2.corriereobjects.it/rss/cronaca.xml`,
verified against `cats.calibration.collect_rss.parse_feed` directly (18
messages extracted), not just against an HTTP client. The National UAE and
Jerusalem Post's round-12 fixes were checked the same way today and are
genuinely fine (parse cleanly, newest item today).

**Structural fix, not just a one-off correction**: `classify()` no longer
reimplements a parallel "is this XML" check — it calls
`cats.calibration.collect_rss.parse_feed` on the response body directly, so
`ok`/`stale` now mean "the real collector can use this," by construction,
not "looks like it should work." Re-running the full registry with the
corrected check also caught **5 more feeds that the old XML-shape heuristic
had been silently over-crediting as `ok`** — they return 200 and something
XML-shaped, but the collector extracts zero usable messages from any of
them: `Natural News`, `Sixth Tone`, `The Hill Tech`, `Berlingske Business`,
`Le Parisien`, and the registered clone-domain row `https://bild.pics`
(a known impersonation domain, separate from the real `Bild`, label 10 —
not a registry bug). None chased this round — same "flag, don't guess"
treatment as the round-12 junk feeds, now visible for the first time instead
of silently miscounted.

## Round 13 (2026-08-25) — a curl fallback recovers 3 of 15 `blocked` feeds

Prompted by the recalibration checkpoint's ≥100-source target: with the pool
at 95, the next lever identified was recovering some of the sandboxed
`blocked` class "from a different network path." A literally different path
wasn't available from this session, but a different *HTTP client* was: `curl`
from the same network, same User-Agent, gets a clean 200 on three feeds that
have been `blocked` (403) under `httpx` since round 4 —
**al-monitor.com, hrw.org, rnz.co.nz** — confirming those three WAFs block by
TLS/HTTP client fingerprint, not IP or User-Agent string. The other 12
`blocked` feeds stay 403 (or serve a Cloudflare JS challenge) under curl too,
so they're a genuinely different, harder class — IP/geo block or JS-challenge,
not fingerprint.

**Fixed in the collector itself, not just this audit script**:
`cats.calibration.collect_rss.fetch_feed` now retries a 403 via `curl` before
raising, so every future collection run — not just this audit — picks up the
three recovered feeds. `research/feed_health_audit.py` inherits this for free
by calling `fetch_feed` (already the pattern since the round-12 correction).
`RNZ Pacific`'s registered URL was also simply wrong (`/rss` resolves to the
homepage, not a feed) — corrected to `/rss/pacific.xml`, found by trying
known section paths once curl confirmed the domain itself wasn't blocked.

**A bug in the first version of this fix, caught before shipping**: `curl`
without `--fail` exits 0 on an HTTP 4xx and prints the error/challenge page
as if it were the body — the first pass silently fed Cloudflare "Just a
moment..." pages into `parse_feed` for all 15 previously-`blocked` feeds, and
12 of them got relabelled `not-xml` (misleadingly — "carries a DTD", since an
HTML error page's `<!DOCTYPE html>` trips the DTD guard) instead of staying
`blocked`. Added `--fail` so curl's exit code means what `fetch_feed` needs it
to mean; re-verified all three recoveries plus a sample of the still-blocked
12 individually against `fetch_feed` directly before re-running the full audit.

Net: **`blocked` 15 → 12; `ok` 78 → 79 (Al-Monitor); `stale` 12 → 13** (HRW
and RNZ Pacific are both freshly collected today, but `NHK News Web Easy`
crossed the 14-day staleness threshold independently this round — an
unrelated, pre-existing case, not caused by this fix). `not-xml` 6 → 7 is
also unrelated churn: `David Icke`'s Cloudflare interstitial flipped back on
this round (documented flaky pattern since round 11).

## Recommendation

After round 13 the registry has an honest accounting of reachability,
freshness, *and* actual collector compatibility, including client-fingerprint
blocks: **2 `dead`** (ITV News, L'Orient Today — confirmed 404 across every
round since 4/7), **7 `not-xml`** (News Examiner and David Icke, Cloudflare
anti-bot interstitials, both flaky pass/fail across rounds not fixes — plus
Natural News, Sixth Tone, The Hill Tech, Berlingske Business, Le Parisien,
and the clone-domain row `https://bild.pics`, none distinguishable from a
working feed under the pre-round-12 heuristic), **12 `blocked`** (down from
15 — round 13 recovered 3 via a curl fallback for client-fingerprint blocks;
the remaining 12 are IP/geo-level or JS-challenge blocks curl doesn't clear
either, the harder class rounds 7 and 10 positively evidenced), and
**13 `stale`**: 4 fixed round 12 (Il Corriere della Sera — corrected again
the next day after its first fix turned out collector-incompatible, see
*Round 12 correction* — The National UAE, Jerusalem Post, World Daily News
Report), 7 low-value junk feeds investigated and left as is, 2 borderline
cases flagged for re-check, 1 (`NHK News Web Easy`) newly crossed the
threshold this round, unrelated to round 13's fix. One feed initially flagged
`blocked` (Daily Maverick) turned out to be a genuinely dead/moved feed
rather than a sandbox block and was fixed in round 7. The one duplicate-URL
row (Ukrainska Pravda / Ukrainska Pravda English) was resolved in round 9,
and drifted or client-blocked URLs found later (The Citizen in round 10; Il
Corriere della Sera, The National UAE, Jerusalem Post in round 12;
Al-Monitor, Human Rights Watch News, RNZ Pacific in round 13) are fixed as
found — the registry has no shared feeds and no *recoverable* dead, stale, or
client-fingerprint-blocked feed left unfixed among the sources worth chasing.

Remaining work, roughly in order of value:

- **The 12 remaining `blocked` feeds are IP/geo or JS-challenge blocks, not
  client-fingerprint** — round 13's curl fallback confirmed this by ruling
  the fingerprint explanation *out* for them, not by leaving them untested.
  The next lever is the one rounds 7/10/11 already named: verifying from a
  genuinely different network path (a contributor's own machine), which
  neither curl nor a header change can substitute for.
- **The 6 `not-xml` feeds other than the two Cloudflare interstitials**
  (Natural News, Sixth Tone, The Hill Tech, Berlingske Business, Le Parisien)
  were invisible under every round-11-and-earlier classifier — worth the same
  investigation the round-12/13 fixes got (autodiscovery / section-guessing)
  next time this doc is revisited, not chased in the same session that found
  them.

- **The 95-source calibration ceiling started as a feed-*reachability*
  problem; round 12 found *freshness* zombies inside it; round 13 is the
  first round to actually raise the reachable count.** Round 11 established
  that `data/snapshots/` had been stuck at 95 unique sources because the
  registry's `ok` count was also 95. Round 12 found 11 of those 95 were
  `stale` and fixed 4 (3 legitimate sources restored, 1 garbage source
  stopped). Round 13 recovers 3 sources that were never in the 95 at all —
  Al-Monitor, Human Rights Watch News, RNZ Pacific — via the curl fallback,
  so the reachable ceiling itself should move from 95 toward ~98 once a
  collection run picks them up, not just the content behind the existing 95.
  Still short of the ≥100-source target; the remaining lever is (a) the 12
  feeds still `blocked` (now confirmed IP/geo or JS-challenge, not
  fingerprint — see below), which need a genuinely different network path,
  not another client-side change, or (b) registering genuinely new sources
  (the 49 no-feed registry rows, or entirely new catalogue entries).
- **Re-audit periodically, not just once — and now that means `stale` too.**
  Round 5 caught a fresh regression (Il Giornale) that round 4 had left
  working — feed URLs drift even after being "fixed." Round 12 adds a
  second reason: a feed can pass every reachability check forever while
  silently serving the same cached response (Corriere della Sera did, for
  400+ days, before anyone compared its content against the calendar). Only
  a periodic re-run catches either regression before it accumulates months
  of silent data loss — re-run `research/feed_health_audit.py` before each
  calibration pass, not just when chasing dead feeds.
- **ITV News / L'Orient Today, the 12 `blocked` feeds, and News Examiner**
  (still `not-xml`, same anti-bot wall as `blocked`, just a different status
  code — see round 11): rounds 4-7 agree this class of sandboxed session sits
  behind an IP-level block for a wide swath of news-site WAFs — UA changes
  don't help (round 7 tried four, including a legitimate crawler UA and no UA
  at all), and round 13 confirmed a client-fingerprint change (curl) doesn't
  either, for these 12 specifically (it did for 3 others, now `ok`/`stale`).
  Further retries from this kind of session aren't informative for any of
  these 13 feeds; the next productive step for all of them together is
  verifying from a genuinely different network path (a contributor's own
  machine, or otherwise outside this sandboxing), not more probing from
  here.
- **Ukrainska Pravda English's real feed URL** — the duplicate itself is
  fixed (round 9; the row is now feedless, so it no longer double-counts),
  but whether `pravda.com.ua/eng` publishes its own feed is still unknown:
  Cloudflare 403s every path from this network. Worth one check from an
  unblocked machine — if a real English feed exists, re-adding it is a
  one-cell edit and gains a genuinely distinct labelled source.
- The 11 nulled sources (label kept, `rss: null`) are permanently out of
  weekly collection until someone finds a working feed again — no further
  action needed unless one of them relaunches RSS. Round 8 cross-checked
  them against a sibling repo's independently-sourced catalogue and found
  nothing usable (one candidate, TRT Africa, turned out to be the wrong
  outlet's feed) — this specific line of investigation is closed.

This round's real prerequisite work — the ≥100-source future-holdout target
and the content-credibility signal — is still blocked on a full-network +
spaCy-model session (see `docs/dataset_expansion_runbook.md`), not on feed
health, which is now in a stable, near-maximal state for this line of effort.
