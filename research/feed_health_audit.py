"""Feed-health audit: which RSS feeds in the label registry are dead?

Motivation. A dead feed silently shrinks (and biases) the collected dataset:
Il Corriere della Sera (label 85, a scarce Italian high-reliability source) was
never collected for months because its registered feed 404s — found by chance.
This script checks every feed in data/labels.jsonl so the rest are found on
purpose, not by accident.

It classifies each feed:
  * ok       — the collector's own parser can extract recent, usable messages
  * stale    — parses fine, but its own newest item is more than
               STALE_AFTER_DAYS old (a feed that answers correctly but has
               stopped publishing — see *The stale case*, below)
  * dead     — 404/410 or DNS/connection failure (genuinely broken → fix/replace)
  * blocked  — still 403/429 or timeout after the curl fallback below (host
               likely blocks by IP/geo, needs JS, or is slow; ambiguous, not
               necessarily dead — flag, don't auto-remove)
  * not-xml  — 200 but the collector can't extract messages from it: not XML at
               all (redirect to an HTML page, etc.), or XML the collector
               deliberately refuses — carries a DTD (rejected outright as a
               defensive measure against XXE, see collect_rss.parse_feed), not
               well-formed, or has no `<item>`/`<entry>` elements

**`ok`/`stale` are decided by actually calling `cats.calibration.collect_rss.parse_feed`
on the body**, not by a separate heuristic — a URL classified `ok` here is
therefore usable by the real collector by construction, not merely "looks like
XML". This was tightened on 2026-08-22 after round 12 shipped a "fix" that
passed an earlier, weaker XML-shape check (looked like valid RSS, had a recent
`<pubDate>`) but that the collector's own defensive DTD check rejects outright
(`corriere.it`'s live feed system emits a harmless-looking but blanket-rejected
`<!DOCTYPE xml>` preamble) — an `ok` classification that was not actually
usable. Reusing the exact function the collector runs closes that gap by
construction instead of chasing each new way a feed can look fine and not be.

The blocked case (2026-08-25). Not every 403 is an IP/geo block: three feeds
long classified `blocked` (al-monitor.com, hrw.org, rnz.co.nz) turned out to
be blocking httpx's specific TLS/HTTP client fingerprint — curl, same
User-Agent, same network, got a clean 200. `fetch_feed` now retries a 403
via curl before giving up (see its docstring); this script inherits that for
free by calling `fetch_feed` instead of its own GET.

The stale case (2026-08-21). Before that fix, `ok`/`dead`/`blocked`/`not-xml`
only ever checked *reachability* — HTTP status and body shape — never whether
the feed's own content is current. That misses a real failure mode: Il
Corriere della Sera's *previous* registered feed (the one that motivated
writing this script) came back to HTTP 200 + valid XML after its 404 was
fixed, but had silently frozen at its 2024-05-13 content — every request
served the identical cached body, for over a year, and nothing here would
have called it anything but `ok`. A recalibration checkpoint
(`docs/calibration_findings_2026-08-21.md`) found 15 of 95 merged sources in
the same state. `stale` compares each feed's own newest parsed message
timestamp against today to catch this.

It also reports *shared* feeds — two registry rows pointing at the same URL.
Those are not a health problem (the feed answers fine) but a dataset one: each
row collects a byte-identical message set, so one source is counted twice in
calibration. merge_snapshots only deduplicates messages *within* a source_id,
so nothing downstream catches it (2026-07-25: Ukrainska Pravda / Ukrainska
Pravda English, found only because a UA sweep listed the same URL twice).

Read-only: it never edits the registry, only reports. The same GET the weekly
collector (cats.calibration.collect_rss) issues, so it is within normal
operation. Needs network.

Run from the repo root:  python research/feed_health_audit.py [--workers N]
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import httpx

from cats.calibration.collect_rss import fetch_feed, parse_feed

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (X11; Linux x86_64) CATS-calibration/1.0"
_RETRY_BACKOFF_S = (2.0, 5.0)  # 429 is "try later", not "blocked" — a couple of
# spaced retries tells the two apart (2026-07-24: Strafatti Quotidiani flagged
# 'blocked' on a single 429 that a same-session retry immediately cleared).

# How long a feed's own newest item can go unrefreshed before it counts as
# 'stale' rather than 'ok'. Generous on purpose: every frozen feed found on
# 2026-08-21 had been stuck for 30+ days (most for months to years), so this
# is well clear of an ordinary quiet week and still catches all of them.
STALE_AFTER_DAYS = 14


def classify(url: str, timeout: float) -> Tuple[str, str]:
    """Return (status, detail) for one feed URL.

    Fetches via ``collect_rss.fetch_feed`` — the exact function the real
    collector calls — not a separate GET, so a 403 gets the same curl
    fallback the collector gets (some WAFs block by client fingerprint, not
    IP or User-Agent; see ``fetch_feed``'s docstring) before being bucketed
    as `blocked`. A URL classified anything other than `blocked`/`dead` here
    is therefore reachable by the real collector by construction.
    """
    body: Optional[str] = None
    status_code: Optional[int] = None
    for attempt, backoff in enumerate((0.0,) + _RETRY_BACKOFF_S):
        if backoff:
            time.sleep(backoff)
        with httpx.Client(follow_redirects=True, timeout=timeout, headers={"User-Agent": UA}) as c:
            try:
                body = fetch_feed(url, c)
            except ValueError as exc:
                cause = exc.__cause__
                if isinstance(cause, httpx.TimeoutException):
                    return "blocked", "timeout"
                if isinstance(cause, httpx.HTTPStatusError):
                    status_code = cause.response.status_code
                elif isinstance(cause, httpx.HTTPError):
                    return "dead", f"conn:{type(cause).__name__}"
                else:
                    return "dead", str(exc)  # e.g. oversize body, no httpx cause
        if status_code == 429 and attempt < len(_RETRY_BACKOFF_S):
            continue  # rate-limited, not necessarily blocked — retry before giving up
        break
    if body is None:
        assert status_code is not None
        if status_code in (404, 410):
            return "dead", f"http:{status_code}"
        return "blocked", f"http:{status_code}"
    try:
        messages = parse_feed(body)
    except ValueError as exc:
        return "not-xml", f"parse:{exc}"
    if not messages:
        return "not-xml", "no usable messages"
    newest = max(datetime.fromisoformat(m["timestamp"].replace("Z", "+00:00")) for m in messages)
    age = datetime.now(timezone.utc) - newest
    if age > timedelta(days=STALE_AFTER_DAYS):
        return "stale", f"newest:{newest.date().isoformat()} ({age.days}d ago)"
    return "ok", "http:200"


def normalise_feed(url: str) -> str:
    """Key for spotting the same feed written two ways (scheme/www/trailing slash)."""
    key = url.strip().lower().rstrip("/")
    for prefix in ("https://", "http://"):
        if key.startswith(prefix):
            key = key[len(prefix) :]
            break
    return key[4:] if key.startswith("www.") else key


def shared_feeds(feeds: List[Tuple[str, str, float]]) -> Dict[str, List[str]]:
    """Map normalised feed URL → the source_ids sharing it (2+ only)."""
    by_feed: Dict[str, List[str]] = {}
    for sid, url, _label in feeds:
        by_feed.setdefault(normalise_feed(url), []).append(sid)
    return {url: sids for url, sids in by_feed.items() if len(sids) > 1}


def main() -> None:
    ap = argparse.ArgumentParser(description="Audit RSS feed health in the label registry.")
    ap.add_argument("--labels", type=Path, default=ROOT / "data/labels.jsonl")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--timeout", type=float, default=20.0)
    args = ap.parse_args()

    rows = [json.loads(line) for line in open(args.labels, encoding="utf-8")]
    feeds: List[Tuple[str, str, float]] = [
        (r.get("source_id", ""), r["rss"], float(r.get("label", -1))) for r in rows if r.get("rss")
    ]
    print(f"Auditing {len(feeds)} feeds ({sum(1 for r in rows if not r.get('rss'))} registry rows have no feed).\n")

    shared = shared_feeds(feeds)
    if shared:
        print("SHARED FEEDS — one source counted twice in calibration (offline check):")
        for url, sids in sorted(shared.items()):
            print(f"  {url}\n    {', '.join(sorted(sids))}")
        print("  Fix: blank the wrong row's 'rss' (keeps the source catalogued, stops collection).\n")

    results: Dict[str, List[Tuple[str, str, float, str]]] = {
        "dead": [],
        "blocked": [],
        "not-xml": [],
        "stale": [],
        "ok": [],
    }

    def _check(item: Tuple[str, str, float]) -> Tuple[str, str, float, str, str]:
        sid, url, label = item
        status, detail = classify(url, args.timeout)
        return sid, url, label, status, detail

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for sid, url, label, status, detail in ex.map(_check, feeds):
            results[status].append((sid, url, label, detail))

    for status in ("ok", "stale", "blocked", "not-xml", "dead"):
        print(f"  {status:<9} {len(results[status])}")

    for status in ("dead", "not-xml", "stale"):
        if results[status]:
            print(f"\n{status.upper()} — action needed (source | label | feed | detail):")
            for sid, url, label, detail in sorted(results[status], key=lambda t: t[2]):
                print(f"  [{int(label):>2}] {sid[:26]:<26} {url[:52]:<52} {detail}")

    if results["blocked"]:
        print("\nBLOCKED (403/429/timeout — likely UA/geo blocking, verify manually):")
        for sid, url, label, detail in sorted(results["blocked"], key=lambda t: t[2]):
            print(f"  [{int(label):>2}] {sid[:26]:<26} {detail}")

    print(
        "\nNote: 'dead' feeds silently drop their source from every collection — fix or\n"
        "replace them (verify a working feed, then update data/labels.jsonl + the\n"
        "catalogue). 'stale' feeds answer correctly but have stopped publishing —\n"
        f"same fix, just harder to notice (no error, just silence past {STALE_AFTER_DAYS}d).\n"
        "'blocked' may just refuse this User-Agent; re-check before removing."
    )


if __name__ == "__main__":
    main()
