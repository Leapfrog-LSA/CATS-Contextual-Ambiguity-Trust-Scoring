import os

os.environ.setdefault("CATS_API_KEY", "test-key")
os.environ.setdefault("CATS_API_KEY_PREV", "old-key")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTE=")

from cats.core.config import settings  # noqa: E402
from cats.core.security import verify_api_key  # noqa: E402


class TestVerifyApiKey:
    # Set the keys on settings directly: the CI environment pre-sets CATS_API_KEY,
    # so os.environ.setdefault above is a no-op there and settings already holds
    # the CI value. monkeypatch keeps each test isolated and self-restoring.
    def test_valid_current_key(self, monkeypatch):
        monkeypatch.setattr(settings, "cats_api_key", "test-key")
        assert verify_api_key("test-key") is True

    def test_valid_previous_key(self, monkeypatch):
        monkeypatch.setattr(settings, "cats_api_key", "current-key")
        monkeypatch.setattr(settings, "cats_api_key_prev", "old-key")
        assert verify_api_key("old-key") is True

    def test_invalid_key(self, monkeypatch):
        monkeypatch.setattr(settings, "cats_api_key", "test-key")
        monkeypatch.setattr(settings, "cats_api_key_prev", None)
        assert verify_api_key("wrong-key") is False

    def test_empty_key(self, monkeypatch):
        monkeypatch.setattr(settings, "cats_api_key", "test-key")
        monkeypatch.setattr(settings, "cats_api_key_prev", None)
        assert verify_api_key("") is False
