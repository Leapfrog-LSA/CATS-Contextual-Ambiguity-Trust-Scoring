"""RSS/Atom collector: attach message histories to a distant-supervision label registry.

:mod:`cats.calibration.label_from_ratings` produces the *labels* half of a
calibration dataset — one ``{source_id, source_type, label, url, rss}`` record
per rated source. This module fills in the other half: it fetches each source's
``rss`` feed, extracts timestamped entries, and emits *labelled sources*
(``{..., "messages": [...]}``) ready for :mod:`cats.calibration.split` and
:mod:`cats.calibration.build_dataset`.

Feed handling
-------------
* RSS 2.0, RSS 1.0 (RDF) and Atom are supported; namespaces are matched by
  local name so ``dc:date`` etc. work without registration.
* Each entry becomes ``{"timestamp": <ISO-8601 UTC>, "text": title [+ summary]}``.
  HTML markup in titles/summaries is stripped; entries without a parseable
  date or any text are dropped (the pipeline normaliser would reject them).
* Defensive parsing: responses are capped at ``--max-bytes`` and documents
  carrying a DTD (``<!DOCTYPE``) are rejected outright.

Sources whose feed fails (missing ``rss``, HTTP error, unparseable XML, fewer
than ``--min-messages`` usable entries) are skipped with a diagnostic — the
output only contains sources that ``build_dataset`` can actually use.

Usage::

    python -m cats.calibration.collect_rss \\
        --labels labels.jsonl --out labelled_sources.jsonl

Then::

    python -m cats.calibration.split --input labelled_sources.jsonl --holdout-fraction 0.2
"""

from __future__ import annotations

import argparse
import json
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple
from xml.etree import ElementTree

import httpx
import structlog

logger = structlog.get_logger()

DEFAULT_MIN_MESSAGES = 3
DEFAULT_MAX_MESSAGES = 200
DEFAULT_TIMEOUT = 15.0
DEFAULT_WORKERS = 8
DEFAULT_MAX_BYTES = 5 * 1024 * 1024
DEFAULT_USER_AGENT = "CATS-calibration-collector/1.0 (+https://github.com/Leapfrog-LSA)"

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


# ── Entry extraction ────────────────────────────────────────────────────────
def strip_html(raw: str) -> str:
    """Drop markup and collapse whitespace: feed titles/summaries often carry HTML."""
    # unescape first: RSS descriptions usually carry HTML as &lt;p&gt;…&lt;/p&gt;
    return _WS_RE.sub(" ", _TAG_RE.sub(" ", unescape(raw or ""))).strip()


def parse_timestamp(raw: str) -> Optional[str]:
    """RFC 822 (RSS) or ISO-8601 (Atom/dc) date → ISO-8601 UTC string; ``None`` if neither."""
    raw = (raw or "").strip()
    if not raw:
        return None
    dt: Optional[datetime] = None
    try:
        dt = parsedate_to_datetime(raw)
    except (ValueError, TypeError):
        try:
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _entry_fields(entry: ElementTree.Element) -> Dict[str, str]:
    """First non-empty text per child local name (namespace-agnostic), lowercased keys."""
    fields: Dict[str, str] = {}
    for child in entry:
        name = _localname(child.tag)
        text = (child.text or "").strip()
        if name == "link" and not text:  # Atom: <link href="..."/>
            text = (child.get("href") or "").strip()
        if text and name not in fields:
            fields[name] = text
    return fields


def parse_feed(xml_text: str) -> List[dict]:
    """Extract ``{"timestamp", "text", "metadata"}`` messages from an RSS/Atom document.

    Raises ``ValueError`` for documents that are not well-formed XML, carry a
    DTD, or contain no ``<item>``/``<entry>`` elements.
    """
    if "<!DOCTYPE" in xml_text[:4096].upper():
        raise ValueError("feed carries a DTD; refusing to parse")
    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError as exc:
        raise ValueError(f"not well-formed XML: {exc}") from exc

    entries = [el for el in root.iter() if _localname(el.tag) in ("item", "entry")]
    if not entries:
        raise ValueError("no <item>/<entry> elements found")

    messages: List[dict] = []
    for entry in entries:
        f = _entry_fields(entry)
        # RSS: pubDate | dc:date; Atom: published | updated
        ts = None
        for key in ("pubdate", "published", "date", "updated"):
            if key in f:
                ts = parse_timestamp(f[key])
                if ts:
                    break
        title = strip_html(f.get("title", ""))
        summary = strip_html(f.get("description") or f.get("summary") or f.get("content") or "")
        if summary and title and summary.lower().startswith(title.lower()):
            title = ""  # some feeds repeat the title inside the description
        text = ". ".join(part for part in (title, summary) if part)
        if not ts or not text:
            continue
        msg: dict = {"timestamp": ts, "text": text}
        link = f.get("link")
        if link:
            msg["metadata"] = {"link": link}
        messages.append(msg)
    return messages


# ── Fetching ────────────────────────────────────────────────────────────────
def fetch_feed(url: str, client: httpx.Client, max_bytes: int = DEFAULT_MAX_BYTES) -> str:
    """GET one feed and return its body; ``ValueError`` on HTTP error or oversize body."""
    try:
        resp = client.get(url)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        raise ValueError(f"fetch failed: {exc}") from exc
    if len(resp.content) > max_bytes:
        raise ValueError(f"feed exceeds {max_bytes} bytes")
    return resp.text


