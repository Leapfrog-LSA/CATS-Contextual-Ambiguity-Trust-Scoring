# Changelog

All notable changes to CATS are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-03-06

### Added
- 4-signal scoring pipeline: coherence, volatility, silence, gaming
- FastAPI REST API with 9-phase evaluation pipeline
- GDPR Art. 13–22 endpoints: `/explain`, `/contest`, `/review`
- AES-256-GCM encrypted audit log (PostgreSQL)
- Redis sliding-window rate limiting (Lua, 30 req/min)
- JWT RS256 authentication with dual API-key rotation
- APScheduler nightly audit purge with distributed Redis lock
- Docker multi-stage build with non-root user
- GitHub Actions CI: lint, unit tests, integration tests, Docker build
- spaCy `it_core_news_lg` for Italian NER
- RFC 7807 Problem Details error responses
- Deep `/health` endpoint (API + Redis + PostgreSQL + NLP)
- WP 4.1/4.3 compliance disclaimer on all explanation responses
- Dynamic weight matrix by source type (social/news)

### Known Limitations
- NLP accuracy ~55–62% (rule-based; see WP 4.1)
- Parameters not empirically calibrated
- Italian-only NLP pipeline

---

## [Unreleased] — v2.0 (2027)

### Planned
- Empirical calibration on a labelled dataset (target AUC-ROC ≥ 0.78)
- Full EU AI Act Annex IX documentation

---

## [1.3.1] — 2026-07-05

### Fixed
- **`CATS_WEIGHTS_FILE` and `CATS_API_KEYS` were silently ignored** — the
  settings fields only matched the bare `WEIGHTS_FILE`/`API_KEYS` names, so
  calibrated weights and multi-tenant keys configured as documented never
  loaded. Both documented spellings are now accepted (validation aliases).
- Gaming: corpora under 50 tokens no longer receive a spurious maximum
  vocabulary-uniformity sub-score (+25 points); the sub-score is neutral (0).
- `/health` no longer returns raw exception strings (could leak DSNs/internal
  hostnames on an unauthenticated endpoint); details are logged instead.
  The payload now includes the running version.
- Audit purge uses a single `DELETE` statement instead of loading and deleting
  expired rows one by one.
- API version string was hardcoded at 1.2.0; now read from `cats.__version__`.

### Added
- `POST /v1/cats/contest/{contest_id}/resolve` — close a pending contest
  (`upheld`/`rejected` + response, tenant-scoped, audit-logged): the GDPR
  Art. 22 appeal flow now has its human-decision endpoint. Migration `003`
  adds `trust_scores.engine_version`.
- `/explain` flags rows scored under an older aggregation engine
  (`engine_mismatch`) instead of silently re-decomposing them with current
  semantics.
- `TRUST_PROXY_HEADERS` setting: `X-Forwarded-For` is honoured only when
  enabled (default true, matching the bundled nginx); rate limiting is now
  keyed per API key (hashed) instead of per client IP.
- Per-source-type silence thresholds table
  (`signals/silence.py:SOURCE_TYPE_THRESHOLDS`; all defaults remain 72 h —
  changing values requires recalibration).
- Docker image now downloads the TextBlob corpora (world-readable
  `NLTK_DATA`), so container sentiment matches `make nlp-download` installs.

### Removed
- Unused JWT machinery (`create_access_token`/`verify_token`/`init_jwt_keys`)
  and the `python-jose` dependency: no route ever consumed tokens — auth is
  API-key based. `cryptography` unpinned to `<50`.

---

## [1.3.0] — 2026-07-05

### Added
- **`cats.lite`** — zero-infrastructure scoring: `from cats.lite import score`
  runs the 4-signal pipeline + aggregation as a plain library call (no
  PostgreSQL, no Redis, no API keys). Same signals, same explainability,
  same caveats as `/evaluate`.
- `CITATION.cff` for academic citation.
- PyPI-ready packaging: the project builds as **`cats-scoring`** with the
  library-surface dependencies only (`pip install cats-scoring[sbert]` for the
  multilingual coherence backend); the API deployment stack stays in
  `requirements.txt`. Colab demo notebook in `examples/cats_lite_demo.ipynb`.

