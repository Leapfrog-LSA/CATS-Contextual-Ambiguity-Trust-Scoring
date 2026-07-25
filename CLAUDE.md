# CLAUDE.md

Operational rules for Claude Code sessions on this repo. Complements
`CONTRIBUTING.md` (human workflow) and `docs/cloud_setup.md` (cloud sessions) —
read those for detail; this file is the short list of things that are easy to
get wrong.

## What CATS is

Trust-intelligence scoring for OSINT sources: four behavioural **signals**
(`coherence`, `volatility`, `silence`, `gaming`) computed from a source's
message history, inverted onto a reliability axis, and combined by a weighted
mean into an ordinal trust score + band. Two surfaces share the same signal
code: the `cats.lite` / `cats.calibration` library and the FastAPI deployment.

## Tests and lint must pass before every commit

- **Lint (exactly as CI, `make lint`):** `black --check cats/ tests/` (line 120),
  `isort --check-only`, `flake8 … --max-line-length=120 --extend-ignore=E203,W503`,
  `mypy cats/ --ignore-missing-imports --no-strict-optional`. `make format` fixes
  black+isort.
- **Test env vars: the trap is setting them *wrong*, not leaving them unset.**
  `cats.core.config.Settings` has no defaults for `CATS_API_KEY`, `DATABASE_URL`,
  `REDIS_URL`, `AUDIT_ENCRYPTION_KEY`, but every test module that imports it
  supplies its own via `os.environ.setdefault` — so with **no env vars at all**
  `pytest` collects the full suite (225) and `tests/unit/` passes 208/208.
  Because it is `setdefault`, an exported variable *wins over* the test's value:
  a `DATABASE_URL` missing the `+asyncpg` driver (plain `postgresql://…`)
  overrides the test's own and fails at collection demanding `psycopg2`, which
  this project does not use. So either export nothing, or copy the CI `test`-job
  values verbatim — `.github/workflows/ci.yml` / `docs/cloud_setup.md`.
- `tests/integration/` needs live Postgres + Redis (`make docker-up`; in a cloud
  session start them with `service postgresql start` / `service redis-server start`
  + `alembic upgrade head`).
- Fresh/cloud session setup: **`docs/cloud_setup.md`**.

## Signal & scoring invariants (easy to break)

- Signal roster lives in `SIGNAL_NAMES` (`cats/calibration/dataset.py`).
- **Polarity:** higher-is-worse signals (`volatility`, `silence`, `gaming`) are
  inverted (`100 − value`) in `aggregate_score` before the weighted mean. Do not
  reintroduce backwards aggregation — that bug (fixed in 1.3.0) ranked a known
  disinformation source *highest*.
- **Weights sum to ~1.0** and are renormalised in `cats/scoring/weights.py`; the
  calibrated production table is `data/calibrated_weights.json` (`CATS_WEIGHTS_FILE`).
- **Domain-provenance is a penalty, not a weighted signal.** It is *not* in
  `SIGNAL_NAMES` and *not* calibrated. `apply_domain_penalty` subtracts
  `0.6 × domain_red_flag` after the weighted mean (ENGINE 1.4), only ever
  lowering a clone/impersonation domain's score. Do not add it to `SIGNAL_NAMES`
  or the weight table — a symmetric weighted term would reward clean domains and
  inflate the low tail. See `docs/architecture.md` → *Domain-provenance penalty*.
- **Changing band semantics requires recalibration + re-validation.** Adding or
  removing a signal, or changing thresholds (band cutoffs 80/60/40/20, silence
  72 h in `signals/silence.py`), invalidates the calibrated weights. Recalibrate
  (`python -m cats.calibration`) and re-validate on the **future holdout**; never
  ship such a change without it.
- **Leakage discipline:** never score from the labelled disinfo set
  (`data/disinfo_sources.csv`). Score from general structure so signals
  generalise to unseen sources, or the validation numbers become circular.
- Adding a signal: follow the checklist in `CONTRIBUTING.md` → *Adding a new
  signal* (`types.py`, `evaluate.py`, `weights.py`, tests).

## NLP is Italian-optimised, and degrades gracefully

Default NER uses spaCy `it_core_news_lg`. If the model is missing, NER coherence
returns a **neutral, zero-confidence** value — do not make it crash. Optional
`sbert`/`bert` backends must fall back to NER/TextBlob when their deps or model
weights are unavailable.

## Config & logging

All configuration goes through `cats/core/config.py` (pydantic-settings). Use
`structlog`; never `print()`. Every signal returns a `SignalResult` subtype.

## Versioning & releases

- Bump the version in **both** `pyproject.toml` and `cats/__init__.py` (they must
  match; the API reports `cats.__version__`).
- Keep `CHANGELOG.md`: log under `[Unreleased]`, then cut a dated version section
  on release.
- **PyPI publish is automatic on a GitHub Release** (`release.yml`, trusted
  publishing/OIDC). Creating the Release publishes — treat it as an outward,
  hard-to-reverse action that needs explicit maintainer confirmation.

## Git workflow for sessions

- One task = one **descriptive** branch = one PR. PRs target the default branch
  `main` (CI runs on PRs to `main`).
- Don't stack new commits on a branch whose PR already merged — branch fresh from
  `main`.

## Compliance — never fabricate

`docs/eu_ai_act/` contains deliberate **human/legal TODOs** (the high-risk
determination, risk-owner, sign-offs, data-governance methodology). Do not invent
legal determinations or fill in sign-offs — flag them for a human. Keep the WP
4.1/4.3 disclaimers: scores are **ordinal**, not calibrated probabilities.
