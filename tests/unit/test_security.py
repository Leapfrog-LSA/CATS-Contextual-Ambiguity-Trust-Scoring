import os

os.environ.setdefault("CATS_API_KEY", "test-key")
os.environ.setdefault("CATS_API_KEY_PREV", "old-key")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTE=")

from cats.core.config import settings  # noqa: E402
from cats.core.security import resolve_tenant, verify_api_key  # noqa: E402


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


class TestTenantResolution:
    def test_default_key_maps_to_default_tenant(self, monkeypatch):
        monkeypatch.setattr(settings, "cats_api_key", "primary")
        monkeypatch.setattr(settings, "cats_api_key_prev", None)
        monkeypatch.setattr(settings, "api_keys", None)
        assert verify_api_key("primary") is True
        assert resolve_tenant("primary") == "default"

    def test_mapped_keys_resolve_their_tenant(self, monkeypatch):
        monkeypatch.setattr(settings, "cats_api_key", "primary")
        monkeypatch.setattr(settings, "cats_api_key_prev", None)
        monkeypatch.setattr(settings, "api_keys", "keyA:tenantA, keyB:tenantB")
        assert verify_api_key("keyA") is True
        assert verify_api_key("keyB") is True
        assert resolve_tenant("keyA") == "tenantA"
        assert resolve_tenant("keyB") == "tenantB"
        # primary key still works and stays on the default tenant
        assert verify_api_key("primary") is True
        assert resolve_tenant("primary") == "default"
        # unknown key is rejected and has no tenant
        assert verify_api_key("nope") is False
        assert resolve_tenant("nope") == "default"

    def test_mapped_key_without_tenant_defaults(self, monkeypatch):
        monkeypatch.setattr(settings, "cats_api_key", "primary")
        monkeypatch.setattr(settings, "api_keys", "lonely")
        assert verify_api_key("lonely") is True
        assert resolve_tenant("lonely") == "default"
