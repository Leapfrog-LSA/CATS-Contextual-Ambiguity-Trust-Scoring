import pytest
from pydantic import ValidationError

from cats.api.schemas import EvaluateRequest, MessageSchema


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
