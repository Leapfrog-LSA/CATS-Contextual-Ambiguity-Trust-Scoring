import os

os.environ.setdefault("CATS_API_KEY", "test-key")
os.environ.setdefault("CATS_API_KEY_PREV", "old-key")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTAwMzI=")

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


class TestRateLimitKeying:
    def test_bucket_is_per_api_key_and_hashed(self):
        from unittest.mock import Mock

        from cats.core.security import rate_limit_id

        req = Mock()
        bucket = rate_limit_id("secret-key", req)
        assert bucket.startswith("key:")
        assert "secret-key" not in bucket  # raw secrets never reach Redis keys
        assert bucket == rate_limit_id("secret-key", req)  # stable
        assert bucket != rate_limit_id("other-key", req)  # fair per key

    def test_falls_back_to_ip_without_key(self, monkeypatch):
        from unittest.mock import Mock

        from cats.core.security import rate_limit_id

        monkeypatch.setattr(settings, "trust_proxy_headers", True)
        req = Mock()
        req.headers = {"X-Forwarded-For": "1.2.3.4"}
        assert rate_limit_id("", req) == "ip:1.2.3.4"


class TestFailedAuthRateLimit:
    """Invalid API-key attempts must be rate-limited per client IP — the
    per-key limiter only runs after successful verification, so failures
    would otherwise allow unlimited brute-force guesses."""

    def _request(self, token="wrong-key", ip="9.9.9.9"):
        from unittest.mock import Mock

        req = Mock()
        req.headers = {"Authorization": f"Bearer {token}"}
        req.client.host = ip
        return req

    async def test_failed_attempts_hit_ip_bucket(self, monkeypatch):
        import cats.core.security as security

        monkeypatch.setattr(settings, "cats_api_key", "real-key")
        monkeypatch.setattr(settings, "cats_api_key_prev", None)
        monkeypatch.setattr(settings, "api_keys", None)
        monkeypatch.setattr(settings, "trust_proxy_headers", False)
        buckets = []

        async def fake_limit(client_id):
            buckets.append(client_id)
            return True

        monkeypatch.setattr(security, "check_rate_limit", fake_limit)
        import pytest
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as exc:
            await security.APIKeyBearer()(self._request())
        assert exc.value.status_code == 401
        assert buckets == ["authfail:9.9.9.9"]

    async def test_failed_attempts_over_limit_get_429(self, monkeypatch):
        import cats.core.security as security

        monkeypatch.setattr(settings, "cats_api_key", "real-key")
        monkeypatch.setattr(settings, "cats_api_key_prev", None)
        monkeypatch.setattr(settings, "api_keys", None)
        monkeypatch.setattr(settings, "trust_proxy_headers", False)

        async def exhausted(client_id):
            return False

        monkeypatch.setattr(security, "check_rate_limit", exhausted)
        import pytest
        from fastapi import HTTPException

        with pytest.raises(HTTPException) as exc:
            await security.APIKeyBearer()(self._request())
        assert exc.value.status_code == 429


class TestNginxForwardedForNotAppended:
    def test_nginx_overwrites_x_forwarded_for(self):
        """get_client_ip takes the FIRST X-Forwarded-For entry and it lands in
        the GDPR audit log, so nginx must overwrite the header with
        $remote_addr — $proxy_add_x_forwarded_for appends to a client-supplied
        value and would let callers forge the audited IP."""
        from pathlib import Path

        conf = Path(__file__).resolve().parents[2] / "deploy" / "nginx.conf"
        text = conf.read_text(encoding="utf-8")
        # Comments may mention the appending variable; active directives must not.
        directives = [ln for ln in text.splitlines() if not ln.lstrip().startswith("#")]
        assert not any("$proxy_add_x_forwarded_for" in ln for ln in directives)
        assert any("proxy_set_header X-Forwarded-For $remote_addr;" in ln for ln in directives)


class TestClientIpTrust:
    def _req(self, xff, host="10.0.0.9"):
        from unittest.mock import Mock

        req = Mock()
        req.headers = {"X-Forwarded-For": xff} if xff else {}
        req.client.host = host
        return req

    def test_xff_honoured_when_trusted(self, monkeypatch):
        from cats.core.security import get_client_ip

        monkeypatch.setattr(settings, "trust_proxy_headers", True)
        assert get_client_ip(self._req("1.2.3.4, 5.6.7.8")) == "1.2.3.4"

    def test_xff_ignored_when_untrusted(self, monkeypatch):
        from cats.core.security import get_client_ip

        monkeypatch.setattr(settings, "trust_proxy_headers", False)
        assert get_client_ip(self._req("1.2.3.4")) == "10.0.0.9"
