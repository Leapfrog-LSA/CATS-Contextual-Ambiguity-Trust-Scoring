# CATS — Draft Classification Recommendation (2026-07-24)

> ⚠️ **This is a non-binding draft, not a determination.** It is a reasoned
> proposal prepared to give the assessor named in `classification.md`
> (provider / qualified counsel) a starting point, built on the evidence in
> [`deployment_context_summary.md`](deployment_context_summary.md). It does
> **not** fill in `classification.md`'s TODO/Outcome fields — those stay open
> until a human confirms, amends, or overrides this draft and signs it. Per
> `CLAUDE.md`, no automated process may treat this file as the classification
> itself.

## 1. Intended purpose, as actually built and distributed

CATS is distributed as a general-purpose OSINT source-reliability tool (a
library, `cats.lite`, and a multi-tenant API) with **no built-in restriction
on deployer sector** — any API-key holder can call it for any purpose
(`deployment_context_summary.md` §2). The repository's own materials frame it
broadly ("trust intelligence for OSINT sources"), not for a named regulated
sector. One external integration is observed pairing it with OSINT
due-diligence/KYC-style screening (`deployment_context_summary.md` §5),
unverified beyond this session.

**Consequence for classification:** because intended purpose is
deployment-dependent and CATS itself does not gate who deploys it, a single
static classification for "CATS" is the wrong frame. The recommendation below
proposes a *conditional* classification: not high-risk **as currently
distributed**, with named triggers that require re-assessment before specific
deployments proceed.

## 2. Annex III screening — draft reasoning per row

| Point | Area | Draft assessment | Reasoning |
|---|---|---|---|
| 1 | Biometrics | **Not applicable** | CATS processes published text only; confirmed in `classification.md` already. |
| 2 | Critical infrastructure | **Not applicable, no evidence of this use** | Nothing in the codebase or observed integrations points to safety management of critical infrastructure. |
| 3 | Education | **Not applicable** | Confirmed already; out of scope. |
| 4 | Employment | **Not applicable** | Confirmed already; out of scope. |
| 5 | Essential private/public services (incl. creditworthiness of natural persons, Art. III(5)(b)) | **Likely not applicable, but the closest call** | CATS scores the reliability of an information *source*, not a natural person directly; it does not itself compute a credit score or an eligibility determination. The one observed integration (OSINT due-diligence/KYC on business counterparties) uses CATS as one evidentiary-quality input inside a human analyst's report, at least one step removed from a creditworthiness/eligibility decision about a natural person. This is a **meaningfully different structure** from a system that itself scores a person's creditworthiness — but if any deployer's downstream process treats CATS's source-reliability score as materially determinative of a natural person's access to credit or a public benefit (rather than one input a human weighs), that specific deployment would need re-assessment. Cannot be resolved definitively without knowing the actual downstream decision logic of that integration. |
| 6 | Law enforcement (incl. Art. III(6)(e): evaluating the reliability of evidence in a criminal investigation/prosecution) | **Structurally the best-fit risk, contingent on deployer** | This is the point CATS's own design maps onto most directly — "assessing the reliability of evidence" is close to a literal description of what the tool computes for an OSINT source. No evidence in this codebase of an actual law-enforcement deployment today. **If** a law-enforcement body deployed CATS to assess the reliability of an information source as evidence in an investigation or prosecution, that deployment would very plausibly be high-risk under Art. III(6)(e) and should be treated as such from the outset, not discovered later. |
| 7 | Migration/asylum/border | **Same structure as point 6, contingent on deployer** | If a migration/asylum/border authority used CATS to assess the reliability of a source relevant to a visa/asylum determination, that would plausibly engage Art. III(7). No evidence of this use today. |
| 8 | Administration of justice / democratic processes | **Narrower fit, contingent on deployer** | Art. III(8)(a) (assisting judicial authorities in researching/interpreting facts) is the closer sub-point if a court used CATS in fact-finding; Art. III(8)(b) (influencing elections/voting behaviour via direct interaction with voters) does not fit CATS's design, which does not interact with voters at all. No evidence of judicial deployment today. |

## 3. Article 6(3) derogation — draft reasoning

CATS's shipped design gives real support to a 6(3) "narrow procedural /
preparatory task, does not materially influence the outcome" argument, **for
deployments where the deployer's own process honours it**:

- Scores are ordinal, disclaimed as such on every response (not a calibrated
  probability or a decision).
- `requires_human_review` forces a human-oversight flag on low/uncertain
  scores; `/contest` and `/review` give an explicit human-decides path
  (`deployment_context_summary.md` §3).
- Nothing in CATS enforces that a downstream system actually blocks on these
  flags before acting — the derogation argument holds only to the extent a
  given deployer's own process genuinely keeps a human in the loop and does
  not treat the score as dispositive. **This is a deployer-behaviour fact,
  not something CATS's code can establish on its own**, and would need to be
  verified per-deployment (e.g. in a data-processing agreement or deployment
  audit), not assumed from the software's design alone.

## 4. Draft recommendation

**Proposed determination: not high-risk, as CATS is currently distributed
(general-purpose library/API, no confirmed Annex III deployment) — subject to
mandatory re-assessment before any of the following, which should be written
into the final `classification.md` as explicit re-assessment triggers:**

1. Onboarding, or becoming aware of, a deployer that is a law-enforcement,
   migration/asylum/border, or judicial authority (Annex III points 6-8) —
   assess *that* deployment specifically before it goes live, given the
   structural fit noted in §2.
2. Learning that any deployer's process treats a CATS score as materially
   determinative (rather than one human-weighed input) of a natural person's
   access to credit, essential services, or public benefits (Annex III point
   5) — including confirming, with the observed OSINT due-diligence/KYC
   integration's owner, exactly how its output is used downstream.
3. Any deployer relying on the Art. 6(3) derogation should be able to
   demonstrate, not just assert, that a human genuinely reviews low-confidence
   or contested scores before they affect an outcome — the derogation record
   required by Art. 6(4) should capture this, not just cite the software's
   design.

**This draft is not a substitute for the sign-off `classification.md`
requires.** It should be reviewed, corrected where the reasoning above is
wrong or incomplete, and either adopted or replaced by whoever is named as
"Assessed by" in that file's Outcome table.
