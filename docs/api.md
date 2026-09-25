# CATS API Reference

Base URL: `https://your-domain/v1/cats`  
Authentication: `Authorization: Bearer <API_KEY>`

**Multi-tenancy:** each API key maps to a tenant (configured server-side via
`CATS_API_KEYS`; unlisted keys use the `default` tenant). Evaluations are stored
per tenant and reads (`/explain`, `/contest`, `/review`, `/stats`) only return
that tenant's data — a trace from another tenant returns `404`.

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
| `source_id` | string | ✅ | 1–256 chars |
| `messages` | array | ✅ | 1–500 messages |
| `messages[].timestamp` | string | ✅ | ISO 8601 (`Z` or offset); anything else is a `422` |
| `messages[].text` | string | ✅ | 1–10 000 chars |
| `messages[].metadata` | object | ❌ | Free-form |
| `context.source_type` | string | ❌ | `social` or `news`; affects weights |

Size, rate and error behaviour for every endpoint: [Limits and errors](#limits-and-errors).

**Response 200**
```json
{
  "trace_id": "550e8400-e29b-41d4-a716-446655440000",
  "score": 72.4,
  "band": "medium_high",
  "requires_review": false,
  "signals": [
    { "name": "coherence", "value": 68.2, "confidence": 0.8, "metadata": {"pairs": 5} },
    { "name": "volatility", "value": 41.0, "confidence": 0.6, "metadata": {"threshold": 0.3} },
    { "name": "silence",    "value": 20.0, "confidence": 0.7, "metadata": {"threshold_h": 96.0, "source_type": "social"} },
    { "name": "gaming",     "value": 15.3, "confidence": 0.9, "metadata": {"token_count": 420} }
  ],
  "language": { "detected": "italian", "confidence": 0.85, "marker_ratio": 0.23, "latin_script_ratio": 1.0 },
  "evidence": { "messages": 12, "min_messages": 3, "sufficient": true, "mean_signal_confidence": 0.75 }
}
```

Two response-time guardrail blocks (both **flags**: they never change `score`
or `band`, and they are not persisted — `/explain` does not report them):

- **`language`** (risk R3) — the NLP stack is Italian-optimised;
  `detected: "other"` means the input does not look Italian and signal quality
  is degraded. Values: `italian` / `other` / `unknown` (insufficient text).
- **`evidence`** (risk R5) — message count vs the configured
  `CATS_MIN_EVIDENCE_MESSAGES` (default 3). Below the minimum,
  `sufficient: false` and `requires_review` is forced `true`: with a
  near-empty history the negative-polarity signals cannot fire, so the raw
  score alone can look deceptively high.

---

## POST /batch

Evaluate multiple sources in a single request. Each item has the same shape as
the `/evaluate` body. All items are scored and persisted atomically (one
transaction); each result carries its own `trace_id`.

**Request**
```json
{
  "items": [
    { "source_id": "twitter:a", "messages": [ ... ], "context": { "source_type": "social" } },
    { "source_id": "news:b",    "messages": [ ... ], "context": { "source_type": "news" } }
  ]
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `items` | array | ✅ | 1–50 evaluation items, each validated like an `/evaluate` body |

The whole request body must also fit the proxy's 2 MB cap (see
[Limits and errors](#limits-and-errors)). Fifty items at the per-item maximum
would be far larger than that, so for big histories send fewer items per call.

**Response 200**
```json
{
  "count": 2,
  "results": [
    { "trace_id": "...", "score": 72.4, "band": "medium_high", "requires_review": false, "signals": [...], "language": {...}, "evidence": {...} },
    { "trace_id": "...", "score": 41.0, "band": "medium",      "requires_review": true,  "signals": [...], "language": {...}, "evidence": {...} }
  ]
}
```

Each item has the same shape as an `/evaluate` response, including the
`language` and `evidence` guardrail blocks.

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
    "signals": [
      {"signal": "coherence", "value": 71.2, "weight": 0.35, "contribution": 24.92,
       "score_share_pct": 41.0, "confidence": 0.8, "metadata": {"pairs": 5}}
    ],
    "primary_driver": "coherence",
    "methodology": "Weighted aggregation of 4 behavioural signals; score_share_pct is each signal's share of the weighted score",
    "disclaimer": "Scores are ordinal rankings of source reliability patterns..."
  }
}
```

`score_share_pct` is each signal's share of the weighted score (a linear-model
attribution), and `primary_driver` is the signal that contributed the most —
both surface *why* a source got its score.

---

## POST /contest/{trace_id}

GDPR Art. 22 — contest an automated decision.

**Request**
```json
{ "reason": "The source was temporarily inactive due to..." }
```
`reason`: 10–2000 chars.

**Response 200**
```json
{ "contest_id": 42, "status": "pending" }
```

---

## POST /contest/{contest_id}/resolve

