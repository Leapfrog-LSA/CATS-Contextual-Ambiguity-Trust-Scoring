"""Read-only comparison of the CATS source catalogue with a local copy of the watchlist catalogue.

Why. CATS keeps its own copy of the OSINT source catalogue (``data/Fonti_OSINT.csv``)
and a curated label registry built from it (``data/labels.jsonl``). The sibling
repository ``Leapfrog-LSA/osint-sources-disinfo-watchlist`` keeps another copy of
the same catalogue (its ``Fonti_OSINT.csv``). The two copies have drifted apart.
Before the maintainer chooses how to align them, this script describes *where*
they differ — by normalised host and by normalised feed URL — and nothing else.

What it does **not** do:

* no network access: it reads only local files;
* no writes under ``data/`` and no change to any input file;
* no scores, no labels: the registry's ``label`` field is dropped on load and
  never used or reported;
* no alignment, deduplication or synchronisation rule: those stay open for the
  maintainer.

Normalisation reuses existing code: hosts go through
``cats.calibration.label_from_ratings.normalize_host`` (lower case, leading
``www.`` removed) and feed/homepage URLs through
``research.feed_health_audit.normalise_feed`` (lower case, scheme, ``www.`` and
trailing slash removed). ``normalize_host`` raises ``ValueError`` on some
malformed URLs (e.g. ``http://[bad``); such rows are counted as "host not
parseable" instead of stopping the run.

The roadmap (``docs/piano_sviluppo_roadmap_2026-09.md``) says the two copies
"diverge on 55 sources of the labelled registry", without documenting how that
was counted. The script computes every candidate definition listed in
``REGISTRY_DEFINITIONS`` and says which of them, if any, gives 55 on the copy
supplied. It does not pick one.

Usage (from the repository root; the ``research`` package must be importable,
so ``python research/catalog_watchlist_diff.py`` does not work)::

    python -m research.catalog_watchlist_diff \\
        --watchlist /path/to/osint-sources-disinfo-watchlist/Fonti_OSINT.csv \\
        --watchlist-commit <sha of that copy> [--out /tmp/detail.json]

The summary on stdout holds counts only. ``--out`` writes the per-source detail
(host lists and per-row classification, with source names) to a JSON file,
which must not be under ``data/`` and is not meant to be committed.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Sequence, Set, Tuple

from cats.calibration.label_from_ratings import normalize_host
from research.feed_health_audit import normalise_feed

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"

URL_COLUMN = "URL"
FEED_COLUMN = "RSS Feed"
NAME_COLUMN = "Fonte"
REQUIRED_COLUMNS: Tuple[str, ...] = (URL_COLUMN, FEED_COLUMN)

# Registry keys read from labels.jsonl. ``label`` is deliberately absent.
REGISTRY_KEYS: Tuple[str, ...] = ("source_id", "source_type", "url", "rss")

ROADMAP_FIGURE = 55


class HeaderError(ValueError):
    """The catalogue CSV lacks a column the comparison needs."""


# ── Loading ────────────────────────────────────────────────────────────────
def sha256_of(path: Path) -> str:
    """Hex SHA-256 of a file's bytes."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_catalog(path: Path) -> List[dict]:
    """Read a ``Fonti_OSINT``-shaped CSV; raise ``HeaderError`` if ``URL``/``RSS Feed`` are missing."""
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        header = [name.strip() for name in (reader.fieldnames or [])]
        missing = [col for col in REQUIRED_COLUMNS if col not in header]
        if missing:
            raise HeaderError(f"{path}: missing column(s) {', '.join(missing)}; header is {header}")
        rows = []
        for raw in reader:
            rows.append({(k or "").strip(): (v or "") for k, v in raw.items() if k is not None})
        return rows


def load_registry(path: Path) -> List[dict]:
    """Read ``labels.jsonl`` keeping only ``REGISTRY_KEYS`` (the ``label`` field is dropped)."""
    rows: List[dict] = []
    with path.open(encoding="utf-8-sig") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            rows.append({key: record.get(key) for key in REGISTRY_KEYS})
    return rows


