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
| [calibration_findings_2026-07-24.md](calibration_findings_2026-07-24.md) | Recalibration attempt blocked by a two-label holdout; motivated the split-axis fix |
| [calibration_findings_2026-07-25.md](calibration_findings_2026-07-25.md) | Recalibration on the corrected temporal split; shipped weights re-validated (not re-shipped) |
| [calibration_findings_2026-07-28.md](calibration_findings_2026-07-28.md) | Future-snapshot validation (6 Jul 2026): concordance 0.755, the declared production result |
| [calibration_findings_2026-08-21.md](calibration_findings_2026-08-21.md) | Checkpoint on the grown snapshot pool (59→95 sources, ~3 to ~7 weeks): same-sign edge, smaller magnitude; no weight change |
| [signal_research_2026-07.md](signal_research_2026-07.md) | Domain-provenance investigation → the ENGINE 1.4 asymmetric penalty |
| [signal_diagnosis_2026-07.md](signal_diagnosis_2026-07.md) | Ablation/LOSO diagnosis: coherence is load-bearing (SBERT), volatility/gaming are the redesign targets |
| [gaming_redesign_2026-08.md](gaming_redesign_2026-08.md) | Gaming's vocab/ttr double-weight bug fixed (3-term mean); recalibrated + future-holdout revalidated, no regression |
| [volatility_retune_2026-08.md](volatility_retune_2026-08.md) | Volatility spike threshold retuned 0.4→0.3 (finer sweep confirms it's the best point in the grid); recalibrated + future-holdout revalidated, no regression |
| [silence_retune_2026-08.md](silence_retune_2026-08.md) | Silence anomaly threshold retuned 72h→96h (rho plateaus there); recalibrated + future-holdout revalidated, no regression |
| [content_credibility_spike_2026-08.md](content_credibility_spike_2026-08.md) | Content-credibility signal spike (claim density, sensationalism, citation): none of three lexicon-based sub-scores clears the bar — recommendation is not to integrate |
| [cross_source_corroboration_spike_2026-08.md](cross_source_corroboration_spike_2026-08.md) | Cross-source corroboration spike: initially-promising correlation traced to a single source-pair content-genre artifact (CNET/Mashable puzzle columns) — feasibility check failed, registry not built |
| [volatility_source_relative_spike_2026-08.md](volatility_source_relative_spike_2026-08.md) | Source-relative (z-score) volatility normalization spike: a numerically strong result flips sign across a narrow hyperparameter window — not shipped, flagged to revisit at a larger holdout |

## Data collection

| Document | What it covers |
|---|---|
| [feed_health_2026-07.md](feed_health_2026-07.md) | RSS feed-health audit + repair log (13 rounds: dead/stale/blocked feeds fixed, a curl fallback for client-fingerprint blocks, new sources registered); `research/feed_health_audit.py` |
| [dataset_expansion_runbook.md](dataset_expansion_runbook.md) | Verified runbook to grow/maintain the labelled registry (with the labels.jsonl safety warning) |

## Compliance

| Document | What it covers |
|---|---|
| [compliance.md](compliance.md) | GDPR + EU AI Act summary mapping |
| [eu_ai_act/](eu_ai_act/README.md) | Conformity scaffold: classification (pending, legal), Annex IV draft, Art. 9 risk register, Art. 10 data governance |

## Planning

| Document | What it covers |
|---|---|
| [piano_sviluppo_roadmap_2026-07.md](piano_sviluppo_roadmap_2026-07.md) | Repo analysis, development plan and 15-point phased roadmap (July 2026, in Italian) |

The technical whitepaper (`CATS_WhitePaper_Tecnico_v1.0.docx`, in Italian) and
the pipeline scheme (`cats_scheme.png`) also live in this folder.
