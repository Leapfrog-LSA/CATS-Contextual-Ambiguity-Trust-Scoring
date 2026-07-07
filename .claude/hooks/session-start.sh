#!/bin/bash
# SessionStart hook for Claude Code on the web.
# Installs the CATS package (editable) with dev/test dependencies and, best
# effort, the Italian NLP assets (spaCy it_core_news_lg + TextBlob corpora)
# so the linters and the full test suite can run in a fresh remote session.
#
# Installs into a project virtualenv (.venv) rather than the Debian system
# Python, whose packages are externally managed and cannot be upgraded in
# place. The venv is persisted onto PATH for the session via $CLAUDE_ENV_FILE.
#
# Idempotent and non-interactive: safe to re-run; the venv is reused and
# pip/spaCy skip work that is already satisfied.
set -euo pipefail

# Only run in Claude Code on the web; a no-op locally so it never interferes
# with a developer's own environment.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-.}"

VENV_DIR="${CLAUDE_PROJECT_DIR:-.}/.venv"
if [ ! -x "$VENV_DIR/bin/python" ]; then
  python3 -m venv "$VENV_DIR"
fi
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# Editable install + full dev/test stack. requirements-dev.txt pulls in
# requirements.txt (FastAPI/SQLAlchemy/... needed by the integration tests)
# plus the linters and pytest. This is the hard requirement for tests+linters.
python -m pip install -e . -r requirements-dev.txt

# Persist the venv for the rest of the session *before* the optional model
# download, so `python`, `pytest`, `black`, etc. resolve to it even if the
# best-effort NLP asset fetch below is blocked or slow. The test env vars
# mirror the CI `test` job (.github/workflows/ci.yml): cats.core.config.Settings
# has no defaults for them, so pytest fails at import-time collection without
# them. These are throwaway test values, not secrets — the DB/Redis URLs only
# matter for the integration suite, which needs live services (`make docker-up`)
# the unit suite does not.
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  {
    echo "export VIRTUAL_ENV=\"$VENV_DIR\""
    echo "export PATH=\"$VENV_DIR/bin:\$PATH\""
    echo "export ENVIRONMENT=test"
    echo "export CATS_API_KEY=test-api-key"
    echo "export DATABASE_URL=postgresql+asyncpg://cats:cats@localhost:5432/cats_test"
    echo "export REDIS_URL=redis://localhost:6379/0"
    echo "export AUDIT_ENCRYPTION_KEY=dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTAwMzI="
  } >> "$CLAUDE_ENV_FILE"
fi

# Italian NLP assets — best effort. The coherence signal (WP 4.1) is
# Italian-optimised: the spaCy NER model powers the default backend and
# TextBlob corpora back the volatility sentiment signal. Both are OPTIONAL:
# without the model, NER coherence degrades to a neutral zero-confidence value
# (see cats/signals/coherence.py) and the test suite covers exactly that path,
# so a fetch blocked by egress policy must not fail the whole hook.
# The spaCy model wheel is served from github.com; if that host is not allowed
# by the session's network policy the download is skipped with a warning.
if ! python -m spacy download it_core_news_lg; then
  echo "WARN: could not download spaCy it_core_news_lg (github.com egress?)." \
       "NER coherence will degrade to a neutral value; tests still pass." >&2
fi
if ! python -m textblob.download_corpora; then
  echo "WARN: could not download TextBlob corpora." >&2
fi
