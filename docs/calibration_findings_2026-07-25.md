# Recalibration on the fixed split — 2026-07-25

Second recalibration attempt, run after the temporal split was corrected in
PR #56 (message axis instead of source axis). The previous attempt
(`docs/calibration_findings_2026-07-24.md`) could not validate because its
holdout carried effectively two labels; that obstacle is gone.

**Disposition: no weights shipped.** `data/calibrated_weights.json` and the
committed train/holdout files are unchanged. The reason is different from last
time, and the run produced one clearly positive result plus one operational
trap worth fixing.

## Pipeline

```bash
python -m cats.calibration.merge_snapshots --inputs data/snapshots/*.jsonl --out merged.jsonl
python -m cats.calibration.split --input merged.jsonl            # message axis (new default)
python -m cats.calibration.build_dataset --input {train,holdout}_sources.jsonl --out {train,holdout}.jsonl
python -m cats.calibration --dataset train.jsonl --metric spearman --seed 42
python -m cats.calibration.evaluate --dataset holdout.jsonl [--weights …]
```

59 sources merged from the six committed snapshots (2 632 duplicate messages
skipped). Everything below ran with `COHERENCE_BACKEND=sbert` unless stated —
see *The trap* for why that qualifier matters more than it looks.

## The one result that is stable

**The shipped production weights beat the static WP 4.1 baseline on a holdout
that can actually rank**, and they do it at both split fractions tried:

| Holdout | Static WP 4.1 | **Production** |
|---|---:|---:|
| fraction 0.2 (n=45) — Spearman | +0.043 | **+0.127** |
| concordance | 0.515 | **0.563** |
| fraction 0.5 (n=47) — Spearman | +0.053 | **+0.141** |
| concordance | 0.527 | **0.565** |

This is the first time the shipped weights have been validated against a
future holdout with real label spread. It is a modest effect on a small
sample, but it is consistent in sign and magnitude across both configurations,
and it is the evidence that was missing on 2026-07-24.

## Why the candidate was not shipped

The candidate weights (calibrated on train, `--metric spearman --seed 42`)
**disagree with themselves across split fractions**:

| Holdout | Production | Candidate |
|---|---:|---:|
| fraction 0.2 — Spearman | +0.127 | **+0.217** |
| concordance | 0.563 | **0.606** |
| band agreement (exact) | **33.3%** | 17.8% |
| fraction 0.5 — Spearman | **+0.141** | +0.135 |
| concordance | **0.565** | 0.561 |
| band agreement (exact) | 29.8% | **36.2%** |

At 0.2 the candidate clearly wins on ranking and clearly loses on band
agreement. At 0.5 the ranking difference vanishes and the band agreement
reverses. A difference whose *sign* depends on a split parameter is not a
difference; at n≈46 with five label levels, this is the noise floor.

Shipping the 0.2 result would mean selecting the configuration that flatters
the candidate, having already seen both — the same circular validation refused
on 2026-07-24. Note the 0.5 fraction was **not** chosen because it scored
better: it was chosen to test a mechanical hypothesis (below), before its
holdout numbers were known, and the default 0.2 was then re-run under identical
conditions specifically so that neither could be quietly dropped.

## The trap: the pipeline degrades silently, and it inverts the conclusion

The first pass of this run used the **default** `COHERENCE_BACKEND=ner`,
because `sentence-transformers` is an optional extra (`requirements-sbert.txt`)
and was not installed. Nothing in the output said so. Under NER the coherence
signal is close to inert, and its distribution does not survive the split:

| Backend | coherence, train | coherence, holdout |
|---|---|---|
| `ner` (default) | mean 1.7, sd 5.28 | mean 0.3, sd 0.63 |
| `sbert` | mean 23.3, sd 11.64 | mean 22.3, sd 7.68 |

Under `sbert` the two sides match (23.3 vs 22.3); under `ner` the signal all
but disappears from the holdout. The conclusions drawn from the two runs are
opposite: under NER every weight set scored **at or below chance** (concordance
0.455–0.470) and the honest reading was "the signals do not transfer across
time". Under SBERT the same data, same split, same seed gives production
+0.141 / 0.565 — a real if modest effect.

`docs/calibration.md` already noted that the calibrated weights assume the
SBERT backend, but a note in a document does not stop a pipeline. `build_dataset`
now prints the active coherence backend and warns explicitly that a dataset
built under `ner` must not be used to judge candidate weights against the
shipped ones.

**Corollary for anyone reading the 2026-07-24 findings:** those numbers were
produced under the same default and are therefore NER-degraded. Their
qualitative conclusion (the holdout could not validate) still holds — that
holdout had two labels regardless of backend — but the magnitudes there should
not be compared with the ones here.

## Secondary finding: window length limits the time-based signals

The default 0.2 fraction gives the holdout a **7-day** wall-clock window, and
14 of its 45 sources span under 72 hours. `silence` fires on gaps ≥72 h, so it
cannot vary for roughly a third of that holdout (sd 3.31 against 22.40 in
train). This is what motivated trying 0.5, which widens the window to 15 days —
it helps, but not enough: silence sd is still 2.74.

The ceiling here is calendar time, not tuning. The committed snapshots span
2026-07-02 → 2026-07-20 — about three weeks of real collection. No split of
three weeks yields two sides both long enough for a 72-hour-gap signal to
vary. This does not improve by collecting more often; it improves only by
collecting for longer.

(Collecting *more often* is still worth doing, for a different reason: 76% of
registered feeds expose a window shorter than 7 days, and the fastest churn 20
items in ~3 hours, so weekly polling discards most of what those sources
publish — see `docs/feed_health_2026-07.md`.)

## Two documented assumptions that did not hold

Both were tested directly in this session, from a default cloud environment:

- **`huggingface.co` is reachable.** `docs/cloud_setup.md` lists SBERT as
  needing a **Custom** network level with `huggingface.co` and
  `cdn-lfs.huggingface.co` allow-listed. The model
  (`paraphrase-multilingual-MiniLM-L12-v2`) downloaded and loaded with no
  custom allowlist. As with the spaCy model on 2026-07-24, the documented
  restriction is stricter than observed behaviour.
- **Arbitrary news domains are reachable.** The same document says tasks
  fetching arbitrary news domains "fail silently under Trusted"; 98 of 115
  registered feeds answer normally from here. The 15 that do not are blocked by
  the *destinations'* WAFs on datacenter IP reputation, which no network-level
  setting on our side changes.

## What would change the answer

1. **More calendar time.** The binding constraint. Weekly (better: daily)
   collection continuing for a few months gives both split sides a window in
   which `silence` and `volatility` can vary.
2. **More sources**, especially in the 30–50 band, which contributes 7 of 59.
3. Re-running this comparison then, with `COHERENCE_BACKEND=sbert` fixed and
   the split fraction chosen *before* looking at holdout numbers.
