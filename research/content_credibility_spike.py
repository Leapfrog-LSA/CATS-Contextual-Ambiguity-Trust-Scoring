"""Research spike (roadmap item 10): does a content-credibility signal carry
rank information the four behavioural signals + domain-provenance miss?

Motivation: the domain-provenance spike (research/domain_provenance_spike.py,
docs/signal_research_2026-07.md) closed the "regular-cadence clone on a
suspicious domain" gap but is explicitly high-precision/low-recall — it
misses fake-news content on *ordinary* domains (worldnewsdailyreport.com,
naturalnews.com), which the domain-provenance findings named as the next
open work item. This spike tests three candidate content-level heuristics
named in docs/piano_sviluppo_roadmap_2026-07.md item 10: claim density,
sensationalism, citation/attribution patterns.

Leakage discipline: every lexicon below is a general-purpose EN/IT
tabloid-language and hedging-language list, written from general knowledge
before looking at any correlation number in this script -- never derived
from `data/disinfo_sources.csv` or by fitting words to this corpus. If a
word list needs tuning to "work", that is p-hacking, not a signal; this
script reports one run's numbers honestly rather than iterating word lists
against the holdout.

Protocol mirrors the gaming/volatility/silence retunes this week: train =
merged 02/03/05-Jul snapshots (n=56), holdout = the untouched 06-Jul
snapshot (n=53, never used to write the lexicons below).

Run from the repo root:  python research/content_credibility_spike.py
Reads only committed data (data/snapshots/labelled_sources_2026-07-0{2,3,5,6}.jsonl).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Sequence

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / "data" / "snapshots"
TRAIN_SNAPSHOTS = ["labelled_sources_2026-07-02", "labelled_sources_2026-07-03", "labelled_sources_2026-07-05"]
HOLDOUT_SNAPSHOT = "labelled_sources_2026-07-06"

# General-purpose EN/IT tabloid/clickbait vocabulary -- not fitted to this
# corpus (see module docstring).
SENSATIONAL_WORDS = {
    "shock",
    "shocking",
    "incredible",
    "unbelievable",
    "bombshell",
    "scandal",
    "scandalous",
    "terrifying",
    "outrageous",
    "stunning",
    "explosive",
    "exclusive",
    "chilling",
    "horrifying",
    "devastating",
    "insane",
    "jaw-dropping",
    "mind-blowing",
    "incredibile",
    "sconvolgente",
    "clamoroso",
    "scandalo",
    "esclusivo",
    "terrificante",
    "scioccante",
    "shockante",
    "choc",
    "bomba",
    "allarme",
    "disastro",
    "drammatico",
    "sconcertante",
    "raccapricciante",
}

# Absolute/unhedged certainty markers vs. hedging/attributive markers.
ABSOLUTE_WORDS = {
    "always",
    "never",
    "everyone",
    "everybody",
    "nobody",
    "no one",
    "definitely",
    "certainly",
    "absolutely",
    "undeniably",
    "impossible",
    "guaranteed",
    "proves",
    "proof",
    "undoubtedly",
    "sempre",
    "mai",
    "tutti",
    "nessuno",
    "certamente",
    "sicuramente",
    "assolutamente",
    "innegabile",
    "impossibile",
    "garantito",
    "dimostra",
    "indubbiamente",
}
HEDGE_WORDS = {
    "allegedly",
    "reportedly",
    "may",
    "might",
    "seems",
    "appears",
    "possibly",
    "reported",
    "according",
    "suggests",
    "believed",
    "presumably",
    "secondo",
    "presumibilmente",
    "potrebbe",
    "sembra",
    "sembrerebbe",
    "forse",
    "riportano",
    "riferisce",
    "avrebbe",
    "sarebbe",
}

# Attribution/citation markers (reporting verbs + phrases).
CITATION_MARKERS = {
    "said",
    "says",
    "stated",
    "told",
    "reported",
    "according to",
    "explained",
    "confirmed",
    "announced",
    "ha detto",
    "ha dichiarato",
    "ha affermato",
    "ha spiegato",
    "ha confermato",
    "ha annunciato",
    "riferisce",
    "secondo fonti",
    "fonti dicono",
}

_WORD_RE = re.compile(r"[a-zà-öø-ÿ']+", re.IGNORECASE)


def _tokens(text: str) -> List[str]:
    return [t.lower() for t in _WORD_RE.findall(text)]


def load_sources(paths: Sequence[Path]) -> List[dict]:
    """Merged labelled sources (dedup on (source_id, first message ts))."""
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
                    # Union message histories across snapshots, same as merge_snapshots.
                    existing_ts = {m["timestamp"] for m in seen[sid].get("messages", [])}
                    for m in r.get("messages", []):
                        if m["timestamp"] not in existing_ts:
                            seen[sid]["messages"].append(m)
    return [r for r in seen.values() if r.get("messages") and "label" in r]


def sensationalism_score(texts: List[str]) -> float:
    """0-100: exclamation density + ALL-CAPS word density + clickbait lexicon hits."""
    if not texts:
        return 0.0
    tokens = [t for txt in texts for t in _tokens(txt)]
    if not tokens:
        return 0.0
    n = len(tokens)
    excl = sum(txt.count("!") for txt in texts) / len(texts)
    raw_words = [w for txt in texts for w in txt.split()]
    caps = sum(1 for w in raw_words if len(w) >= 4 and w.isupper()) / max(len(raw_words), 1)
    lex = sum(1 for t in tokens if t in SENSATIONAL_WORDS) / n
    return min((excl * 15 + caps * 300 + lex * 300), 100.0)


def claim_density_score(texts: List[str]) -> float:
    """0-100: absolute/unhedged-certainty word share relative to hedged language."""
    tokens = [t for txt in texts for t in _tokens(txt)]
    if not tokens:
        return 0.0
    absolute = sum(1 for t in tokens if t in ABSOLUTE_WORDS)
    hedge = sum(1 for t in tokens if t in HEDGE_WORDS)
    return 100.0 * absolute / (absolute + hedge + 1)


def citation_score(texts: List[str]) -> float:
    """0-100: attribution/citation marker density (quotes + reporting verbs)."""
    if not texts:
        return 0.0
    tokens = [t for txt in texts for t in _tokens(txt)]
    n = max(len(tokens), 1)
    quotes = sum(txt.count('"') + txt.count("«") + txt.count("»") for txt in texts) / len(texts)
    joined = " ".join(txt.lower() for txt in texts)
    verbs = sum(joined.count(m) for m in CITATION_MARKERS)
    return min((quotes * 20 + (verbs / n) * 2000), 100.0)


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


def main() -> None:
    train = load_sources([SNAP / f"{n}.jsonl" for n in TRAIN_SNAPSHOTS])
    holdout = load_sources([SNAP / f"{HOLDOUT_SNAPSHOT}.jsonl"])
    print(f"train (merged 02/03/05-Jul): n={len(train)}   holdout (06-Jul, unseen): n={len(holdout)}\n")

    print(f"{'sub-score':<16} {'train rho':>10} {'holdout rho':>12}")
    for name, fn in (
        ("sensationalism", sensationalism_score),
        ("claim_density", claim_density_score),
        ("citation", citation_score),
    ):
        tr_vals = [fn([m["text"] for m in s["messages"]]) for s in train]
        tr_labels = [s["label"] for s in train]
        ho_vals = [fn([m["text"] for m in s["messages"]]) for s in holdout]
        ho_labels = [s["label"] for s in holdout]
        print(f"{name:<16} {spearman(tr_vals, tr_labels):>+10.3f} {spearman(ho_vals, ho_labels):>+12.3f}")

    print("\nmean values at label extremes (holdout):")
    for name, fn in (
        ("sensationalism", sensationalism_score),
        ("claim_density", claim_density_score),
        ("citation", citation_score),
    ):
        vals = [(fn([m["text"] for m in s["messages"]]), s["label"]) for s in holdout]
        low = [v for v, lb in vals if lb <= 30]
        high = [v for v, lb in vals if lb >= 70]
        mlow = sum(low) / len(low) if low else float("nan")
        mhigh = sum(high) / len(high) if high else float("nan")
        print(f"  {name:<16} label<=30: {mlow:6.1f}  (n={len(low):2d})   label>=70: {mhigh:6.1f}  (n={len(high):2d})")


if __name__ == "__main__":
    main()
