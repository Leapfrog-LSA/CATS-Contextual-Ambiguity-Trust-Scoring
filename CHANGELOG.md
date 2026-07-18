# Changelog

All notable changes to CATS are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-03-06

### Added
- 4-signal scoring pipeline: coherence, volatility, silence, gaming
- FastAPI REST API with 9-phase evaluation pipeline
- GDPR Art. 13–22 endpoints: `/explain`, `/contest`, `/review`
- AES-256-GCM encrypted audit log (PostgreSQL)
- Redis sliding-window rate limiting (Lua, 30 req/min)
- JWT RS256 authentication with dual API-key rotation
- APScheduler nightly audit purge with distributed Redis lock
- Docker multi-stage build with non-root user
- GitHub Actions CI: lint, unit tests, integration tests, Docker build
- spaCy `it_core_news_lg` for Italian NER
- RFC 7807 Problem Details error responses
- Deep `/health` endpoint (API + Redis + PostgreSQL + NLP)
- WP 4.1/4.3 compliance disclaimer on all explanation responses
- Dynamic weight matrix by source type (social/news)

### Known Limitations
- NLP accuracy ~55–62% (rule-based; see WP 4.1)
- Parameters not empirically calibrated
- Italian-only NLP pipeline

---

## [Unreleased]

### Added
- Content-credibility signal spike (`research/content_credibility_spike.py`,
  findings in `docs/content_credibility_findings_2026-07.md`): a text-style
  red-flag (caps shouting, clickbait punctuation, bilingual hyperbole lexicon,
  attribution credit) for the fake-news-on-ordinary-domains class that
  domain-provenance misses. Honest result — the raw future-holdout correlation
  (ρ −0.33) is almost entirely a language confound (the registry's low tail is
  Italian, its high tail mostly English), collapsing to ρ +0.08 within Italian
  (n=8), and the feature barely fires except on one overt ALL-CAPS outlet.
  **Not wired**: the committed data cannot validate it — a hard block on the
  language-balanced dataset work.

### Planned
- Content-credibility signal — pending a language-balanced labelled set that
  can disentangle the confound (see the spike findings above). The dataset gap
  is quantified (`research/dataset_language_balance.py`: ρ(is_italian, label)
  = −0.265, high-reliability Italian is the scarce cell) and a verified
  collection runbook is ready for the next network session
  (`docs/dataset_expansion_runbook.md`).
- Full EU AI Act **Annex IV** technical documentation (pending the legal
  high-risk classification).
- v2.0 (2027): recalibration with the diagnosis inputs, concordance/AUC ≥ 0.78
  on a ≥ 100-source future holdout

---

## [1.6.0] — 2026-07-12

### Added
- **Input-language flag (risk R3, roadmap item 8).** Evaluations now assess
  whether the message corpus is Italian (`cats/pipeline/language.py`: a
  dependency-free script check + Italian function-word ratio, 205/205 correct
  on the July snapshot registry, thresholds with a >4× margin). `cats.lite`
  results and `/evaluate` responses carry a `language` block
  (`italian`/`other`/`unknown` + confidence), and explanations warn when the
  Italian-optimised NLP stack is scoring non-Italian text. Flag-only: scores
  and bands never change. Not persisted — `/explain` does not report it.
- **Minimum-evidence guardrail (risk R5, roadmap item 9).** New
  `CATS_MIN_EVIDENCE_MESSAGES` setting (default 3): evaluations on fewer
  messages report `evidence.sufficient=false` and force
  `requires_review`/`requires_human_review` — previously a single message
  aggregated to a "high" band with zero confidence and *no* flag. The
  `evidence` block (message count, minimum, mean behavioural confidence) is
  returned by `cats.lite` and `/evaluate`. Flag-only: scores and bands never
  change (penalising them needs the recalibration cycle). The API schema
  floor stays 1 message for backwards compatibility.

