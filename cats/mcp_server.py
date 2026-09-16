"""MCP server exposing CATS scoring as tools for an LLM client.

A thin wrapper over :mod:`cats.lite` — no signal logic lives here. Requires
the optional ``mcp`` extra (``pip install cats-scoring[mcp]``); importing
this module never requires it, only running the server does (see
:func:`main`).

Run with ``cats-mcp`` (stdio transport), or point an MCP-aware client at
``python -m cats.mcp_server``.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from cats.lite import score as _score
from cats.lite import score_feed as _score_feed

# WP 4.3: scores are ordinal rankings, not calibrated probabilities. Attached
# to every tool response so an LLM client surfaces it, not just the docstrings.
_DISCLAIMER = "Ordinal score, not a probability (WP 4.3)."

_BANDS = [
    {"score_range": "80-100", "band": "high", "recommended_action": "Usable for OSINT"},
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


def explain_bands() -> Dict:
    """Return the CATS trust-score band table and the ordinal-score disclaimer.

    Static reference data — no scoring is performed. Useful for an LLM
    client to explain what a returned ``band`` means without hard-coding the
    thresholds itself.
    """
    return {"bands": _BANDS, "disclaimer": _DISCLAIMER}


def _create_server():
    """Build the FastMCP server with all three tools registered. Requires ``mcp``."""
    from mcp.server.fastmcp import FastMCP

    server = FastMCP("cats-scoring")
    server.tool()(score_source)
    server.tool()(score_messages)
    server.tool()(explain_bands)
    return server


def main() -> None:
    try:
        from mcp.server.fastmcp import FastMCP  # noqa: F401
    except ImportError as exc:
        raise SystemExit(
            "The 'mcp' package is required to run the CATS MCP server.\n"
            "Install it with: pip install cats-scoring[mcp]"
        ) from exc

    _create_server().run()


if __name__ == "__main__":
    main()
