# CATS Architecture

## Pipeline Overview

```
Client (HTTPS + API key)
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
    │       ├─ Phase 5: compute_gaming()        TTR + burst + repetition
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
- Anomaly = gap > threshold (`signals/silence.py:SOURCE_TYPE_THRESHOLDS`, per
  source type; currently 72 h for every type — changing a value alters signal
  semantics and requires recalibration)
- Score = (anomalies / gaps) × 100

### Gaming
- **TTR** (Type-Token Ratio): vocabulary diversity
- **Repetition**: max bigram frequency normalised over 10
- **Burst**: fraction of intervals < avg/3 (posting bursts)
- **Vocab diversity**: inverse uniqueness for long texts — computed and
  returned (`vocab_score`) but **excluded from `value`**: above the 50-token
  floor it is mathematically identical to TTR (both are `1 - unique/total`),
  which silently double-weighted TTR until fixed 2026-08-26 (see
  `docs/signal_diagnosis_2026-07.md` and `docs/gaming_redesign_2026-08.md`)
- Score = mean of 3 sub-scores (repetition, TTR, burst) × 100

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

**Decision (v1.3.0): `aggregate_score` inverts the negative-polarity signals
(`100 − value` for volatility/silence/gaming) before the weighted mean.** Every
term enters the average as a *reliability contribution*, weights stay
non-negative and interpretable as importances, and `/explain` reports both the
raw `value` and the inverted `reliability_value` per signal
(`cats.scoring.engine.NEGATIVE_POLARITY` / `reliability_value`).

History of this decision:

- **≤ v1.2.x** the engine was a plain non-negative weighted mean that treated
  every signal as "higher = better" — a documented placeholder (WP 4.1). The
  July 2026 calibration runs on real data
  ([calibration_findings_2026-07.md](calibration_findings_2026-07.md)) showed
  the defect was not theoretical: silence — the one informative signal, and
  semantically "higher = worse" — entered the average backwards, so the
  calibrated weights ranked a documented disinformation source **highest** in
  the holdout (Spearman −0.42). The identical calibration with inverted
  negative signals reached holdout Spearman +0.32 and 90% band agreement
  within one band, motivating the change.
- The alternative (**signed weights**) was rejected: it makes the weight
  simplex unbounded, the GA search space larger, and the explanation surface
  ("negative importance") harder to read than an explicit polarity table.

Consequences: scores produced from v1.3.0 onwards are **not comparable** with
scores from earlier versions, and weights calibrated under the old engine are
invalid — recalibrate (see [calibration.md](calibration.md)). The static
matrix above remains an unvalidated starting point: **always calibrate before
relying on scores.**

### Domain-provenance penalty (ENGINE 1.4)

The four behavioural signals read a source's *messages* and are structurally
blind to infrastructure impersonation — clone domains (`spiegel.ltd`,
`bild.pics`) whose content is plausible but whose *domain* is the deception.
A source that publishes on a regular cadence defeats `silence`, the only
strongly informative behavioural signal ([signal_research_2026-07.md](signal_research_2026-07.md)).

**Decision (ENGINE 1.4): domain-provenance is applied as an *asymmetric
penalty*, not a fifth weighted signal.** After the behavioural weighted mean,
`apply_domain_penalty` subtracts `0.6 × domain_red_flag_score` (clamped at 0),
where the red-flag score (0–100) comes from general domain structure only
(rare/cheap TLDs, free-hosting subdomains, edit distance to a fixed brand list —
never the labelled disinfo set). It is computed only when the source URL is
supplied (`context["url"]` / `cats.lite.score(url=…)`), so it is backward
compatible.

Why a penalty and not a weighted signal: a symmetric weighted term would treat a
clean domain (red-flag 0) as maximally reliable and *raise* its score — but most
fake-news lives on ordinary domains scoring 0, so that would wrongly inflate the
low tail. The penalty only ever lowers scores, for impersonation/clone domains.
Coefficient `0.6` validated on the 06-Jul-2026 future holdout: pairwise
concordance **0.755 → 0.775** with every correction landing on a low-reliability
clone (reproduce via `research/validate_domain_penalty.py`). The four calibrated
behavioural weights are unchanged. Scores of sources evaluated with a
red-flagged URL are not comparable with ENGINE 1.3 scores (`/explain` flags the
mismatch).

### Response-time guardrails (risk register R3/R5)

Two blocks accompany every evaluation (`/evaluate` response and `cats.lite`
result). Both are **flags**: they never change the score or the band —
penalising the score itself would change scoring semantics and require the
recalibration cycle. Neither is persisted, so `/explain` does not report them.

- **`language`** (`cats/pipeline/language.py`) — Latin-script check plus an
  Italian function-word ratio (marker set curated against English/French/
  Spanish collisions; 205/205 correct on the July 2026 snapshot registries).
  `detected: "other"` means the Italian-optimised NLP stack is scoring foreign
  text and signal quality is degraded; explanations carry a `language_warning`.
- **`evidence`** (`engine.evidence_summary`) — message count vs
  `CATS_MIN_EVIDENCE_MESSAGES` (default 3). Below the minimum the
  negative-polarity signals cannot fire (0 inverts to a perfect reliability
  contribution), so a near-empty history can aggregate deceptively high;
  `sufficient: false` therefore forces `requires_review`.

## Security Design

| Control | Implementation |
|---|---|
| API authentication | `Authorization: Bearer <key>` with dual-key rotation |
| Rate limiting | Redis sliding-window Lua script, 30 req/min per API key; failed auth attempts limited per client IP |
| Audit storage | AES-256-GCM encrypted JSONB in PostgreSQL |
| IP extraction | Safe `X-Forwarded-For` parsing (first IP only); the bundled nginx **overwrites** the header with the real client address, so clients cannot forge the audited IP |
| Data retention | Nightly APScheduler job; distributed lock via Redis |
| Container | Non-root user; read-only filesystem |