- Repo analysis, development plan and numbered roadmap
  (`docs/piano_sviluppo_roadmap_2026-07.md`): state of the project at
  v1.5.0/ENGINE 1.4, strengths, open risks (single-signal discrimination,
  small validation set, unvalidated thresholds, pending legal TODOs, minor
  repo inconsistencies) and a 15-point phased roadmap.
- The `SessionStart` hook promised by `docs/cloud_setup.md` now actually ships
  (`.claude/hooks/session-start.sh` + `.claude/settings.json`): cloud-only,
  idempotent fallback for the environment setup script — installs the dev/test
  stack and the Italian NLP assets on a cold container, fast no-op on a warm one.
- Adversarial robustness regression suite (`tests/unit/test_adversarial.py`)
  turning the Art. 9 risk-register TODOs for R3/R4/R5 into executable tests:
  regular publishing cadence neutralises `silence` and is only caught via the
  domain penalty (R4); a single message currently aggregates to a "high" band
  at zero confidence, and the API schema floor is one message (R5); non-Italian
  input degrades silently with nothing flagging the language mismatch (R3).
  The tests pin current behaviour — weaknesses included — so signal-hardening
  work or accidental regressions must surface as deliberate test changes.
  Risk register §2/§7 updated to reference the suite.
- Signal ablation/LOSO diagnosis (`research/signal_ablation_spike.py`,
  findings in `docs/signal_diagnosis_2026-07.md`): on the future holdout,
  coherence — a near-chance solo ranker (0.528) — is the second-largest
  contributor to the calibrated aggregate (LOSO −0.139 concordance, it breaks
  the ties silence leaves), overturning the earlier "likely overfitting"
  reading; volatility (−0.013) and gaming (−0.005, solo at chance) are the
  real redesign candidates. Operational note: the calibrated weights assume
  the SBERT coherence backend — degraded/NER coherence forfeits that
  contribution.
- Message-level follow-up diagnosis
  (`research/gaming_volatility_diagnosis_spike.py`, findings appended to
  `docs/signal_diagnosis_2026-07.md`): gaming's `vocab` sub-score is
  arithmetically identical to `ttr` above the 50-token floor (TTR silently
  double-weighted; constraint note added in `signals/gaming.py`) and its
  heuristics correlate with newsroom practice, not manipulation — redesign
  candidate; volatility's 0.4 spike threshold is locally the worst setting
  tried (0.1–0.3 give ρ ≈ −0.12…−0.15 in the correct direction on both
  splits, ~3× current information, ceiling: 48.9% of messages have TextBlob
  polarity exactly 0); silence strengthens slightly and consistently at
  ≥ 96 h (ρ −0.47 vs −0.43, plateau from 96 h). All candidate changes are
  gated on the recalibrate → future-holdout revalidate cycle.

### Changed
- `requires_human_review` / `requires_review` is now `true` for evaluations
  below the evidence minimum, regardless of score or band (see the
  minimum-evidence guardrail above).

### Security
- The bundled nginx now **overwrites** `X-Forwarded-For` with `$remote_addr`
  instead of appending to it (`$proxy_add_x_forwarded_for`): the app takes the
  *first* entry of the header and records it in the GDPR audit log, so a
  client-supplied header could forge the audited IP even behind the proxy.
  Regression-tested (`tests/unit/test_security.py`).
- Failed API-key attempts are now rate-limited per client IP (429 beyond the
  sliding window). Previously the limiter only ran after successful
  verification, leaving key brute-forcing unthrottled at the app layer.
- `docker-compose.yml` no longer publishes the app's port 8000 on the host:
  the API is reachable only through nginx, so the proxy's rate limiting,
  security headers and `X-Forwarded-For` rewrite cannot be bypassed.

### Fixed
- The API now starts when the spaCy model is missing: `lifespan` crashed on a
  missing/broken `it_core_news_lg`; it now logs `spacy_model_unavailable` and
  serves in the documented degraded mode (neutral zero-confidence NER
  coherence, `/health` reports `nlp: "not_loaded"`).
