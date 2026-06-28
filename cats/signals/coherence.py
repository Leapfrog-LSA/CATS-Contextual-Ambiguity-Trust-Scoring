import unicodedata
from typing import List, Set

import structlog

from cats.core.config import settings
from cats.signals.types import CoherenceResult, Message

logger = structlog.get_logger()
nlp = None  # N-01: spaCy singleton loaded in lifespan

_sbert_model = None
_sbert_failed = False


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


def _ner_coherence(messages: List[Message]) -> CoherenceResult:
    """Default backend: spaCy NER entity overlap (Jaccard) across messages."""
    if nlp is None:
        # NLP model not loaded (e.g. failed/skipped init): degrade gracefully
        # with a neutral, zero-confidence signal instead of crashing per request.
        # /health already reports nlp as "not_loaded" for this state.
        logger.warning("coherence_nlp_unavailable")
        return CoherenceResult(
            name="coherence",
            value=50.0,
            confidence=0.0,
            metadata={"reason": "nlp_unavailable"},
        )
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
        metadata={"pairs": len(overlaps), "backend": "ner"},
        entity_overlap=avg,
        jaccard_similarity=avg,
    )


def _get_sbert_model():
    """Lazily load the sentence-transformers model once; cache the result.

    On any failure (sentence-transformers/torch missing, model load error) mark
    the backend as failed so callers fall back to the NER backend.
    """
    global _sbert_model, _sbert_failed
    if _sbert_model is not None or _sbert_failed:
        return _sbert_model
    try:
        from sentence_transformers import SentenceTransformer

        _sbert_model = SentenceTransformer(settings.coherence_model)
        logger.info("sbert_loaded", model=settings.coherence_model)
    except Exception as exc:
        _sbert_failed = True
        logger.warning("sbert_unavailable", error=str(exc), fallback="ner")
    return _sbert_model


def _sbert_coherence(messages: List[Message]) -> CoherenceResult:
    """Optional backend: mean cosine similarity of consecutive message embeddings."""
    model = _get_sbert_model()
    if model is None:
        return _ner_coherence(messages)
    if len(messages) < 2:
        return CoherenceResult(
            name="coherence",
            value=100.0,
            confidence=0.0,
            metadata={"reason": "insufficient_messages"},
        )
    try:
        from sentence_transformers import util

        embs = model.encode([m.text for m in messages], convert_to_tensor=True)
        sims = [float(util.cos_sim(embs[i], embs[i + 1])) for i in range(len(messages) - 1)]
    except Exception as exc:
        logger.warning("sbert_inference_failed", error=str(exc), fallback="ner")
        return _ner_coherence(messages)
    avg = sum(sims) / len(sims) if sims else 0.0
    value = max(0.0, min(avg, 1.0)) * 100  # cosine in [-1, 1] -> clamp to [0, 100]
    return CoherenceResult(
        name="coherence",
        value=value,
        confidence=min(len(messages) / 10, 1.0),
        metadata={"pairs": len(sims), "backend": "sbert"},
        entity_overlap=avg,
        jaccard_similarity=avg,
    )


def compute_coherence(messages: List[Message]) -> CoherenceResult:
    if settings.coherence_backend == "sbert":
        return _sbert_coherence(messages)
    return _ner_coherence(messages)
