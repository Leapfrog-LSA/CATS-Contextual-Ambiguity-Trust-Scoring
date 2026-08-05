# Feed-health audit — July 2026

Reproducible via [`research/feed_health_audit.py`](../research/feed_health_audit.py)
(read-only; issues the same GET the weekly collector does).

## Why

A dead feed silently drops its source from every collection and biases the
dataset. *Il Corriere della Sera* (label 85, MBFC High — a scarce Italian
high-reliability source) had never been collected because its registered feed
404s. That was found by chance; this audit finds the rest on purpose.

## Result

| Status | At audit (126 feeds) | After round 1–3 | Before round 4 (2026-07-22) | After round 4 | After round 5 (2026-07-23, 115 feeds) | After round 10 (2026-08-05, 114 feeds) |
|---|---:|---:|---:|---:|---:|---:|
| ok | 64 | 91 | 90 | 97 | 97 | **98** |
| dead | 35 | 9 | 10 | 8 | 2 | **2** |
| not-xml | 10 | 10 | 10 | 5 | 0 | **0** |
| blocked | 17 | 16 | 16 | 16 | 16 | **14** |

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

## Recommendation

After round 10 the registry is close to clean: **0 `not-xml`, 2 `dead`**
(ITV News, L'Orient Today — both believed environment-specific, unchanged
across three rounds), and **14 `blocked`**, all still positively evidenced as
an IP-level sandbox block (rounds 7 and 10 agree, not UA-based) rather than a
dead-feed signal. One feed initially flagged `blocked` (Daily Maverick)
turned out to be a genuinely dead/moved feed rather than a sandbox block and
was fixed in round 7 (see above). The one duplicate-URL row (Ukrainska Pravda
/ Ukrainska Pravda English) was resolved in round 9, and the one drifted URL
found two weeks later (The Citizen) was resolved in round 10 — the registry
has no shared feeds and, as of round 10, no known-dead feed left uninspected.

Remaining work, roughly in order of value:

- **Re-audit periodically, not just once.** Round 5 caught a fresh regression
  (Il Giornale) that round 4 had left working — feed URLs drift over time
  even after being "fixed." Re-run `research/feed_health_audit.py` before
  each calibration pass, not just when chasing dead feeds.
- **ITV News / L'Orient Today, and the remaining 15 `blocked` feeds**:
  rounds 4-7 agree this class of sandboxed session sits behind an
  IP-level block for a wide swath of news-site WAFs — UA changes don't help
  (round 7 tried four, including a legitimate crawler UA and no UA at all).
  Further retries from this kind of session aren't informative for any of
  these 17 feeds; the next productive step for all of them together is
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
