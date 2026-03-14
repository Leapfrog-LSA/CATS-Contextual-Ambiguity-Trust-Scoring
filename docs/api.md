# CATS API Reference

Base URL: `https://your-domain/v1/cats`  
Authentication: `Authorization: Bearer <API_KEY>`

---

## POST /evaluate

Compute the trust score for a source.

**Request**
```json
{
  "source_id": "twitter:account_handle",
  "messages": [
    { "timestamp": "2026-01-01T10:00:00Z", "text": "..." },
    { "timestamp": "2026-01-01T14:00:00Z", "text": "..." }
  ],
  "context": { "source_type": "social" }
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `source_id` | string | ✅ | Max 256 chars |
| `messages` | array | ✅ | Min 1 message; ISO 8601 timestamps |
| `context.source_type` | string | ❌ | `social` or `news`; affects weights |

**Response 200**
```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "score": 72.4,
  "band": "medium_high",
  "requires_review": false,
  "signals": [
    { "name": "coherence", "value": 68.2, "confidence": 0.8, "metadata": {"pairs": 5} },
    { "name": "volatility", "value": 41.0, "confidence": 0.6, "metadata": {"threshold": 0.4} },
    { "name": "silence",    "value": 20.0, "confidence": 0.7, "metadata": {"threshold_h": 72} },
    { "name": "gaming",     "value": 15.3, "confidence": 0.9, "metadata": {"token_count": 420} }
  ]
}
```

---

## GET /explain/{trace_id}

GDPR Art. 14/22 — explainability endpoint.

**Response 200**
```json
{
  "trace_id": "550e8400-...",
  "explanation": {
    "trust_score": 72.4,
    "band": "medium_high",
    "signals": [...],
    "methodology": "Weighted aggregation of 4 behavioural signals",
    "disclaimer": "Scores are ordinal rankings of source reliability patterns..."
  }
}
```

---

## POST /contest/{trace_id}

GDPR Art. 22 — contest an automated decision.

**Request**
```json
{ "reason": "The source was temporarily inactive due to..." }
```

**Response 200**
```json
{ "contest_id": 42, "status": "pending" }
```

---

## GET /stats

Aggregate statistics across all evaluations.

---

## GET /health

Deep health check — returns status of API, Redis, PostgreSQL, NLP model.

---

## Score Bands

| Score | Band | Recommended action |
|---|---|---|
| 80–100 | `high` | Usable for OSINT |
| 60–79  | `medium_high` | Cross-validate key claims |
| 40–59  | `medium` | Human review recommended |
| 20–39  | `low` | Human review required |
| 0–19   | `very_low` | Do not use without validation |

> **Note**: scores are ordinal rankings, not absolute probabilities (WP 4.3).
