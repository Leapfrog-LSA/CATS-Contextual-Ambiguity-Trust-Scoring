import sys

import pytest

from cats.mcp_server import _BANDS, _DISCLAIMER, explain_bands, main, score_messages, score_source

_MESSAGES = [
    {"timestamp": "2026-01-01T08:00:00Z", "text": "Il governo annuncia un piano economico."},
    {"timestamp": "2026-01-02T09:00:00Z", "text": "Il parlamento discute la legge di bilancio."},
    {"timestamp": "2026-01-03T09:00:00Z", "text": "Il presidente firma il decreto."},
]


def test_score_source_wraps_score_feed_and_adds_disclaimer(monkeypatch):
    captured = {}

    def _fake_score_feed(url, source_type="default", **kwargs):
        captured["url"] = url
        captured["source_type"] = source_type
        return {"trust_score": 71.37, "band": "medium_high"}

    monkeypatch.setattr("cats.mcp_server._score_feed", _fake_score_feed)

    result = score_source("https://esempio.it", source_type="news")

    assert captured == {"url": "https://esempio.it", "source_type": "news"}
    assert result["trust_score"] == 71.37
    assert result["disclaimer"] == _DISCLAIMER


def test_score_messages_wraps_score_and_adds_disclaimer(monkeypatch):
    captured = {}

    def _fake_score(messages, source_type="default", url=None, **kwargs):
        captured["messages"] = messages
        captured["source_type"] = source_type
        captured["url"] = url
        return {"trust_score": 50.0, "band": "medium"}

    monkeypatch.setattr("cats.mcp_server._score", _fake_score)

    result = score_messages(_MESSAGES, source_type="news", url="https://esempio.it")

    assert captured["messages"] == _MESSAGES
    assert captured["source_type"] == "news"
    assert captured["url"] == "https://esempio.it"
    assert result["trust_score"] == 50.0
    assert result["disclaimer"] == _DISCLAIMER


def test_score_messages_defaults_url_to_none(monkeypatch):
    captured = {}

    def _fake_score(messages, source_type="default", url=None, **kwargs):
        captured["url"] = url
        return {"trust_score": 50.0, "band": "medium"}

    monkeypatch.setattr("cats.mcp_server._score", _fake_score)

    score_messages(_MESSAGES)

    assert captured["url"] is None


def test_explain_bands_returns_table_and_disclaimer():
    result = explain_bands()

    assert result["disclaimer"] == _DISCLAIMER
    assert result["bands"] == _BANDS
    assert len(result["bands"]) == 5
    assert {b["band"] for b in result["bands"]} == {"high", "medium_high", "medium", "low", "very_low"}


def test_main_without_mcp_extra_raises_clear_error(monkeypatch):
    # If something else in the test session already imported the real `mcp`
    # package (e.g. gradio, when both optional extras happen to be installed
    # together, imports it transitively), its submodules stay cached in
    # sys.modules; blocking only the top-level "mcp" key would then leave
    # `from mcp.server.fastmcp import FastMCP` resolving from that stale
    # cache instead of raising ImportError -- so this actually spins up a
    # real stdio MCP server reading pytest's captured stdin. Clear every
    # mcp/mcp.* entry first so the None sentinel is the only thing found.
    for name in [m for m in sys.modules if m == "mcp" or m.startswith("mcp.")]:
        monkeypatch.delitem(sys.modules, name)
    monkeypatch.setitem(sys.modules, "mcp", None)

    with pytest.raises(SystemExit, match=r"pip install cats-scoring\[mcp\]"):
        main()


def test_server_registers_three_tools():
    pytest.importorskip("mcp")
    from cats.mcp_server import _create_server

    server = _create_server()
    tools = server._tool_manager.list_tools()

    assert {t.name for t in tools} == {"score_source", "score_messages", "explain_bands"}
    for tool in tools:
        assert tool.description  # docstrings written for an LLM client
