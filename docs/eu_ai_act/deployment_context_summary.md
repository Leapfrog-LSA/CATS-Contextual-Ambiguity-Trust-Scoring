# CATS — Deployment Context Summary (factual input for classification)

> **This is evidence, not a determination.** It exists to save the assessor
> (counsel / provider, per `classification.md`) the ricognizione work of
> re-deriving "how is CATS actually built and consumed today" from the
> codebase. It does not answer the TODOs in `classification.md`, does not
> state whether any Annex III point applies, and must not be cited as if it
> were the classification itself. Every claim below is sourced to a specific
> file so it can be checked directly.

## 1. What ships, concretely

Two deployment surfaces, same signal code (`CLAUDE.md`):

- **`cats.lite` — a library call.** No network, no auth, no persistence:
  `from cats.lite import score; score(messages, source_type=...)` returns a
  score in-process (`README.md` §"Try it in 5 lines"). Nothing in the library
  API records *who* called it or *why* — that context lives entirely outside
  CATS, in whatever code imports it.
- **The FastAPI service — a multi-tenant HTTP API.** Endpoints (all behind
  `api_key_bearer`, `cats/api/routes/evaluate.py`):
  - `POST /v1/cats/evaluate`, `POST /v1/cats/batch` — score one or many message
    sets.
  - `GET /v1/cats/explain/{trace_id}` — per-signal attribution + methodology
    disclaimer (GDPR Art. 13–14 implementation, `docs/compliance.md`).
  - `POST /v1/cats/contest/{trace_id}` / `POST /v1/cats/contest/{contest_id}/resolve`
    — appeal a score and a human closes it (GDPR Art. 22 implementation).
  - `POST /v1/cats/review/{trace_id}` — explicitly request human review;
    logged, not auto-resolved.
  - `GET /v1/cats/stats` — per-tenant aggregate counts/bands.

## 2. Who can call it, and what the software itself restricts

Access control is **tenant-by-API-key**, not role- or sector-based
(`cats/core/security.py`): `CATS_API_KEYS` maps `key:tenant` pairs; every key
resolves to a `tenant_id` used only for **data isolation** (rate limiting,
row scoping in `trust_scores`/`contests`). There is no concept in the code of
"deployer category" (e.g. journalist vs. law-enforcement vs. public
authority) — any tenant can call `/evaluate` for any purpose the operator
allows. **Whether CATS is deployed for one of the Annex III activities is
entirely a question of who the actual API-key holders are and what they do
with the score, external to this codebase** — nothing here restricts or
labels that.

## 3. Decision-support design (relevant to the Art. 6(3) narrow-procedural-task question)

Evidence for and against a "the human stays in the loop, this is preparatory
not decisive" characterisation — `classification.md` §Art. 6(3) already
flags this as the derogation to assess; these are the concrete mechanics it
would turn on:

- Scores are **ordinal**, not calibrated probabilities, and the API/response
  disclaimer says so on every call (WP 4.3, `docs/compliance.md`).
- `requires_human_review` (`cats/scoring/engine.py:98-110`) forces a
  human-oversight flag when: band is `low`/`very_low`, evidence is
  insufficient, or confidence is low **and** score < 50. It does not force
  review on `medium`/`high` bands with good evidence — i.e. the design
  assumes low/uncertain scores need a human, not that a human reviews every
  score.
- `/contest` + `/contest/{id}/resolve` implement an explicit human-decides
  appeal path (GDPR Art. 22), and `/review` lets a caller flag a trace for
  human attention independent of the band logic.
- Nothing in the codebase enforces that a human review actually happens
  before a *downstream* decision is taken on a low-confidence or contested
  score — the API returns the score and the flags; whether the calling
  system blocks on them is, again, external to CATS.

## 4. Use-case signals already present in the repo's own materials

- `pyproject.toml` keywords: `osint, trust-scoring, source-reliability,
  disinformation, misinformation, gdpr, eu-ai-act, nlp, fact-checking`
  (`fact-checking` is a discoverability keyword; the README explicitly
  positions CATS as *not* a fact-checker — "How reliable is this source" vs.
  "Is this information true?").
- README framing throughout: **"trust intelligence for OSINT sources"** —
  the named audience is OSINT practice broadly, not a named sector.
- `docs/compliance.md` already carries a forward-looking risk flag, written
  by a prior session, not asserting current deployment: *"law-enforcement,
  migration and judicial uses can engage Annex III points 6–8"* — i.e. the
  three `classification.md` rows marked **TODO — key question** (6, 7, 8)
  were already identified as the ones to watch, from the system's own
  capabilities, not from a known deployer.
- No contract, ToS, or in-repo acceptable-use policy restricts (or confirms)
  deployment to any Annex III sector. No evidence in this codebase of an
  actual current law-enforcement, migration/asylum, or judicial deployment.

## 5. One external consumer observed from this session's environment (unverified beyond this)

This Claude Code environment has a skill catalogue entry, `analista-osint`
("Analista OSINT professionale... con trust scoring CATS delle fonti"),
describing an Italian-language OSINT due-diligence workflow — background
checks / KYC-AML reputational screening on companies, counterparties, and
individuals, framed as GDPR- and TULPS-compliant — that names CATS source
trust scoring as one of its steps. **This is observed from the Claude Code
skill listing available to this session, not from the CATS repository
itself** — it is evidence that at least one integration exists pairing CATS
with due-diligence/vendor-screening use, but its actual scale, deployer
identity, and whether it engages any Annex III point (most plausibly point 5,
"access to essential private/public services", if screening outcomes feed
eligibility decisions — TODO row in `classification.md`) cannot be verified
from this codebase and should be confirmed directly with whoever built that
integration before being relied upon.

## 6. Mapping to the open `classification.md` rows

| `classification.md` row | What §1–5 above adds |
|---|---|
| Intended purpose / deployers (line 23) | No named deployer restriction in-repo; README frames it as general OSINT tooling; §5 above is the one concrete downstream use case observed, unverified beyond this session |
| Annex III point 5 (essential services) | §5: possible if a due-diligence/KYC integration's output feeds an eligibility or onboarding decision — needs confirmation with that integration's owner |
| Annex III point 6 (law enforcement) | No evidence of actual deployment in this codebase; already flagged as a risk to watch in `docs/compliance.md` |
| Annex III point 7 (migration/asylum/border) | Same — no evidence of actual deployment; flagged as a risk to watch |
| Annex III point 8 (justice/democratic processes) | Same — no evidence of actual deployment; flagged as a risk to watch |
| Art. 6(3) derogation | §3: the human-oversight mechanics (`requires_human_review`, contest/review endpoints, ordinal-only disclaimer) are the concrete facts to weigh; the software does not itself guarantee a downstream system honours them |

None of the above resolves a TODO in `classification.md` — it narrows what
still needs a human answer to: **(a)** who actually holds API keys / uses
`cats.lite` today and for what, and **(b)** whether any of those actual
uses maps to Annex III points 5–8.
