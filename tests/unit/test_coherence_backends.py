"""Coherence backends with fake NLP models: the NER Jaccard path and the SBERT path.

The real models (``it_core_news_lg``, the sentence-transformers checkpoint)
are not needed: a fake spaCy pipeline and a fake ``sentence_transformers``
module exercise the scoring arithmetic, the fallbacks and the model caching
deterministically, in any environment.
"""

import os
import sys
import types

os.environ.setdefault("CATS_API_KEY", "test-key")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTAwMzI=")

import pytest  # noqa: E402

from cats.core.config import settings  # noqa: E402
from cats.signals import coherence  # noqa: E402
from cats.signals.types import Message  # noqa: E402

# Lower-case entity -> spaCy label, as the fake pipeline will report them.
_LABELS = {"roma": "GPE", "governo": "ORG", "mattarella": "PER", "tevere": "LOC", "euro": "MISC"}


class _Ent:
    def __init__(self, text, label):
        self.text = text
        self.label_ = label


class _FakeNLP:
    """Tags every known word; records the text it was called with."""

    def __init__(self):
        self.seen = []

    def __call__(self, text):
        self.seen.append(text)
        words = [w.strip(".,") for w in text.split()]
        return types.SimpleNamespace(ents=[_Ent(w, _LABELS[w]) for w in words if w in _LABELS])


def _msgs(*texts):
    return [Message(timestamp=f"2026-01-01T{8 + i:02d}:00:00+00:00", text=t) for i, t in enumerate(texts)]


@pytest.fixture
def fake_nlp(monkeypatch):
    nlp = _FakeNLP()
    monkeypatch.setattr(settings, "coherence_backend", "ner")
    monkeypatch.setattr(coherence, "nlp", nlp)
    return nlp


# --- NER backend -----------------------------------------------------------


def test_jaccard_empty_set_guard_and_value():
    assert coherence._jaccard(set(), {"roma"}) == 0.0
    assert coherence._jaccard({"roma"}, set()) == 0.0
    assert coherence._jaccard({"roma", "governo"}, {"roma"}) == 0.5


def test_ner_mean_jaccard_of_consecutive_pairs(fake_nlp):
    # pairs: {roma,governo}/{roma,governo} = 1.0 ; {roma,governo}/{mattarella} = 0.0
    r = coherence.compute_coherence(_msgs("Roma e il Governo.", "Governo a Roma.", "Mattarella parla."))
    assert r.value == pytest.approx(50.0)
    assert r.entity_overlap == pytest.approx(0.5)
    assert r.jaccard_similarity == pytest.approx(0.5)
    assert r.confidence == pytest.approx(0.3)  # 3 messages / 10
    assert r.metadata == {"pairs": 2, "backend": "ner"}


def test_ner_counts_only_person_org_place_labels(fake_nlp):
    # "euro" is tagged MISC: it must not create overlap on its own.
    r = coherence.compute_coherence(_msgs("euro oggi", "euro domani"))
    assert r.value == 0.0


def test_ner_normalises_case_before_tagging(fake_nlp):
    r = coherence.compute_coherence(_msgs("ROMA", "roma"))
    assert r.value == pytest.approx(100.0)
    assert fake_nlp.seen == ["roma", "roma"]


def test_ner_confidence_caps_at_one(fake_nlp):
    r = coherence.compute_coherence(_msgs(*["Roma"] * 12))
    assert r.confidence == 1.0
    assert r.value == pytest.approx(100.0)


def test_ner_single_message_is_insufficient(fake_nlp):
    r = coherence.compute_coherence(_msgs("Roma"))
    assert (r.value, r.confidence) == (100.0, 0.0)
    assert r.metadata == {"reason": "insufficient_messages"}


def test_init_nlp_loads_the_named_model(monkeypatch):
    loaded = []
    fake_spacy = types.SimpleNamespace(load=lambda name: loaded.append(name) or f"model:{name}")
    monkeypatch.setitem(sys.modules, "spacy", fake_spacy)
    monkeypatch.setattr(coherence, "nlp", None)
    coherence.init_nlp("it_core_news_sm")
    assert loaded == ["it_core_news_sm"]
    assert coherence.nlp == "model:it_core_news_sm"


