"""Check whether the publishers CATS collects from have reserved text and data mining (TDM).

Why. Italian law (L. 633/1941 art. 70-quater, implementing Directive (EU)
2019/790 art. 4) allows text and data mining by anyone with lawful access
*unless the rights holder has expressly reserved it*, for online content "in an
appropriate manner, such as machine-readable means". Whether CATS's RSS
collection can rely on that exception is an open question for the maintainer's
lawyer (``DATA_LICENSE`` §3). This script gathers the *machine-readable signals*
each publisher exposes, so the lawyer works from facts instead of guesses.

**It reports signals, not legal conclusions.** A reservation can also be made in
natural language, typically in a site's terms of use, which this script does not
read. Whether ``robots.txt`` counts as a valid reservation is itself debated. An
empty result therefore never means "TDM allowed".

Signals collected, per publisher in ``data/labels.jsonl``:

* **TDMRep** (W3C Community Group final report, 2024-05-10,
  https://www.w3.org/community/reports/tdmrep/CG-FINAL-tdmrep-20240510/):
  - ``/.well-known/tdmrep.json``: a JSON array of rules
    ``{"location", "tdm-reservation", "tdm-policy"?}``. The first rule whose
    ``location`` pattern matches the URL path applies (robots.txt-style
    patterns: ``*`` = any characters, trailing ``$`` = end of path).
  - The ``tdm-reservation`` / ``tdm-policy`` HTTP response headers.
  - ``<meta name="tdm-reservation">`` / ``<meta name="tdm-policy">`` in HTML.
  - Precedence, per the spec: the file first, then headers, then in-content
    metadata. Each later value supersedes the earlier one; an absent value
    never resets one. ``tdm-reservation`` must be ``0`` or ``1``; anything else
    counts as unset.
  - The effective value is computed for the feed URL CATS fetches and for the
    homepage.
* **robots.txt:** whether the feed path is disallowed for the generic agent
  (``*``), for CATS's own collector User-Agent, and for a list of well-known
  AI / TDM crawler agents (reported as context, since they are not CATS).

Fetches go through :func:`cats.core.url_guard.check_url` at every redirect hop
(threat model T9) and read at most ``MAX_BYTES`` per response. The script reads
public metadata only. It stores no article text.

Usage::

    python research/tdm_reservation_check.py --csv tdm.csv --json tdm.json
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx

from cats.core.url_guard import check_url

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 2_000_000
MAX_REDIRECTS = 5
TIMEOUT = 20.0
COLLECTOR_UA = "Mozilla/5.0 (X11; Linux x86_64) CATS-calibration/1.0"  # the UA collect-rss.yml uses
COLLECTOR_TOKEN = "CATS-calibration"
AI_AGENTS = (
    "GPTBot",
    "ChatGPT-User",
    "CCBot",
    "Google-Extended",
    "ClaudeBot",
    "anthropic-ai",
    "PerplexityBot",
    "Applebot-Extended",
    "Bytespider",
    "meta-externalagent",
    "cohere-ai",
    "Amazonbot",
)


# --------------------------------------------------------------------------- parsing (pure, unit-tested)


def _pattern_regex(location: str) -> "re.Pattern[str]":
    """robots.txt-style path pattern -> regex anchored at the path start."""
    anchored = location.endswith("$")
    body = location[:-1] if anchored else location
    regex = "".join(".*" if ch == "*" else re.escape(ch) for ch in body)
    return re.compile("^" + regex + ("$" if anchored else ""))


def tdmrep_rule_for(rules: Any, path: str) -> Optional[dict]:
    """First rule in a tdmrep.json array whose ``location`` matches ``path`` (None if none or malformed)."""
    if not isinstance(rules, list):
        return None
    for rule in rules:
        if not isinstance(rule, dict) or not isinstance(rule.get("location"), str):
            continue
        location = rule["location"]
        if not location.startswith("/") and not location.startswith("*"):
            location = "/" + location
        if _pattern_regex(location).match(path):
            return rule
    return None


def reservation_value(raw: Any) -> Optional[int]:
    """``1`` or ``0``; anything else is a protocol error and counts as unset (None)."""
    if isinstance(raw, bool):
        return None
    if raw in (0, 1):
        return int(raw)
    if isinstance(raw, str) and raw.strip() in ("0", "1"):
        return int(raw.strip())
    return None


class _MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: Dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag.lower() != "meta":
            return
        a = {k.lower(): (v or "") for k, v in attrs}
        name = a.get("name", "").strip().lower()
        if name in ("tdm-reservation", "tdm-policy") and name not in self.values:
            self.values[name] = a.get("content", "").strip()


def html_tdm_meta(html: str) -> Dict[str, str]:
    """``{"tdm-reservation": ..., "tdm-policy": ...}`` from HTML ``<meta>`` elements (only those present)."""
    parser = _MetaParser()
    try:
        parser.feed(html)
    except Exception:  # noqa: BLE001 - malformed HTML must not abort the audit
        pass
    return parser.values


def effective_reservation(
    file_rule: Optional[dict], headers: Dict[str, str], meta: Dict[str, str]
) -> Tuple[Optional[int], Optional[str], str]:
    """Apply the TDMRep precedence (file, then header, then HTML meta). Returns (reservation, policy, source)."""
    reservation: Optional[int] = None
    policy: Optional[str] = None
    source = "none"
    if file_rule is not None:
        value = reservation_value(file_rule.get("tdm-reservation"))
        if value is not None:
            reservation, source = value, "tdmrep.json"
        if isinstance(file_rule.get("tdm-policy"), str):
            policy = file_rule["tdm-policy"]
    for origin, values in (("http-header", headers), ("html-meta", meta)):
        value = reservation_value(values.get("tdm-reservation"))
        if value is not None:
            reservation, source = value, origin
        if values.get("tdm-policy"):
            policy = values["tdm-policy"]
    return reservation, policy, source


def robots_disallowed(robots_txt: str, url: str, agents: Tuple[str, ...]) -> Dict[str, bool]:
    """For each agent, True when robots.txt disallows fetching ``url``."""
    parser = RobotFileParser()
    parser.parse(robots_txt.splitlines())
    return {agent: not parser.can_fetch(agent, url) for agent in agents}


# --------------------------------------------------------------------------- fetching


@dataclass
class Fetched:
    status: Optional[int] = None
    headers: Dict[str, str] = field(default_factory=dict)
    text: str = ""
    final_url: str = ""
    error: str = ""


def guarded_get(url: str, client: httpx.Client) -> Fetched:
    """GET with the URL guard checked at every redirect hop and a size cap."""
    current = url
    try:
        for _ in range(MAX_REDIRECTS + 1):
            check_url(current)
            with client.stream("GET", current, follow_redirects=False) as resp:
                if resp.is_redirect and "location" in resp.headers:
                    current = str(resp.url.join(resp.headers["location"]))
                    continue
                chunks, total = [], 0
                for chunk in resp.iter_bytes():
                    total += len(chunk)
                    if total > MAX_BYTES:
                        break
                    chunks.append(chunk)
                text = b"".join(chunks).decode(resp.encoding or "utf-8", errors="replace")
                headers = {k.lower(): v for k, v in resp.headers.items()}
                return Fetched(resp.status_code, headers, text, current)
        return Fetched(error="too many redirects", final_url=current)
    except Exception as exc:  # noqa: BLE001 - one site failing must not stop the audit
        return Fetched(error=f"{type(exc).__name__}: {str(exc)[:120]}", final_url=current)


# --------------------------------------------------------------------------- per publisher


@dataclass
class PublisherReport:
    source_id: str
    host: str
    homepage: str
    feed: str
    tdmrep_file: str = "absent"  # absent | present | invalid | error
    tdmrep_rules: int = 0
    feed_reservation: Optional[int] = None
    feed_reservation_source: str = "none"
    home_reservation: Optional[int] = None
    home_reservation_source: str = "none"
    tdm_policy: Optional[str] = None
    robots: str = "absent"  # absent | present | error
    robots_feed_disallowed_star: Optional[bool] = None
    robots_feed_disallowed_collector: Optional[bool] = None
    robots_home_disallowed_ai_agents: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


def check_publisher(record: dict, client: httpx.Client) -> PublisherReport:
    feed = record.get("rss") or ""
    homepage = record.get("url") or feed
    parsed = urlparse(feed or homepage)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    report = PublisherReport(record.get("source_id", ""), parsed.hostname or "", homepage, feed)

    rules: Any = None
    tdm = guarded_get(origin + "/.well-known/tdmrep.json", client)
    if tdm.error:
        report.tdmrep_file = "error"
        report.errors.append(f"tdmrep.json: {tdm.error}")
    elif tdm.status == 200:
        try:
            rules = json.loads(tdm.text)
            report.tdmrep_file = "present" if isinstance(rules, list) else "invalid"
            report.tdmrep_rules = len(rules) if isinstance(rules, list) else 0
        except ValueError:
            report.tdmrep_file = "invalid"  # e.g. an HTML 'not found' page served with 200

    for target, attr in ((feed, "feed"), (homepage, "home")):
        if not target:
            continue
        fetched = guarded_get(target, client)
        if fetched.error:
            report.errors.append(f"{attr}: {fetched.error}")
        rule = tdmrep_rule_for(rules, urlparse(fetched.final_url or target).path or "/")
        headers = {k: v for k, v in fetched.headers.items() if k in ("tdm-reservation", "tdm-policy")}
        is_html = "html" in fetched.headers.get("content-type", "")
        meta = html_tdm_meta(fetched.text) if is_html else {}
        value, policy, source = effective_reservation(rule, headers, meta)
        setattr(report, f"{attr}_reservation", value)
        setattr(report, f"{attr}_reservation_source", source)
        report.tdm_policy = report.tdm_policy or policy

    robots = guarded_get(origin + "/robots.txt", client)
    if robots.error:
        report.robots = "error"
        report.errors.append(f"robots.txt: {robots.error}")
    elif robots.status == 200 and "html" not in robots.headers.get("content-type", ""):
        report.robots = "present"
        if feed:
            feed_rules = robots_disallowed(robots.text, feed, ("*", COLLECTOR_TOKEN))
            report.robots_feed_disallowed_star = feed_rules["*"]
            report.robots_feed_disallowed_collector = feed_rules[COLLECTOR_TOKEN]
        home_rules = robots_disallowed(robots.text, homepage, AI_AGENTS)
        report.robots_home_disallowed_ai_agents = [a for a, blocked in home_rules.items() if blocked]
    return report


def summarize(reports: List[PublisherReport]) -> Dict[str, Any]:
    n = len(reports)
    return {
        "publishers": n,
        "tdmrep_file_present": sum(r.tdmrep_file == "present" for r in reports),
        "feed_reserved_tdmrep": sum(r.feed_reservation == 1 for r in reports),
        "home_reserved_tdmrep": sum(r.home_reservation == 1 for r in reports),
        "explicitly_not_reserved_tdmrep": sum(r.feed_reservation == 0 or r.home_reservation == 0 for r in reports),
        "robots_present": sum(r.robots == "present" for r in reports),
        "feed_disallowed_for_star": sum(bool(r.robots_feed_disallowed_star) for r in reports),
        "feed_disallowed_for_collector": sum(bool(r.robots_feed_disallowed_collector) for r in reports),
        "blocks_any_ai_agent": sum(bool(r.robots_home_disallowed_ai_agents) for r in reports),
        "with_errors": sum(bool(r.errors) for r in reports),
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--labels", type=Path, default=ROOT / "data/labels.jsonl")
    parser.add_argument("--csv", type=Path, help="one row per publisher")
    parser.add_argument("--json", type=Path, help="summary plus per-publisher rows")
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args(argv)

    records = [json.loads(line) for line in args.labels.read_text(encoding="utf-8").splitlines() if line.strip()]
    records = [r for r in records if r.get("rss") or r.get("url")]

    def run(record: dict) -> PublisherReport:
        with httpx.Client(timeout=TIMEOUT, headers={"User-Agent": COLLECTOR_UA}) as client:
            return check_publisher(record, client)

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        reports = list(pool.map(run, records))

    summary = summarize(reports)
    rows = [asdict(r) for r in reports]
    if args.csv:
        with args.csv.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            for row in rows:
                row = dict(row)
                row["robots_home_disallowed_ai_agents"] = ";".join(row["robots_home_disallowed_ai_agents"])
                row["errors"] = " | ".join(row["errors"])
                writer.writerow(row)
    if args.json:
        args.json.write_text(json.dumps({"summary": summary, "publishers": rows}, indent=2) + "\n", encoding="utf-8")
    sys.stdout.write(json.dumps(summary, indent=2) + "\n")
    sys.stdout.write(
        "Signals only: terms-of-use reservations are not read. An empty result does NOT mean 'TDM allowed'.\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