### Changed
- **Signal polarity fix in `aggregate_score`** — the higher-is-worse signals
  (volatility, silence, gaming) are now inverted (`100 − value`) before the
  weighted average, so every signal enters the score as a reliability
  contribution. On ≤ 1.2.x the one empirically informative signal (silence)
  entered the average backwards, making calibrated weights rank a documented
  disinformation source *highest* on the July 2026 holdout (Spearman −0.42 →
  +0.32 with the fix; band agreement 0% → 90% within one band). See
  `docs/calibration_findings_2026-07.md` and the updated design decision in
  `docs/architecture.md`.
- `/explain` signal details now include `polarity` and `reliability_value`
  (the inverted value actually aggregated); `contribution`/`score_share_pct`
  are computed on the reliability axis so they decompose the real score.

### Breaking
- Trust scores are **not comparable** with scores produced by ≤ 1.2.x.
- Weights calibrated under the pre-1.3 engine are invalid — recalibrate with
  `python -m cats.calibration` (recalibrated weights for the July 2026
  snapshots ship in `data/calibrated_weights.json`).

---

## [1.2.0] — 2026-06-29

### Added
- Optional Sentence-BERT coherence backend (`COHERENCE_BACKEND=sbert`, model via
  `COHERENCE_MODEL`): mean cosine similarity of consecutive message embeddings.
  `sentence-transformers` is optional (`requirements-sbert.txt`); falls back to
  the spaCy NER backend when unavailable, so the default stays light.
- Per-signal attribution in `/explain`: `score_share_pct` (each signal's share
  of the weighted score) and `primary_driver` — a dependency-free, SHAP-style
  breakdown of *why* a source got its score.

---

## [1.1.0] — 2026-06-29

### Added
- Optional BERT Italian sentiment backend for the volatility signal
  (`SENTIMENT_BACKEND=bert`, model configurable via `SENTIMENT_MODEL`).
  `transformers`/`torch` are optional (`requirements-bert.txt`); the backend
  falls back to TextBlob when they are unavailable, so the default stays light.
- Row-level multi-tenancy: a `tenant_id` (bound to the API key via the optional
  `CATS_API_KEYS` "key:tenant" map, never client-supplied) is stored on every
  `TrustScore` / `AuditLog` / `Contest`, and all reads (`/explain`, `/contest`,
  `/review`, `/stats`) are scoped to the caller's tenant. Backwards compatible:
  unlisted keys resolve to the `default` tenant. Migration `002`.
- `POST /v1/cats/batch` endpoint: evaluate multiple sources in one request
  (1–50 items), persisted atomically in a single transaction.
- Prometheus metrics at `GET /metrics` (`prometheus-client`): HTTP request
  count/latency (labelled by route template) plus `cats_evaluations_total`
  (by band) and a `cats_trust_score` histogram.
- nginx reverse-proxy config (`deploy/nginx.conf`) wired into `docker-compose`:
  per-IP rate limiting (30 req/min), security headers, correct
  `X-Forwarded-For`, and a documented TLS 1.3 server block.
- Weight calibration toolkit (`cats.calibration`): dependency-free genetic
  search that tunes per-source-type signal weights against a labelled dataset,
  optimising rank-agreement (Spearman / pairwise concordance). Calibrated
  weights are served via the `CATS_WEIGHTS_FILE` setting. See
  [docs/calibration.md](docs/calibration.md). GA design inspired by
  SantanderAI/genetic-algorithm (Apache-2.0).

### Fixed
- `compute_coherence` no longer crashes when the spaCy model is not loaded
  (`nlp is None`): it degrades gracefully to a neutral, zero-confidence signal,
  consistent with `/health` reporting `nlp: not_loaded`.
- CI is green again: applied black/isort across the codebase and fixed the
  remaining flake8/mypy errors plus structlog-config and test-isolation bugs
  that had been failing every run.