# ── Attaching messages to the registry ──────────────────────────────────────
@dataclass
class CollectStats:
    total_sources: int = 0
    collected: int = 0
    no_feed: int = 0
    feed_error: int = 0  # fetch or parse failure
    too_few_messages: int = 0
    total_messages: int = 0
    by_source_type: Dict[str, int] = field(default_factory=dict)


def attach_messages(
    registry: List[dict],
    fetch: Callable[[str], List[dict]],
    min_messages: int = DEFAULT_MIN_MESSAGES,
    max_messages: int = DEFAULT_MAX_MESSAGES,
    since: Optional[str] = None,
    workers: int = DEFAULT_WORKERS,
) -> Tuple[List[dict], CollectStats]:
    """Fetch every registry entry's feed and emit labelled-source records.

    ``fetch`` maps a feed URL to a message list (fetch+parse), raising
    ``ValueError`` on failure — injected so tests and alternative collectors
    can bypass the network. Feeds are fetched concurrently but results keep
    the registry order, so runs are reproducible.
    """
    stats = CollectStats(total_sources=len(registry))
    with_feed = [(i, rec) for i, rec in enumerate(registry) if (rec.get("rss") or "").strip()]
    stats.no_feed = len(registry) - len(with_feed)

    def _one(rec: dict) -> List[dict]:
        return fetch(str(rec["rss"]).strip())

    results: List[Optional[List[dict]]] = [None] * len(with_feed)
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = [pool.submit(_one, rec) for _, rec in with_feed]
        for slot, ((_, rec), fut) in enumerate(zip(with_feed, futures)):
            sid = rec.get("source_id", rec.get("rss"))
            try:
                results[slot] = fut.result()
            except ValueError as exc:
                logger.warning("collect_rss_feed_error", source=sid, error=str(exc))
                stats.feed_error += 1

    records: List[dict] = []
    for (_, rec), messages in zip(with_feed, results):
        if messages is None:
            continue
        if since:
            messages = [m for m in messages if m["timestamp"] >= since]
        messages.sort(key=lambda m: m["timestamp"])
        messages = messages[-max_messages:]
        if len(messages) < min_messages:
            sid = rec.get("source_id", rec.get("rss"))
            logger.warning("collect_rss_too_few_messages", source=sid, messages=len(messages))
            stats.too_few_messages += 1
            continue
        out = dict(rec)
        out["messages"] = messages
        records.append(out)
        stats.collected += 1
        stats.total_messages += len(messages)
        st = str(rec.get("source_type") or "default")
        stats.by_source_type[st] = stats.by_source_type.get(st, 0) + 1
    return records, stats


# ── CLI ─────────────────────────────────────────────────────────────────────
def _read_jsonl(path: Path) -> List[dict]:
    raw = path.read_text(encoding="utf-8").strip()
    return [json.loads(line) for line in raw.splitlines() if line.strip()] if raw else []


def _write_jsonl(records: List[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m cats.calibration.collect_rss",
        description="Fetch each labelled source's RSS/Atom feed and attach its messages.",
    )
    parser.add_argument("--labels", required=True, type=Path, help="label registry (.jsonl from label_from_ratings)")
    parser.add_argument("--out", required=True, type=Path, help="output labelled sources (.jsonl)")
    parser.add_argument(
        "--min-messages",
        type=int,
        default=DEFAULT_MIN_MESSAGES,
        help=f"skip sources with fewer usable entries (default: {DEFAULT_MIN_MESSAGES})",
    )
    parser.add_argument(
        "--max-messages",
        type=int,
        default=DEFAULT_MAX_MESSAGES,
        help=f"keep at most the N most recent entries per source (default: {DEFAULT_MAX_MESSAGES})",
    )
    parser.add_argument("--since", default=None, help="drop entries older than this ISO-8601 UTC instant")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="per-feed HTTP timeout in seconds")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help="concurrent feed fetches")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="reject feeds larger than this")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="User-Agent header for feed requests")
    args = parser.parse_args(argv)

    if not args.labels.exists():
        parser.error(f"labels file not found: {args.labels}")
    since = None
    if args.since:
        since = parse_timestamp(args.since)
        if since is None:
            parser.error(f"--since is not a parseable date: {args.since}")

    registry = _read_jsonl(args.labels)
    if not registry:
        parser.error(f"no records found in {args.labels}")

    with httpx.Client(
        timeout=args.timeout,
        follow_redirects=True,
        headers={"User-Agent": args.user_agent},
    ) as client:

        def fetch(url: str) -> List[dict]:
            return parse_feed(fetch_feed(url, client, max_bytes=args.max_bytes))

        records, stats = attach_messages(
            registry,
            fetch,
            min_messages=args.min_messages,
            max_messages=args.max_messages,
            since=since,
            workers=args.workers,
        )

    if not records:
        print("No sources yielded enough messages; nothing written.")
        print(f"  registry: {stats.total_sources}, no feed: {stats.no_feed}, feed errors: {stats.feed_error}")
        return 1

    _write_jsonl(records, args.out)
    print(f"Wrote {stats.collected} labelled source(s) with messages to {args.out}")
    print(
        f"  registry {stats.total_sources}: no feed {stats.no_feed}, feed errors {stats.feed_error}, "
        f"too few messages {stats.too_few_messages}"
    )
    print(f"  {stats.total_messages} message(s) total")
    print("  source_type distribution:")
    for st, n in sorted(stats.by_source_type.items()):
        print(f"    {st:12s} {n}")
    print(
        "\nNext: temporal split, then build the dataset:\n"
        f"  python -m cats.calibration.split --input {args.out} --holdout-fraction 0.2"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