- The Docker image now ships `data/calibrated_weights.json`. Pointing
  `CATS_WEIGHTS_FILE` at it inside the container hit the missing-file fallback
  and silently scored with the static, unvalidated weight estimates.
- `normalize_messages` sorts chronologically under mixed UTC offsets:
  timestamps are normalised to UTC before sort/dedup (the previous ISO-string
  sort mis-ordered mixed-timezone histories, skewing the temporal signals;
  naive timestamps are taken as UTC). Non-string `text`/`timestamp` entries
  and non-dict records are now counted and skipped instead of raising
  `AttributeError` from `cats.lite` on non-text input.
- `make split` no longer litters the repo root with `train.jsonl` /
  `holdout.jsonl`: outputs go to the gitignored `data/splits/`, and the CLI's
  default output names are gitignored at the root as a safety net. Missing
  `.PHONY` declarations (`docker-logs`, `db-downgrade`, `generate-key`) added.
- `docs/compliance.md` asserted CATS is a "Limited Risk AI System" under the
  EU AI Act — a legal determination that contradicts the *pending*
  classification decision tracked in `docs/eu_ai_act/classification.md`.
  Softened to "pending legal decision" with a pointer to the classification
  prerequisite; the same doc's stale accuracy rows (weights described as
  uncalibrated) and version roadmap were brought up to the v1.5.0 state.
- Documentation state sync: `docs/README.md` was an empty stub (now a full
  index), `CITATION.cff` still cited version 1.3.0 (now 1.5.0),
  `SUMMARY.md`/README lacked `docs/cloud_setup.md`, the README roadmap was
  frozen at v1.3.1, and `docs/architecture.md`/`docs/api.md` did not describe
  the response-time guardrail blocks.
- Alembic migrations now honour the `DATABASE_URL` environment variable
  (falling back to `alembic.ini`): `alembic upgrade head` / `make db-migrate`
  previously always targeted the hardcoded localhost `cats` database and
  failed in the CI/cloud test environments, which configure `cats_test`.
- `CONTRIBUTING.md` no longer directs pull requests at the non-existent
  `develop` branch (PRs target `main`); the inert `develop` push trigger was
  removed from CI.
- README license links pointed at `LICENSE/` (404 on GitHub); now `LICENSE`.
- The future-snapshot validation was misdated "28 July 2026" in the findings
  title and its citations — it ran on **6 July 2026** (commit `2b41982`).
  Living docs and code comments now carry the correct date; the findings
  filename and released changelog entries are kept for link stability.

---

## [1.5.0] — 2026-07-08

### Added
- **Domain-provenance penalty (ENGINE 1.4).** Signal-hardening so discriminative
  power no longer rests on `silence` alone: impersonation/clone domains
  (rare/cheap TLDs, free-hosting subdomains, brand typo-squats) now lower a
  source's score via an asymmetric post-aggregation penalty
  (`score − 0.6 × domain_red_flag`, clamped at 0), applied when a source URL is
  supplied (`context["url"]`, `cats.lite.score(url=…)`). Red-flags come from
  general domain structure only, never the labelled disinfo set. Validated on
  the 28 Jul 2026 future holdout: pairwise concordance **0.755 → 0.775**, every
  correction a low-reliability clone (reproduce via
  `research/validate_domain_penalty.py`). The four calibrated behavioural weights
  are unchanged; `/explain` reports the penalty separately. Not a weighted fifth
  signal — a symmetric term would reward clean domains and inflate the low tail
  (fake-news on ordinary domains). See `docs/architecture.md`,
  `docs/signal_research_2026-07.md`.

### Changed
- **`ENGINE_VERSION` 1.3 → 1.4.** Scores of sources evaluated with a red-flagged
  URL are not comparable with earlier engines; `/explain` flags rows scored
  under a previous engine. Sources evaluated without a URL are unaffected.

---

## [1.4.0] — 2026-07-07

### Added
- Validated calibrated weights shipped as the recommended production table in
  `data/calibrated_weights.json` — point `CATS_WEIGHTS_FILE` at it.
