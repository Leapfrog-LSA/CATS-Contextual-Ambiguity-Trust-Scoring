"""Dataset gap analysis: quantify the language x label-band imbalance that
blocks the content-credibility signal (and inflates any content feature).

The content-credibility spike (docs/content_credibility_findings_2026-07.md)
found its apparent power was a language confound: the labelled registry's low
tail is Italian and its high tail mostly English, so a feature separating the
two languages scores a spurious correlation with the label. That was measured
on the 53-source holdout. This script measures it across ALL sources that have
collected message text (every snapshot merged) and turns "we need more data"
into a concrete, per-cell collection target.

It fabricates nothing: it reads committed snapshots, detects language from the
message text with cats.pipeline.language, and reports the cross-tab plus the
minimum additions that would make language roughly independent of the label.

Run from the repo root:  python research/dataset_language_balance.py
Reads only committed data (data/snapshots/labelled_sources_*.jsonl).
"""

from __future__ import annotations

import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

# Inert placeholders so cats.core.config imports outside the API deployment.
os.environ.setdefault("CATS_API_KEY", "spike-unused")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost:1/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:1/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTAwMzI=")

from cats.calibration.merge_snapshots import _read_jsonl, merge_records  # noqa: E402
from cats.pipeline.language import detect_language  # noqa: E402
from cats.signals.types import Message  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
# Band cutoffs mirror determine_band (engine.py): very_low/low/medium/…
BANDS: List[Tuple[str, float, float]] = [
    ("low (<=30)", 0.0, 30.0),
    ("mid (31-69)", 31.0, 69.0),
    ("high (>=70)", 70.0, 100.0),
]
LANGS = ("italian", "other", "unknown")


def _band(label: float) -> str:
    for name, lo, hi in BANDS:
        if lo <= label <= hi:
            return name
    return BANDS[-1][0]


def _source_language(messages: Sequence[dict]) -> str:
    msgs = [Message(timestamp="2026-01-01T00:00:00+00:00", text=m["text"]) for m in messages if m.get("text")]
    return detect_language(msgs).detected


def _rank(v: Sequence[float]) -> List[float]:
    order = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def _spearman(xs: Sequence[float], ys: Sequence[float]) -> float:
    rx, ry = _rank(xs), _rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def main() -> None:
    snaps = sorted(ROOT.glob("data/snapshots/labelled_sources_*.jsonl"))
    records, _, _ = merge_records([_read_jsonl(p) for p in snaps])
    sources = [r for r in records if r.get("messages") and "label" in r]
    print(f"Merged {len(snaps)} snapshots -> {len(sources)} sources with text + label.\n")

    grid: Dict[Tuple[str, str], int] = defaultdict(int)
    is_italian: List[float] = []
    labels: List[float] = []
    for r in sources:
        lang = _source_language(r["messages"])
        grid[(lang, _band(float(r["label"])))] += 1
        is_italian.append(1.0 if lang == "italian" else 0.0)
        labels.append(float(r["label"]))

    print("1) Language x label-band cross-tab (source counts):")
    header = "   " + f"{'':<12}" + "".join(f"{b.split()[0]:>12}" for b, _, _ in BANDS) + f"{'total':>10}"
    print(header)
    for lang in LANGS:
        row = [grid[(lang, b)] for b, _, _ in BANDS]
        if sum(row) == 0:
            continue
        print("   " + f"{lang:<12}" + "".join(f"{c:>12}" for c in row) + f"{sum(row):>10}")
    print(
        "   "
        + f"{'total':<12}"
        + "".join(f"{sum(grid[(la, b)] for la in LANGS):>12}" for b, _, _ in BANDS)
        + f"{len(sources):>10}"
    )

    print(f"\n2) Confound magnitude: rho(is_italian, label) = {_spearman(is_italian, labels):+.3f}")
    print("   (strongly negative => 'Italian' alone predicts a low label — the confound)")

    # Concrete target: for each band, how many Italian sources are missing to
    # reach parity with the non-Italian count in that band (a simple, honest
    # balance target — enough Italian sources in every band that language no
    # longer separates the tails).
    print("\n3) Collection target to break the confound (add Italian sources per band):")
    total_needed = 0
    for b, _, _ in BANDS:
        it = grid[("italian", b)]
        non_it = sum(grid[(la, b)] for la in LANGS if la != "italian")
        need = max(0, non_it - it)
        total_needed += need
        print(f"   {b:<14} italian={it:<3} non-italian={non_it:<3} -> add ~{need} Italian source(s)")
    print(f"   ---> ~{total_needed} Italian sources to add (priority: the high band, where they are scarcest)")
    print(
        "\nNote: a language-balanced set is the prerequisite for validating the\n"
        "content-credibility signal and for the ≥100-source future holdout target.\n"
        "This needs a network session (RSS/MBFC access); the target above is what\n"
        "to collect. Feeds are NOT invented here."
    )


if __name__ == "__main__":
    main()
