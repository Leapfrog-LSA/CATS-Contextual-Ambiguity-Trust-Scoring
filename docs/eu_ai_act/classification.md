# CATS — High-Risk Classification Assessment (Art. 6 / Annex III)

> ⚠️ **Not legal advice.** This worksheet structures the classification
> question; the determination itself must be made with qualified counsel and
> documented before any conformity work proceeds.

## Why this comes first

Article 6(2) makes an AI system high-risk if it is intended to be used for a
purpose listed in **Annex III**. Whether CATS is high-risk is **use-dependent**:
the *same* scoring engine can be low-risk in one deployment and high-risk in
another. The obligations in the rest of this folder (Annex IV, Art. 9, Art. 10,
…) are mandatory **only** if CATS is high-risk.

## System purpose (intended use)

CATS computes an **ordinal reliability score for an OSINT *source* over time**
from four behavioural signals (coherence, volatility, silence, gaming). It is
**not** a fact-checker and, per WP 4.3, its output is a relative ranking, not an
absolute probability, and is "not suitable as sole basis for autonomous
decisions".

> TODO (provider): State the *concrete* intended purpose(s) and intended
> deployers. Classification turns on this. Example axes: who uses it (analysts,
> journalists, law enforcement, public authorities), and what decisions it
> feeds.

## Annex III screening

For each category, record applicability and rationale.

| Annex III point | Area | Potentially applicable to CATS? | Notes |
|---|---|---|---|
| 1 | Biometrics | No | CATS processes published text, not biometric data | 
| 2 | Critical infrastructure | TODO | Only if used to manage safety of critical infrastructure |
| 3 | Education / vocational training | No | Out of scope |
| 4 | Employment / worker management | No | Out of scope |
| 5 | Access to essential private/public services | TODO | Unlikely, unless wired into eligibility decisions |
| 6 | Law enforcement | **TODO — key question** | e.g. reliability of evidence/sources, intelligence triage may engage 6(a)/(e) |
| 7 | Migration, asylum, border control | **TODO — key question** | Source/risk assessment in this context can be high-risk |
| 8 | Administration of justice / democratic processes | **TODO** | Use in judicial fact-assessment or election-integrity contexts |

## Article 6(3) derogation

Even if an intended use maps to Annex III, Art. 6(3) lets a system *not* be
high-risk where it performs a **narrow procedural / preparatory task** and does
**not** materially influence the outcome of decision-making. CATS' ordinal,
human-in-the-loop, "not sole basis" design may support a 6(3) argument.

> TODO (legal): Assess whether Art. 6(3) applies. If relied upon, the
> assessment must be **documented and registered** per Art. 6(4).

## Outcome

| Field | Value |
|---|---|
| Determination | TODO: high-risk / not high-risk |
| Annex III point(s) engaged, if any | TODO |
| Art. 6(3) derogation relied upon? | TODO |
| Assessed by | TODO (name / counsel) |
| Date | TODO |
| Re-assessment trigger | TODO (new deployment context, new deployer category) |

If **not high-risk**, the remaining files in this folder are good-practice only.
If **high-risk**, proceed to
[`annex_iv_technical_documentation.md`](annex_iv_technical_documentation.md).
