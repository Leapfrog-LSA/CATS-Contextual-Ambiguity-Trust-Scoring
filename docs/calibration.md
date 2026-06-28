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
