import os

import pytest

os.environ.setdefault("CATS_API_KEY", "test-key")
os.environ.setdefault("CATS_API_KEY_PREV", "old-key")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTE=")

from cats.core.security import verify_api_key


class TestVerifyApiKey:
    def test_valid_current_key(self):
        assert verify_api_key("test-key") is True

    def test_valid_previous_key(self):
        assert verify_api_key("old-key") is True

    def test_invalid_key(self):
        assert verify_api_key("wrong-key") is False

    def test_empty_key(self):
        assert verify_api_key("") is False