- Cloud setup guide for Claude Code on the web (`docs/cloud_setup.md`):
  environment setup script, CI-mirrored test env vars, and per-phase network
  access for running linters and the test suite in a fresh cloud session.

### Changed
- **Calibrated weights validated on a future snapshot (28 Jul 2026).**
  Calibrated on the merged 02/03/05-Jul snapshots, evaluated on the unseen
  06-Jul snapshot: pairwise concordance **0.755** (> 0.70 target), Spearman
  **+0.553**, 79.2% band agreement within one band, low tail discriminating
  correctly. Accuracy declaration and `docs/calibration_findings_2026-07-28.md`
  updated.

### Fixed
- Calibrated weight files whose independently-rounded entries summed to just off
  1.0 (e.g. 1.000001) were rejected by `_validate_weights`, silently falling
  back to the static table so the calibrated weights never loaded. The check now
  accepts a loose tolerance and renormalises, and rejects only genuinely
  malformed tables (sum ≤ 0 or off by > 1e-3).
- Audit purge reads the deleted-row count defensively (`getattr`) — the DELETE
  `CursorResult` exposes `rowcount`, but the base `Result` type does not, which
  broke the mypy CI check.

---

## [1.3.1] — 2026-07-05

### Fixed
- **`CATS_WEIGHTS_FILE` and `CATS_API_KEYS` were silently ignored** — the
  settings fields only matched the bare `WEIGHTS_FILE`/`API_KEYS` names, so
  calibrated weights and multi-tenant keys configured as documented never
  loaded. Both documented spellings are now accepted (validation aliases).
- Gaming: corpora under 50 tokens no longer receive a spurious maximum
  vocabulary-uniformity sub-score (+25 points); the sub-score is neutral (0).
- `/health` no longer returns raw exception strings (could leak DSNs/internal
  hostnames on an unauthenticated endpoint); details are logged instead.
  The payload now includes the running version.
- Audit purge uses a single `DELETE` statement instead of loading and deleting
  expired rows one by one.
- API version string was hardcoded at 1.2.0; now read from `cats.__version__`.

### Added
- `POST /v1/cats/contest/{contest_id}/resolve` — close a pending contest
  (`upheld`/`rejected` + response, tenant-scoped, audit-logged): the GDPR
  Art. 22 appeal flow now has its human-decision endpoint. Migration `003`
  adds `trust_scores.engine_version`.
- `/explain` flags rows scored under an older aggregation engine
  (`engine_mismatch`) instead of silently re-decomposing them with current
  semantics.
- `TRUST_PROXY_HEADERS` setting: `X-Forwarded-For` is honoured only when
  enabled (default true, matching the bundled nginx); rate limiting is now
  keyed per API key (hashed) instead of per client IP.
- Per-source-type silence thresholds table
  (`signals/silence.py:SOURCE_TYPE_THRESHOLDS`; all defaults remain 72 h —
  changing values requires recalibration).
- Docker image now downloads the TextBlob corpora (world-readable
  `NLTK_DATA`), so container sentiment matches `make nlp-download` installs.

### Removed
- Unused JWT machinery (`create_access_token`/`verify_token`/`init_jwt_keys`)
  and the `python-jose` dependency: no route ever consumed tokens — auth is
  API-key based. `cryptography` unpinned to `<50`.

---

## [1.3.0] — 2026-07-05

### Added
- **`cats.lite`** — zero-infrastructure scoring: `from cats.lite import score`
  runs the 4-signal pipeline + aggregation as a plain library call (no
  PostgreSQL, no Redis, no API keys). Same signals, same explainability,
  same caveats as `/evaluate`.
- `CITATION.cff` for academic citation.
- PyPI-ready packaging: the project builds as **`cats-scoring`** with the
  library-surface dependencies only (`pip install cats-scoring[sbert]` for the
  multilingual coherence backend); the API deployment stack stays in
  `requirements.txt`. Colab demo notebook in `examples/cats_lite_demo.ipynb`.

