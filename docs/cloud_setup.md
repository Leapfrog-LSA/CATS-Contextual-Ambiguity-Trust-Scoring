# Running CATS on Claude Code for the web

This guide configures a [Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web)
cloud environment so linters and the test suite run in a fresh session, and the
Italian NLP assets CATS depends on are available.

Two mechanisms install dependencies in a cloud session. They overlap, so pick
per the trade-off below rather than running both blindly:

| | **Setup script** | **SessionStart hook** |
| --- | --- | --- |
| Attached to | The cloud environment (UI field) | The repo (`.claude/settings.json`) |
| Runs | Before Claude launches, **only when the environment cache is cold** | After Claude launches, on **every** session incl. resume |
| Cached | **Yes** — filesystem snapshot; installs run once | No — re-runs each session (adds startup latency) |
| Scope | Cloud only | Local **and** cloud |

CATS pulls heavy dependencies (spaCy + models, optionally torch), so the
**setup script is the primary mechanism** — environment caching means it runs
once and later sessions start fast. This repo also ships a cloud-only
`SessionStart` hook (`.claude/hooks/session-start.sh`) as a version-controlled
fallback; it is idempotent, so with a warm cache it only re-checks.

## 1. Setup script

Paste into the environment's **Setup script** field
(*environment selector → settings → Setup script*).

```bash
#!/bin/bash
# CATS — setup script for Claude Code on the web. Runs once, then cached.
# NOT `set -e`: non-critical downloads use `|| true` so one flaky fetch never
# blocks the session. Keep total runtime under ~5 min so the cache can build.
set -uo pipefail

# --- Core (required): package + dev/test stack + Italian NLP ---------------
# requirements-dev.txt pulls in requirements.txt (FastAPI/SQLAlchemy/... for the
# integration tests) plus the linters and pytest. If the base image's pip is
# "externally managed" and errors, add --break-system-packages here.
#
# --ignore-installed PyJWT: the base image ships a Debian-packaged PyJWT with no
# RECORD file. pip cannot uninstall it to satisfy the resolved version and
# aborts the whole install ("Cannot uninstall PyJWT 2.7.0, RECORD file not
# found"), so without the flag nothing gets installed at all.
pip install --ignore-installed PyJWT -e . -r requirements-dev.txt

# Fail loudly: a setup script that "succeeded" with no pytest wastes a session.
python -c "import pytest, cats" || echo "SETUP FAILED: dev/test stack missing — read the pip output above."

# spaCy Italian model — served from github.com (in the default "Trusted"
# allowlist). Powers the default NER coherence backend. Non-fatal: without it
# NER coherence degrades to a neutral value and the test suite still passes.
python -m spacy download it_core_news_lg || true

# TextBlob corpora — back the volatility sentiment signal.
python -m textblob.download_corpora || true

# --- Optional heavy backends (uncomment to enable) -------------------------
# SBERT coherence (COHERENCE_BACKEND=sbert) and/or BERT sentiment
# (SENTIMENT_BACKEND=bert). torch/transformers come from PyPI, but the MODEL
# WEIGHTS download from huggingface.co at first use — requires a Custom network
# allowlist with huggingface.co + cdn-lfs.huggingface.co, else these fall back
# to NER / TextBlob. Installed in parallel to stay under the ~5-min cache limit.
#
# pip install -r requirements-sbert.txt &
# pip install -r requirements-bert.txt &
# wait
# python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')" || true
# python -c "from transformers import pipeline; pipeline('sentiment-analysis', model='neuraly/bert-base-italian-cased-sentiment')" || true
```

> The optional editable extras are `[sbert]` and `[bert]` only — there is **no**
> `[dev]` extra. Dev/test tools live in `requirements-dev.txt`, so install with
> `pip install -e . -r requirements-dev.txt`, not `pip install -e ".[dev]"`.

## 2. Environment variables

Paste into the environment's **Environment variables** field (`.env` format,
one `KEY=value` per line, no quotes). These mirror the `test` job in
`.github/workflows/ci.yml` — throwaway test values, **not secrets** (the env
field is visible to anyone who can edit the environment, so never put real
secrets here).

Copy them **verbatim**. `cats.core.config.Settings` has no defaults for these,
but the test modules that import it fall back to their own via
`os.environ.setdefault`, so leaving them unset is harmless — the full suite
still collects and `tests/unit/` still passes. `setdefault` also means an
exported variable *overrides* the test's, which is where the damage comes from:
a `DATABASE_URL` without the `+asyncpg` driver (plain `postgresql://…`) sends
SQLAlchemy looking for the synchronous `psycopg2`, which this project does not
depend on, and collection dies on a `ModuleNotFoundError` that looks like a
missing dependency rather than a bad URL.

```
ENVIRONMENT=test
CATS_API_KEY=test-api-key
DATABASE_URL=postgresql+asyncpg://cats:cats@localhost:5432/cats_test
REDIS_URL=redis://localhost:6379/0
AUDIT_ENCRYPTION_KEY=dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTAwMzI=
```

The **unit** suite (`pytest tests/unit/`) runs with just these. The
**integration** suite needs live services: Postgres 16 and Redis 7 are
pre-installed but not running, so per session ask Claude to start them and
migrate before `pytest tests/integration/`:

```bash
service postgresql start
service redis-server start
alembic upgrade head
```

(Services started in the setup script do **not** carry over — the cache stores
files, not running processes.)

## 3. Network access

Network access is per environment. The default **Trusted** level allows package
registries plus `github.com` and its release-asset hosts (`objects.` /
`release-assets.githubusercontent.com`, `codeload.github.com`,
`raw.githubusercontent.com`), so the spaCy model download works without any
custom domains.

| Work | Level | Add to allowlist |
| --- | --- | --- |
| Diagnostics / integration on repo-local data | **Trusted** (default) | — (PyPI + github already covered) |
| SBERT / BERT backends | **Custom** (+ defaults) | `huggingface.co`, `cdn-lfs.huggingface.co` |
| External dataset / RSS collection (e.g. MBFC, EUvsDisinfo, feeds) | **Full**, or **Custom** with each feed host | e.g. `mediabiasfactcheck.com`, `euvsdisinfo.eu`, plus every RSS host in `data/labels.jsonl` |

Tasks that fetch from arbitrary news domains fail silently under **Trusted**.
For dataset/RSS collection, either switch to **Full** for those runs or list the
specific hosts under **Custom**; then return to **Trusted** for everything else.

> **Measured 2026-07-25 — this table is stricter than observed behaviour.**
> From a default cloud environment with no custom allowlist, both the SBERT
> model (`huggingface.co`) and arbitrary news domains were reachable: 98 of the
> 115 registered RSS feeds answered normally. Before assuming a network level
> is the blocker, test the specific host — the same over-strict assumption about
> `github.com` cost a session on 2026-07-23 (see
> `docs/dataset_expansion_runbook.md`).
>
> The 15 feeds that do **not** answer are blocked by the destinations' own WAFs
> on datacenter IP reputation, not by our egress policy, so no network level
> here changes them — that needs a different egress IP
> (`docs/feed_health_2026-07.md`, round 7).

## Notes

- One task = one session = one branch/PR. Push local commits before
  `claude --cloud`, since the VM clones from GitHub, not your machine.
- The git proxy restricts pushes to the current working branch.
- CLI session handoff is one-way: `--teleport` pulls a cloud session into your
  terminal; `--cloud` starts a new one. Pushing a local session to the web is
  only available from the Desktop app.
- Cloud sessions share your account's rate limits; parallel tasks consume more.
