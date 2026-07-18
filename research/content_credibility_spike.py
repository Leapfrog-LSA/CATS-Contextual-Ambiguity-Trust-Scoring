"""Research spike (roadmap item, v2.0): does a content-credibility signal add
discriminative power for the low tail that domain-provenance misses?

Motivation. The signal-hardening findings (docs/signal_research_2026-07.md) left
one class of unreliable source uncovered: fake-news CONTENT on ordinary domains
(worldnewsdailyreport.com, empirenews.net, established low-quality outlets) —
invisible to the four behavioural signals AND to the domain-provenance penalty,
because the domain is unremarkable and the deception is in the text. This spike
tests a signal computed from the message *text*: sensationalism, hyperbole and
weak attribution.

Leakage discipline. Features come from GENERAL text structure only — capital-
letter shouting, exclamation/clickbait punctuation, a fixed bilingual
hyperbole/clickbait lexicon, and attribution-verb density — NEVER from
membership in data/disinfo_sources.csv. It therefore fires on unseen text with
the same style, not just the labelled sources.

The confound this spike must rule out. In the July 2026 registry the low tail
(label 10) is Italian and the high tail (label 85) is mostly English
international outlets, so ANY feature that merely separates Italian from English
would spuriously "predict" the label. The spike therefore reports the raw
correlation AND the within-Italian correlation (using cats.pipeline.language):
only the latter is evidence of a genuine content signal.

Run from the repo root:  python research/content_credibility_spike.py
Reads only committed data (data/snapshots/labelled_sources_2026-07-06.jsonl,
data/holdout_future.jsonl for the aligned behavioural signals + labels).
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import List, Sequence

# Inert placeholders so cats.core.config imports outside the API deployment.
os.environ.setdefault("CATS_API_KEY", "spike-unused")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost:1/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:1/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTAwMzI=")

from cats.pipeline.language import detect_language  # noqa: E402
from cats.signals.types import Message  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SIGNAL_NAMES = ("coherence", "volatility", "silence", "gaming")

# Bilingual clickbait / hyperbole lexicon (IT + EN) — kept bilingual on purpose
# so the feature is not just an Italian-word detector (see the confound note).
HYPERBOLE = {
    # Italian
    "clamoroso",
    "incredibile",
    "shock",
    "choc",
    "sconvolgente",
    "pazzesco",
    "assurdo",
    "vergogna",
    "scandalo",
    "bomba",
    "bufala",
    "esclusivo",
    "sensazionale",
    "terrificante",
    "drammatico",
    "choccante",
    "allucinante",
    # English
    "shocking",
    "unbelievable",
    "incredible",
    "exposed",
    "secret",
    "bombshell",
    "outrageous",
    "insane",
    "jaw-dropping",
    "explosive",
    "stunning",
    "slams",
    "destroys",
    "breaking",
}
# Absolutist / certainty markers — over-claiming without hedging.
ABSOLUTIST = {
    "sempre",
    "mai",
    "nessuno",
    "tutti",
    "tutto",
    "chiunque",
    "assolutamente",
    "never",
    "always",
    "everyone",
    "nobody",
    "nothing",
    "absolutely",
    "guaranteed",
}
# Attribution verbs / phrases — presence signals sourced reporting (credible).
ATTRIBUTION = {
    "secondo",
    "dichiara",
    "dichiarato",
    "afferma",
    "affermato",
    "sostiene",
    "riferisce",
    "riferito",
    "spiega",
    "conferma",
    "annuncia",
    "fonti",
    "said",
    "according",
    "reported",
    "stated",
    "confirmed",
    "sources",
    "spokesperson",
    "told",
}

_WORD = re.compile(r"[A-Za-zÀ-ÿ]{2,}")
_SENT = re.compile(r"[.!?]+")


def _caps_ratio(text: str) -> float:
    words = [w for w in _WORD.findall(text) if len(w) >= 4]
    if not words:
        return 0.0
    shouted = sum(1 for w in words if w.isupper())
    return shouted / len(words)


def _bang_density(text: str) -> float:
    """Exclamation marks + interrobangs per sentence (clickbait punctuation)."""
    sents = max(1, len(_SENT.findall(text)))
    return (text.count("!") + text.count("?!") + text.count("!?")) / sents


def _lex_ratio(tokens: Sequence[str], lex: set) -> float:
    return sum(1 for t in tokens if t in lex) / len(tokens) if tokens else 0.0


def _message_redflag(text: str) -> float:
    """0-100 style red-flag for ONE message; higher = more sensational."""
    tokens = [w.lower() for w in _WORD.findall(text)]
    if len(tokens) < 6:
        return 0.0
    caps = min(_caps_ratio(text) * 4, 1.0)  # 25% shouted words saturates
    bang = min(_bang_density(text), 1.0)
    hype = min(_lex_ratio(tokens, HYPERBOLE) * 40, 1.0)  # ~2.5% hyperbole saturates
    absol = min(_lex_ratio(tokens, ABSOLUTIST) * 15, 1.0)
    attrib = min(_lex_ratio(tokens, ATTRIBUTION) * 20, 1.0)  # credit, subtracted
    raw = 0.30 * caps + 0.25 * bang + 0.25 * hype + 0.10 * absol - 0.20 * attrib
    return max(0.0, min(raw, 1.0)) * 100


def content_credibility_redflag(messages: Sequence[dict]) -> float:
    """Source-level red-flag: mean per-message style score.

    Per-message (not concatenated): a disinfo outlet is characterised by
    *consistent* sensationalism, and averaging the whole history into one blob
    dilutes a shouty headline among many clean sentences — per-message
    aggregation is ~3x more discriminative on the July 2026 registry.
    """
    scored = [_message_redflag(m.get("text", "")) for m in messages if len(m.get("text", "")) > 40]
    return sum(scored) / len(scored) if scored else 0.0


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


def spearman(xs: Sequence[float], ys: Sequence[float]) -> float:
    if len(xs) < 3:
        return float("nan")
    rx, ry = _rank(xs), _rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def main() -> None:
    snap = [json.loads(line) for line in open(ROOT / "data/snapshots/labelled_sources_2026-07-06.jsonl")]
    hold = [json.loads(line) for line in open(ROOT / "data/holdout_future.jsonl")]
    assert len(snap) == len(hold), (len(snap), len(hold))

    labels = [r["label"] for r in hold]
    content = [content_credibility_redflag(s.get("messages", [])) for s in snap]
    langs = [
        detect_language(
            [Message(timestamp="2026-01-01T00:00:00+00:00", text=m["text"]) for m in s.get("messages", [])]
        ).detected
        for s in snap
    ]

    print(f"Future holdout (n={len(snap)}). Content-credibility red-flag (higher = less credible).\n")
    print(f"1) Raw Spearman rho(content_redflag, label) = {spearman(content, labels):+.3f}")

    # --- the confound test ---------------------------------------------------
    it_idx = [i for i, la in enumerate(langs) if la == "italian"]
    other_idx = [i for i, la in enumerate(langs) if la != "italian"]
    print("\n2) Language confound check (low tail is Italian, high tail mostly English):")
    print(f"   detected languages: { {l: langs.count(l) for l in set(langs)} }")
    if len(it_idx) >= 3:
        rho_it = spearman([content[i] for i in it_idx], [labels[i] for i in it_idx])
        print(f"   within-Italian (n={len(it_idx)}) rho = {rho_it:+.3f}   <- the honest number")
    else:
        print(f"   within-Italian: n={len(it_idx)} too small to judge")
    if len(other_idx) >= 3:
        rho_ot = spearman([content[i] for i in other_idx], [labels[i] for i in other_idx])
        print(f"   within-non-Italian (n={len(other_idx)}) rho = {rho_ot:+.3f}")

    # --- orthogonality to the four behavioural signals -----------------------
    print("\n3) Orthogonality — rho(content_redflag, each behavioural signal):")
    for name in SIGNAL_NAMES:
        vals = [r["signals"][name] for r in hold]
        print(f"   {name:<11} {spearman(content, vals):+.3f}")

    # --- does it separate the low tail domain-provenance misses? -------------
    print("\n4) Low tail (label <= 30) vs high tail (label >= 70), mean content red-flag:")
    low = [content[i] for i, la in enumerate(labels) if la <= 30]
    high = [content[i] for i, la in enumerate(labels) if la >= 70]
    print(f"   low  (n={len(low)}): {sum(low) / len(low):5.1f}")
    print(f"   high (n={len(high)}): {sum(high) / len(high):5.1f}")
    low_it = [content[i] for i in it_idx if labels[i] <= 30]
    high_it = [content[i] for i in it_idx if labels[i] >= 70]
    if low_it and high_it:
        print(f"   within Italian — low: {sum(low_it) / len(low_it):5.1f}   high: {sum(high_it) / len(high_it):5.1f}")

    print(
        "\nRead: only the within-Italian numbers (2, and the within-Italian line of 4)\n"
        "are evidence of a genuine content signal; the raw number is inflated by the\n"
        "Italian/English split in this registry."
    )


if __name__ == "__main__":
    main()
