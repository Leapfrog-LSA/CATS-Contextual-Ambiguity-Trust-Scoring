# CATS — Data Governance (Art. 10)

> **Regulation (EU) 2024/1689, Article 10.** Governance and quality of the
> training, validation and testing data used by a high-risk AI system.
>
> ⚠️ **Not legal advice.** Template pre-filled from current CATS behaviour;
> `TODO` markers flag provider decisions and data work. Mandatory only if CATS
> is high-risk (see [`classification.md`](classification.md)).

## 0. A note on what data CATS actually "trains" on

CATS is **not** an end-to-end trained model. Its scoring is a weighted
aggregation of four hand-designed signals. The data-governance surface is
therefore narrower than for a deep-learning system, and concentrates on:

1. The **calibration / labelling dataset** used to tune signal **weights**
   (`cats/calibration/`, [`../calibration.md`](../calibration.md)).
2. The **third-party NLP models** CATS relies on (spaCy `it_core_news_lg`,
   TextBlob, optional BERT / Sentence-BERT) and their training provenance.
3. The **runtime input data** (OSINT source messages) — operational, not
   training data, but in scope for bias and representativeness.

> The general source registry (e.g. `Fonti_OSINT_v*.csv`: ~5k OSINT outlets with
> URL/RSS/language/country metadata) is a **source catalogue, not a labelled
> calibration dataset** — it carries no reliability labels. To become calibration
> data it must be paired with messages + reliability labels in the
> `{source_type, signals, label}` JSONL shape (`cats/calibration/dataset.py`).

## 1. Calibration dataset — design (Art. 10(2))

| Aspect | Description / TODO |
|---|---|
| Unit of labelling | **(source + time window of messages) → ordinal reliability label**, *not* per-message truth |
| Format | `.jsonl`, one `{source_type, signals{coherence,volatility,silence,gaming}, label}` per line |
| Label scale | 0–100 ordinal (ranking only need be sensible); calibration optimises rank agreement (Spearman/concordance) |
| Label sources | TODO: (a) expert annotation (e.g. NATO Admiralty Code A–F mapped to bands), (b) external ground truth (NewsGuard / MBFC / fact-checker verdicts, platform CIB takedown lists), (c) proxy (later-suspended sources → low) |
| Inter-annotator agreement | TODO: ≥2 annotators/source, report Cohen's κ / Krippendorff's α (target ≥ ~0.6) |
| Collection methodology | TODO: document how sources/messages were sampled |

## 2. Relevance, representativeness, completeness (Art. 10(3))

> TODO: characterise the calibration dataset:
- Coverage across **all five bands** and each `source_type` (social / news /
  default) — avoid class imbalance.
- Coverage across **languages and regions** present in deployment (the source
  catalogue is heavily multi-lingual/international; CATS itself is
  Italian-optimised — a known representativeness gap, R3).
- Volume: target at least a few hundred labelled sources **per `source_type`**
  for stable weights.

## 3. Bias examination & mitigation (Art. 10(2)(f)–(g))

> TODO: examine and document possible biases:
- **Language bias** — Italian-tuned NLP underperforms on other languages.
- **Source-type bias** — social vs news vs default thresholds.
- **Label bias** — external ratings (NewsGuard/MBFC) carry their own
  editorial/geographic bias; annotator bias.
- **Leakage** — the label must **not** be derived from the same signals being
  calibrated (would inflate measured agreement).
Record detection method and mitigation for each.

## 4. Data splitting & validation (Art. 10(3))

- Use a **temporal** train/holdout split (calibrate on the past, validate on the
  future) to prevent leakage and capture drift — **not** a random split.
- Run: `python -m cats.calibration --dataset train.jsonl --out calibrated_weights.json --metric spearman`,
  then evaluate on `holdout.jsonl`; deploy via `CATS_WEIGHTS_FILE`.
- TODO: record split ratio, dates, and achieved holdout metric (feeds Art. 15
  accuracy declaration; v2.0 target AUC-ROC ≥ 0.78 for binary labels).

## 5. Provenance, processing & personal data (Art. 10(2)(b)–(c), Art. 10(5))

- **Provenance:** TODO — list each data source (catalogues, external rating
  feeds, annotation batches) with licence/terms.
- **Processing operations:** messages → 4 signals (`compute_*`) → label →
  JSONL; see the planned `build_dataset` helper (not in scope of this PR).
- **Personal data:** CATS stores **no raw personal data** in `trust_scores`;
  audit logs are AES-256-GCM encrypted (GDPR Art. 25/32). OSINT messages may
  nonetheless contain personal data — TODO: confirm lawful basis and
  minimisation for any retained message text; Art. 10(5) special-category
  handling only if strictly necessary for bias monitoring and with safeguards.

## 6. Third-party NLP model provenance

> TODO: document the models CATS depends on and their training data at a
> high level: spaCy `it_core_news_lg`, TextBlob, optional `dbmdz`/BERT Italian
> sentiment, Sentence-BERT. Note licences and that their training data is not
> controlled by the CATS provider (a documented dependency risk).

## 7. Maintenance

- TODO: re-labelling / recalibration cadence; trigger conditions (drift detected
  via post-market monitoring, Art. 72 → `risk_management_art9.md`).
