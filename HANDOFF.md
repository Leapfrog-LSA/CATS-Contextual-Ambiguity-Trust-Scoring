# Session handoff — CATS (July 2026)

Continuation note for picking this work up in a fresh Claude Code session.
Everything is already on GitHub; a new session clones `main` and can read the
open/closed PRs directly.

## Current state

- **`main` is at v1.6.0** (production; PyPI + GitHub Release). CI green.
- **PR #42 — ✅ MERGED into `main`.**
  Branch `claude/feed-quality-fixes`. Production data-quality fixes now live:
  - **28 dead RSS feeds repaired** (registry **35 dead / 64 ok → 9 dead / 91 ok**,
    ~72% healthy). Every replacement verified HTTP 200 + valid XML + correct
    outlet/language. Most notable: **Il Corriere della Sera** (label 85, a scarce
    Italian high-reliability source) whose feed 404'd, so it had *never* been
    collected — the only "corriere" in the snapshots was the disinfo clone
    *Corriere del Corsaro* (label 10).
  - **+2 verified Italian high-reliability sources**: `repubblica.it`,
    `open.online` (MBFC **High**, read from the MBFC pages).
  - Tool `research/feed_health_audit.py` + `docs/feed_health_2026-07.md` +
    `docs/dataset_expansion_runbook.md` (with the data-safety warning below).
- **PR #41 — CLOSED (not merged) = research archive.**
  Branch `claude/repo-analysis-roadmap-yvsggk`. Content-credibility spike,
  signal ablation/diagnosis, dataset language-balance. **Do not reopen; do not
  re-merge into #42.**

## Rules / gotchas (verified — do not relearn the hard way)

- **`data/labels.jsonl` is a curated MERGE** of MBFC ratings *and* the
  documented-disinfo registry. It is **NOT** reproducible from `ratings.csv`
  alone: `label_from_ratings --scale mbfc --out data/labels.jsonl` drops
  160→141 records, **deleting the entire low tail** (Corriere del Corsaro label
  10, etc.). Always write MBFC output to a separate file and merge.
- **MBFC ratings must be READ from the source** (mediabiasfactcheck.com), never
  invented (CLAUDE.md: never fabricate).
- **Byte-exact data edits**: `data/Fonti_OSINT.csv` is **CRLF** (Windows). Use a
  bytes-level replace, not text-mode Python `open().write()`, or the whole file
  reflows (5277-line diff).
- **Every feed replacement** must be verified: HTTP 200 + XML body + the correct
  outlet *and language* (e.g. AFP's `/en/` path still serves French; Le Parisien
  had an English edition — both traps that were caught and skipped).
- Scoring semantics are frozen: any signal/threshold change needs
  recalibration + future-holdout re-validation (CLAUDE.md). Legal EU AI Act
  TODOs are never filled in by an agent.

## Next steps (pick one)

1. ✅ **PR #42 merged** — the 28 feed repairs + 2 Italian sources are in `main`;
   the next weekly collection will pick up ~28 previously-dead sources
   (incl. the scarce Italian high tail).
2. **Round 4 feed repair** — the ~9 still-dead feeds via per-source WebSearch:
   TRT Africa, Jakarta Globe, DPA, Mediazona, L'Orient Today, Taiwan News,
   Iran International, Rudaw, Caixin, Jordan Times, B92, SF Gate. Hard tail,
   diminishing returns; some no longer publish a usable public feed.
3. **BLOCKED on network+model**: recalibration with the repaired feeds + the
   content-credibility signal — needs a session with **Full** network and the
   spaCy model (`build_dataset` degrades coherence without it).
4. **BLOCKED on a human**: EU AI Act high-risk classification
   (`docs/eu_ai_act/classification.md`) — legal decision.

## Housekeeping

- No stale scheduled triggers (the PR #41 check-in and an obsolete 28-Jul
  validation trigger were removed). One check-in is armed for PR #42; it stops
  itself on merge/close.
- Workflow: one task = one branch = one PR to `main`; CI green before every
  push. This `HANDOFF.md` lives on branch `claude/session-handoff` and is not
  meant to be merged to `main`.