# ── Normalisation ──────────────────────────────────────────────────────────
def safe_host(url: Optional[str]) -> Optional[str]:
    """Normalised host; '' for an empty URL; ``None`` when ``normalize_host`` raises."""
    try:
        return normalize_host(str(url or ""))
    except ValueError:
        return None


def feed_key(url: Optional[str]) -> str:
    """Normalised feed/homepage URL; '' for an empty cell."""
    text = str(url or "").strip()
    return normalise_feed(text) if text else ""


# ── Indexing ───────────────────────────────────────────────────────────────
@dataclass
class CatalogIndex:
    """One catalogue copy, indexed by normalised host and by normalised feed."""

    rows: int = 0
    rows_by_host: Dict[str, List[int]] = field(default_factory=dict)
    feeds_by_host: Dict[str, Set[str]] = field(default_factory=dict)
    homepages_by_host: Dict[str, Set[str]] = field(default_factory=dict)
    rows_by_feed: Dict[str, List[int]] = field(default_factory=dict)
    names: List[str] = field(default_factory=list)
    unparseable_host_rows: List[int] = field(default_factory=list)
    empty_host_rows: List[int] = field(default_factory=list)

    @property
    def hosts(self) -> Set[str]:
        return set(self.rows_by_host)

    @property
    def feeds(self) -> Set[str]:
        return set(self.rows_by_feed)


def index_catalog(rows: Sequence[dict]) -> CatalogIndex:
    """Index catalogue rows by normalised host (from ``URL``) and normalised feed (``RSS Feed``)."""
    index = CatalogIndex(rows=len(rows))
    for i, row in enumerate(rows):
        index.names.append(str(row.get(NAME_COLUMN) or "").strip())
        feed = feed_key(row.get(FEED_COLUMN))
        if feed:
            index.rows_by_feed.setdefault(feed, []).append(i)
        host = safe_host(row.get(URL_COLUMN))
        if host is None:
            index.unparseable_host_rows.append(i)
            continue
        if not host:
            index.empty_host_rows.append(i)
            continue
        index.rows_by_host.setdefault(host, []).append(i)
        feeds = index.feeds_by_host.setdefault(host, set())
        if feed:
            feeds.add(feed)
        homepage = feed_key(row.get(URL_COLUMN))
        index.homepages_by_host.setdefault(host, set()).add(homepage)
    return index


# ── Catalogue vs catalogue ─────────────────────────────────────────────────
CATALOG_DEFINITIONS: Dict[str, str] = {
    "hosts_only_cats": "normalised hosts present in the CATS catalogue and absent from the watchlist",
    "hosts_only_watchlist": "normalised hosts present in the watchlist and absent from the CATS catalogue",
    "hosts_common": "normalised hosts present in both copies",
    "feeds_only_cats": "normalised feed URLs present in the CATS catalogue and absent from the watchlist",
    "feeds_only_watchlist": "normalised feed URLs present in the watchlist and absent from the CATS catalogue",
    "feeds_common": "normalised feed URLs present in both copies",
    "multi_row_hosts_cats": "hosts with more than one row in the CATS catalogue",
    "multi_row_hosts_watchlist": "hosts with more than one row in the watchlist",
    "common_hosts_feed_differs": (
        "common hosts where both copies list at least one feed and the two sets of normalised feeds differ"
    ),
    "common_hosts_feed_disjoint": (
        "subset of the previous: common hosts whose two non-empty feed sets share no feed at all"
    ),
    "common_hosts_feed_only_cats": "common hosts with a feed in the CATS catalogue and no feed in the watchlist",
    "common_hosts_feed_only_watchlist": "common hosts with a feed in the watchlist and no feed in the CATS catalogue",
    "unparseable_host_rows_cats": "CATS catalogue rows whose URL cannot be parsed into a host",
    "unparseable_host_rows_watchlist": "watchlist rows whose URL cannot be parsed into a host",
    "empty_url_rows_cats": "CATS catalogue rows with an empty URL",
    "empty_url_rows_watchlist": "watchlist rows with an empty URL",
}


