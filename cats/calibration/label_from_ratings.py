"""Distant-supervision labels: join an OSINT source catalogue with external ratings.

Distant supervision reuses *existing* reliability ratings (NewsGuard, Media
Bias/Fact Check, fact-checker verdicts, …) as ground-truth labels instead of
hand-annotating each source. This module performs the join and the scale
mapping; it **never invents a rating** — every label comes from the ratings
file you supply.

Inputs
------
* **sources CSV** — the OSINT catalogue (``Fonti_OSINT`` shape). Required columns:
  ``Fonte`` (name), ``URL``. Optional: ``Macro-categoria`` (→ source_type),
  ``RSS Feed``, ``Lingua``, ``Paese / Area``.
* **ratings file** — ``.csv`` (columns ``domain``/``url`` + ``rating``) or ``.json``
  (``{host: rating}`` or ``[{"domain": ..., "rating": ...}]``). Hosts are matched
  by normalised hostname (lowercased, ``www.`` stripped), so the OSINT ``URL`` and
  the ratings ``domain``/``url`` join regardless of scheme or ``www``.

Output
------
A **label registry** ``.jsonl``: one ``{source_id, source_type, label, url, rss}``
record per *matched* source — the *labels* half of a calibration dataset.
Messages are attached in a later step (e.g. from the RSS feeds) before
``build_dataset`` computes the four signals.

Usage::

    python -m cats.calibration.label_from_ratings \\
        --sources Fonti_OSINT.csv --ratings mbfc.csv --scale mbfc --out labels.jsonl
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

from cats.scoring.engine import determine_band

# ── Rating-scale → CATS 0-100 ordinal label ────────────────────────────────
# Built-in mappings. Labels need only be ordinally sensible (calibration
# optimises rank agreement), so the exact midpoints are conventional.
MBFC_SCALE: Dict[str, float] = {
    "very high": 95.0,
    "high": 85.0,
    "mostly factual": 70.0,
    "mixed": 50.0,
    "low": 30.0,
    "very low": 10.0,
}

# NATO Admiralty Code reliability of source (A best … F cannot be judged → skip).
ADMIRALTY_SCALE: Dict[str, float] = {
    "a": 95.0,
    "b": 78.0,
    "c": 60.0,
    "d": 42.0,
    "e": 20.0,
}


def map_label(raw: str, scale: str, custom: Optional[Dict[str, float]] = None) -> Optional[float]:
    """Map one raw rating to a 0-100 label; ``None`` if it cannot be mapped.

    ``scale``: ``mbfc`` | ``admiralty`` | ``numeric`` | ``custom``. ``numeric``
    passes a 0-100 score through (clamped); ``custom`` uses the provided dict
    keyed by lowercased rating string.
    """
    raw = (raw or "").strip()
    if not raw:
        return None
    if scale == "numeric":
        try:
            return max(0.0, min(float(raw), 100.0))
        except ValueError:
            return None
    table = {
        "mbfc": MBFC_SCALE,
        "admiralty": ADMIRALTY_SCALE,
        "custom": {k.lower(): float(v) for k, v in (custom or {}).items()},
    }.get(scale)
    if table is None:
        raise ValueError(f"unknown scale '{scale}'; choose mbfc|admiralty|numeric|custom")
    return table.get(raw.lower())


# ── Source-type derivation from the catalogue category ─────────────────────
def source_type_from_category(category: str) -> str:
    """Map an OSINT macro-category onto a CATS scoring group (social/news/default)."""
    c = (category or "").lower()
    if "social" in c:
        return "social"
    if any(k in c for k in ("media", "testate", "giornalist", "fact-check", "fact check", "stampa")):
        return "news"
    return "default"


def normalize_host(url: str) -> str:
    """Lowercased hostname with a leading ``www.`` removed; '' if unparseable."""
    raw = (url or "").strip()
    if not raw:
        return ""
    if "//" not in raw:
        raw = "//" + raw  # let urlparse read a bare "example.com/x" as netloc
    host = (urlparse(raw).hostname or "").lower()
    return host[4:] if host.startswith("www.") else host


# ── Loading ────────────────────────────────────────────────────────────────
def load_ratings(path: Path) -> Dict[str, str]:
    """Load ratings keyed by normalised host → raw rating string."""
    out: Dict[str, str] = {}
    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = [{"domain": k, "rating": v} for k, v in data.items()] if isinstance(data, dict) else list(data)
    else:
        with path.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
    for row in rows:
        key = row.get("domain") or row.get("url") or row.get("host") or ""
        host = normalize_host(str(key))
        rating = row.get("rating")
        if host and rating is not None:
            out[host] = str(rating)
    return out


@dataclass
class RegistryStats:
    total_sources: int = 0
    matched: int = 0
    unmapped_rating: int = 0  # matched a host but the rating did not map to a label
    by_band: Dict[str, int] = field(default_factory=dict)
    by_source_type: Dict[str, int] = field(default_factory=dict)


def build_label_registry(
    sources: List[dict],
    ratings: Dict[str, str],
    scale: str,
    custom: Optional[Dict[str, float]] = None,
) -> Tuple[List[dict], RegistryStats]:
    """Join catalogue rows with ratings and emit labelled-source records."""
    records: List[dict] = []
    stats = RegistryStats(total_sources=len(sources))
    for row in sources:
        url = row.get("URL") or row.get("url") or ""
        host = normalize_host(str(url))
        if not host or host not in ratings:
            continue
        label = map_label(ratings[host], scale, custom)
        if label is None:
            stats.unmapped_rating += 1
            continue
        st = source_type_from_category(row.get("Macro-categoria", ""))
        rec = {
            "source_id": (row.get("Fonte") or host).strip(),
            "source_type": st,
            "label": label,
            "url": str(url).strip(),
            "rss": (row.get("RSS Feed") or "").strip() or None,
        }
        records.append(rec)
        stats.matched += 1
        band = determine_band(label)
        stats.by_band[band] = stats.by_band.get(band, 0) + 1
        stats.by_source_type[st] = stats.by_source_type.get(st, 0) + 1
    return records, stats


def _read_sources_csv(path: Path) -> List[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _write_jsonl(records: List[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m cats.calibration.label_from_ratings",
        description="Join an OSINT source catalogue with external ratings into a distant-supervision label registry.",
    )
    parser.add_argument("--sources", required=True, type=Path, help="OSINT catalogue CSV (Fonti_OSINT shape)")
    parser.add_argument("--ratings", required=True, type=Path, help="external ratings (.csv or .json)")
    parser.add_argument(
        "--scale",
        required=True,
        choices=["mbfc", "admiralty", "numeric", "custom"],
        help="rating scale to map onto 0-100 labels",
    )
    parser.add_argument(
        "--custom-map",
        type=Path,
        default=None,
        help="JSON {rating: label} for --scale custom",
    )
    parser.add_argument("--out", required=True, type=Path, help="output label registry (.jsonl)")
    args = parser.parse_args(argv)

    for p in (args.sources, args.ratings):
        if not p.exists():
            parser.error(f"file not found: {p}")
    custom = None
    if args.scale == "custom":
        if not args.custom_map or not args.custom_map.exists():
            parser.error("--scale custom requires --custom-map pointing to a JSON {rating: label}")
        custom = json.loads(args.custom_map.read_text(encoding="utf-8"))

    sources = _read_sources_csv(args.sources)
    ratings = load_ratings(args.ratings)
    records, stats = build_label_registry(sources, ratings, args.scale, custom)

    if not records:
        print("No sources matched the ratings; nothing written.")
        print(f"  catalogue rows: {stats.total_sources}, ratings: {len(ratings)}")
        return 1

    _write_jsonl(records, args.out)
    print(f"Wrote {stats.matched} labelled source(s) to {args.out}")
    print(f"  matched {stats.matched}/{stats.total_sources} catalogue rows; {stats.unmapped_rating} rating(s) unmapped")
    print("  label band distribution:")
    for band in ("high", "medium_high", "medium", "low", "very_low"):
        if band in stats.by_band:
            print(f"    {band:12s} {stats.by_band[band]}")
    print("  source_type distribution:")
    for st, n in sorted(stats.by_source_type.items()):
        print(f"    {st:12s} {n}")
    print("\nNext: attach message histories from the RSS feeds:")
    print(f"  python -m cats.calibration.collect_rss --labels {args.out} --out labelled_sources.jsonl")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
