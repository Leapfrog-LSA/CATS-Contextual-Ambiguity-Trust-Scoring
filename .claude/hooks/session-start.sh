#!/bin/bash
# CATS — SessionStart hook for Claude Code on the web (docs/cloud_setup.md).
# Version-controlled fallback for the environment's Setup script: on a cold
# cloud container it installs the dev/test stack and the Italian NLP assets;
# with a warm cache every check below is a fast no-op. Non-critical downloads
# (spaCy model, TextBlob corpora) stay silent on failure so one flaky fetch
# never blocks the session; the dev/test stack does not — a session that cannot
# run lint or tests has to be told so, not left to find out.
set -uo pipefail

# Cloud-only by design: local sessions exit immediately so developer startup
# stays instant. Claude Code remote containers expose these markers.
if [ -z "${CLAUDE_CODE_CONTAINER_ID:-}" ] && [ "${CCR_AGENT_PROXY_ENABLED:-0}" != "1" ]; then
    exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}" || exit 0

# Dev/test stack — requirements-dev.txt pulls in requirements.txt (the API
# deployment deps needed by the integration tests) plus linters and pytest.
#
# `--ignore-installed PyJWT` is not optional here. The cloud base image ships a
# Debian-packaged PyJWT, which carries no RECORD file, so pip cannot uninstall
# it to satisfy the version this project resolves to and aborts the *entire*
# install ("Cannot uninstall PyJWT 2.7.0, RECORD file not found. Hint: The
# package was installed by debian") — leaving pytest, httpx and pydantic absent.
# Nothing is reinstalled needlessly: this branch only runs when the stack is
# missing altogether.
if ! python -c "import pytest, cats" > /dev/null 2>&1; then
    echo "cats session-start: installing dev/test stack..."
    install_log="$(mktemp)"
    if ! python -m pip install -q --ignore-installed PyJWT -e . -r requirements-dev.txt > "$install_log" 2>&1; then
        echo "cats session-start: pip install failed — last lines:"
        tail -n 10 "$install_log"
    fi
    rm -f "$install_log"
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

# Report what happened, not what was attempted. This line used to be
# unconditional, so a session whose install had failed was told "environment
# ready" and only discovered otherwise when lint and tests would not run.
if python -c "import pytest, cats" > /dev/null 2>&1; then
    echo "cats session-start: environment ready."
else
    echo "cats session-start: environment NOT ready — 'import pytest, cats' still fails, so lint and tests will not run."
    echo "cats session-start: retry with 'python -m pip install --ignore-installed PyJWT -e . -r requirements-dev.txt'."
fi
