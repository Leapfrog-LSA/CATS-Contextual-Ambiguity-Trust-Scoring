# Zenodo deposit checklist — CATS technical whitepaper

Task 21 of the post-1.7.0 plan. This is a **human-executed** checklist: the
PDF conversion and the actual Zenodo deposit both need a human at a Zenodo
account (OAuth via GitHub or ORCID) — nothing here is automatable from this
repo, and no deposit is created by merging this doc. It exists so the
maintainer doesn't have to reconstruct Zenodo's field list and this repo's
own metadata from scratch each time.

## 0. Source file

- `docs/CATS_WhitePaper_Tecnico_v1.0.docx` (Italian). Confirm before
  converting whether the content still matches the **shipped** v1.7.0
  engine (signals, weights, band thresholds, `ENGINE_VERSION`) — the
  whitepaper is versioned independently (`v1.0`) and may predate later
  calibration/retune docs indexed in `docs/README.md`. If it's stale on any
  numeric claim, fix the source `.docx` first; don't deposit a whitepaper
  that contradicts the current `docs/calibration_findings_*.md`.

## 1. Convert to PDF

- [ ] Export `CATS_WhitePaper_Tecnico_v1.0.docx` → PDF (Word/LibreOffice
      "Save as PDF", not a printed screenshot — Zenodo indexes PDF text).
- [ ] Open the PDF and check: page breaks, headers/footers, and any tables
      or the `cats_scheme.png` pipeline diagram didn't shift or clip.
- [ ] Name it something Zenodo-stable, e.g.
      `CATS_WhitePaper_Tecnico_v1.0.pdf` (keep the version in the filename —
      Zenodo treats a later upload to the same record as a new version, not
      a rename).

## 2. Zenodo deposit metadata

Upload at [zenodo.org/deposit/new](https://zenodo.org/deposit/new) (or via
their API/`zenodo_get` if preferred). Suggested field values, drawn from
this repo's own `CITATION.cff` / `LICENSE` / `README.md` so the Zenodo
record and the GitHub record agree:

| Field | Value |
|---|---|
| Upload type | Publication → Technical note (or "Preprint" if the maintainer prefers) |
| Title | CATS — Contextual Ambiguity & Trust Scoring: Whitepaper Tecnico v1.0 |
| Authors | `Leapfrog-LSA` (match `CITATION.cff`; add an ORCID per author if/when individual authors are attributed instead of the org) |
| Description | Adapt the abstract already in `CITATION.cff`: "Trust intelligence scoring for OSINT sources: behavioural reliability analysis (narrative coherence, sentiment volatility, temporal silence, gaming detection) with empirical weight calibration, GDPR Art. 13-22 endpoints and EU AI Act documentation." Add one line noting the whitepaper is in Italian and that it documents the method independent of a specific engine version. |
| Version | `1.0` (the whitepaper's own version — do **not** put the software version `1.7.0` here; they version independently) |
| Language | Italian (`ita`) |
| License | MIT (matches repo `LICENSE`) — Zenodo's license picker has MIT natively |
| Keywords | `OSINT`, `trust-scoring`, `source-reliability`, `disinformation`, `EU-AI-Act`, `GDPR` (copy verbatim from `CITATION.cff` so the two records are keyword-consistent) |
| Related/alternate identifiers | Add the GitHub repo as "is supplement to": `https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring`; add the `v1.7.0` GitHub Release as "references": `https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring/releases/tag/v1.7.0` |
| Access right | Open access |
| Publication date | Date of actual deposit (not the `.docx` file's original date) |
| Funding | None known — leave blank unless the maintainer has a grant to declare |

## 3. GitHub ↔ Zenodo linking (optional but recommended)

Zenodo's GitHub integration mints a **new DOI automatically on every future
GitHub Release** if enabled — decide up front whether that's wanted:

- [ ] Decide: manual one-off deposit (this checklist only) vs. enabling
      [Zenodo's GitHub app](https://zenodo.org/account/settings/github/) so
      each future release (`v1.8.0`, etc.) gets its own version DOI
      automatically. If enabling it, do so **before** cutting the next
      release, and note that this mints a DOI per release — only do it if
      that cadence is wanted for citation purposes, not just for this one
      whitepaper.
- [ ] If manual: after the deposit is published, Zenodo gives both a
      **version DOI** (this specific v1.0 upload) and a **concept DOI**
      (stable across all future versions of the same record). Record both.

## 4. After publishing

- [ ] Add the DOI badge/link to `README.md` (the "public demo + whitepaper
      DOI" line already referenced in the roadmap section) — use the
      **concept DOI** if future versions are expected, the **version DOI**
      if this is a one-off snapshot.
- [ ] Add the DOI to `CITATION.cff` (a `identifiers:` entry, `type: doi`) so
      `cats.__version__`-style citation and the whitepaper citation are
      both discoverable from the repo.
- [ ] Update `docs/README.md`'s whitepaper line (currently: *"The technical
      whitepaper (...) also lives in this folder"*) to link the Zenodo DOI
      alongside the local `.docx`.
- [ ] These are small, non-behavioural doc edits — normal `CHANGELOG.md`
      `[Unreleased]` entry, one PR, no version bump needed on their own.

## Explicitly out of scope here

- No legal/authorship determination beyond what `CITATION.cff` already
  states — if individual named authors (vs. the `Leapfrog-LSA` org) need to
  be credited with ORCIDs, that's a maintainer decision, not something to
  infer.
- No automatic re-deposit on every release unless the GitHub↔Zenodo app is
  explicitly enabled per step 3.
