# Contributing to CATS

Thank you for your interest in contributing!

## Quick start

```bash
git clone https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring.git
cd CATS-Contextual-Ambiguity-Trust-Scoring
cp .env.example .env          # edit as needed
make dev-install              # install deps + pre-commit hooks
make nlp-download             # download spaCy model
make docker-up                # start Postgres + Redis
make db-migrate               # run migrations
make test                     # all tests
```

## Development workflow

1. Fork the repository and create a feature branch: `git checkout -b feat/my-feature`
2. Write code following the project style (Black + isort; 120-char line limit)
3. Add or update tests in `tests/unit/` and/or `tests/integration/`
4. Run `make lint` and `make test` — both must pass
5. Update `CHANGELOG.md` under `[Unreleased]`
6. Open a Pull Request against `main` (the default branch; CI runs on PRs to `main`)

## Code standards

- **Python 3.11+**, async-first
- **Black** formatting, **isort** imports, **flake8** linting
- **mypy** type annotations on all public functions
- Every signal function must return a `SignalResult` subtype
- All new config must go through `cats/core/config.py` (pydantic-settings)
- Structured logging via `structlog` — no `print()` statements

## Adding a new signal

1. Create `cats/signals/my_signal.py` implementing `compute_my_signal(messages) -> MySignalResult`
2. Define `MySignalResult(SignalResult)` in `cats/signals/types.py`
3. Register in `cats/api/routes/evaluate.py` signals list
4. Add weight in `cats/scoring/weights.py` (weights must still sum to 1.0)
5. Write unit tests in `tests/unit/test_signals.py`

## Reporting issues

Use GitHub Issues with the appropriate template (bug / feature request).
For security issues, see [SECURITY.md](SECURITY.md).

## Reporting a score disagreement

If a CATS score or band for a specific source doesn't look right, open an
issue with the **"Score feedback"** template
(`.github/ISSUE_TEMPLATE/score_feedback.yml`) rather than the generic bug
report — it asks for exactly what a reviewer needs: the source URL, the
command/call and version you used, the score you got vs. the one you
expected, and your reasoning. This never changes a score automatically, and
CATS scores are ordinal rankings of behavioural reliability, not fact-checks
— explain what publishing/behavioural pattern the score seems to be missing,
not whether a specific claim is true or false.

With your explicit consent (a checkbox on the template), a maintainer may
add your case, anonymised, to `data/human_labels.jsonl` — a record of
human/CATS disagreements used only for **validation** of future
calibration, never as direct input to the signals themselves (that would be
leakage). Declining the checkbox is fine; the issue is still reviewed either
way.
