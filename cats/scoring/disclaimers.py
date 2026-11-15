"""Disclaimer strings shared by the CATS output surfaces (WP 4.1 / WP 4.3).

Constants only, no imports and no runtime logic: the text is static on
purpose. ``GET /explain/{trace_id}`` re-explains stored rows with the weights
saved on each row, so the currently loaded weight table may not be the one the
row was scored with; a disclaimer conditioned on it could be wrong.

TODO (human): the long-form wording below is a proposal pending maintainer
(and possibly legal) review — the ``/explain`` disclaimer is cited as an
existing mitigation of risk R1 in the EU AI Act risk-management documentation.
"""

# Common core of the short-form disclaimers (CLI, MCP).
ORDINAL_CORE = "Ordinal score, not a probability"

# Long form, returned as ``disclaimer`` by ``generate_explanation`` (/explain).
# Deliberately does not claim the weights are validated: a table configured via
# CATS_WEIGHTS_FILE, or a caller override, can be any table.
EXPLAIN_DISCLAIMER = (
    "Scores are ordinal rankings of source reliability patterns, not absolute "
    "probabilities. NLP accuracy ~55-62% with the default backends. "
    "Aggregation weights are static initial estimates unless a calibrated "
    "weights table is configured (CATS_WEIGHTS_FILE). Band thresholds are not "
    "calibrated (WP 4.1). Not suitable as sole basis for autonomous decisions "
    "(WP 4.3)."
)

# Short form for the human-readable CLI report.
CLI_NOTE = f"{ORDINAL_CORE}. Cross-validate key claims. See docs/architecture.md."

# Short form attached to every MCP tool response.
MCP_DISCLAIMER = f"{ORDINAL_CORE} (WP 4.3)."
