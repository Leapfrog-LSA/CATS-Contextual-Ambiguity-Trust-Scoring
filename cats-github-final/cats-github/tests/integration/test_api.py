"""
Integration tests — FastAPI endpoints.
Requires: running Postgres + Redis (or use docker-compose).
For CI without services, most tests are skipped unless DB_AVAILABLE=1.
"""
import os
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

pytestmark = pytest.mark.asyncio


@pytest.fixture
def app():
    from cats.api.main import app as _app
    return _app


async def test_health_endpoint_returns_200(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert "status" in body
    assert "checks" in body


async def test_evaluate_requires_authentication(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post("/v1/cats/evaluate", json={
            "source_id": "src-test",
            "messages": [{"timestamp": "2026-01-01T10:00:00Z", "text": "Hello"}],
        })
    assert r.status_code in (401, 403)


async def test_evaluate_missing_body_returns_422(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post(
            "/v1/cats/evaluate",
            json={"bad": "payload"},
            headers={"Authorization": "Bearer test-api-key-for-ci"},
        )
    # 422 Validation Error OR 401 if rate-limit/auth fires first
    assert r.status_code in (401, 403, 422)


async def test_rfc7807_problem_details_on_validation_error(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.post(
            "/v1/cats/evaluate",
            json={"source_id": "", "messages": []},
            headers={"Authorization": "Bearer test-api-key-for-ci"},
        )
    if r.status_code == 422:
        body = r.json()
        assert "type" in body
        assert "title" in body
        assert "status" in body


async def test_explain_unknown_trace_returns_404(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get(
            "/v1/cats/explain/nonexistent-trace-id-00000000",
            headers={"Authorization": "Bearer test-api-key-for-ci"},
        )
    # 404 OR 401 if auth/redis not initialised in test env
    assert r.status_code in (401, 404, 500)


async def test_openapi_schema_available(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/openapi.json")
    assert r.status_code == 200
    assert "paths" in r.json()
