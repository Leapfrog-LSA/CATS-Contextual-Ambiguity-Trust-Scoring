# CATS Compliance Documentation

## GDPR (EU 2016/679)

| Article | Requirement | CATS Implementation |
|---|---|---|
| Art. 5(1)(e) | Storage limitation | 90-day audit retention; nightly APScheduler purge with distributed Redis lock |
| Art. 13–14 | Transparency | `/v1/cats/explain/{trace_id}` returns full signal breakdown + methodology disclaimer |
| Art. 22 | Right not to be subject to automated decision | `/v1/cats/contest/{trace_id}` endpoint; `requires_review` flag forces human oversight for scores < 40 |
| Art. 25 | Data protection by design | AES-256-GCM encrypted audit logs; no raw personal data stored in `trust_scores` |
| Art. 32 | Security of processing | TLS 1.3 (nginx); encrypted audit trail; non-root container; rate limiting |

## EU AI Act (2024/1689)

CATS is classified as a **Limited Risk AI System** under Article 6(2) / Annex III.

| Obligation | CATS Status |
|---|---|
| Transparency | Explainability endpoint; disclaimer on every explanation response |
| Human oversight | `requires_review` flag; contest/review endpoints |
| Accuracy documentation | WP 4.1 — NLP accuracy ~55–62%; parameters not empirically calibrated |
| Ordinal scoring | WP 4.3 — scores are rankings, not absolute probabilities |

## Known Limitations (WP 4.1)

- **NLP accuracy ~55–62%**: spaCy NER and TextBlob rule-based sentiment are naive implementations for Italian text
- **Parameters uncalibrated**: all thresholds (spike_threshold=0.4, silence=72h, gaming min_tokens=10) are initial estimates, not empirically validated on labelled data
- **Ordinal only**: trust scores represent relative reliability rankings and are **not** suitable as sole basis for autonomous decisions (WP 4.3)
- **Language**: optimised for Italian (`it_core_news_lg`); other languages will produce degraded results

## Roadmap to Higher Accuracy

| Version | Target | Improvement |
|---|---|---|
| v1.1 (Q2 2026) | NLP | BERT-based Italian sentiment (replace TextBlob) |
| v1.2 (Q3 2026) | Coherence | Sentence-BERT similarity; SHAP explainability |
| v2.0 (2027) | Validation | AUC-ROC ≥ 0.78 on labelled OSINT dataset; full EU AI Act Annex IX documentation |

## Contact

GDPR queries: technical@cats-system.org
