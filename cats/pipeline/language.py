"""Input-language assessment for the Italian-optimised NLP pipeline (risk R3).

CATS's default NLP stack (spaCy ``it_core_news_lg``, TextBlob with Italian
negation correction) is Italian-optimised: non-Italian input silently degrades
signal quality (documented as WP 4.1 / risk register R3). This module detects
the mismatch so callers can *flag* it — it never changes scores or bands.

Dependency-free heuristic, two stages:

1. **Script check** — if fewer than half the alphabetic characters are Latin,
   the text cannot be Italian (``detected="other"``).
2. **Function-word ratio** — Italian function words (articles, prepositions,
   clitics) are so frequent that genuine Italian prose scores well above 15%
   marker tokens; other Latin-script languages score near zero. The marker set
   deliberately excludes forms shared with English/Spanish/French one-letter
   words and false friends (``come``, ``in``, ``a``, ``e``…) so the ratio
   separates cleanly.

Assessment is ``"unknown"`` (confidence 0) below a minimum evidence floor —
mirroring how signals return neutral zero-confidence values when they cannot
be computed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List

from cats.signals.types import Message

# High-frequency Italian function words, curated to avoid collisions with
# common English/French/Spanish tokens: no "come"/"in"/"a"/"e" (English), and
# no "la"/"le"/"lo"/"si"/"del"/"una" (shared Romance articles/pronouns that
# would let a French or Spanish text accumulate marker hits).
ITALIAN_MARKERS = frozenset(
    {
        "di", "che", "il", "non", "per", "sono", "della", "delle", "dei",
        "degli", "nel", "nella", "nelle", "gli", "ma", "anche", "più",
        "questo", "questa", "questi", "queste", "essere", "stato", "stata",
        "hanno", "erano", "è", "sarà", "però", "già", "così", "dopo",
        "senza", "ancora", "molto", "tutti", "tutto", "tutte", "alla",
        "dalla", "sulla", "sulle", "tra", "fra", "perché", "quando",
        "viene", "vengono", "fino", "contro", "ogni", "quindi", "inoltre",
        "infatti", "aveva", "possono", "può", "deve", "devono", "loro",
        "suo", "sua", "suoi", "sue", "nostro", "nostra", "anni", "governo",
        "città",
    }
)  # fmt: skip

# Below these floors there is no linguistic evidence to assess.
_MIN_TOKENS = 8
_MIN_ALPHA_CHARS = 40

# Decision thresholds on the marker-token ratio, validated on the July 2026
# snapshot registry (~215 source evaluations): Italian outlets score
# 0.145-0.32; English, French and Spanish ones <= 0.013 (the marker set
# excludes shared Romance tokens). These thresholds cut the gap with a >4x
# margin on both sides.
_ITALIAN_RATIO = 0.12
_OTHER_RATIO = 0.06

_LATIN_WORD = re.compile(r"[a-zàèéìíòóùú]+")


@dataclass
class LanguageAssessment:
    detected: str  # "italian" | "other" | "unknown"
    confidence: float  # 0..1, evidence-based
    marker_ratio: float
    latin_script_ratio: float
    metadata: Dict = field(default_factory=dict)

    def as_dict(self) -> Dict:
        return {
            "detected": self.detected,
            "confidence": round(self.confidence, 2),
            "marker_ratio": round(self.marker_ratio, 3),
            "latin_script_ratio": round(self.latin_script_ratio, 3),
            **({"reason": self.metadata["reason"]} if "reason" in self.metadata else {}),
        }


def detect_language(messages: List[Message]) -> LanguageAssessment:
    """Assess whether a message corpus is Italian (flag-only: never scores)."""
    text = " ".join(m.text for m in messages).lower()
    alpha = [c for c in text if c.isalpha()]
    if len(alpha) < _MIN_ALPHA_CHARS:
        return LanguageAssessment("unknown", 0.0, 0.0, 0.0, {"reason": "insufficient_text"})

    latin = sum(1 for c in alpha if "a" <= c <= "z" or c in "àèéìíòóùú")
    latin_ratio = latin / len(alpha)
    if latin_ratio < 0.5:
        return LanguageAssessment(
            "other",
            min(len(alpha) / 200.0, 1.0),
            0.0,
            latin_ratio,
            {"reason": "non_latin_script"},
        )

    tokens = _LATIN_WORD.findall(text)
    if len(tokens) < _MIN_TOKENS:
        return LanguageAssessment("unknown", 0.0, 0.0, latin_ratio, {"reason": "insufficient_text"})

    ratio = sum(1 for t in tokens if t in ITALIAN_MARKERS) / len(tokens)
    evidence = min(len(tokens) / 80.0, 1.0)
    if ratio >= _ITALIAN_RATIO:
        return LanguageAssessment("italian", evidence, ratio, latin_ratio)
    if ratio < _OTHER_RATIO:
        return LanguageAssessment("other", evidence, ratio, latin_ratio)
    # Boundary zone: some Italian markers but below fluent-prose frequency
    # (mixed-language feeds, heavy named-entity text). Report the uncertainty.
    return LanguageAssessment("unknown", evidence * 0.5, ratio, latin_ratio, {"reason": "ambiguous_ratio"})
