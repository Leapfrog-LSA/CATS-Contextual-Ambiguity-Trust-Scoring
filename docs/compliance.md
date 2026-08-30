# CATS Compliance Documentation

## GDPR (EU 2016/679)

| Article | Requirement | CATS Implementation |
|---|---|---|
| Art. 5(1)(e) | Storage limitation | 90-day audit retention; nightly APScheduler purge with distributed Redis lock |
| Art. 13–14 | Transparency | `/v1/cats/explain/{trace_id}` returns full signal breakdown + methodology disclaimer |
| Art. 22 | Right not to be subject to automated decision | `/v1/cats/contest/{trace_id}` endpoint; `requires_review` flag forces human oversight for scores < 40 or evaluations below the evidence minimum |
| Art. 25 | Data protection by design | AES-256-GCM encrypted audit logs; no raw personal data stored in `trust_scores` |
| Art. 32 | Security of processing | TLS 1.3 (nginx); encrypted audit trail; non-root container; rate limiting |

## EU AI Act (2024/1689)

> **Classification is a pending legal decision, not a settled fact.** Whether
> CATS is high-risk under Article 6 / Annex III depends on the deployment
> context (law-enforcement, migration and judicial uses can engage Annex III
> points 6–8) and must be assessed with legal counsel — see
> [eu_ai_act/classification.md](eu_ai_act/classification.md). Until that
> determination is recorded, this repo maintains the documentation below as
> good practice without asserting a risk class.

| Obligation | CATS Status |
|---|---|
| Transparency | Explainability endpoint; disclaimer on every explanation response |
| Human oversight | `requires_review` flag (low bands, or insufficient evidence); contest/review endpoints |
| Accuracy documentation | WP 4.1 — NLP accuracy ~55–62%; signal weights calibrated and validated on a future snapshot (concordance 0.750 → 0.762 with the domain penalty, as of the Aug 2026 gaming/volatility/silence fixes); band/silence thresholds still initial estimates |
| Ordinal scoring | WP 4.3 — scores are rankings, not absolute probabilities |

## Known Limitations (WP 4.1)

- **NLP accuracy ~55–62% (default backends)**: spaCy NER and TextBlob rule-based sentiment; optional BERT/Sentence-BERT backends available
- **Thresholds unvalidated**: signal *weights* are calibrated and future-snapshot validated, but the operating thresholds (volatility spike 0.4, silence 72 h, band cutoffs 80/60/40/20) remain initial estimates — the [signal diagnosis](signal_diagnosis_2026-07.md) measured better candidates (spike 0.1–0.3, silence ≥ 96 h), pending the recalibration cycle
- **Ordinal only**: trust scores represent relative reliability rankings and are **not** suitable as sole basis for autonomous decisions (WP 4.3)
- **Language**: optimised for Italian (`it_core_news_lg`); non-Italian input is detected and flagged in the response (`language` block, risk R3) but is still scored with the Italian-tuned stack

## Roadmap to Higher Accuracy

| Version | Target | Improvement |
|---|---|---|
| v1.1–v1.2 | ✅ NLP backends | BERT Italian sentiment · Sentence-BERT coherence · per-signal attribution |
| v1.4 | ✅ Validation | Calibrated weights validated on a future snapshot (concordance 0.755) |
| v1.5 | ✅ Hardening | Domain-provenance asymmetric penalty (ENGINE 1.4, 0.755 → 0.775) |
| v1.6 | ✅ Guardrails & audit fixes | Language flag (R3) · minimum-evidence flag (R5) · adversarial regression suite · audit-IP spoofing fix, degraded NLP startup, calibrated weights shipped in Docker |
| Aug 2026 | ✅ Signal fixes | Gaming/volatility/silence bugs fixed and recalibrated (concordance 0.755 → 0.750, 0.775 → 0.762 with domain penalty — no regression); content-credibility and cross-source corroboration signals spiked and rejected; Tranco popularity corroboration added to the domain penalty |
| v2.0 (2027) | Validation | Concordance/AUC ≥ 0.78 on a ≥ 100-source future holdout with multi-month per-source history; band-threshold validation; full EU AI Act **Annex IV** technical documentation |

> **Annex IV vs Annex IX.** The general "document the system" artefact under the
> AI Act is **Annex IV** technical documentation (Art. 11) — *not* Annex IX.
> Annex IX (Art. 60) covers only information to submit when **testing in
> real-world conditions** outside regulatory sandboxes, which CATS does not
> currently do. See [eu_ai_act/](eu_ai_act/) for the conformity scaffold and the
> high-risk classification prerequisite.

## Contact

GDPR queries: technical@cats-system.org
