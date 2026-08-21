"""Feed-health audit: which RSS feeds in the label registry are dead?

Motivation. A dead feed silently shrinks (and biases) the collected dataset:
Il Corriere della Sera (label 85, a scarce Italian high-reliability source) was
never collected for months because its registered feed 404s — found by chance.
This script checks every feed in data/labels.jsonl so the rest are found on
purpose, not by accident.

It classifies each feed:
  * ok       — HTTP 200, looks like XML/RSS/Atom, and its newest item is recent
  * stale    — HTTP 200, valid XML/RSS/Atom, but its own newest item is more than
               STALE_AFTER_DAYS old (a feed that answers correctly but has
               stopped publishing — see *The stale case*, below)
  * dead     — 404/410 or DNS/connection failure (genuinely broken → fix/replace)
  * blocked  — 403/429 or timeout (host likely blocks this User-Agent or is slow;
               ambiguous, not necessarily dead — flag, don't auto-remove)
  * not-xml  — 200 but the body is not a feed (redirect to an HTML page, etc.)

The stale case (2026-08-21). `ok`/`dead`/`blocked`/`not-xml` only ever checked
*reachability* — HTTP status and body shape — never whether the feed's own
content is current. That misses a real failure mode: Il Corriere della Sera's
registered feed (the same one that motivated this script) came back to HTTP
200 + valid XML after its 404 was fixed, but had silently frozen at its
2024-05-13 content — every request served the identical cached body, for over
a year, and nothing here would have called it anything but `ok`. A recalibration
checkpoint (`docs/calibration_findings_2026-08-21.md`) found 15 of 95 merged
sources in the same state. `stale` compares each feed's own newest
`<pubDate>`/`<updated>` against today to catch this.

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
import re
import time
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import httpx

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (X11; Linux x86_64) CATS-calibration/1.0"
_XML_HINTS = (b"<?xml", b"<rss", b"<feed", b"<rdf")
_RETRY_BACKOFF_S = (2.0, 5.0)  # 429 is "try later", not "blocked" — a couple of
# spaced retries tells the two apart (2026-07-24: Strafatti Quotidiani flagged
# 'blocked' on a single 429 that a same-session retry immediately cleared).

# How long a feed's own newest item can go unrefreshed before it counts as
# 'stale' rather than 'ok'. Generous on purpose: every frozen feed found on
# 2026-08-21 had been stuck for 30+ days (most for months to years), so this
# is well clear of an ordinary quiet week and still catches all of them.
STALE_AFTER_DAYS = 14

_DATE_TAG_RE = re.compile(rb"<(?:pubDate|updated|published)>([^<]+)</(?:pubDate|updated|published)>", re.I)


def newest_item_date(body: bytes) -> Optional[datetime]:
    """The most recent parseable item timestamp in a feed body, or None.

    RSS/Atom list items newest-first by convention, so the first parseable
    date tag is taken as the feed's newest — not the max of all of them, so
    one corrupt future-dated item can't hide genuine staleness (the same
    failure mode found in the calibration dataset, see the module docstring).
    Tries RFC 822 (RSS ``pubDate``) first, then ISO 8601 (Atom
    ``updated``/``published``); a tag neither parses as is skipped, not fatal.
    """
    for raw in _DATE_TAG_RE.findall(body):
        text = raw.decode("utf-8", errors="replace").strip()
        try:
            dt = parsedate_to_datetime(text)
        except (TypeError, ValueError):
            try:
                dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
            except ValueError:
                continue
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    return None


def classify(url: str, timeout: float) -> Tuple[str, str]:
    """Return (status, detail) for one feed URL."""
    for attempt, backoff in enumerate((0.0,) + _RETRY_BACKOFF_S):
        if backoff:
            time.sleep(backoff)
        try:
            with httpx.Client(follow_redirects=True, timeout=timeout, headers={"User-Agent": UA}) as c:
                r = c.get(url)
        except httpx.TimeoutException:
            return "blocked", "timeout"
        except httpx.HTTPError as exc:
            return "dead", f"conn:{type(exc).__name__}"
        if r.status_code == 429 and attempt < len(_RETRY_BACKOFF_S):
            continue  # rate-limited, not necessarily blocked — retry before giving up
        break
    if r.status_code in (404, 410):
        return "dead", f"http:{r.status_code}"
    if r.status_code in (403, 429):
        return "blocked", f"http:{r.status_code}"
    if r.status_code >= 400:
        return "blocked", f"http:{r.status_code}"
    head = r.content[:512].lstrip().lower()
    if not any(h in head for h in _XML_HINTS):
        return "not-xml", f"http:{r.status_code}"
    newest = newest_item_date(r.content)
    if newest is not None:
        age = datetime.now(timezone.utc) - newest
        if age > timedelta(days=STALE_AFTER_DAYS):
            return "stale", f"newest:{newest.date().isoformat()} ({age.days}d ago)"
    return "ok", f"http:{r.status_code}"


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