def compare_catalogs(cats: CatalogIndex, watchlist: CatalogIndex) -> Dict[str, List[str]]:
    """Return, for each key of ``CATALOG_DEFINITIONS``, the sorted list of hosts/feeds/rows it counts."""
    common = cats.hosts & watchlist.hosts
    differs: List[str] = []
    disjoint: List[str] = []
    only_cats_feed: List[str] = []
    only_watchlist_feed: List[str] = []
    for host in common:
        mine = cats.feeds_by_host.get(host, set())
        theirs = watchlist.feeds_by_host.get(host, set())
        if mine and theirs:
            if mine != theirs:
                differs.append(host)
                if not mine & theirs:
                    disjoint.append(host)
        elif mine:
            only_cats_feed.append(host)
        elif theirs:
            only_watchlist_feed.append(host)

    def row_labels(index: CatalogIndex, rows: List[int]) -> List[str]:
        return [f"row {i + 2}: {index.names[i]}" for i in rows]  # +2: header line and 1-based numbering

    return {
        "hosts_only_cats": sorted(cats.hosts - watchlist.hosts),
        "hosts_only_watchlist": sorted(watchlist.hosts - cats.hosts),
        "hosts_common": sorted(common),
        "feeds_only_cats": sorted(cats.feeds - watchlist.feeds),
        "feeds_only_watchlist": sorted(watchlist.feeds - cats.feeds),
        "feeds_common": sorted(cats.feeds & watchlist.feeds),
        "multi_row_hosts_cats": sorted(h for h, r in cats.rows_by_host.items() if len(r) > 1),
        "multi_row_hosts_watchlist": sorted(h for h, r in watchlist.rows_by_host.items() if len(r) > 1),
        "common_hosts_feed_differs": sorted(differs),
        "common_hosts_feed_disjoint": sorted(disjoint),
        "common_hosts_feed_only_cats": sorted(only_cats_feed),
        "common_hosts_feed_only_watchlist": sorted(only_watchlist_feed),
        "unparseable_host_rows_cats": row_labels(cats, cats.unparseable_host_rows),
        "unparseable_host_rows_watchlist": row_labels(watchlist, watchlist.unparseable_host_rows),
        "empty_url_rows_cats": row_labels(cats, cats.empty_host_rows),
        "empty_url_rows_watchlist": row_labels(watchlist, watchlist.empty_host_rows),
    }


# ── Registry vs watchlist ──────────────────────────────────────────────────
@dataclass
class RegistryRow:
    """How one registry row compares with the watchlist (no label)."""

    source_id: str
    source_type: str
    host: str
    host_status: str  # "in_watchlist" | "absent" | "no_host" | "unparseable"
    feed_status: str  # "same" | "different" | "registry_only" | "watchlist_only" | "both_empty" | "n/a"
    homepage_differs: bool
    feed_anywhere_in_watchlist: bool
    has_feed: bool = False


def classify_registry(registry: Sequence[dict], watchlist: CatalogIndex) -> List[RegistryRow]:
    """Classify each registry row against the watchlist by host, feed and homepage.

    Feed comparison is per host: the registry feed is "same" when it equals any
    of the watchlist's normalised feeds for that host (a host can have several
    watchlist rows).
    """
    out: List[RegistryRow] = []
    for record in registry:
        host = safe_host(record.get("url"))
        feed = feed_key(record.get("rss"))
        anywhere = bool(feed) and feed in watchlist.rows_by_feed
        if host is None or not host:
            out.append(
                RegistryRow(
                    source_id=str(record.get("source_id") or ""),
                    source_type=str(record.get("source_type") or ""),
                    host="",
                    host_status="unparseable" if host is None else "no_host",
                    feed_status="n/a",
                    homepage_differs=False,
                    feed_anywhere_in_watchlist=anywhere,
                    has_feed=bool(feed),
                )
            )
            continue
        if host not in watchlist.rows_by_host:
            host_status, feed_status, homepage_differs = "absent", "n/a", False
        else:
            host_status = "in_watchlist"
            theirs = watchlist.feeds_by_host.get(host, set())
            if feed and feed in theirs:
                feed_status = "same"
            elif feed and theirs:
                feed_status = "different"
            elif feed:
                feed_status = "registry_only"
            elif theirs:
                feed_status = "watchlist_only"
            else:
                feed_status = "both_empty"
            homepage_differs = feed_key(record.get("url")) not in watchlist.homepages_by_host.get(host, set())
        out.append(
            RegistryRow(
                source_id=str(record.get("source_id") or ""),
                source_type=str(record.get("source_type") or ""),
                host=host,
                host_status=host_status,
                feed_status=feed_status,
                homepage_differs=homepage_differs,
                feed_anywhere_in_watchlist=anywhere,
                has_feed=bool(feed),
            )
        )
    return out


