# English NLP stack — research spike, November 2026

**Task 27** (roadmap): does an English-tuned NLP stack beat the shipped
Italian-optimised one on the future holdout's English-language sources?
CATS's default stack (`it_core_news_lg` for NER coherence, TextBlob + an
Italian negation-word correction for volatility) is Italian-optimised;
non-Italian input is flagged (`language.detected`) but still scored with
that stack. Reproducible via
[`research/english_stack_spike.py`](../research/english_stack_spike.py)
(requires `en_core_web_lg`: `python -m spacy download en_core_web_lg`).
**Research only — nothing shipped, no weight change** (this spike imports
and reconfigures `cats.signals.coherence`'s model and reimplements
volatility's polarity step locally; it never edits `cats/signals/*`).

## Caveat up front: there is no "english" language category

`cats.pipeline.language.detect_language` only distinguishes `"italian"` from
`"other"`/`"unknown"` — it was built to flag the one case that matters for
production (is the Italian-tuned stack the right one or not), not to
classify every language. This spike needed an English-specific subset, so
it adds its own local marker-word heuristic (same method as the Italian
one: ratio of high-frequency function words over Latin-script tokens,
`_ENGLISH_RATIO = 0.12`, same threshold the Italian detector uses) — **not
a proposed addition to `cats/pipeline/language.py`**, just enough to build
a comparison subset for this spike.

## Method

Same future holdout as every other calibration spike this cycle: the 53
sources in `data/holdout_future.jsonl` (signals + labels, current stack),
aligned by row order with `data/snapshots/labelled_sources_2026-07-06.jsonl`
(URLs + raw messages, same protocol as
[`validate_domain_penalty.py`](../research/validate_domain_penalty.py)).

1. Run the local English-marker heuristic on each source's messages; keep
   those above the ratio threshold.
2. For that subset, recompute two of the four signals under an
   English-tuned config:
   - **coherence**: load `en_core_web_lg` into `cats.signals.coherence`'s
     model (same NER-Jaccard algorithm, different model) instead of
     `it_core_news_lg`.
   - **volatility**: reimplement `compute_volatility`'s exact algorithm
     (0.3 spike threshold) but with plain `TextBlob(...).sentiment.polarity`
     — no Italian negation-word correction, which
     `cats.signals.sentiment._textblob_polarity` applies unconditionally
     regardless of input language. TextBlob has no built-in negation
     handling for any language, so "TextBlob inglese" here just means *not*
     applying the Italian-specific correction.
   - `silence` and `gaming` are unchanged: neither is language-dependent
     (no NLP model, no lexicon) — confirmed by inspection of both modules.
3. Recombine with `cats.scoring.engine.aggregate_score` and the shipped
   calibrated weights (`CATS_WEIGHTS_FILE=data/calibrated_weights.json`,
   same as production), then compare concordance/Spearman against the human
   labels for **current stack** vs. **English stack**, on the English
   subset only.

## Results

English-marker subset: **34 of 53** future-holdout sources (64%) — the
MBFC-heavy catalogue (see `data/README.md`'s calibration caveats: "MBFC
coverage skews to English-language ... outlets") means most of this holdout
is English, not the minority case production code assumes.

| Stack                              | Concordance | Spearman |
| ----------------------------------- | ----------: | -------: |
| Current (Italian, `it_core_news_lg`) |       0.691 |    0.434 |
| English (`en_core_web_lg`)           |       0.724 |    0.479 |

A real, consistent gain on both metrics (+0.033 concordance, +0.045
Spearman) — small in absolute terms and on n=34, but in the expected
direction and not noise-sized relative to the other spikes this cycle (cf.
`docs/volatility_source_relative_spike_2026-08.md`'s sign-flip
instability at a similar subset size).

## The coherence surprise: values drop sharply, but ranking still improves

The per-source coherence delta (English stack − current stack) is negative
for 29 of 34 sources, often by 10–29 points — `en_core_web_lg` returns
*fewer or differently-shaped* named-entity overlaps than `it_core_news_lg`
does on the same English text (different model, different training
corpus/tokenisation, and `en_core_web_lg` (3.8.0) vs `it_core_news_lg`
(3.7.0) are not the same spaCy release either — a confound this spike does
not isolate). Despite the absolute value dropping across almost the whole
subset, the **relative ordering** shifts enough to improve concordance —
consistent with the existing finding
(`docs/signal_diagnosis_2026-07.md`) that coherence's value is mostly in
its *rank* information, not its absolute scale.

## Caveats

- **n=34 is small** for a concordance/Spearman comparison — indicative, not
  a validated result. The 0.033/0.045 gain is a real signal but well within
  the kind of single-holdout noise that moved the domain-provenance
  correction from 0.755→0.775 on a comparably-sized future holdout
  (`docs/signal_research_2026-07.md`) — i.e. plausible, not proven at this
  sample size.
- **The English-detector heuristic is spike-only**, tuned to roughly the
  same threshold as the Italian one with no independent validation — some
  of the 34 sources may be misclassified (mixed-language content, wire-copy
  boilerplate).
- **Model-version confound**: `en_core_web_lg` 3.8.0 vs. the shipped
  `it_core_news_lg` 3.7.0 are different spaCy releases; some of the
  coherence-value shift could be a training-corpus/version effect rather
  than a language-tuning effect.
- **Volatility's own bottleneck is untouched**: `docs/volatility_retune_2026-08.md`
  notes ~49% of Italian-text messages carry TextBlob polarity exactly 0.0
  (lexicon coverage gap); this spike didn't measure whether that ceiling is
  the same, better, or worse for English text specifically.
- Silence/gaming untouched by design (language-independent) — the full
  four-signal English-stack picture wasn't evaluated end-to-end beyond what's
  above.

## Recommendation

**Not shipped.** The direction is right and the subset is a majority of the
current future holdout (a genuine signal, not a fluke of cherry-picking a
handful of sources), but n=34, the version confound, and the unvalidated
English-detector heuristic are each enough to withhold a production change
on this evidence alone. Flagged as the most promising of the recent
NLP-stack-adjacent spikes: worth revisiting once (a) the future holdout
pool is larger (Task 25/Fase D recalibration work already targets this),
and (b) `cats.pipeline.language.detect_language` gets or doesn't get an
actual `"english"` category — a real per-language config switch in
production would need that, not this spike's local heuristic. No weight
change, no `cats/signals/*` change, this cycle.
