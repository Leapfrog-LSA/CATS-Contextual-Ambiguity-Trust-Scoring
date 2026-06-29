# Weight Calibration

CATS ships with hand-picked signal weights (WP 4.1 initial estimates). The
`cats.calibration` package lets you replace them with **empirically calibrated**
weights learned from a labelled dataset, using a small, dependency-free genetic
algorithm.

Because CATS scores are *ordinal* rankings (WP 4.3), calibration optimises a
**rank-agreement** metric rather than absolute error.

> **Attribution.** The pluggable-fitness GA design is inspired by the public
> [SantanderAI/genetic-algorithm](https://github.com/SantanderAI/genetic-algorithm)
> project (Apache-2.0). `cats/calibration/ga.py` is an independent
> reimplementation — no third-party code is bundled and there are no runtime
> dependencies.

## 1. Build a labelled dataset

A dataset is a `.jsonl` (one object per line) or `.json` array. Each record
carries the four signal values for one evaluation plus a ground-truth `label`
expressing how reliable that source actually was (higher = more reliable).
Labels only need to be **ordinally** meaningful.

```json
{"source_type": "social",
 "signals": {"coherence": 82.0, "volatility": 30.0, "silence": 10.0, "gaming": 12.0},
 "label": 85.0}
```

`source_type` is mapped onto one of three scoring groups: `social`, `news`, or
`default` (anything else). A sample dataset lives at
[`examples/calibration_sample.jsonl`](../examples/calibration_sample.jsonl).

### Generating the `signals` automatically from labelled sources

Computing the four `signals` by hand is impractical — they come out of the same
pipeline `/evaluate` runs. `cats.calibration.build_dataset` does it for you:
given *labelled sources* (messages + a reliability `label`), it runs the
pipeline and emits the calibration `.jsonl`.

Input (`.json` array / `{"sources": [...]}` or `.jsonl`), one source per record:

```json
{"source_id": "twitter:acme",
 "source_type": "social",
 "label": 80.0,
 "messages": [
   {"timestamp": "2026-01-01T08:00:00Z", "text": "..."},
   {"timestamp": "2026-01-01T09:00:00Z", "text": "..."}
 ]}
```

```bash
python -m cats.calibration.build_dataset \
    --input examples/labelled_sources_sample.jsonl \
    --out train.jsonl
    # --source-type social   # fallback when a record omits source_type
    # --no-init-nlp          # skip spaCy load (coherence -> neutral/0-confidence)
```

`source_id` is optional (diagnostics only); records missing a `label` or
`messages` are skipped with a warning. The spaCy NER model is loaded once up
front so coherence runs at full fidelity — run `make nlp-download` first, or
expect coherence to degrade to a neutral value (exactly as a request does when
the model is unavailable). A sample input lives at
[`examples/labelled_sources_sample.jsonl`](../examples/labelled_sources_sample.jsonl).

> **Avoid leakage:** the `label` must come from independent ground truth (expert
> annotation, external ratings, later-confirmed outcomes) — never derive it from
> the same signals being calibrated. Use a **temporal** train/holdout split.

## 2. Run calibration

```bash
make calibrate
# or, with full control:
python -m cats.calibration \
    --dataset examples/calibration_sample.jsonl \
    --out calibrated_weights.json \
    --metric spearman \        # or: concordance
    --generations 80 \
    --pop-size 60 \
    --seed 7                    # for reproducible runs
```

The run reports the baseline metric (current weights) versus the calibrated
metric, and writes a weights file:

```json
{
  "metric": "spearman",
  "score": 0.83,
  "baseline_score": 0.61,
  "improvement": 0.22,
  "groups": ["default", "news", "social"],
  "weights": {
    "social":  {"coherence": 0.41, "volatility": 0.19, "silence": 0.12, "gaming": 0.28},
    "news":    {"coherence": 0.52, "volatility": 0.14, "silence": 0.21, "gaming": 0.13},
    "default": {"coherence": 0.44, "volatility": 0.20, "silence": 0.18, "gaming": 0.18}
  }
}
```

## 3. Serve the calibrated weights

Point the `CATS_WEIGHTS_FILE` setting at the output file:

```bash
# .env
CATS_WEIGHTS_FILE=/path/to/calibrated_weights.json
```

`cats.scoring.weights.get_dynamic_weights` loads this table at runtime and uses
it per source-type group, falling back to the static estimates when the setting
is unset or the file is missing/invalid.

## Metrics

| Metric | Meaning |
|---|---|
| `spearman` (default) | Spearman rank correlation between predicted scores and labels |
| `concordance` | Pairwise concordance (AUC-like); fraction of correctly ordered pairs, ties = 0.5 |

## Caveats

- Calibration is only as good as the labelled data: small or biased datasets
  produce overfit weights. Validate on a held-out split before deploying.
- Weights are normalised to sum to 1.0 per group on decode.
- This tunes the **aggregation weights** only; signal algorithms and band
  thresholds are out of scope (future work).
