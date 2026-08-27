# Content-credibility signal — research spike, 27 August 2026 (roadmap item 10)

The [domain-provenance findings](signal_research_2026-07.md) closed the
regular-cadence-clone gap but named its own blind spot explicitly: fake-news
content on ordinary domains (`worldnewsdailyreport.com`, `naturalnews.com`)
has no suspicious TLD, no typo-squat, nothing for a domain-structure signal
to catch. The roadmap's item 10 named the candidate: a content-level signal
— claim density, sensationalism, citation/attribution patterns. This is that
spike, reproducible via
[`research/content_credibility_spike.py`](../research/content_credibility_spike.py)
(stdlib only, no NLP model assets needed — same dependency-free style as
`domain_provenance_spike.py`).

## Hypothesis

Behavioural signals score *timing and structure* of a message history;
domain-provenance scores the *domain*. Neither looks at what the text
actually *claims*. A source that habitually overstates ("SHOCKING proof",
"nobody wants you to know"), makes unhedged claims without attribution, and
never cites a source should be separable from one that reports carefully —
independent of both cadence and domain.

## Prototype

Three EN/IT lexicon-based sub-scores (0–100), each written from general
knowledge *before* looking at any correlation number — never fitted to this
corpus or to `data/disinfo_sources.csv` (same leakage discipline as
domain-provenance):

- **`sensationalism`**: exclamation-mark density + ALL-CAPS word density +
  a ~30-word EN/IT clickbait/tabloid lexicon ("shock", "bombshell",
  "clamoroso", "sconvolgente", …).
- **`claim_density`**: share of absolute/unhedged-certainty words
  ("always", "never", "definitely", "sempre", "certamente", …) relative to
  hedging/attributive words ("allegedly", "may", "secondo", "potrebbe", …).
- **`citation`**: quote-mark density + a reporting-verb/attribution-phrase
  lexicon ("said", "according to", "ha dichiarato", "secondo fonti", …).

Same protocol as this week's three threshold retunes: train = merged
02/03/05-Jul snapshots (n=56), holdout = the untouched 06-Jul snapshot
(n=53) — the lexicons above were finalised before this script was ever run
against either split.

## Result — none of the three clears the bar

| sub-score | ρ train | ρ holdout |
|---|---:|---:|
| sensationalism | −0.027 | −0.096 |
| claim_density | +0.056 | **−0.179** |
| citation | +0.074 | +0.042 |

All three are weak — the same magnitude as gaming's dead sub-scores
post-fix (|ρ| ≤ 0.09 on the holdout in
[`docs/gaming_redesign_2026-08.md`](gaming_redesign_2026-08.md)), not the
magnitude of a real signal (silence: ρ ≈ −0.47). `claim_density` is the
one number that looks interesting in isolation (−0.179, the strongest of
the three, correct semantic direction: more unhedged absolutism →
less reliable) — but it **flips sign between train (+0.056) and holdout
(−0.179)**. A feature whose sign depends on which snapshot window it is
measured on is not evidence of a real relationship; it is the same failure
mode the volatility retune found at threshold 0.4 (train +0.028, wrong
sign) before that threshold was corrected — except here there is no
correction to make, because `claim_density` was never tuned against these
numbers in the first place. The honest read is noise, likely driven by
topic-mix differences between the two snapshot windows (e.g. how much
breaking/political vs. feature/lifestyle content each happened to carry)
rather than a source-level reliability property.

Label-extreme means (holdout) tell the same story: `citation` and
`sensationalism` move in the semantically correct direction but by a small
margin (citation 6.8→12.2, sensationalism 4.1→3.2); `claim_density` shows a
real gap (28.8→13.8) that the sign-flip against train says not to trust.

## Recommendation — do not integrate; this is a "no", not a "not yet"

**Cheap lexicon-based content-credibility heuristics do not carry
production-usable rank information on this dataset.** This is the
decision point the roadmap's own path calls for (spike → decision →
calibration → revalidation) — the decision is not to proceed with this
approach:

1. **Don't wire these three sub-scores into scoring.** None individually
   clears even gaming's now-diagnosed weak-signal bar, and gaming's
   post-mortem already showed re-weighting sub-scores at this strength
   rescues nothing (`docs/gaming_redesign_2026-08.md`).
2. **A real content-credibility signal needs model-based features, not
   keyword lists** — the same gap that separates coherence (SBERT/NER
   embeddings) from gaming (raw tokenisation): claim extraction,
   stance/hedging classification, or an LLM-based judge would need to
   *understand* the text, not count words in it. That is a materially
   bigger investment (new model dependency, likely similar in scope to
   the SBERT coherence backend) than this repo's existing signals, and
   is not justified by this spike's results alone.
3. **The domain-provenance gap this was meant to close stays open.**
   Fake-news-on-ordinary-domains remains invisible to every signal CATS
   currently has. Worth re-raising if/when embedding- or LLM-based
   features become in-scope, but not with the lexicon approach tried here.
4. **Leakage discipline held**: lexicons were fixed before any correlation
   was computed, exactly like the domain-provenance brand list. This
   spike's negative result is therefore trustworthy in the way that
   matters most — it is not an artifact of tuning the word lists to this
   corpus.

## Caveats

n=53 holdout, distant-supervision labels (MBFC + documented disinformation
networks): indicative, not certified. EN/IT lexicons only — the merged
snapshot pool includes other languages (French, German, Arabic via BBC
Arabic) where both lexicons are structurally blind, the same degradation
pattern volatility has on Italian TextBlob polarity. A larger or
differently-constructed lexicon might shift these numbers, but the
sign-flip on `claim_density` — the one candidate with any real magnitude —
is the more fundamental problem a bigger word list would not fix.
