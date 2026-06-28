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

## [Unreleased] — v1.1 (Q2 2026)

### Added
- Optional Sentence-BERT coherence backend (`COHERENCE_BACKEND=sbert`, model via
  `COHERENCE_MODEL`): mean cosine similarity of consecutive message embeddings.
  `sentence-transformers` is optional (`requirements-sbert.txt`); falls back to
  the spaCy NER backend when unavailable, so the default stays light.
- Optional BERT Italian sentiment backend for the volatility signal
  (`SENTIMENT_BACKEND=bert`, model configurable via `SENTIMENT_MODEL`).
  `transformers`/`torch` are optional (`requirements-bert.txt`); the backend
  falls back to TextBlob when they are unavailable, so the default stays light.
- Row-level multi-tenancy: a `tenant_id` (bound to the API key via the optional
  `CATS_API_KEYS` "key:tenant" map, never client-supplied) is stored on every
  `TrustScore` / `AuditLog` / `Contest`, and all reads (`/explain`, `/contest`,
  `/review`, `/stats`) are scoped to the caller's tenant. Backwards compatible:
  unlisted keys resolve to the `default` tenant. Migration `002`.
- nginx reverse-proxy config (`deploy/nginx.conf`) wired into `docker-compose`:
  per-IP rate limiting (30 req/min), security headers, correct
  `X-Forwarded-For`, and a documented TLS 1.3 server block.
- Prometheus metrics at `GET /metrics` (`prometheus-client`): HTTP request
  count/latency (labelled by route template) plus `cats_evaluations_total`
  (by band) and a `cats_trust_score` histogram.
- `POST /v1/cats/batch` endpoint: evaluate multiple sources in one request
  (1–50 items), persisted atomically in a single transaction.
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

### Planned
- BERT-based Italian sentiment (replace TextBlob)
- PostgreSQL multi-tenant support
