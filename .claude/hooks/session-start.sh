#!/bin/bash
# CATS — SessionStart hook for Claude Code on the web (docs/cloud_setup.md).
# Version-controlled fallback for the environment's Setup script: on a cold
# cloud container it installs the dev/test stack and the Italian NLP assets;
# with a warm cache every check below is a fast no-op. Non-critical downloads
# use `|| true` so one flaky fetch never blocks the session.
set -uo pipefail

# Cloud-only by design: local sessions exit immediately so developer startup
# stays instant. Claude Code remote containers expose these markers.
if [ -z "${CLAUDE_CODE_CONTAINER_ID:-}" ] && [ "${CCR_AGENT_PROXY_ENABLED:-0}" != "1" ]; then
    exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" || exit 0

# Dev/test stack — requirements-dev.txt pulls in requirements.txt (the API
# deployment deps needed by the integration tests) plus linters and pytest.
if ! python -c "import pytest, cats" > /dev/null 2>&1; then
    echo "cats session-start: installing dev/test stack..."
    python -m pip install -q -e . -r requirements-dev.txt || true
fi

# spaCy Italian model — powers the default NER coherence backend. Non-fatal:
# without it NER coherence degrades to a neutral value (tests still pass).
if ! python -c "import it_core_news_lg" > /dev/null 2>&1; then
    echo "cats session-start: downloading spaCy it_core_news_lg..."
    python -m spacy download it_core_news_lg > /dev/null 2>&1 || true
fi

# TextBlob corpora — back the volatility sentiment signal.
if [ ! -d "${NLTK_DATA:-$HOME/nltk_data}" ]; then
    echo "cats session-start: downloading TextBlob corpora..."
    python -m textblob.download_corpora > /dev/null 2>&1 || true
fi

echo "cats session-start: environment ready."
