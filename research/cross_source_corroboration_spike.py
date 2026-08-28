"""Research spike (roadmap item 11): does cross-source corroboration carry
rank information the existing signals miss?

Motivation, from the 28-Jul findings
(docs/calibration_findings_2026-07-28.md): "candidate directions: domain/
impersonation features..., cross-source corroboration, and longer per-source
spans than a monthly RSS window affords." The hypothesis: legitimate outlets
mostly cover the same major stories as other legitimate outlets (a story
breaks, many newsrooms report it within hours); a source fabricating its own
narrative has nothing else to corroborate it. This spike checks whether that
holds on the committed calibration data before any commitment to a shared
cross-source registry (a real data-design change, per the roadmap item).

Leakage discipline: corroboration is measured from GENERAL lexical overlap
between messages across different sources within a time window -- never from
membership in `data/disinfo_sources.csv`, and the design choices below
(distinctive-word length floor, similarity threshold, time window) were fixed
before this script was run against any label.

Protocol mirrors this week's other spikes: train = merged 02/03/05-Jul
snapshots (n=56), holdout = the untouched 06-Jul snapshot (n=53).

Method (stdlib only, no NLP model assets):
  1. Per message, extract a "distinctive word set" -- lowercased alphabetic
     tokens of length >= 5, minus a stopword list (a cheap proxy for content
     words vs function words; deliberately simple to keep this a spike, not
     a claim-matching NLP system).
  2. Build an inverted index (word -> postings) over ALL messages in the
     split, tagged by source_id and timestamp.
  3. For each message, look up candidate matches via its own distinctive
     words, keep only postings from a DIFFERENT source_id within +/- 48h,
     and count it "corroborated" if Jaccard(distinctive words) >= 0.3 with
     at least one candidate.
  4. Per source: corroboration_rate = share of its messages with >= 1
     corroborating match elsewhere. Correlate against label.

Run from the repo root:  python research/cross_source_corroboration_spike.py
Reads only committed data (data/snapshots/labelled_sources_2026-07-0{2,3,5,6}.jsonl).
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Sequence, Set, Tuple

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / "data" / "snapshots"
TRAIN_SNAPSHOTS = ["labelled_sources_2026-07-02", "labelled_sources_2026-07-03", "labelled_sources_2026-07-05"]
HOLDOUT_SNAPSHOT = "labelled_sources_2026-07-06"

TIME_WINDOW_HOURS = 48.0
JACCARD_THRESHOLD = 0.3
MIN_WORD_LEN = 5

_STOPWORDS = {
    "about",
    "after",
    "again",
    "their",
    "there",
    "these",
    "those",
    "which",
    "would",
    "could",
    "should",
    "while",
    "where",
    "being",
    "other",
    "первый",
    "sopra",
    "sotto",
    "quello",
    "questa",
    "questo",
    "anche",
    "molto",
    "sempre",
    "ancora",
    "avere",
    "essere",
    "fatto",
    "prima",
    "dopo",
    "hanno",
    "sarebbe",
    "https",
    "www",
    "com",
}
_WORD_RE = re.compile(r"[a-zà-öø-ÿ]+", re.IGNORECASE)


def _distinctive_words(text: str) -> Set[str]:
    return {w for w in (t.lower() for t in _WORD_RE.findall(text)) if len(w) >= MIN_WORD_LEN and w not in _STOPWORDS}


def _parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_sources(paths: Sequence[Path]) -> List[dict]:
    """Merged labelled sources (union message histories across snapshots)."""
    seen: Dict[str, dict] = {}
    for p in paths:
        with p.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                r = json.loads(line)
                sid = r.get("source_id") or r.get("url") or ""
                if sid not in seen:
                    seen[sid] = r
                else:
                    existing_ts = {m["timestamp"] for m in seen[sid].get("messages", [])}
                    for m in r.get("messages", []):
                        if m["timestamp"] not in existing_ts:
                            seen[sid]["messages"].append(m)
    return [r for r in seen.values() if r.get("messages") and "label" in r]


class _Entry:
    __slots__ = ("source_id", "ts", "words")

    def __init__(self, source_id: str, ts: datetime, words: Set[str]):
        self.source_id = source_id
        self.ts = ts
        self.words = words


def corroboration_rates(sources: List[dict]) -> Dict[str, float]:
    """source_id -> share of its messages corroborated by a different source."""
    entries: List[_Entry] = []
    index: Dict[str, List[int]] = defaultdict(list)
    for s in sources:
        sid = s["source_id"]
        for m in s["messages"]:
            try:
                ts = _parse_ts(m["timestamp"])
            except ValueError:
                continue
            words = _distinctive_words(m.get("text", ""))
            if len(words) < 3:
                continue
            entries.append(_Entry(sid, ts, words))
            idx = len(entries) - 1
            for w in words:
                index[w].append(idx)

    window = TIME_WINDOW_HOURS * 3600
    corroborated_count: Dict[str, int] = defaultdict(int)
    total_count: Dict[str, int] = defaultdict(int)

    for i, e in enumerate(entries):
        total_count[e.source_id] += 1
        candidates: Set[int] = set()
        for w in e.words:
            candidates.update(index[w])
        candidates.discard(i)
        matched = False
        for j in candidates:
            other = entries[j]
            if other.source_id == e.source_id:
                continue
            if abs((other.ts - e.ts).total_seconds()) > window:
                continue
            union = e.words | other.words
            jac = len(e.words & other.words) / len(union) if union else 0.0
            if jac >= JACCARD_THRESHOLD:
                matched = True
                break
        if matched:
            corroborated_count[e.source_id] += 1

    return {sid: corroborated_count[sid] / total_count[sid] for sid in total_count if total_count[sid] > 0}


def _rank(v: Sequence[float]) -> List[float]:
    o = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
            j += 1
        for k in range(i, j + 1):
            r[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(xs: Sequence[float], ys: Sequence[float]) -> float:
    rx, ry = _rank(xs), _rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def _report(name: str, sources: List[dict]) -> Tuple[List[float], List[float]]:
    rates = corroboration_rates(sources)
    labels_by_id = {s["source_id"]: s["label"] for s in sources}
    vals, labels = [], []
    for sid, rate in rates.items():
        vals.append(rate)
        labels.append(labels_by_id[sid])
    rho = spearman(vals, labels)
    zero = sum(1 for v in vals if v == 0.0)
    print(f"{name:<10} n={len(vals):3d}  rho={rho:+.3f}  mean={sum(vals)/len(vals):.3f}  all-zero={zero}/{len(vals)}")
    return vals, labels


def main() -> None:
    train = load_sources([SNAP / f"{n}.jsonl" for n in TRAIN_SNAPSHOTS])
    holdout = load_sources([SNAP / f"{HOLDOUT_SNAPSHOT}.jsonl"])
    print(f"train (merged 02/03/05-Jul): n={len(train)}   holdout (06-Jul, unseen): n={len(holdout)}")
    print(f"params: window=+/-{TIME_WINDOW_HOURS:.0f}h  jaccard>={JACCARD_THRESHOLD}  min_word_len={MIN_WORD_LEN}\n")

    tr_vals, tr_labels = _report("train", train)
    ho_vals, ho_labels = _report("holdout", holdout)

    print("\nmean corroboration_rate at label extremes (holdout):")
    pairs = list(zip(ho_vals, ho_labels))
    low = [v for v, lb in pairs if lb <= 30]
    high = [v for v, lb in pairs if lb >= 70]
    mlow = sum(low) / len(low) if low else float("nan")
    mhigh = sum(high) / len(high) if high else float("nan")
    print(f"  label<=30: {mlow:.3f}  (n={len(low)})   label>=70: {mhigh:.3f}  (n={len(high)})")

    # Cross-check on a pool that spans BOTH splits (larger n, more corroboration
    # opportunities per source since the pool of "other sources" to match
    # against is bigger).
    both_sources = {s["source_id"]: s for s in train}
    for s in holdout:
        if s["source_id"] in both_sources:
            existing_ts = {m["timestamp"] for m in both_sources[s["source_id"]]["messages"]}
            for m in s["messages"]:
                if m["timestamp"] not in existing_ts:
                    both_sources[s["source_id"]]["messages"].append(m)
        else:
            both_sources[s["source_id"]] = s
    print("\npooled (train U holdout, larger corroboration pool):")
    _report("pooled", list(both_sources.values()))


if __name__ == "__main__":
    main()
