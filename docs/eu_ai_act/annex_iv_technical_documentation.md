# CATS — Technical Documentation (Annex IV / Art. 11)

> **Regulation (EU) 2024/1689, Annex IV** — technical documentation referred to
> in Article 11(1). Section headings below follow Annex IV points 1–9.
>
> ⚠️ **Not legal advice.** Pre-filled from the current CATS implementation;
> `TODO` markers flag content requiring provider decisions or empirical data.
> Applicable only if CATS is classified high-risk (see
> [`classification.md`](classification.md)).

| Field | Value |
|---|---|
| System name | CATS — Contextual Ambiguity & Trust Scoring |
| Version covered | 1.2.0 (see [`../../CHANGELOG.md`](../../CHANGELOG.md)) |
| Provider | TODO (legal entity, address, contact) |
| Document owner | TODO |
| Last updated | TODO |

---

## 1. General description of the AI system

**Intended purpose.** CATS produces an **ordinal reliability score (0–100) for
an OSINT *source*** based on the behavioural patterns of its messages over time.
It answers *"how reliable is this source, in this context, right now"* — it is
**not** a fact-checker and does not assess the truth of individual claims.

**What it is *not* / intended-use limits.**
- Scores are **ordinal rankings, not probabilities** (WP 4.3).
- **Not suitable as the sole basis for autonomous decisions** — human oversight
  is required (the `requires_review` flag forces this for low scores).
- Optimised for **Italian** (`it_core_news_lg`); other languages degrade.

**Deployers / users.** TODO (must align with [`classification.md`](classification.md)).

**System form.** Software-only REST API (FastAPI), deployed behind nginx
(TLS 1.3), with PostgreSQL 16 (audit) and Redis 7 (rate limiting). Container
images are non-root.

**Interface (high-level).**
- `POST /v1/cats/evaluate` — score one source from its messages
- `POST /v1/cats/batch` — up to 50 sources at once
- `GET  /v1/cats/explain/{trace_id}` — per-signal breakdown (transparency)
- `POST /v1/cats/contest/{trace_id}` — human contest of a result
- `GET  /v1/cats/stats`, `GET /health`, `GET /metrics`

See [`../api.md`](../api.md) for the full reference.

---

## 2. Detailed description of elements and development process

**Pipeline (9 phases).** Ingest → normalise → four signal extractors →
weighted aggregation → banding → explanation/audit. See
[`../architecture.md`](../architecture.md).

**The four signals.**

| Signal | Measures | Method | Code |
|---|---|---|---|
| Coherence | Entity/argument consistency across messages | spaCy NER + Jaccard, optional Sentence-BERT | `cats/signals/coherence.py` |
| Volatility | Abrupt tone changes | TextBlob, optional BERT sentiment, spike detection | `cats/signals/volatility.py`, `sentiment.py` |
| Silence | Anomalous publishing gaps | Gap analysis vs source-type thresholds | `cats/signals/silence.py` |
| Gaming | Algorithmic-manipulation signs | Repetition + TTR + burst + vocab diversity | `cats/signals/gaming.py` |

**Aggregation & banding.** Weighted linear aggregation of the four signals
(`cats/scoring/engine.py`, weight matrix in `cats/scoring/weights.py`) mapped to
five bands (`very_low … high`). Band thresholds: see README "Trust Score Bands".

**Weights & calibration.** Weights are tunable via genetic-search calibration
on a labelled dataset (`cats/calibration/`, [`../calibration.md`](../calibration.md)),
loadable through `CATS_WEIGHTS_FILE`.

> ⚠️ **Limitation (WP 4.1):** calibration tunes **weights only** — not the
> signal algorithms and not the band thresholds, which remain initial estimates.

**Pre-determined changes.** TODO (any planned automatic updates / continuous
learning — currently none; weights change only via explicit recalibration).

---

## 3. Monitoring, functioning and control