def _absent(r: RegistryRow) -> bool:
    return r.host_status != "in_watchlist"


def _feed_mismatch(r: RegistryRow) -> bool:
    return r.feed_status in ("different", "registry_only", "watchlist_only")


# (key, plain-language definition, predicate). Each is a *candidate* reading of
# "registry source on which the two copies diverge"; none is preferred.
REGISTRY_DEFINITIONS: Tuple[Tuple[str, str, Callable[[RegistryRow], bool]], ...] = (
    (
        "D1_host_absent",
        "registry rows whose homepage host is not in the watchlist (or has no parseable host)",
        _absent,
    ),
    (
        "D2_feed_different",
        "host in the watchlist, both sides have a feed, and the registry feed matches none of the watchlist "
        "feeds for that host",
        lambda r: r.feed_status == "different",
    ),
    (
        "D3a_feed_watchlist_only",
        "host in the watchlist, the registry has no feed, the watchlist has one for that host",
        lambda r: r.feed_status == "watchlist_only",
    ),
    (
        "D3b_feed_registry_only",
        "host in the watchlist, the registry has a feed, the watchlist has none for that host",
        lambda r: r.feed_status == "registry_only",
    ),
    (
        "D4_feed_mismatch",
        "D2 or D3a or D3b: host in the watchlist and the feed is not the same on both sides "
        "(rows where both sides have no feed are not counted)",
        _feed_mismatch,
    ),
    (
        "D5_homepage_differs",
        "host in the watchlist, but the registry homepage (normalised URL) matches none of the watchlist "
        "homepages for that host",
        lambda r: r.homepage_differs,
    ),
    (
        "D6_absent_or_feed_mismatch",
        "D1 or D4",
        lambda r: _absent(r) or _feed_mismatch(r),
    ),
    (
        "D7_feed_mismatch_or_homepage",
        "D4 or D5",
        lambda r: _feed_mismatch(r) or r.homepage_differs,
    ),
    (
        "D8_any_divergence",
        "D1 or D4 or D5",
        lambda r: _absent(r) or _feed_mismatch(r) or r.homepage_differs,
    ),
    (
        "D9_feed_not_in_watchlist",
        "registry rows with a feed that appears nowhere among the watchlist feeds, whatever the host",
        lambda r: r.has_feed and not r.feed_anywhere_in_watchlist,
    ),
)


def count_definitions(rows: Sequence[RegistryRow]) -> List[Tuple[str, str, int]]:
    """Count registry rows meeting each candidate definition in ``REGISTRY_DEFINITIONS``."""
    return [(key, text, sum(1 for r in rows if predicate(r))) for key, text, predicate in REGISTRY_DEFINITIONS]


def roadmap_check(counts: Sequence[Tuple[str, str, int]], target: int = ROADMAP_FIGURE) -> List[str]:
    """Keys of the definitions whose count equals ``target`` (empty → not reproducible)."""
    return [key for key, _text, total in counts if total == target]


