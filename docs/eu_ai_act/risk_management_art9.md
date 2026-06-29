# CATS — Risk Management System (Art. 9)

> **Regulation (EU) 2024/1689, Article 9.** A continuous, iterative risk
> management process run across the system's lifecycle.
>
> ⚠️ **Not legal advice.** Template pre-filled from current CATS behaviour;
> `TODO` markers flag provider decisions. Mandatory only if CATS is high-risk
> (see [`classification.md`](classification.md)).

## 1. Process & ownership

- **Owner:** TODO (named risk owner).
- **Cadence:** continuous; formal review at each release and on incident.
  TODO: set review interval (e.g. quarterly).
- **Records:** this document + linked issues/PRs; incidents logged via
  [`../../SECURITY.md`](../../SECURITY.md) channel.

## 2. Risk register

Likelihood/impact: Low / Medium / High. Pre-seeded — extend and quantify.

| ID | Risk | Likelihood | Impact | Existing mitigation | Residual / TODO |
|---|---|---|---|---|---|
| R1 | **Over-reliance**: deployer treats ordinal score as ground truth | High | High | `requires_review` flag; WP 4.3 disclaimer on every `/explain`; "not sole basis" in docs | Instructions for use must state this explicitly (Art. 13) |
| R2 | **NLP inaccuracy** (~55–62% default) mis-ranks a source | Medium | High | Optional BERT/Sentence-BERT backends; confidence per signal; calibration | Empirical validation pending (WP 4.1) → §Art.15 |
| R3 | **Language degradation** on non-Italian content | High | Medium | Italian-optimised models documented as a limitation | Detect/flag non-Italian input — TODO |
| R4 | **Adversarial gaming** evades the gaming signal | Medium | Medium | Gaming signal (repetition/TTR/burst/vocab) | Adversarial robustness testing — TODO |
| R5 | **Small-sample instability** (few messages) yields unstable scores | Medium | Medium | Min message count via schema; confidence values | Define/expose a minimum-evidence threshold — TODO |
| R6 | **Uncalibrated band thresholds** misassign bands | Medium | Medium | Calibration tunes weights | Thresholds remain estimates (WP 4.1) — validate |
| R7 | **Bias** against source types / regions / languages | Medium | High | source-type aware thresholds | Bias examination — see `data_governance_art10.md` |
| R8 | **Security / data exposure** | Low | High | TLS 1.3, API-key+JWT auth, rate limiting, AES-256 audit, tenant isolation, non-root | Pen-test / threat model — TODO |
| R9 | **Misuse in unintended high-stakes context** (e.g. law enforcement) without safeguards | TODO | High | Intended-use limits documented | Gate by classification + contractual use limits |

## 3. Risk treatment (Art. 9(5))

Order of measures: eliminate/reduce by design → mitigate → provide information
& training to deployers.

- **By design:** ordinal output; human-in-the-loop (`requires_review`, contest
  endpoint); per-signal confidence; explainability; input validation.
- **Mitigation:** optional higher-accuracy NLP backends; calibration pipeline;
  rate limiting; encrypted audit.
- **Information:** WP 4.1/4.3 disclaimers; this folder; TODO instructions for use.

## 4. Residual risk acceptance

> TODO (provider/legal): record the residual-risk judgement for each register
> entry and an overall acceptance statement, with sign-off name + date.

## 5. Human oversight (Art. 14) — link

- `requires_review` forces human review for low scores.
- `POST /v1/cats/contest/{trace_id}` lets a human contest an outcome (GDPR
  Art. 22 alignment).
- TODO: define the deployer-side oversight procedure (who reviews, SLA, how
  override is recorded).

## 6. Post-market monitoring (Art. 72) — link

- Operational telemetry via `/metrics` (Prometheus); encrypted audit trail.
- TODO: define the post-market monitoring plan — what is collected, how
  drift/accuracy degradation is detected, and the feedback loop into this
  register.

## 7. Testing against measures (Art. 9(6)–(8))

- Unit/integration tests in `tests/` (signals, scoring, explainer, security,
  schemas, calibration, API).
- TODO: add risk-driven test cases (adversarial gaming, non-Italian input,
  minimal-sample inputs) and record results in §Art.15 of the Annex IV doc.