### Changed
- **Signal polarity fix in `aggregate_score`** — the higher-is-worse signals
  (volatility, silence, gaming) are now inverted (`100 − value`) before the
  weighted average, so every signal enters the score as a reliability
  contribution. On ≤ 1.2.x the one empirically informative signal (silence)
  entered the average backwards, making calibrated weights rank a documented
  disinformation source *highest* on the July 2026 holdout (Spearman −0.42 →
  +0.32 with the fix; band agreement 0% → 90% within one band). See
  `docs/calibration_findings_2026-07.md` and the updated design decision in
  `docs/architecture.md`.
- `/explain` signal details now include `polarity` and `reliability_value`
  (the inverted value actually aggregated); `contribution`/`score_share_pct`
  are computed on the reliability axis so they decompose the real score.

### Breaking
- Trust scores are **not comparable** with scores produced by ≤ 1.2.x.
- Weights calibrated under the pre-1.3 engine are invalid — recalibrate with
  `python -m cats.calibration` (recalibrated weights for the July 2026
  snapshots ship in `data/calibrated_weights.json`).

---

## [1.2.0] — 2026-06-29

### Added
- Optional Sentence-BERT coherence backend (`COHERENCE_BACKEND=sbert`, model via
  `COHERENCE_MODEL`): mean cosine similarity of consecutive message embeddings.
  `sentence-transformers` is optional (`requirements-sbert.txt`); falls back to
  the spaCy NER backend when unavailable, so the default stays light.
- Per-signal attribution in `/explain`: `score_share_pct` (each signal's share
  of the weighted score) and `primary_driver` — a dependency-free, SHAP-style
  breakdown of *why* a source got its score.

---

## [1.1.0] — 2026-06-29

### Added
- Optional BERT Italian sentiment backend for the volatility signal
  (`SENTIMENT_BACKEND=bert`, model configurable via `SENTIMENT_MODEL`).
  `transformers`/`torch` are optional (`requirements-bert.txt`); the backend
  falls back to TextBlob when they are unavailable, so the default stays light.
- Row-level multi-tenancy: a `tenant_id` (bound to the API key via the optional
  `CATS_API_KEYS` "key:tenant" map, never client-supplied) is stored on every
  `TrustScore` / `AuditLog` / `Contest`, and all reads (`/explain`, `/contest`,
  `/review`, `/stats`) are scoped to the caller's tenant. Backwards compatible:
  unlisted keys resolve to the `default` tenant. Migration `002`.
- `POST /v1/cats/batch` endpoint: evaluate multiple sources in one request
  (1–50 items), persisted atomically in a single transaction.
- Prometheus metrics at `GET /metrics` (`prometheus-client`): HTTP request
  count/latency (labelled by route template) plus `cats_evaluations_total`
  (by band) and a `cats_trust_score` histogram.
- nginx reverse-proxy config (`deploy/nginx.conf`) wired into `docker-compose`:
  per-IP rate limiting (30 req/min), security headers, correct
  `X-Forwarded-For`, and a documented TLS 1.3 server block.
- Weight calibration toolkit (`cats.calibration`): dependency-free genetic
  search that tunes per-source-type signal weights against a labelled dataset,
  optimising rank-agreement (Spearman / pairwise concordance). Calibrated
  weights are served via the `CATS_WEIGHTS_FILE` setting. See
  [docs/calibration.md](docs/calibration.md). GA design inspired by
  SantanderAI/genetic-algorithm (Apache-2.0).

### Fixed
- `compute_coherence` no longer crashes when the spaCy model is not loaded
  (`nlp is None`): it degrades gracefully to a neutral, zero-confidence signal,
  consistent with `/health` reporting `nlp: not_loaded`.
- CI is green again: applied black/isort across the codebase and fixed the
  remaining flake8/mypy errors plus structlog-config and test-isolation bugs
  that had been failing every run.
