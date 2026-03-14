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

### Planned
- BERT-based Italian sentiment (replace TextBlob)
- PostgreSQL multi-tenant support
- Prometheus metrics integration
- `/v1/cats/batch` endpoint
