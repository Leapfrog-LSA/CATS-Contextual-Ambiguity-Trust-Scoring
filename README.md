# CATS — Contextual Ambiguity & Trust Scoring

> **Trust intelligence for OSINT sources — not fact-checking, but source reliability over time.**

[![CI](https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring/actions/workflows/ci.yml/badge.svg)](https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring/actions)
[![Coverage](https://codecov.io/gh/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring/branch/main/graph/badge.svg)](https://codecov.io/gh/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GDPR Compliant](https://img.shields.io/badge/GDPR-Art.13--22-blue)](docs/compliance.md)
[![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-documented-blue)](docs/compliance.md)

---

## What is CATS?

| ❌ Fact-checking | ✅ CATS |
|---|---|
| "Is this information true?" | **"How reliable is this source, in this context, right now?"** |

CATS analyses the *behavioural patterns* of a source over time — narrative consistency, sentiment volatility, temporal gaps, and signs of algorithmic manipulation — and returns a transparent, explainable trust score.

---

## Signals

| Signal | What it measures | Method |
|---|---|---|
| **Coherence** | Entity/argument consistency across messages | spaCy NER + Jaccard (or optional Sentence-BERT) similarity |
| **Volatility** | Abrupt narrative tone changes | TextBlob (or optional BERT) sentiment spike detection |
| **Silence** | Anomalous temporal gaps in publishing | Gap analysis vs. source-type thresholds |
| **Gaming** | Signs of algorithmic manipulation | Repetition + TTR + burst + vocab diversity |

---

## Quick Start

```bash
# 1. Clone and configure
git clone https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring.git && cd CATS-Contextual-Ambiguity-Trust-Scoring
cp .env.example .env          # fill in secrets (see .env.example)

# 2. Install
make dev-install              # deps + pre-commit hooks
make nlp-download             # spaCy it_core_news_lg + TextBlob corpora

# 3. Start services and run
make docker-up                # PostgreSQL 16 + Redis 7
make db-migrate               # Alembic migrations
uvicorn cats.api.main:app --reload

# 4. Test
make test
```

> **Generate a secure AUDIT_ENCRYPTION_KEY**: `make generate-key`

---

## API Example

```bash
curl -s -X POST http://localhost:8000/v1/cats/evaluate \
  -H "Authorization: Bearer $CATS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "source_id": "twitter:example_handle",
    "messages": [
      {"timestamp": "2026-01-01T08:00:00Z", "text": "Governo annuncia piano economico."},
      {"timestamp": "2026-01-01T09:00:00Z", "text": "Protesta dei lavoratori in piazza."},
      {"timestamp": "2026-01-01T10:00:00Z", "text": "Parlamento discute la legge di bilancio."}
    ],
    "context": {"source_type": "social"}
  }' | jq
```

```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "score": 68.4,
  "band": "medium_high",
  "requires_review": false,
  "signals": [
    {"name": "coherence",  "value": 71.2, "confidence": 0.3},
    {"name": "volatility", "value": 55.0, "confidence": 0.15},
    {"name": "silence",    "value": 0.0,  "confidence": 0.1},
    {"name": "gaming",     "value": 12.8, "confidence": 0.06}
  ]
}
```

---

## Trust Score Bands

| Score | Band | Recommended Action |
|---|---|---|
| 80–100 | `high` | Usable for OSINT |
| 60–79  | `medium_high` | Cross-validate key claims |
| 40–59  | `medium` | Human review recommended |
| 20–39  | `low` | Human review required |
| 0–19   | `very_low` | Do not use without validation |

> ⚠️ Scores are **ordinal rankings**, not absolute probabilities (WP 4.3).

---

## Architecture

![CATS — 9-phase OSINT evaluation pipeline](CATS%20SCHEME.png)

```
Client (HTTPS + Bearer token)
        │
   nginx (TLS 1.3 · rate 30 req/min)
        │
   FastAPI — 9-phase pipeline
   ├─ POST /v1/cats/evaluate
   ├─ POST /v1/cats/batch                ← evaluate up to 50 sources at once
   ├─ GET  /v1/cats/explain/{trace_id}   ← GDPR Art.14/22
   ├─ POST /v1/cats/contest/{trace_id}   ← GDPR Art.22
   ├─ GET  /v1/cats/stats
   └─ GET  /health  /metrics
        │                │
     Redis 7          PostgreSQL 16
  (rate limiting)   (AES-256 audit log)
                    + APScheduler purge
```

The nginx reverse proxy (TLS, rate limiting, security headers) is configured in
[`deploy/nginx.conf`](deploy/nginx.conf) and started by `make docker-up`.

See [docs/architecture.md](docs/architecture.md) for full signal and security details.

---

## Documentation

| Document | Description |
|---|---|
| [docs/api.md](docs/api.md) | Full API reference |
| [docs/architecture.md](docs/architecture.md) | Signal algorithms, weight matrix, security design |
| [docs/compliance.md](docs/compliance.md) | GDPR + EU AI Act compliance |
| [docs/calibration.md](docs/calibration.md) | Empirical weight calibration (genetic search) |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Development guide |
| [SECURITY.md](SECURITY.md) | Vulnerability reporting |

---

## Known Limitations (WP 4.1)

- **NLP accuracy ~55–62% (default)**: spaCy NER + TextBlob; optional BERT sentiment and Sentence-BERT coherence backends are available for higher accuracy (see `.env.example`)
- **Uncalibrated parameters**: thresholds are initial estimates; signal weights can now be empirically tuned with [`cats.calibration`](docs/calibration.md), but band thresholds remain unvalidated
- **Italian-optimised**: using `it_core_news_lg`; other languages degrade accuracy
- **Ordinal scoring only**: not suitable as sole basis for autonomous decisions

---

## Roadmap

| Version | Status | Key features |
|---|---|---|
| **v1.0** | ✅ | spaCy NER · 9-phase pipeline · GDPR API · Docker |
| **v1.1** | ✅ | BERT Italian sentiment · multi-tenant PostgreSQL · batch endpoint · Prometheus `/metrics` · nginx |
| **v1.2** | ✅ | Sentence-BERT coherence · explainer attribution · weight calibration |
| v2.0 | 2027 | AUC-ROC ≥ 0.78 · full EU AI Act Annex IX |

---

## License

[MIT](LICENSE) — technical@cats-system.org
