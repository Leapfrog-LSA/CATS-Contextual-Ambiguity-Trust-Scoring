import pytest
from pydantic import ValidationError

from cats.api.schemas import BatchEvaluateRequest, EvaluateRequest, EvaluateResponse, MessageSchema


class TestMessageSchema:
    def test_valid_message(self):
        m = MessageSchema(timestamp="2026-01-01T08:00:00Z", text="Hello")
        assert m.text == "Hello"

    def test_invalid_timestamp(self):
        with pytest.raises(ValidationError):
            MessageSchema(timestamp="not-a-date", text="Hello")

    def test_empty_text_rejected(self):
        with pytest.raises(ValidationError):
            MessageSchema(timestamp="2026-01-01T08:00:00Z", text="")


class TestEvaluateRequest:
    def test_valid_request(self):
        r = EvaluateRequest(
            source_id="test:source",
            messages=[{"timestamp": "2026-01-01T08:00:00Z", "text": "Hello"}],
        )
        assert r.source_id == "test:source"
        assert len(r.messages) == 1

    def test_empty_messages_rejected(self):
        with pytest.raises(ValidationError):
            EvaluateRequest(source_id="test", messages=[])

    def test_max_messages_enforced(self):
        msgs = [{"timestamp": f"2026-01-01T{i:02d}:00:00Z", "text": f"msg {i}"} for i in range(501)]
        with pytest.raises(ValidationError):
            EvaluateRequest(source_id="test", messages=msgs)


class TestBatchEvaluateRequest:
    @staticmethod
    def _item(source_id="test:source"):
        return {
            "source_id": source_id,
            "messages": [{"timestamp": "2026-01-01T08:00:00Z", "text": "Hello"}],
        }

    def test_valid_batch(self):
        r = BatchEvaluateRequest(items=[self._item("a"), self._item("b")])
        assert len(r.items) == 2
        assert r.items[0].source_id == "a"

    def test_empty_items_rejected(self):
        with pytest.raises(ValidationError):
            BatchEvaluateRequest(items=[])

    def test_max_items_enforced(self):
        with pytest.raises(ValidationError):
            BatchEvaluateRequest(items=[self._item(str(i)) for i in range(51)])


class TestEvaluateResponse:
    _BASE = {"trace_id": "t-1", "score": 61.0, "band": "medium_high", "requires_review": False, "signals": []}

    def test_valid_without_domain_popularity(self):
        r = EvaluateResponse(**self._BASE)
        assert r.domain_popularity is None

    def test_valid_with_domain_popularity(self):
        block = {
            "loaded": True,
            "entries": 2,
            "version": {"list_id": "TEST1", "list_date": None, "downloaded_at": None},
        }
        r = EvaluateResponse(**self._BASE, domain_popularity=block)
        assert r.domain_popularity == block
        assert r.model_dump()["domain_popularity"]["version"]["list_id"] == "TEST1"

    def _base(self, **extra):
        return EvaluateResponse(
            trace_id="t", score=60.0, band="medium_high", requires_review=False, signals=[], **extra
        )

    def test_coherence_backend_defaults_to_none(self):
        assert self._base().coherence_backend is None

    def test_coherence_backend_accepted(self):
        status = {"configured": "sbert", "effective": "ner", "fallback": True}
        assert self._base(coherence_backend=status).coherence_backend == status
