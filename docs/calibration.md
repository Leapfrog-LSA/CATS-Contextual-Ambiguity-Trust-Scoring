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

### Getting `label`s without hand-annotation: distant supervision

Hand-labelling every source is the bottleneck. `cats.calibration.label_from_ratings`
reuses **existing** reliability ratings (NewsGuard, Media Bias/Fact Check,
fact-checker verdicts, NATO Admiralty Code) as labels by joining a source
catalogue (the `Fonti_OSINT` CSV) with a ratings file you supply, on normalised
hostname:

```bash
python -m cats.calibration.label_from_ratings \
    --sources Fonti_OSINT.csv \
    --ratings mbfc.csv \           # CSV (domain,rating) or JSON {host: rating}
    --scale mbfc \                 # mbfc | admiralty | numeric | custom
    --out labels.jsonl
```

Output is a **label registry** — one `{source_id, source_type, label, url, rss}`
per *matched* source (the *labels* half of a dataset). It then reports the match
rate and the label band/`source_type` distribution so you can judge coverage and
balance before investing in message collection.

> **It never invents a rating.** Every label comes from the ratings file; sources
> with no rating are dropped. The tool only joins and maps the scale onto CATS's
> 0–100 ordinal.
>
> ⚠️ **Distant-supervision caveats.** External ratings carry their own editorial
> and geographic bias; domain-level ratings apply to *every* path under that host;
> and ratings sourced from the same evidence the signals measure risk **leakage**.
> Treat distant-supervision validation as indicative, and prefer expert
> annotation for a true gold standard (see
> [eu_ai_act/data_governance_art10.md](eu_ai_act/data_governance_art10.md)).

**Next step:** attach message histories to each source, producing the
`{..., "messages": [...]}` shape below, then run `build_dataset`.

### Attaching message histories from the RSS feeds

The registry already carries each source's `rss` feed (from the catalogue).
`cats.calibration.collect_rss` fetches those feeds (RSS 2.0 / RSS 1.0 / Atom),
turns each entry into a timestamped message (title + summary, HTML stripped,
dates normalised to ISO-8601 UTC) and emits the labelled sources. Each
message's `metadata` also keeps `link`, `title_len`, pseudonymous `authors`
IDs and `categories` when the feed has them. No signal reads these fields
yet; see
[`newsguard_criteria_comparison_2026-11.md`](newsguard_criteria_comparison_2026-11.md).

```bash
python -m cats.calibration.collect_rss \
    --labels labels.jsonl \
    --out labelled_sources.jsonl
    # --min-messages 3      # skip sources with fewer usable entries
    # --max-messages 200    # keep only the N most recent entries per source
    # --since 2026-01-01T00:00:00Z   # drop older entries
    # --timeout 15 --workers 8       # HTTP timeout / concurrent fetches
```

Sources with no feed, an unreachable/unparseable feed, or fewer than
`--min-messages` usable entries are skipped with a diagnostic, so the output
only contains sources `build_dataset` can use. Defensive parsing: responses are
size-capped (`--max-bytes`) and documents carrying a DTD are rejected.

> **Snapshot caveat.** An RSS feed only exposes the *recent* window of a
> source's activity (typically 10–50 entries). That is enough for the signal
> pipeline, but re-run the collector periodically and merge snapshots if you
> want longer histories — silence/volatility estimates improve with span.
> A single snapshot also weakens the *temporal split*: fast-publishing outlets
> all share "now" as their last activity while sporadic (often low-quality)
> sources sort into the past, so the holdout ends up label-flat.

### Accumulating history across snapshots