# --- SBERT backend ---------------------------------------------------------


class _FakeSBERT:
    """encode() returns the given vectors, one per message, in order."""

    def __init__(self, vectors):
        self.vectors = vectors

    def encode(self, texts, convert_to_tensor=True):
        assert len(texts) == len(self.vectors)
        return self.vectors


def _cos(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    return dot / (na * nb)


@pytest.fixture
def fake_st(monkeypatch):
    """A fake ``sentence_transformers`` module; returns it so tests can extend it."""
    module = types.ModuleType("sentence_transformers")
    module.util = types.SimpleNamespace(cos_sim=_cos)
    monkeypatch.setitem(sys.modules, "sentence_transformers", module)
    monkeypatch.setattr(settings, "coherence_backend", "sbert")
    monkeypatch.setattr(coherence, "_sbert_failed", False)
    return module


def test_sbert_mean_cosine_of_consecutive_pairs(monkeypatch, fake_st):
    # pairs: identical (1.0), orthogonal (0.0) -> mean 0.5
    monkeypatch.setattr(coherence, "_sbert_model", _FakeSBERT([[1, 0], [1, 0], [0, 1]]))
    r = coherence.compute_coherence(_msgs("a", "b", "c"))
    assert r.value == pytest.approx(50.0)
    assert r.confidence == pytest.approx(0.3)
    assert r.metadata == {"pairs": 2, "backend": "sbert"}
    assert r.entity_overlap == pytest.approx(0.5)


def test_sbert_negative_similarity_clamps_to_zero(monkeypatch, fake_st):
    monkeypatch.setattr(coherence, "_sbert_model", _FakeSBERT([[1, 0], [-1, 0]]))
    r = coherence.compute_coherence(_msgs("a", "b"))
    assert r.value == 0.0
    assert r.entity_overlap == pytest.approx(-1.0)  # raw mean is reported unclamped


def test_sbert_single_message_is_insufficient(monkeypatch, fake_st):
    monkeypatch.setattr(coherence, "_sbert_model", _FakeSBERT([[1, 0]]))
    r = coherence.compute_coherence(_msgs("a"))
    assert (r.value, r.confidence) == (100.0, 0.0)
    assert r.metadata == {"reason": "insufficient_messages"}


def test_sbert_inference_error_falls_back_to_ner(monkeypatch, fake_st):
    class _Broken:
        def encode(self, texts, convert_to_tensor=True):
            raise RuntimeError("CUDA out of memory")

    monkeypatch.setattr(coherence, "_sbert_model", _Broken())
    monkeypatch.setattr(coherence, "nlp", None)
    r = coherence.compute_coherence(_msgs("a", "b"))
    assert r.value == 50.0
    assert r.metadata == {"reason": "nlp_unavailable"}


def test_sbert_model_is_loaded_once_and_cached(monkeypatch, fake_st):
    loads = []

    class _ST:
        def __init__(self, name):
            loads.append(name)
            self.name = name

        def encode(self, texts, convert_to_tensor=True):
            return [[1.0, 0.0]] * len(texts)

    fake_st.SentenceTransformer = _ST
    monkeypatch.setattr(coherence, "_sbert_model", None)
    monkeypatch.setattr(settings, "coherence_model", "fake-model")

    first = coherence.compute_coherence(_msgs("a", "b"))
    second = coherence.compute_coherence(_msgs("c", "d"))
    assert loads == ["fake-model"]
    assert first.value == second.value == pytest.approx(100.0)
    assert coherence._sbert_failed is False


def test_sbert_failed_backend_is_not_retried(monkeypatch, fake_st):
    def _should_not_load(name):
        raise AssertionError("a failed backend must not retry the load")

    fake_st.SentenceTransformer = _should_not_load
    monkeypatch.setattr(coherence, "_sbert_model", None)
    monkeypatch.setattr(coherence, "_sbert_failed", True)
    monkeypatch.setattr(coherence, "nlp", None)
    r = coherence.compute_coherence(_msgs("a", "b"))
    assert r.metadata == {"reason": "nlp_unavailable"}
