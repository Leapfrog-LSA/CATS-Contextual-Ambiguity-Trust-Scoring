"""Integration tests for the CATS API.

These tests require PostgreSQL and Redis running (see docker-compose.yml).
Skipped automatically if services are unavailable.
"""

import os

import pytest

os.environ.setdefault("CATS_API_KEY", "test-api-key")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://cats:cats@localhost:5432/cats_test")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTE=")
os.environ.setdefault("ENVIRONMENT", "test")

try:
    from httpx import ASGITransport, AsyncClient

    from cats.api.main import app

    HAS_DEPS = True
except Exception:
    HAS_DEPS = False

pytestmark = pytest.mark.skipif(not HAS_DEPS, reason="Integration deps not available")


@pytest.fixture
def api_headers():
    return {
        "Authorization": "Bearer test-api-key",
        "Content-Type": "application/json",
    }


@pytest.fixture
async def client():
    # ASGITransport does not run the app lifespan, so initialise the pieces the
    # request path needs: Redis (rate limiting in auth) and the DB tables that
    # /explain and /contest query. NLP is not exercised by these tests, so the
    # spaCy model is intentionally not loaded here.
    import cats.core.models  # noqa: F401  (register tables on Base.metadata)
    from cats.core.db import Base, engine
    from cats.core.security import init_redis

    await init_redis()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


class TestHealthEndpoint:
    async def test_health_returns_status(self, client):
        r = await client.get("/health")
        assert r.status_code == 200
        data = r.json()
        assert "status" in data
        assert "checks" in data
        assert data["checks"]["api"] == "ok"


class TestEvaluateEndpoint:
    async def test_evaluate_requires_auth(self, client):
        r = await client.post("/v1/cats/evaluate", json={})
        assert r.status_code in (401, 403, 422)

    async def test_evaluate_validates_input(self, client, api_headers):
        r = await client.post("/v1/cats/evaluate", json={}, headers=api_headers)
        assert r.status_code == 422

    async def test_evaluate_rejects_empty_messages(self, client, api_headers):
        r = await client.post(
            "/v1/cats/evaluate",
            json={
                "source_id": "test:source",
                "messages": [],
            },
            headers=api_headers,
        )
        assert r.status_code == 422

    async def test_evaluate_rejects_over_500_messages(self, client, api_headers):
        msgs = [{"timestamp": f"2026-01-01T{i % 24:02d}:00:00Z", "text": f"msg {i}"} for i in range(501)]
        r = await client.post(
            "/v1/cats/evaluate",
            json={
                "source_id": "test:source",
                "messages": msgs,
            },
            headers=api_headers,
        )
        assert r.status_code == 422


class TestExplainEndpoint:
    async def test_explain_not_found(self, client, api_headers):
        r = await client.get("/v1/cats/explain/nonexistent-trace", headers=api_headers)
        assert r.status_code == 404


class TestContestEndpoint:
    async def test_contest_not_found(self, client, api_headers):
        r = await client.post(
            "/v1/cats/contest/nonexistent-trace",
            json={
                "reason": "This is a valid contest reason with enough length.",
            },
            headers=api_headers,
        )
        assert r.status_code == 404

    async def test_contest_short_reason_rejected(self, client, api_headers):
        r = await client.post(
            "/v1/cats/contest/some-trace",
            json={
                "reason": "short",
            },
            headers=api_headers,
        )
        assert r.status_code == 422


class TestStatsEndpoint:
    async def test_stats_requires_auth(self, client):
        r = await client.get("/v1/cats/stats")
        assert r.status_code in (401, 403)
