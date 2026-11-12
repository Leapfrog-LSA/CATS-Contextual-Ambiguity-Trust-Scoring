# CATS — EU AI Act Conformity Documentation

> **Regulation (EU) 2024/1689** ("AI Act"). Working folder for CATS conformity
> artefacts.
>
> The newest document here, [`post_market_monitoring_art72.md`](post_market_monitoring_art72.md),
> works from the Regulation as amended by **Regulation (EU) 2026/1744** (Digital
> Omnibus on AI). Its effect on the other documents and on timelines is to be
> verified by counsel (`TODO` legal).
>
> ⚠️ **This is not legal advice.** These documents are engineering-facing
> templates mapping what CATS implements onto the Regulation. They must be
> reviewed against the [consolidated text on EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)
> by qualified legal counsel before being relied upon. `TODO` markers flag
> decisions or data that require human/legal input.

---

## Which Annex do we actually need? (important)

A recurring confusion: **Annex IX is *not* the general technical
documentation.** Per Regulation (EU) 2024/1689:

| Annex / Article | What it actually covers | Relevant to CATS? |
|---|---|---|
| **Annex III** | List of high-risk use cases (Art. 6(2)) | **First question** — determines whether the rest applies at all |
| **Annex IV** (Art. 11) | **Technical documentation** of a high-risk AI system | **Yes — this is the general "document the system" artefact** |
| Annex VIII (Art. 49) | Information to register the system in the EU database | If high-risk and placed on the market |
| **Annex IX** (Art. 60) | Information to submit when **testing in real-world conditions** *outside* regulatory sandboxes | **Only if** field tests with real data/subjects are run |

So for "document CATS for the AI Act", the artefact is **Annex IV**, not
Annex IX. Annex IX applies *only* if and when CATS undergoes real-world
testing under Article 60. The previous `docs/compliance.md` reference to
"Annex IX documentation" as the general v2.0 target was imprecise and has
been corrected to Annex IV.

---

## Step 0 — Classification (do this first)

Everything below is conditional on CATS being a **high-risk** system under
Article 6 / Annex III. A source-reliability scoring tool for OSINT *may not*
fall into any Annex III category — or it may, depending on deployment (e.g.
use by law enforcement or in migration/asylum/border contexts can trigger
Annex III points 6–7).

**This classification decision is a prerequisite and must be made with legal
counsel.** See [`classification.md`](classification.md).

- If **not high-risk**: only the transparency obligations (Art. 50, where
  applicable) and good-practice documentation apply. Most of Annex IV is then
  voluntary but still useful.
- If **high-risk**: Annex IV technical documentation (Art. 11), a risk
  management system (Art. 9), data governance (Art. 10), and the rest of
  Chapter III Section 2 become mandatory.

---

## Documents in this folder

| File | Maps to | Status |
|---|---|---|
| [`classification.md`](classification.md) | Art. 6 / Annex III | Decision pending (legal) |
| [`annex_iv_technical_documentation.md`](annex_iv_technical_documentation.md) | Annex IV / Art. 11 | Draft, pre-filled from implementation |
| [`risk_management_art9.md`](risk_management_art9.md) | Art. 9 | Draft template |
| [`data_governance_art10.md`](data_governance_art10.md) | Art. 10 | Draft template |
| [`post_market_monitoring_art72.md`](post_market_monitoring_art72.md) | Art. 72 / Annex IV point 9 | Draft plan; thresholds and owner TODO |
| [`accuracy_declaration.md`](accuracy_declaration.md) | Art. 15 / Annex IV §6 | Generated from the future holdout (2026-08-30); provenance and sign-off TODO |
| [`deployment_context_summary.md`](deployment_context_summary.md) | Input to Art. 6 / Annex III | Evidence, not a determination |
| [`draft_recommendation_2026-07-24.md`](draft_recommendation_2026-07-24.md) | Art. 6 / Annex III | Non-binding draft; the decision stays with counsel |

The measured accuracy declaration (Art. 15) is
[`accuracy_declaration.md`](accuracy_declaration.md), generated from the future
holdout (`data/holdout_future.jsonl`, n=53: pairwise concordance 0.750, Spearman
+0.554); the validation itself is tracked in [`../calibration.md`](../calibration.md).
The v2.0 roadmap target (AUC-ROC ≥ 0.78) is not yet met, and scores remain
**ordinal**, not calibrated probabilities (WP 4.1/4.3).

---

## Relationship to existing compliance material

- [`../compliance.md`](../compliance.md) — high-level GDPR + AI Act summary
- [`../architecture.md`](../architecture.md) — signal algorithms, security design
- [`../calibration.md`](../calibration.md) — empirical weight calibration

These remain the source of truth for implementation detail; the files here
restructure that detail against the Regulation's required headings.
