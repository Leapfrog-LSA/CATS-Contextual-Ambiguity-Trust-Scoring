# Calibration findings — 2026-07-24 recalibration attempt (not shipped)

The spaCy blocker recorded in `dataset_expansion_runbook.md` (2026-07-23) did
not reproduce this session: `python -m spacy download it_core_news_lg`
completed under the default *Trusted* network level, and
`spacy.load('it_core_news_lg')` loads correctly. With full-fidelity NER
coherence available, the end-to-end recalibration pipeline was run for the
first time since the 2026-07-06 production ship. **Result: do not ship** — see
§3.

## 1. Pipeline run

```
python -m cats.calibration.merge_snapshots --inputs data/snapshots/labelled_sources_2026-07-{02,03,05,06,13,20}.jsonl --out data/labelled_sources.jsonl
# -> 59 sources, 7337 messages (2632 duplicates skipped, feed overlap between runs)

python -m cats.calibration.split --input data/labelled_sources.jsonl --holdout-fraction 0.2 \
  --train-out data/train_sources.jsonl --holdout-out data/holdout_sources.jsonl
# -> 47 train / 12 holdout (most-recent-by-latest-message split)

python -m cats.calibration.build_dataset --input data/train_sources.jsonl   --out data/train.jsonl          # spacy_loaded model=it_core_news_lg
python -m cats.calibration.build_dataset --input data/holdout_sources.jsonl --out data/holdout_future.jsonl # spacy_loaded model=it_core_news_lg

python -m cats.calibration --dataset data/train.jsonl --metric spearman
# -> train Spearman baseline 0.3258 -> calibrated 0.4796 (Δ +0.1539)
```

This is the first calibration run against all six committed weekly snapshots
(the 2026-07-13 and 2026-07-20 snapshots — collected post feed-repair, PRs
#42/#44/#45 — had never been merged into `data/labelled_sources.jsonl`
before). The merged pool grew from the shipped 50 sources to 59.

## 2. Validation on the future holdout

`cats.calibration.evaluate --dataset data/holdout_future.jsonl`, three weight
sets:

| Weights | Spearman | Concordance | Band agreement |
|---|---:|---:|---:|
| Static WP 4.1 baseline | −0.076 | 0.436 | 0% exact, 58.3% within 1 |
| **Current production** (`data/calibrated_weights.json`, Jul-6 vintage) | +0.000 | **0.487** | 0% exact, 58.3% within 1 |
| New candidate (calibrated on the 47-source train split above) | −0.272 | 0.359 | 0% exact, 58.3% within 1 |

The new candidate underperforms **both** the static baseline and the weights
already in production. This is a hard stop under CLAUDE.md's "recalibration +
re-validation" rule — a change that doesn't validate must not ship.

## 3. Root cause: the 12-source holdout has almost no label spread

```
$ python -c "... print label per holdout record ..."
10.0, 70.0, 85.0, 70.0, 85.0, 85.0, 70.0, 70.0, 70.0, 70.0, 70.0, 85.0
```

11 of 12 holdout sources sit at label 70 or 85 (Mostly-Factual / High); one
label-10 disinformation outlier; nothing at 30/50/95. `split.py`'s temporal
split orders by each source's **most recent message timestamp** and takes the
newest 20% — with only 59 sources total, that slice happens to be dominated by
outlets the recent feed-health rounds repaired or added (mainstream,
mid/high-reliability by construction), not a representative cross-section.
Rank-correlation metrics on a near-constant label vector are dominated by
noise, which is consistent with all three weight sets scoring far below the
2026-07-06 production validation (concordance 0.755 on a 53-source, full-band
holdout — see the `2b41982` commit message).

This is a **dataset-size** problem, not a signal-quality regression, and not
fixable by retrying different `--holdout-fraction` values until one scores
well (that would be circular/cherry-picked validation, not honest
re-validation per CLAUDE.md). The fix is the dataset_expansion_runbook's
existing ≥100-source, cross-band target: grow the labelled pool (especially
low/mixed-band Italian and non-Italian sources with active feeds) before the
next recalibration attempt.

> **Superseded in part — read `docs/calibration_findings_2026-07-25.md` first.**
> Two things about this report changed the day after it was written. The root
> cause diagnosed here (a holdout with no label spread) was a defect in the
> *split axis*, fixed in PR #56, so the "wait for a larger pool" conclusion was
> premature. And every number here was produced under the default
> `COHERENCE_BACKEND=ner`, which leaves the coherence signal close to inert —
> the qualitative finding stands (that holdout carried two labels under any
> backend), but the magnitudes must not be compared with SBERT-backed runs.

## 4. Disposition

`data/calibrated_weights.json`, `data/train.jsonl`, `data/holdout_future.jsonl`,
`data/train_sources.jsonl`, `data/holdout_sources.jsonl`, and
`data/labelled_sources.jsonl` are **left at their committed 2026-07-06 (`2b41982`)
state** — the 59-source merge and the derived split described above were run
locally to produce this report and then discarded (`git checkout --`) rather
than committed, to avoid shipping a known-non-validating split as if it were
the current reference. Re-run the pipeline in `dataset_expansion_runbook.md`
once the pool is larger and more band-diverse.