Dated snapshots (one `labelled_sources_<YYYY-MM-DD>.jsonl` per collection
day) are collected by a scheduled workflow in the separate data repository
[`Leapfrog-LSA/cats-snapshots`](https://github.com/Leapfrog-LSA/cats-snapshots),
not in this one: at ~2–4 MB a day they had become most of this repository's
size and history. The 67 snapshots committed here before the move —
2026-07-02 through **2026-09-30** — stay under `data/snapshots/` unchanged, and
are byte-identical to the data repository's copies. They stay because the published
calibration and research results cite them by path (the 2026-07-02/03/05
training snapshots and the 2026-07-06 future holdout among them); nothing is
added there any more.

To work with the full history, download the data repository's snapshots into
the same directory. Every file is checked against the repository's
`SHA256SUMS` manifest; files already present with a matching hash are skipped,
and a local file that differs is **never overwritten** — the remote version is
saved next to it as `<name>.remote` and the command exits non-zero, so you can
union the two with `merge_snapshots`:

The data repository is **private** since 2026-11-15, so the download needs a
GitHub token that can read it. A fine-grained personal access token with
read-only *Contents* access to `Leapfrog-LSA/cats-snapshots` is enough.
Export it as `CATS_SNAPSHOTS_TOKEN` (`GITHUB_TOKEN` and `GH_TOKEN` also work).
Without it, the command stops with a 404 that names these variables.

```bash
export CATS_SNAPSHOTS_TOKEN=...   # read-only token for the data repository
make snapshots-download        # = python -m cats.calibration.fetch_snapshots
# pin a data-repo commit for a reproducible run:
python -m cats.calibration.fetch_snapshots --ref <commit-sha>
```

Downloaded files are git-ignored (`data/snapshots/*.jsonl`), so they cannot be
committed back here by accident; the files that were already tracked stay
tracked.

`cats.calibration.merge_snapshots` unions snapshots into cumulative per-source
histories (messages deduplicated on `(timestamp, text)`, newest metadata wins):

```bash
python -m cats.calibration.merge_snapshots \
    --inputs data/snapshots/*.jsonl --out labelled_sources.jsonl
```

**Timestamp sanity filter.** Some feeds mix old or mis-dated items into their
"recent" window: a literal `1970-01-01` parser default, a feed serving
2022–2024 archive items. Merged into a history, they create multi-year fake
gaps that distort `silence` and `volatility`
([snapshot history audit](snapshot_history_audit_2026-09.md)). Use the
filter for any new calibration dataset built from the accumulated snapshots:

```bash
python -m cats.calibration.merge_snapshots \
    --inputs data/snapshots/*.jsonl --out labelled_sources.jsonl \
    --not-before 2026-06-01 --not-after <date of the newest snapshot>
```

- **What it keeps:** only messages dated within those whole UTC days, both
  ends inclusive. Once a bound is set, messages with an unparseable
  timestamp are dropped too.
- **The floor:** `2026-06-01` is the audit's data-driven break, not a guess.
  January–May 2026 held only 109 messages across all sources, then June
  jumps to 458.
- **The ceiling:** pass it explicitly and never default to "today", so a
  build gives the same output whenever it is re-run.
- **The report:**
  - A source the filter empties is **excluded and named**, because the
    temporal split cannot place a source without a timestamp.
  - A source that loses more than half its messages is kept but **flagged
    for a feed-health check**.
- **Defaults and scope:** the filter is off by default. Without the flags,
  the output is byte-identical to before, so the shipped July calibration
  inputs stay reproducible. It only affects the calibration dataset, never
  live scoring.

The strongest validation this enables: calibrate on the merged history up to a
cutoff, then validate on a **later snapshot** the calibrator never saw
(`split --cutoff <date of the last calibration snapshot>`).

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

Each output record carries `source_type`, `signals` and `label` exactly as
before, plus one extra top-level key, `diagnostics` (never inside `signals`):
`source_id` (from the input, `null` when absent), `n_messages` (after
normalisation), `span_hours` (first to last message, `null` with fewer than
two), `signal_confidence` (per-signal `SignalResult.confidence`) and
`language` (`italian` / `other` / `unknown`, from
`cats.pipeline.language.detect_language`). It is **diagnostics only**:
`load_dataset`, calibration and `cats.calibration.evaluate` ignore it, so it
never weights, filters or excludes a sample, and it holds no message text. The
language detector is a function-word heuristic that only separates Italian
from "other" or "uncertain" (`unknown`). `research/holdout_composition.py`
counts a dataset's label x language mix from it; records without
`diagnostics` (all datasets committed before it existed) count as `unknown`.

`source_id` is optional (diagnostics only); records missing a `label` or
`messages` are skipped with a warning. The spaCy NER model is loaded once up
front so coherence runs at full fidelity — run `make nlp-download` first, or
expect coherence to degrade to a neutral value (exactly as a request does when
the model is unavailable). A sample input lives at
[`examples/labelled_sources_sample.jsonl`](../examples/labelled_sources_sample.jsonl).

> **Avoid leakage:** the `label` must come from independent ground truth (expert
> annotation, external ratings, later-confirmed outcomes) — never derive it from
> the same signals being calibrated. Use a **temporal** train/holdout split.

### Temporal train/holdout split

Split labelled sources **by time** before building the dataset — calibrate on the
past, validate on the future. `cats.calibration.split` offers two axes:

```bash
# default: cut every source's message history at a shared boundary
python -m cats.calibration.split --input sources.jsonl --holdout-fraction 0.2
# or a fixed boundary (messages at/after the cutoff form the holdout):
python -m cats.calibration.split --input sources.jsonl --cutoff 2026-01-01T00:00:00Z
# legacy: hold out whole unseen sources, ranked by their most recent message
python -m cats.calibration.split --input sources.jsonl --axis source
```

**Use the default `message` axis unless you know why you want the other one.**
On RSS data the `source` axis is degenerate: every live feed's newest message is
hours old at collection time, so ranking sources by it ranks them by *publishing
frequency*, which is close to a proxy for the label. Measured on the 2026-07-20
snapshot, Spearman(recency, label) = **+0.539**; on the merged 59-source pool the
`source` axis yields a 12-source holdout of which 11 are labels 70/85, while the
`message` axis yields 45 sources spanning five labels including the disinfo tail.
That degenerate holdout is what stopped the 2026-07-24 recalibration
(`docs/calibration_findings_2026-07-24.md`).

The `message` axis puts a source on **both** sides — earlier behaviour trains,
later behaviour validates — so it measures drift rather than generalisation to
unseen sources. With four weights there is no capacity to memorise a source, so
the overlap is not leakage; if you specifically want the unseen-source question,
`--axis source` still asks it, and becomes trustworthy once the pool is large
enough for its newest slice to be label-diverse on its own.

A side is dropped when it holds fewer than `--min-messages` (default 3, the same
floor `collect_rss` applies) — below that the behavioural signals are not
estimable. Both axes print the label distribution of each side and warn when a
holdout carries fewer than three distinct labels, since such a holdout cannot
rank anything.

It writes `train.jsonl` / `holdout.jsonl` (labelled-sources shape), which you
then run through `build_dataset` separately. Run `split` **before** `build_dataset`
because the post-build records carry no timestamp.

### End-to-end pipeline

```
sources.csv + external ratings
        │  label_from_ratings        → label registry
        │  collect_rss               → + messages from the RSS feeds
        ▼
labelled sources ──split──▶ train/ holdout
        │ build_dataset                    │ build_dataset
        ▼                                  ▼
   train.jsonl ──calibrate──▶ weights.json │
                                  └──────▶ evaluate(holdout) / report → accuracy declaration
```

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
CATS_WEIGHTS_FILE=/path/to/calibrated_weights.json   # e.g. data/calibrated_weights.json
```

`cats.scoring.weights.get_dynamic_weights` loads this table at runtime and uses
it per source-type group, falling back to the static estimates when the setting
is unset or the file is missing/invalid.

> **Validated for production, most recently 28 Aug 2026.** `data/calibrated_weights.json`
> was originally validated on a **future** snapshot the calibrator never saw
> (6 Jul 2026): pairwise concordance 0.755, Spearman +0.553, band agreement
> 79.2% within one band, low tail discriminating correctly (see
> [calibration_findings_2026-07-28.md](calibration_findings_2026-07-28.md)).
> Since then, three diagnosed signal bugs (gaming's duplicated sub-score, a
> mistuned volatility threshold, a short silence threshold) were fixed, each
> with its own recalibration + future-holdout revalidation cycle on the same
> 56/53-source split — see
> [gaming_redesign_2026-08.md](gaming_redesign_2026-08.md),
> [volatility_retune_2026-08.md](volatility_retune_2026-08.md) and
> [silence_retune_2026-08.md](silence_retune_2026-08.md). **Current numbers:
> concordance 0.750 (0.762 with the domain-provenance penalty), Spearman
> +0.554 (+0.578)** — no regression from the original result, small
> movement within GA/measurement noise. These are the recommended
> production weights. **Caveat:** the result still rests mostly on the
> *silence* signal; coherence is a load-bearing tie-breaker; volatility and
> gaming carry little rank information even after their bugs were fixed — a
> content-credibility signal and a cross-source corroboration signal were
> both investigated as replacements and rejected on real data (see
> [content_credibility_spike_2026-08.md](content_credibility_spike_2026-08.md),
> [cross_source_corroboration_spike_2026-08.md](cross_source_corroboration_spike_2026-08.md)) —
> so re-validate before relying on CATS against an adversary who can manage
> their publishing cadence.
>
> **Backend requirement:** these weights were calibrated with the **SBERT**
> coherence backend, and the ablation diagnosis
> ([signal_diagnosis_2026-07.md](signal_diagnosis_2026-07.md)) shows coherence
> is the second-largest contributor to the validated concordance (LOSO
> −0.139). Deploy them with `COHERENCE_BACKEND=sbert`; with the default NER
> backend (or a missing spaCy model) that contribution is forfeited.

## 4. Evaluate scoring quality (eval harness)

Calibration *tunes* weights; the eval harness *measures* how well a given weight
set ranks sources against ground-truth labels — i.e. **are the score bands
meaningful?** It reuses the same metrics calibration optimises, so the numbers
are directly comparable.

```bash
make eval                       # static (WP 4.1) weights on the sample dataset
# or, with full control:
python -m cats.calibration.evaluate \
    --dataset examples/calibration_sample.jsonl \
    --weights calibrated_weights.json \   # omit to use the static estimates
    --json                                # machine-readable output
```

It reports Spearman, pairwise concordance, a per-(predicted-)band table
(count, mean predicted score, mean label), **band agreement** (how often the
predicted band matches the band the label falls into, exact and within one
band), **per-class precision/recall/F1** (see below), and a per-`source_type`
breakdown.

### Per-class F1 — reading the low tail

Rank metrics average over the whole score range. A source set can rank well
overall while the *low tail* — the sources an analyst most needs flagged — is
missed entirely, and no single averaged number shows it. The harness therefore
also reduces both prediction and label to a binary class via `determine_band`
(`unreliable` = bands `low`/`very_low`, i.e. below 40; `reliable` = the rest)
and reports precision, recall and F1 for each side, plus their macro-F1.

The split is *derived* from the band cutoffs rather than hard-coded, so
changing the band thresholds moves it automatically — there is no second
threshold to keep in sync. A class with no labelled members (or no
predictions) reports `n/a` rather than `0.0`: the data cannot define the
quantity, which is not the same as the scorer failing.

On the 06-Jul-2026 future holdout with the shipped calibrated weights:

```text
Concordance (AUC~) : 0.750
Macro-F1           : 0.692

Per class (unreliable = bands low/very_low):
  class         supp  pred  precis  recall      f1
  unreliable      15     5   1.000   0.333   0.500
  reliable        38    48   0.792   1.000   0.884
```

Read together: every source CATS calls unreliable on this holdout *is*
unreliable, but it calls only 5 of the 15 — recall 0.333. That is
[§3.1 of the roadmap](piano_sviluppo_roadmap_2026-07.md) ("discrimination
rests on one signal") stated as a number instead of a description, and it is
the figure the Phase D recalibration has to move. Both figures rest on 53
sources; the perfect precision in particular is measured over 5 predictions
and should be read as small-sample.

**Before vs after calibration** is a one-command comparison and shows why
calibration matters on this dataset:

```text
# static WP 4.1 weights
Spearman           : -0.888      # anti-correlated!
Band agreement     : 16.7% exact, 50.0% within 1 band

# calibrated weights (python -m cats.calibration ... --seed 7)
Spearman           : +0.993
Band agreement     : 33.3% exact, 100.0% within 1 band
```

> **Polarity note (changed in v1.3.0).** Since v1.3.0 `aggregate_score` inverts
> the higher-is-worse signals (volatility, silence, gaming: `100 − value`)
> before the weighted average, so all weights are non-negative importances on a
> common reliability axis. Weights calibrated under the pre-1.3 engine are
> **invalid** — recalibrate. On ≤ 1.2.x the sample numbers above could even
> come out anti-correlated for the static weights; the July 2026 findings
> ([calibration_findings_2026-07.md](calibration_findings_2026-07.md)) document
> the defect on real data and the motivation for the change — see
> [architecture.md → Signal Polarity & Scoring](architecture.md#signal-polarity--scoring-design-decision).


### Uncertainty and paired comparison (optional)

Every number above is a point estimate on a few dozen sources. The harness can
also report how much it would move under resampling, and whether a candidate
weight table beats another *on the same rows*:

```bash
python -m cats.calibration.evaluate \
    --dataset holdout.jsonl \
    --weights candidate_weights.json \
    --bootstrap-replicates N \        # required, no default
    --bootstrap-level L \             # required, no default; strictly between 0 and 1
    --bootstrap-seed S \              # optional, default 0
    --compare-weights production_weights.json   # or the literal `static`
```

- **Method:** percentile bootstrap — dataset rows are resampled with
  replacement (stdlib `random.Random(seed)`, like the GA), scores are computed
  once per weight table with `predict_scores` and resampled by index, and the
  interval ends are the `(1−L)/2` and `(1+L)/2` percentiles of the defined
  replicates (linear interpolation). The method name, replicates, seed and level
  are printed with the result.
- **Metrics:** pairwise concordance, Spearman and the `unreliable` recall.
- **Undefined replicates are excluded and counted, never scored as 0:**
  concordance when the replicate has a single distinct label, Spearman when its
  predictions or labels are constant, `unreliable` recall when it contains no
  label below 40. The `excluded` column reports the count per metric.
- **Paired comparison (`--compare-weights`):** the same resampled rows are
  applied to both tables and the interval is for the difference
  `--weights table − --compare-weights table`; the point estimate of each table
  and their difference are printed alongside. A table compared with itself gives
  a difference of exactly 0.
- **Resampled unit:** the dataset row. Records carry no source identifier, so
  on a `message`-axis split a row is a source *slice*, not a whole source.
- **Output:** a trailing `Uncertainty:` section in the text output, a separate
  `uncertainty` key in `--json`. `--bootstrap-replicates` and
  `--bootstrap-level` are both required as soon as any of these options is
  given. **Without these options the output is byte-for-byte what it was
  before.**

No replicate count or level is recommended here: for the January 2027
recalibration they are open decisions (see below).

## Validation protocol for the January 2027 recalibration

> **Status: draft, to be completed and dated by the maintainer before
> 12 January 2027** — i.e. before the January holdout data is looked at. It
> fixes *how* the recalibration will be judged; it does not record any result.
> Every item marked *to be decided by the maintainer* is deliberately left
> open. The roadmap exit criterion (`docs/piano_sviluppo_roadmap_2026-09.md`,
> *Ricalibrazione completa*) is concordance ≥ 0.78 on a future holdout of
> **≥ 100 sources** with improving low-tail recall; runs on the current
> 53-source holdout only exercise the tooling and say nothing about that
> criterion.

**Fixed requirements**

1. **Coherence backend:** run with `COHERENCE_BACKEND=sbert`. The published
   weights were calibrated with SBERT (see *Backend requirement* in §3); a run
   on another backend is not comparable.
2. **Split declared before looking at the holdout:** the axis
   (`--axis message` or `--axis source` of `cats.calibration.split`) and the
   `--holdout-fraction` or `--cutoff` are written into this section before any
   holdout metric is computed, and not changed afterwards.
3. **Two protocols, reported separately** — they are not the same measurement
   (`docs/calibration_findings_2026-08-21.md` explains why 0.755 and 0.537 are
   not a regression):
   - *Future snapshot:* a whole later snapshot never used in calibration. Here a
     row is a **source**.
   - *Message-axis cut:* every source's history cut at a shared boundary. Here
     a row is a **source slice**, and the same source appears on both sides.
4. **The `Per predicted band` table is mandatory at every checkpoint** (the
   harness already prints it), so a collapse into one band is visible next to
   the rank metrics.
5. **Every point estimate is reported with its interval and with the paired
   comparison candidate vs production** (`--compare-weights` with the shipped
   `data/calibrated_weights.json`), using the replicates, level and seed fixed
   below.

**Open decisions**

- Resampling unit for January: source or source slice (the tool resamples
  dataset rows; on a message-axis cut a row is a slice) — *to be decided by the
  maintainer*.
- Number of bootstrap replicates — *to be decided by the maintainer*.
- Interval level — *to be decided by the maintainer*.
- Seed — *to be decided by the maintainer*.
- Interval method (the tool implements the simple percentile bootstrap; another
  method would be a separate change) — *to be decided by the maintainer*.
- Which quantity is compared with 0.78: the harness's pairwise concordance (the
  roadmap says "concordanza") or "AUC-ROC" as worded in
  `cats/calibration/report.py`; and whether with or without the
  domain-provenance penalty (currently 0.750 without, 0.762 with) — *to be
  decided by the maintainer*.
- Whether 0.78 applies to the point estimate or to the lower end of the
  interval — *to be decided by the maintainer*.
- How "improving low-tail recall" is judged: against which reference value and
  with what margin — *to be decided by the maintainer*.
- Split axis and fraction (or cutoff) for January — *to be decided by the
  maintainer*.
- `--not-before` / `--not-after` values for the timestamp filter of
  `cats.calibration.merge_snapshots` (off by default) — *to be decided by the
  maintainer*.
- Whether intervals also appear in the accuracy declaration
  (`cats/calibration/report.py`, `docs/eu_ai_act/`); until decided, the
  declaration is unchanged — *to be decided by the maintainer (or legal)*.
- Whether the domain-penalty variant gets its own interval (today its 0.762 is
  computed only by `research/validate_domain_penalty.py`) — *to be decided by
  the maintainer*.

**Completed and dated by the maintainer:** *TODO (maintainer) — date and
sign-off before 12 January 2027.*

## 5. Accuracy declaration (EU AI Act Art. 15)

`cats.calibration.report` runs the eval harness on a holdout dataset and renders
a Markdown **accuracy declaration** for the Annex IV §6 / Art. 15 section. The
measured metrics are filled in; provenance and sign-off stay `TODO` (they need
human/legal input — the generator never fabricates them).

```bash
python -m cats.calibration.report \
    --dataset holdout.jsonl \
    --weights calibrated_weights.json \   # omit to use the static estimates
    --out docs/eu_ai_act/accuracy_declaration.md
```

This is the last step of the chain: once a real labelled holdout exists, going
from data to a validated accuracy declaration is a single command.

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
