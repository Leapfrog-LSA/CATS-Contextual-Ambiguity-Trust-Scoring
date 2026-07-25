"""Feed-health audit: which RSS feeds in the label registry are dead?

Motivation. A dead feed silently shrinks (and biases) the collected dataset:
Il Corriere della Sera (label 85, a scarce Italian high-reliability source) was
never collected for months because its registered feed 404s — found by chance.
This script checks every feed in data/labels.jsonl so the rest are found on
purpose, not by accident.

It classifies each feed:
  * ok       — HTTP 200 and the body looks like XML/RSS/Atom
  * dead     — 404/410 or DNS/connection failure (genuinely broken → fix/replace)
  * blocked  — 403/429 or timeout (host likely blocks this User-Agent or is slow;
               ambiguous, not necessarily dead — flag, don't auto-remove)
  * not-xml  — 200 but the body is not a feed (redirect to an HTML page, etc.)

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
from pathlib import Path
from typing import Dict, List, Tuple

import httpx

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (X11; Linux x86_64) CATS-calibration/1.0"
_XML_HINTS = (b"<?xml", b"<rss", b"<feed", b"<rdf")
_RETRY_BACKOFF_S = (2.0, 5.0)  # 429 is "try later", not "blocked" — a couple of
# spaced retries tells the two apart (2026-07-24: Strafatti Quotidiani flagged
# 'blocked' on a single 429 that a same-session retry immediately cleared).


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
    if any(h in head for h in _XML_HINTS):
        return "ok", f"http:{r.status_code}"
    return "not-xml", f"http:{r.status_code}"


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

    results: Dict[str, List[Tuple[str, str, float, str]]] = {"dead": [], "blocked": [], "not-xml": [], "ok": []}

    def _check(item: Tuple[str, str, float]) -> Tuple[str, str, float, str, str]:
        sid, url, label = item
        status, detail = classify(url, args.timeout)
        return sid, url, label, status, detail

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for sid, url, label, status, detail in ex.map(_check, feeds):
            results[status].append((sid, url, label, detail))

    for status in ("ok", "blocked", "not-xml", "dead"):
        print(f"  {status:<9} {len(results[status])}")

    for status in ("dead", "not-xml"):
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
        "catalogue). 'blocked' may just refuse this User-Agent; re-check before removing."
    )


if __name__ == "__main__":
    main()
