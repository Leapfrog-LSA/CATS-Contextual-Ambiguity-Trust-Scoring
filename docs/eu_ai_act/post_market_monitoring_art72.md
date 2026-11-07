# CATS — Post-Market Monitoring Plan (Art. 72) — DRAFT

> **Regulation (EU) 2024/1689, Article 72**, as amended by **Regulation (EU)
> 2026/1744** (Digital Omnibus on AI).
>
> ⚠️ **Not legal advice. Draft, 2026-11-07.** This plan is pre-filled from
> what the CATS codebase measures today.
> - **Thresholds and cadences:** every alert threshold and review cadence is a
>   `TODO (maintainer)`. The draft shows the existing reference values only
>   so the maintainer can choose.
> - **Legal points:** every legal point is a `TODO (legal)`.
> - **Mandatory only if CATS is high-risk.** That determination is still
>   open: see [`classification.md`](classification.md). If CATS is not
>   high-risk, this plan is good practice only.
> - **Scores are ordinal**, not calibrated probabilities (WP 4.1/4.3). Every
>   accuracy figure below is a rank-agreement measure.

## 0. Legal frame (status on 2026-11-07, to be verified by counsel)

| Point | Status | Source |
|---|---|---|
| Art. 72(1)–(2) | The provider must establish and document a PMM system, proportionate to the technology and its risks. The system must actively and systematically collect, document and analyse performance data over the system's lifetime, including data from deployers or other sources, to evaluate continued compliance with Chapter III Section 2 (Arts. 8–15). Where relevant, this covers interaction with other AI systems. It does **not** cover sensitive operational data of deployers that are law-enforcement authorities. | [AI Act, Art. 72](https://artificialintelligenceact.eu/article/72/) |
| Art. 72(3), amended | The PMM system is based on a **PMM plan**, which is part of the Annex IV technical documentation (Annex IV point 9). The Omnibus replaced the implementing act that was to set a mandatory template. Instead, the Commission is to adopt **guidance, including a template**, by **2 September 2027**. On 2026-11-07 no template has been published: the Commission's guidelines page lists a *voluntary* PMM template as "in preparation". | [Reg. (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng); [Commission guidelines tracker](https://digital-strategy.ec.europa.eu/en/news/supporting-implementation-ai-act-clear-guidelines) |
| Application dates | Reg. 2026/1744 (in force since 27 July 2026) moves the Chapter III high-risk obligations to **2 December 2027** for Annex III systems and to **2 August 2028** for Annex I systems. | [Reg. (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng); [overview](https://artificialintelligenceact.eu/ai-act-explorer/digital-omnibus/) |
| Linked articles | Art. 3(25), definition of the PMM system. Art. 12(2)(c), logs that support PMM. Art. 17(1)(h)–(i), PMM and incident reporting as part of the QMS. Art. 20, corrective actions. Art. 26(5)–(6), deployers monitor and inform the provider, and keep logs. Art. 73, serious-incident reporting (immediately, and within 15 days at most). | [Reg. (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) |

- **TODO (legal):** confirm the wording above against the consolidated text
  on EUR-Lex. This draft relies partly on secondary summaries.
- **TODO (legal):** Arts. 72–73 sit in Chapter IX. Do they bind an Annex III
  provider before 2 December 2027, or only from that date, together with
  Chapter III?
- **TODO (maintainer):** when the Commission publishes its voluntary
  template (due by 2 September 2027), re-map this plan onto it.

## 1. Scope and proportionality (Art. 72(1))

- **System covered:**
  - the CATS scoring engine (`ENGINE_VERSION = "1.4"`,
    `cats/scoring/engine.py`);
  - the calibrated weights (`data/calibrated_weights.json`);
  - both surfaces that share it: the FastAPI deployment and the
    `cats.lite` / CLI / MCP library.
- **Proportionality:** CATS is a small open-source project. It produces an
  ordinal score with human-in-the-loop safeguards: `requires_review`, the
  contest endpoint, and the standing disclaimer. The plan therefore relies
  on what the code already emits, plus a short list of engineering gaps
  (§8). It does not propose a separate monitoring platform.
- **Two populations, monitored differently:**
  1. **The research registry**, about 125 labelled feeds collected daily into
     `Leapfrog-LSA/cats-snapshots`. The project controls it, so it can
     re-validate accuracy against labels.
  2. **Deployer traffic.** The project does not host deployments. It sees
     only what deployers report (Art. 26(5)) or what users send through the
     public feedback channels (§3, groups D–E).
- **TODO (maintainer):** name the PMM owner. This is the same open point as
  the risk owner in [`risk_management_art9.md`](risk_management_art9.md) §1.

## 2. Roles

| Role | Responsibility under this plan |
|---|---|
| Provider (CATS maintainers) | Run the reviews in §5, keep the records in §7, act on triggers (§6), update the risk register. **TODO (maintainer): named owner and deputy.** |
| Deployers | Monitor in line with the instructions for use, and inform the provider of risks and serious incidents (Art. 26(5)). Keep logs (Art. 26(6)). **TODO (maintainer/legal):** the instructions for use (Art. 13(3)) do not exist yet. They must say what deployers should report, and where. |
| Feedback givers | Anyone filing a *score feedback* issue (`.github/ISSUE_TEMPLATE/score_feedback.yml`) or contesting via the API. |

Exclusion: CATS must never request or receive sensitive operational data
from deployers that are law-enforcement authorities (Art. 72(2)).
**TODO (legal):** write this into the instructions for use and any deployer
agreement.

## 3. What is monitored

Each indicator maps to the Chapter III requirement it evidences. The
**Threshold** column is deliberately empty: the maintainer sets it (`TODO`).
**Reference** shows existing values from the repository, for context only.
**Source status:** ✅ the data exists today; ⚠️ it exists, but needs the work
listed in §8; ❌ it does not exist yet.

### A. Accuracy and ranking quality (Art. 15, Art. 9)

| # | Indicator | Data source | Source status | Reference (not a threshold) | Threshold |
|---|---|---|---|---|---|
| A1 | Pairwise concordance on the **future holdout** | `cats.calibration.evaluate` / `report` on `data/holdout_future.jsonl` (53 sources) | ✅ (manual run) | 0.750 (0.762 with domain penalty), last validated 2026-08-28 (`accuracy_declaration.md`); 0.70 used as the "generalises forward" bar (`calibration_findings_2026-07-28.md`); v2.0 target AUC-ROC ≥ 0.78 | TODO (maintainer) |
| A2 | Spearman rank correlation, same holdout | same | ✅ | +0.554 (+0.578 with penalty) | TODO (maintainer) |
| A3 | Band agreement, exact and within 1 band | same | ✅ | 26.4% / 79.2% | TODO (maintainer) |
| A4 | Size of the validation set (sources with a future window) | `data/holdout_future.jsonl` | ✅ | 53; roadmap target > 100 sources | TODO (maintainer) |

### B. Score and input drift (Art. 15, Art. 9 R2/R3/R5)

| # | Indicator | Data source | Source status | Reference | Threshold |
|---|---|---|---|---|---|
| B1 | Band distribution of scores served | `cats_evaluations_total{band}`, `cats_trust_score` histogram (`cats/core/metrics.py`) | ⚠️ in-process only: no Prometheus server or alert rules in the repo | Band cutoffs 80/60/40/20 | TODO (maintainer) |
| B2 | Per-signal medians, by source type / language / country | `research/observatory_aggregate.py` → `docs/observatory/` (aggregates only, no source identifiers) | ✅ (run once, 2026-09-17) | 2026-09-17 report | TODO (maintainer) |
| B3 | Share of evaluations flagged non-Italian | `language` block in each response (`cats/pipeline/language.py`) | ❌ not persisted, no metric | — | TODO (maintainer) |
| B4 | Share with `evidence.sufficient = false` | `evidence` block (`CATS_MIN_EVIDENCE_MESSAGES = 3`) | ❌ not persisted, no metric | — | TODO (maintainer) |
| B5 | Share with degraded NLP (`nlp_unavailable`) | `degraded_signals`; `/health` `nlp` field | ❌ not persisted, no metric | — | TODO (maintainer) |
| B6 | `requires_review` rate | response field | ❌ not persisted, no metric | — | TODO (maintainer) |
| B7 | Engine-version mix of stored scores | `trust_scores.engine_version` (alembic 003); `/explain` flags a mismatch | ✅ | `ENGINE_VERSION = "1.4"` | TODO (maintainer) |

### C. Data pipeline integrity (Art. 10)

| # | Indicator | Data source | Source status | Reference | Threshold |
|---|---|---|---|---|---|
| C1 | Feeds `ok` / `stale` / `dead` / `blocked` / `not-xml` | `research/feed_health_audit.py`, log in `docs/feed_health_2026-07.md` | ✅ (manual rounds) | Round 15 (2026-11-07): 96 / 8 / 5 / 10 / 6 of 125 | TODO (maintainer) |
| C2 | Daily snapshot collected | `Leapfrog-LSA/cats-snapshots` (`SHA256SUMS`) | ✅ | daily | TODO (maintainer) |

### D. Human oversight and disagreement (Art. 14, GDPR Art. 22)

| # | Indicator | Data source | Source status | Reference | Threshold |
|---|---|---|---|---|---|
| D1 | Contests opened, resolved, upheld (score changed) | `contests` table; `/contest/{id}/resolve` | ⚠️ no listing endpoint; no outcome taxonomy | — | TODO (maintainer) |
| D2 | Time to resolve a contest | `contests.created_at` / `resolved_at` | ⚠️ as D1 | — | TODO (maintainer) |
| D3 | Human disagreement labels and their agreement with CATS | `data/human_labels.jsonl` (validation-only, never training) via `research/ingest_score_feedback.py` | ⚠️ 0 records today; ingestion manual | — | TODO (maintainer) |

### E. Robustness, security and bias (Art. 15, Art. 10(2)(f), Art. 9 R4/R7/R8)

| # | Indicator | Data source | Source status | Reference | Threshold |
|---|---|---|---|---|---|
| E1 | Adversarial regression suite | `tests/unit/test_adversarial.py` (runs in CI on every PR) | ✅ | must stay green | — |
| E2 | Known-vulnerable dependencies | `.github/workflows/audit.yml` (weekly pip-audit) | ✅ | blocking on runtime deps | — |
| E3 | Security reports | `SECURITY.md` (ack 48 h, assessment 7 days) | ✅ | — | — |
| E4 | Threat-model items still open | `docs/threat_model_2026-09.md` (T1–T11) | ✅ | — | TODO (maintainer) |
| E5 | Band skew by source type / language / country | B2 output, compared with `data_governance_art10.md` | ⚠️ manual | — | TODO (maintainer) |

### F. Interaction with other AI systems (Art. 72(2))

- **What exists:** CATS ships an MCP server (`cats/mcp_server.py`), so LLM
  agents can call it and act on its scores. The optional `sbert` / `bert`
  backends embed third-party models.
- **TODO (maintainer/legal):** decide whether "interaction with other AI
  systems" is relevant. If it is, decide what deployers using CATS through
  MCP must report, for example an agent acting on a score without human
  review.

### G. Operational health (supports Art. 15 robustness)

`cats_http_requests_total` (5xx share), `cats_http_request_duration_seconds`
(latency), and `/health`. These are useful context for drift, and not
compliance indicators in themselves. **TODO (maintainer):** thresholds, if
any.

## 4. Collection rules (data protection)

- **Aggregates only.** Use aggregates wherever possible. Reports never name
  a source, the same rule `research/observatory_aggregate.py` enforces with
  `_check_no_identifiers`.
- **No personal data beyond what each source already holds:**
  - the audit log is AES-256-GCM encrypted, with 90-day retention;
  - `trust_scores` and `contests` are kept indefinitely today
    (threat model T5);
  - `human_labels.jsonl` requires the filer's consent.
- **Deployer reports** are taken in only through the channels in §6, and
  never include law-enforcement operational data (§2).
- **TODO (legal):** confirm that the GDPR basis and retention cover the
  PMM uses above, in particular the indefinite retention of `trust_scores`
  and `contests` (open threat-model item T5).

## 5. Analysis and review

| Review | What | Proposed cadence | Decided cadence |
|---|---|---|---|
| R-1 Accuracy re-validation | A1–A4 on the future holdout; on a breach, the recalibration cycle in §6 | proposal: quarterly, and at every release that touches signals, weights or thresholds | TODO (maintainer) |
| R-2 Drift review | B1–B7, C1–C2, E5; observatory re-run | proposal: monthly | TODO (maintainer) |
| R-3 Oversight review | D1–D3; read every new contest and score-feedback issue | proposal: monthly, plus on each new report | TODO (maintainer) |
| R-4 Security review | E1–E4 | continuous (CI); proposal: threat-model refresh twice a year | TODO (maintainer) |
| R-5 Plan review | this document | proposal: yearly, and when the Commission template is published | TODO (maintainer) |

**Output of each review:** a dated record (§7). Each finding is mapped to an
entry in the risk register (`risk_management_art9.md` §2), new or existing.

## 6. Triggers and actions

| Trigger | Action |
|---|---|
| An indicator crosses its threshold (once set) | Open a GitHub issue labelled `pmm`. Assess it against the risk register. If it is confirmed, take the corrective action (Art. 20) and record the residual risk. |
| Accuracy breach (A1–A3) | Run the recalibration cycle that CLAUDE.md and `docs/calibration.md` require: `python -m cats.calibration`, then re-validation on the **future holdout**. Never ship new weights or thresholds without it. |
| Drift without an accuracy breach (B, C) | Investigate the cause (feeds, language mix, NLP availability) before touching weights. |
| A contest is upheld, or a feedback issue shows a systematic error | Record it in `human_labels.jsonl` (validation-only), check it against the A-indicators, and update the risk register if it is a pattern. |
| A deployer reports a risk (Art. 26(5)) | Assess it, and inform deployers if the risk is confirmed. **TODO (legal):** when market surveillance authorities must be told. |
| **Possible serious incident (Art. 3(49), Art. 73)** | **TODO (legal/maintainer):** there is no Art. 73 procedure today. It needs: who decides that an event is a serious incident; the clock (immediately once a causal link is established or reasonably likely, and within 15 days at the latest, with shorter limits for some cases); which authority to notify; and the Commission's reporting template. Until it exists, `SECURITY.md` (security only) is the only incident channel. |

**TODO (maintainer):** a channel for deployers' non-security reports
(performance, misuse). `SECURITY.md` covers security only.

## 7. Records

- **Proposal:** keep one dated report per review in `docs/pmm/<YYYY-MM-DD>.md`,
  generated from aggregates, like `docs/observatory/`. Findings go into
  `risk_management_art9.md`.
- **TODO (maintainer):** decide where the records live, and how long they
  are kept. Annex IV documentation must be retained for 10 years under
  Art. 18. **TODO (legal):** confirm.

## 8. Engineering gaps

These are not done by this draft. Each would be a separate PR.

1. **Persist the guardrail flags** (`language`, `evidence`,
   `requires_review`, degraded signals) on `trust_scores`, or count them as
   Prometheus counters (B3–B6).
   - Persisting them needs an alembic migration.
   - Counters need no schema change. They are the cheaper first step.
2. **Contest reporting** (D1–D2):
   - a list/aggregate endpoint or script;
   - an outcome taxonomy (score upheld / changed / out of scope);
   - an audit row for contest creation (today `log_contest` writes none);
   - an `event_type` that is not always `evaluation`.
3. **A path from resolved contests to `human_labels.jsonl`**: the schema has
   `provenance: api_contest`, but nothing feeds it.
4. **A scheduled job** (GitHub Actions cron) that runs the feed-health audit,
   the holdout evaluation and the observatory, and writes the report in §7.
   Today all three are manual.
5. **Example Prometheus alert rules** for deployers who run Prometheus,
   shipped as documentation once the thresholds in §3 are set.
6. **Instructions for use (Art. 13(3))**, with a "what to report to the
   provider" section (Art. 26(5)).

## 9. Open decisions (summary)

| Decision | Who |
|---|---|
| Is CATS high-risk (classification)? Does this plan become mandatory? | legal |
| When Arts. 72–73 apply to an Annex III provider (Chapter IX vs. the 2 December 2027 date) | legal |
| PMM owner and deputy | maintainer |
| Thresholds for A1–A4, B1–B7, C1–C2, D1–D3, E4–E5, G | maintainer |
| Review cadences R-1 … R-5 | maintainer |
| Art. 73 serious-incident procedure | legal + maintainer |
| Deployer reporting channel and instructions for use | maintainer + legal |
| Relevance of "interaction with other AI systems" (MCP) | maintainer + legal |
| Retention of `trust_scores` / `contests` and of PMM records | legal |
| Which engineering gaps (§8) to build, and in what order | maintainer |
