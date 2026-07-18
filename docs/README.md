# CATS documentation index

## Using CATS

| Document | What it covers |
|---|---|
| [api.md](api.md) | Full REST API reference (evaluate, batch, explain, contest, review, stats) |
| [architecture.md](architecture.md) | Signal algorithms, aggregation engine, polarity/penalty design decisions, security design |
| [cloud_setup.md](cloud_setup.md) | Running CATS in Claude Code on the web: setup script, test env vars, network access |

## Calibration & empirical validation

| Document | What it covers |
|---|---|
| [calibration.md](calibration.md) | Weight calibration toolkit (genetic search) and the validated production weights |
| [calibration_findings_2026-07.md](calibration_findings_2026-07.md) | First calibration on real data; the signal-polarity defect that motivated v1.3 |
| [calibration_findings_2026-07-28.md](calibration_findings_2026-07-28.md) | Future-snapshot validation (6 Jul 2026): concordance 0.755, the declared production result |
| [signal_research_2026-07.md](signal_research_2026-07.md) | Domain-provenance investigation → the ENGINE 1.4 asymmetric penalty |
| [signal_diagnosis_2026-07.md](signal_diagnosis_2026-07.md) | Ablation/LOSO diagnosis: coherence is load-bearing (SBERT), volatility/gaming are the redesign targets |

## Compliance

| Document | What it covers |
|---|---|
| [compliance.md](compliance.md) | GDPR + EU AI Act summary mapping |
| [eu_ai_act/](eu_ai_act/README.md) | Conformity scaffold: classification (pending, legal), Annex IV draft, Art. 9 risk register, Art. 10 data governance |

## Planning

| Document | What it covers |
|---|---|
| [piano_sviluppo_roadmap_2026-07.md](piano_sviluppo_roadmap_2026-07.md) | Repo analysis, development plan and 15-point phased roadmap (July 2026, in Italian) |
| [content_credibility_findings_2026-07.md](content_credibility_findings_2026-07.md) | Content-credibility spike + the quantified dataset language-confound |
| [dataset_expansion_runbook.md](dataset_expansion_runbook.md) | Verified runbook to add Italian sources and break the confound (next network session) |

The technical whitepaper (`CATS_WhitePaper_Tecnico_v1.0.docx`, in Italian) and
the pipeline scheme (`cats_scheme.png`) also live in this folder.
