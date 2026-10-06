"""MCP server exposing CATS scoring as tools for an LLM client.

A thin wrapper over :mod:`cats.lite` — no signal logic lives here. Requires
the optional ``mcp`` extra (``pip install cats-scoring[mcp]``); importing
this module never requires it, only running the server does (see
:func:`main`).

Run with ``cats-mcp`` (stdio transport), or point an MCP-aware client at
``python -m cats.mcp_server``.
"""

from __future__ import annotations

import sys
from typing import Any, Dict, List, Optional

import structlog

from cats.lite import compare_feeds as _compare_feeds
from cats.lite import score as _score
from cats.lite import score_feed as _score_feed

# WP 4.3: scores are ordinal rankings, not calibrated probabilities. Attached
# to every tool response so an LLM client surfaces it, not just the docstrings.
_DISCLAIMER = "Ordinal score, not a probability (WP 4.3)."

# Each source costs a feed fetch plus NLP over its messages; an LLM client can
# be prompted into long lists, so one call is capped (cf. threat model T1).
MAX_COMPARE_SOURCES = 10

_BANDS = [
    {
        "score_range": "80-100",
        "band": "high",
        "recommended_action": "Lower review priority; still cross-check key claims",
    },
    {"score_range": "60-79", "band": "medium_high", "recommended_action": "Cross-validate key claims"},
    {"score_range": "40-59", "band": "medium", "recommended_action": "Human review recommended"},
    {"score_range": "20-39", "band": "low", "recommended_action": "Human review required"},
    {"score_range": "0-19", "band": "very_low", "recommended_action": "Do not use without validation"},
]


def score_source(url: str, source_type: str = "default") -> Dict:
    """Score an OSINT source's trust/reliability directly from its URL.

    Fetches the source's RSS/Atom feed (discovering it automatically if
    ``url`` is a homepage rather than a feed) and scores its message history
    with the CATS behavioural-signal pipeline. ``source_type`` should be
    ``"news"`` for news outlets or ``"default"`` otherwise — it selects the
    calibrated signal weights.

    Returns a dict with ``trust_score`` (0-100), ``band`` (``high`` down to
    ``very_low``), ``requires_human_review``, per-signal ``signals``,
    ``language``/``evidence`` flags, a full ``explanation`` (which signal
    drove the score and why), a ``source`` block (feed URL, message count,
    time span), and a ``disclaimer``. Raises an error if the host is
    unreachable, no feed can be found, or the feed has no usable messages.
    """
    result = _score_feed(url, source_type=source_type)
    result["disclaimer"] = _DISCLAIMER
    return result


def score_messages(messages: List[dict], source_type: str = "default", url: Optional[str] = None) -> Dict:
    """Score an OSINT source's trust/reliability from an already-collected message history.

    Use this instead of ``score_source`` when the messages were gathered some
    other way (not a public RSS/Atom feed). Each message is
    ``{"timestamp": ISO-8601 string, "text": string}``. ``source_type``
    should be ``"news"`` for news outlets or ``"default"`` otherwise.
    ``url``, if given, enables the domain-provenance penalty (impersonation/
    clone domains only ever lower the score).

    Returns the same shape as ``score_source`` minus the ``source`` block.
    Raises an error if no messages remain after normalisation.
    """
    result = _score(messages, source_type=source_type, url=url)
    result["disclaimer"] = _DISCLAIMER
    return result


def compare_sources(urls: List[str], source_type: str = "default") -> Dict:
    """Score several OSINT sources from their URLs and rank them side by side.

    Use this instead of calling ``score_source`` repeatedly when the user wants
    to compare or prioritise a list of sources (2 to 10 URLs per call).
    Duplicates are dropped. ``source_type`` (``"news"`` or ``"default"``)
    applies to every source; compare news outlets with ``"news"``.

    Returns ``ranked`` (highest trust score first; each row has ``rank``,
    ``url``, ``trust_score``, ``band``, ``primary_driver``, raw ``signals``,
    ``messages``, ``requires_human_review``, ``review_reason``,
    ``degraded_signals``, ``domain_red_flag``), ``errors`` (sources that could
    not be scored, with the reason; they do not stop the comparison), a
    ``note`` and a ``disclaimer``. The ranking describes publishing behaviour,
    not truthfulness, and holds only within this call: tell the user so rather
    than presenting the top source as "true".
    """
    unique = list(dict.fromkeys(urls))
    if len(unique) < 2:
        raise ValueError("compare_sources needs at least two distinct URLs")
    if len(unique) > MAX_COMPARE_SOURCES:
        raise ValueError(f"compare_sources accepts at most {MAX_COMPARE_SOURCES} URLs per call, got {len(unique)}")
    result = _compare_feeds(unique, source_type=source_type)
    result["disclaimer"] = _DISCLAIMER
    return result


def explain_bands() -> Dict:
    """Return the CATS trust-score band table and the ordinal-score disclaimer.

    Static reference data — no scoring is performed. Useful for an LLM
    client to explain what a returned ``band`` means without hard-coding the
    thresholds itself.
    """
    return {"bands": _BANDS, "disclaimer": _DISCLAIMER}


def _server_class() -> Any:
    """The MCP server class: ``MCPServer`` in mcp 2.x, ``FastMCP`` in 1.x.

    Both take a server name, register tools with ``.tool()`` and serve stdio
    with ``.run()``. Raises ``ImportError`` when neither is importable.
    """
    try:
        from mcp.server.mcpserver import MCPServer

        return MCPServer
    except ImportError:
        # mcp 2.x keeps an mcp.server.fastmcp stub without FastMCP, so type-check
        # against 2.x flags this 1.x-only import; at runtime 2.x never reaches it.
        from mcp.server.fastmcp import FastMCP  # type: ignore[attr-defined]

        return FastMCP


def _create_server():
    """Build the MCP server with all four tools registered. Requires ``mcp``."""
    server = _server_class()("cats-scoring")
    server.tool()(score_source)
    server.tool()(score_messages)
    server.tool()(compare_sources)
    server.tool()(explain_bands)
    return server


def _log_to_stderr() -> None:
    """Send structlog output to stderr for the life of the server process.

    The stdio transport owns stdout: anything else written there corrupts the
    JSON-RPC stream, which the MCP spec forbids. structlog's default logger
    prints to stdout, and the library logs on ordinary paths (a missing spaCy
    model, every fetched feed).
    """
    structlog.configure(logger_factory=structlog.PrintLoggerFactory(file=sys.stderr))


def main() -> None:
    try:
        _server_class()
    except ImportError as exc:
        try:
            import mcp  # noqa: F401
        except ImportError:
            raise SystemExit(
                "The 'mcp' package is required to run the CATS MCP server.\n"
                "Install it with: pip install cats-scoring[mcp]"
            ) from exc
        raise SystemExit(
            "The installed 'mcp' package has neither MCPServer (mcp 2.x) nor FastMCP (mcp 1.x).\n"
            'Install a supported version with: pip install "cats-scoring[mcp]"'
        ) from exc

    _log_to_stderr()
    _create_server().run()


if __name__ == "__main__":
    main()
