"""The interactive API docs and the OpenAPI schema are opt-in (threat model T8).

They map the whole attack surface for any visitor, and the bundled nginx proxies
every path, so the app serves them only when ``CATS_API_DOCS`` is set.
"""

import httpx
import pytest
from fastapi import FastAPI

from cats.api import main
from cats.api.routes.evaluate import router as evaluate_router
from cats.core.config import Settings

DOC_PATHS = ["/docs", "/redoc", "/openapi.json"]


def _app(enabled: bool) -> FastAPI:
    app = FastAPI(**main.docs_urls(enabled))
    app.include_router(evaluate_router, prefix="/v1/cats")
    return app


async def _status(app: FastAPI, path: str) -> int:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        return (await client.get(path)).status_code


def test_docs_are_off_by_default(monkeypatch):
    monkeypatch.delenv("CATS_API_DOCS", raising=False)
    monkeypatch.delenv("API_DOCS", raising=False)
    assert Settings(_env_file=None).api_docs is False


@pytest.mark.parametrize("name", ["CATS_API_DOCS", "API_DOCS"])
def test_docs_can_be_enabled(monkeypatch, name):
    monkeypatch.setenv(name, "true")
    assert Settings(_env_file=None).api_docs is True


def test_the_app_follows_the_setting():
    expected = main.docs_urls(main.settings.api_docs)
    assert main.app.docs_url == expected["docs_url"]
    assert main.app.redoc_url == expected["redoc_url"]
    assert main.app.openapi_url == expected["openapi_url"]


@pytest.mark.parametrize("path", DOC_PATHS)
async def test_disabled_docs_are_not_served(path):
    assert await _status(_app(False), path) == 404


@pytest.mark.parametrize("path", DOC_PATHS)
async def test_enabled_docs_are_served(path):
    assert await _status(_app(True), path) == 200


async def test_enabled_schema_lists_the_scoring_routes():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=_app(True)), base_url="http://test") as client:
        schema = (await client.get("/openapi.json")).json()
    assert "/v1/cats/evaluate" in schema["paths"]