Close a pending contest (the human decision on a GDPR Art. 22 appeal).
Tenant-scoped; resolving an already-resolved contest returns **409**.

**Request**
```json
{ "status": "upheld", "response": "Re-evaluated with fresh messages; band corrected." }
```
`status` must be `upheld` or `rejected`; `response`: 10–4000 chars.

**Response 200**
```json
{ "contest_id": 42, "status": "upheld", "resolved_at": "2026-07-05T12:00:00+00:00" }
```

---

## GET /stats

Aggregate statistics across all evaluations.

---

## GET /health

Deep health check — returns status of API, Redis, PostgreSQL, NLP model.

---

## GET /metrics

Prometheus exposition format (`text/plain`). Includes HTTP request
count/latency (labelled by route template), `cats_evaluations_total` by band,
and a `cats_trust_score` histogram.

The app serves it **without authentication**, so the bundled nginx proxy does
**not** serve it: a request for `/metrics` through the public entry point gets
`403`. Scrape the app directly on the internal network instead, at
`http://app:8000/metrics` in the bundled `docker-compose.yml`. The app port is
exposed only to the compose network, never published on the host.

Do not replace the `deny all` with an allow-list of private ranges such as
`172.16.0.0/12`. Behind Docker's userland proxy, an external client can reach
nginx with the bridge gateway (`172.x.0.1`) as its source address, so such a
rule would open `/metrics` to everyone. To serve it through nginx for one
scraper, allow that scraper's IP explicitly (see the comment in
`deploy/nginx.conf`).

---

## Limits and errors

These are enforced by the request schemas (`cats/api/schemas.py`), the auth
layer (`cats/core/security.py`) and the bundled proxy (`deploy/nginx.conf`).

**Request size**

| Limit | Value | Where | On violation |
|---|---|---|---|
| Request body | 2 MB | nginx `client_max_body_size` | `413` |
| `source_id` | 1–256 chars | schema | `422` |
| `messages` per evaluation | 1–500 | schema | `422` |
| `messages[].text` | 1–10 000 chars | schema | `422` |
| `messages[].timestamp` | ISO 8601 | schema | `422` |
| `items` per `/batch` | 1–50 | schema | `422` |
| Contest `reason` | 10–2000 chars | schema | `422` |
| Resolve `response` | 10–4000 chars | schema | `422` |

The 2 MB body cap is set only in nginx. The app itself does not cap the body,
which is one more reason never to publish the app port directly.

**Rate limits** (both answer `429`)

| Layer | Limit | Keyed by |
|---|---|---|
| nginx | 30 requests/min, burst 10 | client IP |
| app (Redis sliding window) | `REDIS_RATE_LIMIT_MAX` requests per `REDIS_RATE_LIMIT_WINDOW_SECONDS` (default 30 per 60 s) | API key (hashed); failed authentications separately by client IP |

**Status codes**

| Code | When |
|---|---|
| `401` | Missing or invalid API key |
| `404` | Unknown `trace_id` or contest, or one that belongs to another tenant |
| `409` | Resolving a contest that is already resolved |
| `413` | Body over 2 MB (from nginx, before the app sees it) |
| `422` | Schema validation failed. The body is an RFC 7807 problem document, whose `detail` lists the failing fields |
| `429` | Rate limit exceeded (nginx or app) |
| `500` | Unexpected error. RFC 7807 body with a generic `detail`; the cause is only logged server-side |

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

---

## Library: scoring from a feed

Everything above is the FastAPI deployment. For research, notebooks or quick
evaluation, `cats.lite` runs the same signal pipeline with no database, Redis
or API key — see the module docstring for `score(messages, ...)`.

`score_feed(url)` goes one step further: given just a source's URL, it fetches
its RSS/Atom feed and scores it directly, without building the `messages` list
by hand.

```python
from cats.lite import score_feed

result = score_feed("https://example-news-outlet.it", source_type="news")
print(result["trust_score"], result["band"])
print(result["source"])  # feed_url, message count, time span, how it was found
```

If `url` is not itself a feed, `score_feed` tries autodiscovery in order:
1. the page's `<link rel="alternate" type="application/rss+xml|atom+xml">` tags,
2. well-known paths (`/feed`, `/rss`, `/feed.xml`, `/rss.xml`, `/atom.xml`, `/index.xml`).

`FeedNotFoundError` is raised if the host answers but no feed is found;
`FeedFetchError` if the host (and every candidate path) is unreachable. As
with `score()`, `ValueError` is raised if the feed yields zero usable
messages after normalisation. The domain-provenance penalty (see
[architecture.md](architecture.md#domain-provenance-penalty-engine-14)) is
applied against the source `url`, not the feed URL.

`score_feed` accepts an injectable `client: httpx.Client` — useful for tests,
or to reuse a client with custom headers/proxies across calls — plus
`max_messages`, `timeout`, and any `score()` keyword argument
(`weights`, `explain`, `load_nlp`, …).
