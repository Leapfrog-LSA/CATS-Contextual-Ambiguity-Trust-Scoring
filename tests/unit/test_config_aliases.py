"""Regression tests for the documented env-var spellings.

CATS_WEIGHTS_FILE and CATS_API_KEYS are the names every doc uses; before
1.3.1 only the bare field names (WEIGHTS_FILE / API_KEYS) were accepted, so
calibrated weights and multi-tenant keys silently never loaded.
"""

import os

os.environ.setdefault("CATS_API_KEY", "test-key")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTE=")

from cats.core.config import Settings  # noqa: E402


def _fresh_settings(monkeypatch, **env):
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    return Settings(_env_file=None)


def test_cats_weights_file_alias(monkeypatch):
    s = _fresh_settings(monkeypatch, CATS_WEIGHTS_FILE="/tmp/w.json")
    assert s.weights_file == "/tmp/w.json"


def test_bare_weights_file_still_accepted(monkeypatch):
    monkeypatch.delenv("CATS_WEIGHTS_FILE", raising=False)
    s = _fresh_settings(monkeypatch, WEIGHTS_FILE="/tmp/w2.json")
    assert s.weights_file == "/tmp/w2.json"


def test_cats_api_keys_alias(monkeypatch):
    s = _fresh_settings(monkeypatch, CATS_API_KEYS="keyA:tenantA")
    assert s.api_keys == "keyA:tenantA"


def test_bare_api_keys_still_accepted(monkeypatch):
    monkeypatch.delenv("CATS_API_KEYS", raising=False)
    s = _fresh_settings(monkeypatch, API_KEYS="keyB:tenantB")
    assert s.api_keys == "keyB:tenantB"


def test_trust_proxy_headers_default_true(monkeypatch):
    monkeypatch.delenv("TRUST_PROXY_HEADERS", raising=False)
    assert Settings(_env_file=None).trust_proxy_headers is True
