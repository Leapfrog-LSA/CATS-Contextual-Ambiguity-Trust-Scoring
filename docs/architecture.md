# CATS Architecture

## Pipeline Overview

```
Client (HTTPS + JWT/API-Key)
    │
nginx (TLS 1.3 · rate 30 req/min per IP)
    │
FastAPI (async, Python 3.11)
    │
    ├─ POST /v1/cats/evaluate
    │       │
    │       ├─ Phase 1: normalize_messages()    validate · sort UTC · dedup
    │       ├─ Phase 2: compute_coherence()     spaCy NER + Jaccard similarity
    │       ├─ Phase 3: compute_volatility()    TextBlob sentiment spike detection
    │       ├─ Phase 4: compute_silence()       temporal gap analysis
    │       ├─ Phase 5: compute_gaming()        TTR + burst + repetition + vocab
    │       ├─ Phase 6: get_dynamic_weights()   context-aware weight selection
    │       ├─ Phase 7: aggregate_score()       weighted mean
    │       ├─ Phase 8: determine_band()        score → ordinal band
    │       └─ Phase 9: log_evaluation()        AES-256-GCM audit log
    │
    ├─ GET  /v1/cats/explain/{trace_id}  GDPR Art.14/22
    ├─ POST /v1/cats/contest/{trace_id}  GDPR Art.22
    ├─ POST /v1/cats/review/{trace_id}
    └─ GET  /v1/cats/stats
                │              │
            Redis 7         PostgreSQL 16
        (rate limiting)   (trust_scores, audit_logs, contests)
                          + APScheduler nightly purge (GDPR Art.5)
```

## Signal Details

### Coherence
- Extracts named entities (PER, ORG, GPE, LOC) via spaCy `it_core_news_lg`
- Computes Jaccard similarity between consecutive messages
- Score = average overlap × 100

### Volatility
- TextBlob polarity per message with Italian negation correction
- Counts spikes where |Δsentiment| > 0.4 between consecutive messages
- Score = (spikes / pairs) × 100

### Silence
- Sorts message timestamps; computes inter-message gaps in hours
- Anomaly = gap > threshold (default 72 h, configurable per source type)
- Score = (anomalies / gaps) × 100

### Gaming
- **TTR** (Type-Token Ratio): vocabulary diversity
- **Repetition**: max bigram frequency normalised over 10
- **Burst**: fraction of intervals < avg/3 (posting bursts)
- **Vocab diversity**: inverse uniqueness for long texts
- Score = mean of 4 sub-scores × 100

## Weight Matrix

| Source type | coherence | volatility | silence | gaming |
|---|---|---|---|---|
| `social` | 0.25 | **0.30** | 0.20 | 0.25 |
| `news` | **0.35** | 0.20 | 0.25 | 0.20 |
| default | 0.30 | 0.25 | 0.25 | 0.20 |

## Signal Polarity & Scoring (design decision)

The four signals **do not share a common polarity**:

| Signal | Direction | Higher value means |
|---|---|---|
| coherence | positive | more consistent → *more* reliable |
| volatility | **negative** | more tone swings → *less* reliable |
| silence | **negative** | more anomalous gaps → *less* reliable |
| gaming | **negative** | more manipulation signs → *less* reliable |

`aggregate_score` (Phase 7) is a **non-negative weighted mean**, so it treats
every signal as "higher = better". Because the weights cannot be negative, the
aggregation **cannot invert** the three negative-polarity signals. Two
consequences follow:

1. **The static weight matrix above is a placeholder, not a validated baseline**
   (WP 4.1). On data where the negative-polarity signals carry the signal,
   reliable ranking depends almost entirely on calibration loading weight onto
   coherence. The eval harness makes this measurable: on
   `examples/calibration_sample.jsonl` the static weights score Spearman
   **−0.89** (anti-correlated) versus **+0.99** after calibration — see
   [calibration.md](calibration.md).
2. A weighted mean of mixed-polarity signals is **not** a faithful reliability
   model on its own; it leans on calibration to approximate the right ordering.

**Decision (current iteration): keep the engine as-is and document the
limitation; do not change scoring semantics now.** Options deliberately *not*
taken yet:

- **Invert negative signals before aggregation** (e.g. use `100 − value` for
  volatility/silence/gaming), making all signals positive-polarity and the
  weights interpretable as importance.
- **Allow signed weights** so the aggregation can encode polarity directly.

Both alter scoring semantics and band thresholds and would need re-validation on
labelled data, so they are deferred to the NLP/scoring hardening on the roadmap
(v2.0). Until then, **always calibrate before relying on scores**, and treat the
static weights as an unvalidated starting point.

## Security Design

| Control | Implementation |
|---|---|
| API authentication | `Authorization: Bearer <key>` with dual-key rotation |
| Rate limiting | Redis sliding-window Lua script, 30 req/min per IP |
| Audit storage | AES-256-GCM encrypted JSONB in PostgreSQL |
| JWT | RS256 with ephemeral keypair per process startup |
| IP extraction | Safe `X-Forwarded-For` parsing (first IP only) |
| Data retention | Nightly APScheduler job; distributed lock via Redis |
| Container | Non-root user; read-only filesystem |
