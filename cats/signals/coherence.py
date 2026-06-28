import unicodedata
from typing import List, Set

import structlog

from cats.signals.types import CoherenceResult, Message

logger = structlog.get_logger()
nlp = None  # N-01: singleton loaded in lifespan


def init_nlp(model_name: str = "it_core_news_lg") -> None:
    global nlp
    import spacy

    nlp = spacy.load(model_name)
    logger.info("spacy_loaded", model=model_name)


def _normalize(text: str) -> str:
    return unicodedata.normalize("NFC", text).lower()


def _entities(text: str) -> Set[str]:
    doc = nlp(_normalize(text))
    return {e.text for e in doc.ents if e.label_ in {"PER", "ORG", "GPE", "LOC"}}


def _jaccard(a: Set[str], b: Set[str]) -> float:
    # N-04: empty-set guard -> 0.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def compute_coherence(messages: List[Message]) -> CoherenceResult:
    if len(messages) < 2:
        return CoherenceResult(
            name="coherence",
            value=100.0,
            confidence=0.0,
            metadata={"reason": "insufficient_messages"},
        )
    ents = [_entities(m.text) for m in messages]
    overlaps = [_jaccard(ents[i], ents[i + 1]) for i in range(len(ents) - 1)]
    avg = sum(overlaps) / len(overlaps) if overlaps else 0.0
    return CoherenceResult(
        name="coherence",
        value=avg * 100,
        confidence=min(len(messages) / 10, 1.0),
        metadata={"pairs": len(overlaps)},
        entity_overlap=avg,
        jaccard_similarity=avg,
    )
