import sys

import pytest

from cats.mcp_server import (
    _BANDS,
    _DISCLAIMER,
    MAX_COMPARE_SOURCES,
    compare_sources,
    explain_bands,
    main,
    score_messages,
    score_source,
)

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


def _mcp_stdio_session(requests, timeout=120):
    """Run ``python -m cats.mcp_server`` and exchange JSON-RPC lines over stdio.

    Returns (responses by id, every stdout line). Talks raw JSON-RPC rather than
    through the mcp client API, so the same test runs against mcp 1.x and 2.x.
    """
    import json
    import subprocess

    proc = subprocess.Popen(
        [sys.executable, "-m", "cats.mcp_server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    lines, responses = [], {}
    try:
        for request in requests:
            proc.stdin.write(json.dumps(request) + "\n")
            proc.stdin.flush()
            if "id" not in request:
                continue
            while request["id"] not in responses:
                line = proc.stdout.readline()
                assert line, "server closed stdout"
                lines.append(line)
                message = json.loads(line)  # anything that is not JSON-RPC fails here
                if "id" in message:
                    responses[message["id"]] = message
    finally:
        proc.kill()
        proc.wait(timeout=timeout)
    return responses, lines


def test_stdio_session_lists_and_calls_tools_with_a_clean_stdout():
    pytest.importorskip("mcp")
    import json

    responses, lines = _mcp_stdio_session(
        [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "t", "version": "0"},
                },
            },
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "explain_bands", "arguments": {}}},
            # Scoring logs (spaCy model loaded or missing): those lines must go to stderr.
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {"name": "score_messages", "arguments": {"messages": _MESSAGES, "source_type": "news"}},
            },
        ]
    )

    assert all(json.loads(line).get("jsonrpc") == "2.0" for line in lines)
    tools = responses[2]["result"]["tools"]
    assert {t["name"] for t in tools} == {"score_source", "score_messages", "compare_sources", "explain_bands"}
    assert all(t["description"] for t in tools)  # docstrings written for an LLM client
    bands = json.loads(responses[3]["result"]["content"][0]["text"])
    assert bands["disclaimer"] == _DISCLAIMER
    scored = json.loads(responses[4]["result"]["content"][0]["text"])
    assert not responses[4]["result"].get("isError")
    assert scored["disclaimer"] == _DISCLAIMER
    assert 0 <= scored["trust_score"] <= 100


def test_main_names_an_unsupported_mcp_version(monkeypatch):
    # mcp is importable but exposes neither server class (a future major).
    import types

    fake = types.ModuleType("mcp")
    monkeypatch.setitem(sys.modules, "mcp", fake)
    for name in ("mcp.server", "mcp.server.mcpserver", "mcp.server.fastmcp"):
        monkeypatch.setitem(sys.modules, name, None)

    with pytest.raises(SystemExit, match="neither MCPServer"):
        main()


def test_compare_sources_wraps_compare_feeds_and_adds_disclaimer(monkeypatch):
    captured = {}

    def _fake_compare(urls, source_type="default", **kwargs):
        captured["urls"] = urls
        captured["source_type"] = source_type
        return {"source_type": source_type, "ranked": [], "errors": [], "note": "n"}

    monkeypatch.setattr("cats.mcp_server._compare_feeds", _fake_compare)

    result = compare_sources(["https://a.it", "https://b.it", "https://a.it"], source_type="news")

    assert captured == {"urls": ["https://a.it", "https://b.it"], "source_type": "news"}
    assert result["disclaimer"] == _DISCLAIMER


@pytest.mark.parametrize(
    "urls",
    [
        ["https://a.it"],
        ["https://a.it", "https://a.it"],
        [f"https://s{i}.it" for i in range(MAX_COMPARE_SOURCES + 1)],
    ],
)
def test_compare_sources_rejects_too_few_or_too_many(monkeypatch, urls):
    monkeypatch.setattr("cats.mcp_server._compare_feeds", lambda *a, **k: pytest.fail("must not score"))
    with pytest.raises(ValueError):
        compare_sources(urls)