# ── Rendering ──────────────────────────────────────────────────────────────
def render_summary(
    *,
    meta: Dict[str, str],
    sizes: Dict[str, int],
    catalog_diff: Dict[str, List[str]],
    registry_rows: Sequence[RegistryRow],
    counts: Sequence[Tuple[str, str, int]],
) -> str:
    """Markdown summary with counts only (no source names)."""
    lines = ["# CATS catalogue vs watchlist catalogue (counts only)", ""]
    for key, value in meta.items():
        lines.append(f"- {key}: `{value}`")
    lines += ["", "## Inputs", "", "| Input | Rows |", "|---|---:|"]
    for key, value in sizes.items():
        lines.append(f"| {key} | {value:,} |")
    lines += ["", "## Catalogue vs catalogue", "", "| Count | Value | Definition |", "|---|---:|---|"]
    for key, text in CATALOG_DEFINITIONS.items():
        lines.append(f"| {key} | {len(catalog_diff[key]):,} | {text} |")

    lines += ["", "## Registry vs watchlist", "", "| Host status | Rows |", "|---|---:|"]
    for status in ("in_watchlist", "absent", "no_host", "unparseable"):
        lines.append(f"| {status} | {sum(1 for r in registry_rows if r.host_status == status):,} |")
    lines += ["", "| Feed status (host in watchlist) | Rows |", "|---|---:|"]
    for status in ("same", "different", "registry_only", "watchlist_only", "both_empty"):
        lines.append(f"| {status} | {sum(1 for r in registry_rows if r.feed_status == status):,} |")
    homepage = sum(1 for r in registry_rows if r.homepage_differs)
    lines += ["", f"Homepage differs at the same host: {homepage:,} rows.", ""]

    lines += [
        f"## Candidate definitions of a diverging registry source (roadmap figure: {ROADMAP_FIGURE})",
        "",
        "| Definition | Rows | Meaning |",
        "|---|---:|---|",
    ]
    for key, text, total in counts:
        lines.append(f"| {key} | {total:,} | {text} |")
    matches = roadmap_check(counts)
    lines.append("")
    if matches:
        lines.append(f"{ROADMAP_FIGURE} is reproduced on this copy by: {', '.join(matches)}.")
    else:
        lines.append(f"{ROADMAP_FIGURE}: not reproducible with any candidate definition on this copy.")
    return "\n".join(lines) + "\n"


def _is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m research.catalog_watchlist_diff",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--watchlist", required=True, type=Path, help="local copy of the watchlist Fonti_OSINT.csv")
    parser.add_argument("--watchlist-commit", required=True, help="git commit of that copy (reported, not checked)")
    parser.add_argument("--catalog", type=Path, default=DATA_DIR / "Fonti_OSINT.csv", help="CATS catalogue CSV")
    parser.add_argument("--labels", type=Path, default=DATA_DIR / "labels.jsonl", help="CATS label registry")
    parser.add_argument("--out", type=Path, help="per-source detail as JSON (refused under data/)")
    args = parser.parse_args(argv)

    for path in (args.watchlist, args.catalog, args.labels):
        if not path.is_file():
            sys.stderr.write(f"error: file not found: {path}\n")
            return 2
    if args.out is not None and _is_under(args.out, DATA_DIR):
        sys.stderr.write(f"error: --out must not be under {DATA_DIR}: {args.out}\n")
        return 2

    try:
        cats_rows = load_catalog(args.catalog)
        watchlist_rows = load_catalog(args.watchlist)
    except HeaderError as exc:
        sys.stderr.write(f"error: {exc}\n")
        return 2
    registry = load_registry(args.labels)

    cats_index = index_catalog(cats_rows)
    watchlist_index = index_catalog(watchlist_rows)
    catalog_diff = compare_catalogs(cats_index, watchlist_index)
    registry_rows = classify_registry(registry, watchlist_index)
    counts = count_definitions(registry_rows)

    meta = {
        "watchlist commit": args.watchlist_commit,
        "watchlist sha256": sha256_of(args.watchlist),
        "CATS catalogue sha256": sha256_of(args.catalog),
        "CATS registry sha256": sha256_of(args.labels),
    }
    sizes = {
        "CATS catalogue rows": cats_index.rows,
        "watchlist rows": watchlist_index.rows,
        "registry rows": len(registry),
        "registry distinct source_id": len({str(r.get("source_id") or "") for r in registry}),
    }
    sys.stdout.write(
        render_summary(meta=meta, sizes=sizes, catalog_diff=catalog_diff, registry_rows=registry_rows, counts=counts)
    )

    if args.out is not None:
        payload = {
            "meta": meta,
            "sizes": sizes,
            "catalog": catalog_diff,
            "registry": [asdict(r) for r in registry_rows],
            "definitions": [{"key": k, "definition": t, "rows": n} for k, t, n in counts],
            "roadmap_figure_matches": roadmap_check(counts),
        }
        args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
