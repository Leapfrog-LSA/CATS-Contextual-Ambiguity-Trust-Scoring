"""Aggregate-only observatory: source_type/language/country statistics, never source names.

Task 23, option (a) only — the maintainer's explicit decision after
weighing the three options in the plan (aggregates only / named sources
already in the group's public watchlist / full named ranking): **only
aggregate statistics, never any source identifier**, pending legal review
for the other two options.

This script merges the accumulated `data/snapshots/*.jsonl` (reusing
`cats.calibration.merge_snapshots`, not reimplementing the merge), scores
every source with the same production pipeline used everywhere else
(`cats.lite.score` — zero signal logic here, a thin aggregation layer over
it), and writes only grouped statistics to `docs/observatory/<date>.md`:
source count, band distribution and per-signal median, broken down by
`source_type`, detected language, and a best-effort country derived from
each source's domain ccTLD. No `source_id`, no URL, no domain, no per-source
score ever reaches the output — `_check_no_identifiers` (also exercised by
`tests/unit/test_observatory_aggregate.py`) asserts this before writing.

Usage::

    python research/observatory_aggregate.py \\
        --snapshots "data/snapshots/*.jsonl" --out docs/observatory/2026-09-17.md
"""

from __future__ import annotations

import argparse
import glob
import json
import statistics
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Sequence
from urllib.parse import urlparse

from cats.calibration.dataset import SIGNAL_NAMES
from cats.calibration.merge_snapshots import merge_records
from cats.lite import score

# Best-effort country label from a ccTLD. Deliberately small and generic-TLD
# aware: most of the registry is .com/.org/.net/.info/.eu/.media/.online/…,
# which carry no country signal at all and fall into "unknown (generic TLD)"
# rather than being guessed. This is NOT a verified per-source country field
# (none exists in the label schema) — it is a coarse proxy, documented as
# such in the generated report, and only ever used in an aggregate bucket.
_CCTLD_COUNTRY = {
    "it": "Italy",
    "fr": "France",
    "de": "Germany",
    "uk": "United Kingdom",
    "es": "Spain",
    "pt": "Portugal",
    "nl": "Netherlands",
    "be": "Belgium",
    "dk": "Denmark",
    "se": "Sweden",
    "no": "Norway",
    "fi": "Finland",
    "pl": "Poland",
    "ro": "Romania",
    "hu": "Hungary",
    "hr": "Croatia",
    "gr": "Greece",
    "ie": "Ireland",
    "ch": "Switzerland",
    "at": "Austria",
    "ua": "Ukraine",
    "ru": "Russia",
    "by": "Belarus",
    "us": "United States",
    "ca": "Canada",
    "mx": "Mexico",
    "za": "South Africa",
    "ng": "Nigeria",
    "ke": "Kenya",
    "tz": "Tanzania",
    "ug": "Uganda",
    "africa": "Africa (regional)",
    "jp": "Japan",
    "cn": "China",
    "tw": "Taiwan",
    "kr": "South Korea",
    "id": "Indonesia",
    "ph": "Philippines",
    "pk": "Pakistan",
    "in": "India",
    "il": "Israel",
    "tr": "Turkey",
    "ae": "United Arab Emirates",
    "au": "Australia",
    "nz": "New Zealand",
    "cl": "Chile",
    "br": "Brazil",
    "ar": "Argentina",
}
_GENERIC_TLDS = {"com", "org", "net", "info", "eu", "media", "online", "tv", "pics", "co", "biz", "io"}


def _country_from_url(url: Optional[str]) -> str:
    """Best-effort country label from a URL's TLD — see `_CCTLD_COUNTRY` above."""
    if not url:
        return "unknown (no URL)"
    host = urlparse(url).netloc or url
    host = host.split(":")[0].split("@")[-1]
    parts = [p for p in host.split(".") if p]
    if not parts:
        return "unknown (no URL)"
    tld = parts[-1].lower()
    if tld in _GENERIC_TLDS:
        return "unknown (generic TLD)"
    return _CCTLD_COUNTRY.get(tld, "unknown (unmapped TLD)")


def _load_snapshots(pattern: str) -> List[List[dict]]:
    paths = sorted(glob.glob(pattern))
    snapshots = []
    for path in paths:
        records = []
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        snapshots.append(records)
    return snapshots


def collect_source_stats(snapshot_pattern: str, *, load_nlp: bool = False) -> List[Dict]:
    """Score every merged source; return one stats dict per source (never persisted raw)."""
    snapshots = _load_snapshots(snapshot_pattern)
    if not snapshots:
        return []
    records, _total, _dupes = merge_records(snapshots)

    stats = []
    for record in records:
        messages = record.get("messages") or []
        if not messages:
            continue
        source_type = record.get("source_type") or "default"
        result = score(messages, source_type=source_type, load_nlp=load_nlp, explain=False)
        stats.append(
            {
                "source_type": source_type,
                "language": result["language"]["detected"],
                "country": _country_from_url(record.get("url")),
                "band": result["band"],
                "signals": {name: result["signals"][name] for name in SIGNAL_NAMES},
            }
        )
    return stats


