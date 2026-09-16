"""Spike: does an English-tuned NLP stack beat the shipped Italian-optimised one
on the future holdout's English-language sources?

CATS's default NLP stack is Italian-optimised (`it_core_news_lg` for NER
coherence, TextBlob + an Italian negation-word correction for volatility's
sentiment). Non-Italian input is flagged (`language.detected`) but still
scored with that Italian-tuned stack. This spike measures how much
concordance/Spearman that costs on the (small) English-language slice of the
existing future holdout, and whether swapping in `en_core_web_lg` + plain
(non-negation-corrected) TextBlob recovers it — **research only, nothing
shipped**: this script imports and reconfigures `cats.signals.coherence`'s
model (loads `en_core_web_lg` into its module-global instead of the Italian
model) and reimplements volatility's algorithm locally with a different
polarity function; it never edits `cats/signals/*`. No weight change either
way — see `docs/english_stack_spike_2026-11.md` for the write-up.

Caveat up front: ``cats.pipeline.language.detect_language`` only
distinguishes "italian" from "other"/"unknown" (see its docstring) — it does
not have an "english" category, so this script uses its own local English
marker-word heuristic (mirroring the Italian one's method) purely to build
the comparison subset. That heuristic is not proposed for
`cats/pipeline/language.py`.

Reads only committed data: signals + labels from `data/holdout_future.jsonl`
(the unseen 06-Jul future snapshot), and the aligned source URLs/messages
from `data/snapshots/labelled_sources_2026-07-06.jsonl` (same order, see
`research/validate_domain_penalty.py`). Requires `en_core_web_lg`
(`python -m spacy download en_core_web_lg`) — not otherwise a CATS
dependency.

Run from the repo root:
    CATS_WEIGHTS_FILE=data/calibrated_weights.json python research/english_stack_spike.py
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import List, Tuple

os.environ.setdefault("CATS_WEIGHTS_FILE", "data/calibrated_weights.json")
# Inert placeholders so cats.core.config imports outside the API deployment.
os.environ.setdefault("CATS_API_KEY", "spike-unused")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost:1/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:1/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTAwMzI=")

from textblob import TextBlob  # noqa: E402

from cats.pipeline.normalizer import normalize_messages  # noqa: E402
from cats.scoring.engine import aggregate_score  # noqa: E402
from cats.scoring.weights import get_dynamic_weights  # noqa: E402
from cats.signals import coherence as coherence_module  # noqa: E402
from cats.signals.coherence import compute_coherence  # noqa: E402
from cats.signals.types import Message, SignalResult  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# ── spike-only English detector (mirrors cats/pipeline/language.py's method:
# ratio of high-frequency function words over Latin-script alphabetic tokens
# -- NOT a proposed change to that module, just enough to build the subset). ──
_ENGLISH_MARKERS = frozenset(
    {
        "the", "and", "of", "to", "in", "is", "that", "for", "on", "with",
        "as", "at", "by", "an", "was", "are", "this", "from", "have", "has",
        "its", "be", "not", "but", "will", "who", "which", "their", "they",
        "we", "you", "been", "were", "more", "also", "about", "after", "new",
        "one", "can", "could", "would", "said", "than", "into", "over",
        "when", "what", "how", "all", "there", "it's", "or", "if",
    }
)  # fmt: skip
_MIN_TOKENS = 8
_ENGLISH_RATIO = 0.12  # same threshold cats/pipeline/language.py uses for Italian
_LATIN_WORD = re.compile(r"[a-z']+")


def is_english(messages: List[Message]) -> Tuple[bool, float]:
    text = " ".join(m.text for m in messages).lower()
    tokens = _LATIN_WORD.findall(text)
    if len(tokens) < _MIN_TOKENS:
        return False, 0.0
    ratio = sum(1 for t in tokens if t in _ENGLISH_MARKERS) / len(tokens)
    return ratio >= _ENGLISH_RATIO, ratio


# ── volatility reimplemented with plain (non-Italian-corrected) TextBlob ────
# Mirrors cats.signals.volatility.compute_volatility exactly (same 0.3
# spike_threshold, same aggregation), but cats.signals.sentiment always
# applies an Italian negation-word correction regardless of input language --
# this swaps it for plain TextBlob polarity, which is what "TextBlob inglese"
# means (TextBlob has no built-in negation handling for any language).
def english_volatility(messages: List[Message], spike_threshold: float = 0.3) -> SignalResult:
    if len(messages) < 3:
        return SignalResult(name="volatility", value=0.0, confidence=0.0)
    sents = [TextBlob(m.text).sentiment.polarity for m in messages]
    deltas = [abs(sents[i] - sents[i - 1]) for i in range(1, len(sents))]
    spikes = sum(1 for d in deltas if d > spike_threshold)
    score = min((spikes / len(deltas)) * 100, 100.0) if deltas else 0.0
    return SignalResult(name="volatility", value=score, confidence=min(len(messages) / 20, 1.0))


# ── rank statistics (same implementation as research/validate_domain_penalty.py) ──
def _rank(v):
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


def spearman(xs, ys) -> float:
    if len(xs) < 2:
        return 0.0
    rx, ry = _rank(xs), _rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def concordance(preds, labels) -> float:
    n = len(preds)
    num = den = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            if labels[i] == labels[j]:
                continue
            den += 1
            hi, lo = (i, j) if labels[i] > labels[j] else (j, i)
            if preds[hi] > preds[lo]:
                num += 1
            elif preds[hi] == preds[lo]:
                num += 0.5
    return num / den if den else 0.0


def behavioural_score(signals: dict, source_type: str) -> float:
    results = [SignalResult(name=k, value=float(v), confidence=1.0) for k, v in signals.items()]
    weights = get_dynamic_weights({"source_type": source_type})
    return aggregate_score(results, weights)


def main() -> None:
    hold = [json.loads(line) for line in open(ROOT / "data/holdout_future.jsonl")]
    snap = [json.loads(line) for line in open(ROOT / "data/snapshots/labelled_sources_2026-07-06.jsonl")]
    assert len(hold) == len(snap), (len(hold), len(snap))

    subset = []
    for h, s in zip(hold, snap):
        messages = normalize_messages(s["messages"])
        english, ratio = is_english(messages)
        if english:
            subset.append((h, s, messages, ratio))

    print(f"Future holdout n={len(hold)}; English-marker subset n={len(subset)}\n")
    if len(subset) < 5:
        print(
            "WARNING: fewer than 5 English sources in the subset -- concordance/Spearman "
            "on this few pairs is not statistically meaningful. Findings below are indicative only."
        )

    if not subset:
        print("No English-language sources found in this holdout; nothing to compare.")
        return

    coherence_module.init_nlp("en_core_web_lg")

    labels = [h["label"] for h, _, _, _ in subset]
    baseline_scores = [behavioural_score(h["signals"], h.get("source_type", "default")) for h, _, _, _ in subset]

    en_scores = []
    coherence_deltas = []
    for h, s, messages, _ in subset:
        new_coherence = compute_coherence(messages)
        new_volatility = english_volatility(messages)
        new_signals = dict(h["signals"])
        new_signals["coherence"] = new_coherence.value
        new_signals["volatility"] = new_volatility.value
        en_scores.append(behavioural_score(new_signals, h.get("source_type", "default")))
        coherence_deltas.append(new_coherence.value - h["signals"]["coherence"])

    print(f"{'':32s}{'concordance':>12s}{'spearman':>10s}")
    print(
        f"{'current stack (it_core_news_lg)':32s}{concordance(baseline_scores, labels):>12.3f}{spearman(baseline_scores, labels):>10.3f}"
    )
    print(
        f"{'english stack (en_core_web_lg)':32s}{concordance(en_scores, labels):>12.3f}{spearman(en_scores, labels):>10.3f}"
    )

    print("\nPer-source coherence delta (english stack - current stack):")
    for (h, s, _, ratio), delta in zip(subset, coherence_deltas):
        print(
            f"  label={h['label']:>5.1f}  marker_ratio={ratio:.3f}  coherence_delta={delta:+6.2f}  {s.get('url', '')}"
        )


if __name__ == "__main__":
    main()