- **Human oversight (Art. 14).** `requires_review` flips true for low scores,
  routing results to mandatory human review; `POST /contest/{trace_id}` lets a
  human formally contest an outcome. See `risk_management_art9.md` and
  [`../compliance.md`](../compliance.md).
- **Expected accuracy.** See §6.
- **Foreseeable unintended outcomes.** Mis-ranking of a source under
  adversarial gaming, language drift (non-Italian), small-sample instability.
  TODO: quantify once validation data exists.

---

## 4. Performance metrics & appropriateness

> TODO: State the metrics that define "working correctly" for the intended use
> and why they are appropriate (e.g. Spearman rank correlation / concordance vs
> analyst gold labels; the v2.0 AUC-ROC ≥ 0.78 target for binary
> reliable/unreliable). Today only the operational `/metrics` (Prometheus) are
> emitted; **predictive** accuracy is not yet empirically validated (WP 4.1).

---

## 5. Risk management system (Art. 9)

Summarised here; full system in [`risk_management_art9.md`](risk_management_art9.md).

---

## 6. Lifecycle changes & validation/testing (accuracy, robustness, cybersecurity — Art. 15)

**Accuracy.**
- Current default NLP accuracy ~55–62% (spaCy NER + TextBlob); optional BERT /
  Sentence-BERT backends improve this. **Predictive reliability is not yet
  validated on labelled OSINT data** (WP 4.1).
- TODO: attach validation report once the labelled dataset + temporal
  train/holdout split (see [`../calibration.md`](../calibration.md)) is run; declare
  the achieved metric and the conditions it holds under.

**Robustness.**
- Input validation via Pydantic schemas (`cats/api/schemas.py`): message count
  1–500, text ≤ 10k chars, ISO-8601 timestamps, batch ≤ 50.
- Graceful fallbacks (TextBlob if BERT unavailable; Jaccard if Sentence-BERT
  unavailable).
- TODO: adversarial/gaming robustness evaluation.

**Cybersecurity.**
- TLS 1.3 (nginx), Bearer API-key auth with constant-time comparison
  (`hmac.compare_digest`), RS256 JWT support, sliding-window rate limiting
  (Redis Lua), non-root containers, security headers.
- AES-256-GCM encrypted audit log; row-level multi-tenant isolation bound to
  the API key server-side (`cats/core/security.py`).
- Vulnerability reporting: [`../../SECURITY.md`](../../SECURITY.md).

---

## 7. Data and data governance (Art. 10)

Summarised here; full description in
[`data_governance_art10.md`](data_governance_art10.md). Covers provenance of
OSINT sources, the calibration/labelling dataset, bias examination, and the
Italian-language limitation.

---

## 8. Logging & record-keeping (Art. 12)

- Every evaluation produces a `trace_id` and an **AES-256-GCM encrypted audit
  record** (`cats/audit/logger.py`).
- Retention: 90 days, with a nightly APScheduler purge under a distributed
  Redis lock (GDPR Art. 5(1)(e)).
- `GET /explain/{trace_id}` reconstructs the decision for a given record.
- TODO: confirm retention period satisfies the intended-use audit needs.

---

## 9. Transparency & information to deployers (Art. 13)

- `GET /explain/{trace_id}` returns each signal's `value`, `weight`,
  `contribution`, `score_share_pct`, `confidence`, the `primary_driver`, the
  `methodology` string, and a standing **disclaimer** (WP 4.1/4.3) on every
  response (`cats/scoring/explainer.py`).
- README + this documentation state intended purpose, accuracy level and
  limitations.
- TODO: produce formal **instructions for use** for deployers (Art. 13(3)
  content: identity/contact of provider, characteristics/limitations/accuracy,
  human-oversight measures, expected lifetime, maintenance).

---

## Declaration of conformity / registration

- EU declaration of conformity (Art. 47): TODO.
- Registration in EU database (Art. 49 / Annex VIII): TODO if applicable.
- Real-world testing under Art. 60 → **Annex IX** information: only if such
  testing is conducted (not currently planned).