def _aggregate_bucket(bucket_stats: List[Dict]) -> Dict:
    bands: Dict[str, int] = defaultdict(int)
    for s in bucket_stats:
        bands[s["band"]] += 1
    medians = {name: round(statistics.median(s["signals"][name] for s in bucket_stats), 2) for name in SIGNAL_NAMES}
    return {"n": len(bucket_stats), "bands": dict(bands), "median_signals": medians}


def build_aggregates(stats: List[Dict]) -> Dict[str, Dict[str, Dict]]:
    """Group stats by source_type / language / country — aggregates only, no identifiers."""
    grouped: Dict[str, Dict[str, List[Dict]]] = {
        "source_type": defaultdict(list),
        "language": defaultdict(list),
        "country": defaultdict(list),
    }
    for s in stats:
        grouped["source_type"][s["source_type"]].append(s)
        grouped["language"][s["language"]].append(s)
        grouped["country"][s["country"]].append(s)

    return {
        dimension: {key: _aggregate_bucket(bucket) for key, bucket in sorted(buckets.items())}
        for dimension, buckets in grouped.items()
    }


_IDENTIFIER_KEYS = {"source_id", "url", "rss", "domain"}


def _check_no_identifiers(aggregates: Dict) -> None:
    """Defence in depth: assert no per-source identifier leaked into the aggregate structure.

    `build_aggregates` never receives these keys by construction (`collect_source_stats`
    only forwards `source_type`/`language`/`country`/`band`/`signals`), but this
    keeps the guarantee explicit and machine-checked rather than only true "by
    reading the code" — the same check the test suite exercises independently.
    """

    def _walk(node) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(key, str) and key.lower() in _IDENTIFIER_KEYS:
                    raise AssertionError(f"identifier key {key!r} leaked into aggregate output")
                _walk(value)
        elif isinstance(node, (list, tuple)):
            for item in node:
                _walk(item)

    _walk(aggregates)


def render_markdown(aggregates: Dict[str, Dict[str, Dict]], *, report_date: str, total_sources: int) -> str:
    lines = [
        f"# CATS observatory — {report_date}",
        "",
        "Aggregate-only snapshot of the currently monitored source pool. **No source",
        "names, URLs or domains appear below or anywhere in this report** — only",
        "counts, band distributions and per-signal medians, grouped by category.",
        "Scores are ordinal (WP 4.3), not calibrated probabilities; a low median in a",
        "bucket describes the bucket's pattern, not any single source in it.",
        "",
        f"**Total scored sources: {total_sources}**",
        "",
        "`country` is a best-effort label derived from each source's domain ccTLD",
        "(not a verified field) — most sources sit on generic TLDs (`.com`, `.org`, …)",
        "and fall into an `unknown (generic TLD)` bucket rather than being guessed.",
        "",
    ]
    _DIMENSION_TITLES = {
        "source_type": "By source type",
        "language": "By detected language",
        "country": "By country (best-effort, ccTLD-derived)",
    }
    for dimension in ("source_type", "language", "country"):
        lines.append(f"## {_DIMENSION_TITLES[dimension]}")
        lines.append("")
        lines.append(
            "| Group | n | Band distribution | Median coherence | Median volatility | Median silence | Median gaming |"
        )
        lines.append("|---|--:|---|--:|--:|--:|--:|")
        for key, bucket in aggregates[dimension].items():
            bands_str = ", ".join(f"{band}: {n}" for band, n in sorted(bucket["bands"].items()))
            ms = bucket["median_signals"]
            lines.append(
                f"| {key} | {bucket['n']} | {bands_str} | {ms['coherence']} | {ms['volatility']} | "
                f"{ms['silence']} | {ms['gaming']} |"
            )
        lines.append("")
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshots", default="data/snapshots/*.jsonl", help="glob pattern for snapshot .jsonl files")
    parser.add_argument("--out", type=Path, default=None, help="output .md path; default docs/observatory/<today>.md")
    parser.add_argument("--load-nlp", action="store_true", help="load the spaCy NER model for coherence (slower)")
    args = parser.parse_args(argv)

    stats = collect_source_stats(args.snapshots, load_nlp=args.load_nlp)
    if not stats:
        print("No sources with messages found; nothing written.")
        return 1

    aggregates = build_aggregates(stats)
    _check_no_identifiers(aggregates)

    report_date = date.today().isoformat()
    out_path = args.out or Path(f"docs/observatory/{report_date}.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    markdown = render_markdown(aggregates, report_date=report_date, total_sources=len(stats))
    out_path.write_text(markdown, encoding="utf-8")

    print(f"Wrote aggregate-only observatory report for {len(stats)} source(s) -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
