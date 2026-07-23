## What this is

<!-- One or two sentences: what changed and why. -->

## Changes

<!-- Bullet list of the concrete changes. -->

## Verification

<!-- How you confirmed this works — required before requesting review, per CONTRIBUTING.md: -->

- [ ] `make lint` passes (black, isort, flake8, mypy)
- [ ] `make test` passes (or `pytest tests/unit/` if integration services aren't available)
- [ ] `CHANGELOG.md` updated under `[Unreleased]` (if user-facing)
- [ ] No `cats/labels.jsonl` / weight-table changes without the recalibration + future-holdout revalidation CLAUDE.md requires (if applicable)

## Related issues

<!-- Closes #123, relates to #456 -->
