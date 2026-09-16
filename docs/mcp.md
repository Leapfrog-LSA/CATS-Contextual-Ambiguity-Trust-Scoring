# MCP server

`cats.mcp_server` exposes CATS scoring as [MCP](https://modelcontextprotocol.io)
tools for an LLM client (Claude Code, Claude Desktop, or any MCP-aware
agent), so it can score an OSINT source directly instead of shelling out to
the CLI or writing a Python call. It is a thin wrapper over `cats.lite` — no
signal logic lives here.

## Install

```bash
pip install "cats-scoring[mcp]"
```

The `mcp` package (`mcp>=1.0,<2.0`) is an optional extra, not a core
dependency — importing `cats.mcp_server` never requires it, only running the
server does.

## Run

```bash
cats-mcp
```

Runs over stdio. If the `mcp` extra is not installed, `cats-mcp` exits with a
clear message telling you to install it — it never crashes with a raw
`ImportError`.

## Configure in Claude Code

Add to your MCP configuration (e.g. `.mcp.json` or via `claude mcp add`):

```json
{
  "mcpServers": {
    "cats-scoring": {
      "command": "cats-mcp"
    }
  }
}
```

Or, without installing the console script:

```json
{
  "mcpServers": {
    "cats-scoring": {
      "command": "python",
      "args": ["-m", "cats.mcp_server"]
    }
  }
}
```

## Tools

### `score_source(url, source_type="default")`

Scores a source directly from its URL — fetches (and autodiscovers, if
needed) its RSS/Atom feed, then runs the CATS signal pipeline. Same
autodiscovery behaviour as `cats.lite.score_feed`/`cats score <url>`. Returns
`score()`'s result plus a `source` block (feed URL, message count, time
span) and a `disclaimer`.

### `score_messages(messages, source_type="default", url=None)`

Scores a source from an already-collected list of
`{"timestamp": ISO-8601, "text": str}` messages — use this when the source
isn't a public feed. `url`, if given, enables the domain-provenance penalty.
Returns `score()`'s result plus a `disclaimer`.

### `explain_bands()`

Static reference: the trust-score band table (`high` down to `very_low`,
with the recommended action for each) and the ordinal-score disclaimer. No
scoring is performed.

## Caveats

Same as everywhere else in CATS: scores are ordinal rankings, not calibrated
probabilities (every tool response carries a `disclaimer` field saying so);
the default NLP stack is Italian-optimised; `score_source` needs network
access to fetch the source's feed. See [architecture.md](architecture.md)
and the top-level [README](../README.md) for the full picture.
