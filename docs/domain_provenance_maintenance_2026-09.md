# Domain-provenance maintenance — 7 September 2026

Roadmap item 12 ("manutenzione di domain-provenance": periodic TLD/free-host/
brand list updates, recalibration of the `0.6` penalty coefficient when the
dataset grows, re-validation via `research/validate_domain_penalty.py`). This
is the first maintenance pass since the module shipped (ENGINE 1.4, July 2026)
and the Tranco popularity corroboration bonus (August 2026).

## Method

Two checks not previously run:

1. **False-positive audit against the full legitimate catalogue.** Every prior
   validation of this module measured its effect on the 53-source future
   holdout only — a *recall*-oriented check. Nothing had checked its
   *precision* against sources it was never trained or tested on, even though
   the module's own design goal is "high precision, low recall" and its
   docstring explicitly claims "near-zero false positives." Ran
   `compute_domain_provenance` over all 5 275 URLs in `data/Fonti_OSINT.csv`
   (the full source registry, not just the labelled subset) and inspected
   every source that scored above zero.
2. **Coefficient stability sweep.** Swept `DOMAIN_PENALTY_WEIGHT` from 0.0 to
   2.0 against the same 53-source future holdout used for every other
   validation this project runs, checking for the sign-instability pattern
   that has disqualified other candidates this cycle (content-credibility's
   `claim_density`, the pre-fix volatility threshold, the source-relative
   volatility z-score).

Both checks reuse `research/validate_domain_penalty.py`'s existing
concordance/Spearman machinery; no new spike script was needed since this is
list/coefficient maintenance on an already-shipped module, not a new-signal
decision.

## Finding 1 — four `SUSPICIOUS_TLDS` entries are real national ccTLDs

`co`, `in`, `me`, `ws` sat in `SUSPICIOUS_TLDS` (fires standalone, 40 points)
alongside genuine novelty/cheap gTLDs (`xyz`, `top`, `click`, `cfd`, ...). They
are also real ISO country-code TLDs — Colombia, India, Montenegro, Samoa — and
the catalogue audit found substantial legitimate use:

| TLD | legit hits / 5 275 | examples |
|---|---:|---|
| `in` | 45 (0.85%) | thewire.in, scroll.in, caravanmagazine.in |
| `co` | 28 (0.53%) | tempo.co, portafolio.co, coconuts.co |
| `me` | 10 (0.19%) | pobjeda.me (Montenegro's oldest paper) |
| `ws` | 3 (0.06%) | samoaobserver.ws + two Samoan government sites |

This is not purely theoretical: `data/disinfo_sources.csv` (the Doppelganger
threat-intel corpus) documents real clone use of all four (`co` ×4, `ws` ×2,
`in` ×1, `me` ×1) — including `empiresports.co`, the one domain-provenance
catch currently active on the 53-source future holdout. So this is a genuine
precision/recall tension, not a simple bug: these TLDs carry real signal *and*
real false-positive risk.

**Resolution.** Checked the real Tranco top-1M table (downloaded via
`make tranco-download` for this audit, 2026-09-07): every one of the
legitimate examples above is ranked (thewire.in #15045, tempo.co #15208,
pobjeda.me #247308, samoaobserver.ws #266976, ...), while `empiresports.co` is
not. Moved the four TLDs to a new `AMBIGUOUS_CCTLDS` set that fires (as
`ambiguous_cctld_unranked`, same 40-point weight) only when the domain is
*also* Tranco-unranked — mirroring the corroboration-only design already used
for the Tranco bonus itself, rather than a new mechanism. Deliberately
excluded from the separate `low_popularity_corroboration` bonus to avoid
double-counting the same unranked evidence for one domain.

Residual false positives from this same mechanism: a handful of legitimate
but unranked subdomains/government sites (`en.tempo.co`, `monitor.co.me`,
`cbs.gov.ws`) still fire — this is the same already-documented 24%-unranked-
among-legitimate-sources limitation the Tranco corroboration bonus already
accepts, not a new problem.

**Tradeoff worth flagging.** Before this fix, `empiresports.co`'s catch
(and its contribution to the 0.750→0.762 concordance gain) fired on TLD
alone, independent of Tranco. After this fix, that same catch requires the
popularity table to be present. `make tranco-download` is a manual step not
run automatically anywhere in this repo (checked: not in CI, not in
`docs/cloud_setup.md`, not in any workflow) — so in a deployment that never
runs it, this specific catch (and the pre-existing standalone corroboration
bonus from August) never fires. See "Re-validation" below for both numbers.
This is a real regression in the no-Tranco case relative to the immediately-
prior shipped behaviour, traded for removing false positives on ~86 real
international outlets whenever domain-provenance runs on them (in or out of
this holdout). Recommend as a follow-up, not done here: make the Tranco
refresh part of routine ops (e.g. a scheduled workflow like
`collect-rss.yml`) rather than a manual target, so this corroboration
machinery isn't silently inert by default.

## Finding 2 — the typosquat check over-triggers on short brands

The catalogue audit's *biggest* false-positive source was not the ccTLD issue
above but the fixed edit-distance-≤2 typosquat window. A short brand has many
more strings within distance 2 by chance than a long one: `ansa.it` (7 chars)
alone false-flagged **6** unrelated legitimate Italian institutional domains —
`fnsi.it`, `asi.it`, `ance.it`, `anfia.it`, `dna.it` (all distance 2) — plus
`welt.de` (1: `zeit.de`) and the newly-added `rbc.ua` (2: `cbc.ca`, `rbc.ru`,
see Finding 3). None of these are typos of the brand; they are unrelated
short acronym domains that happen to land within 2 edits by coincidence.

Checked whether tightening the window would cost real recall: every
documented distance-2 typosquat in `data/disinfo_sources.csv` against a
≤7-character brand (`ansa.ltd`, `welt.ws`) is independently caught by
`brand_on_bad_tld` or `ambiguous_cctld_unranked` already, so nothing is lost.
Distance-2 catches on *longer* brands (`ilfattoquotidaino.it` vs
`ilfattoquotidiano.it`, 20 chars) are real and have no other detector backing
them up, so the window must stay open there.

**Resolution.** Typosquat distance threshold is now length-tiered: brands of
7 characters or fewer require distance 1 (was ≤2); longer brands keep ≤2
unchanged. Reduced the catalogue's flagged-source count from 36 to 28 (of
5 275, 0.68% → 0.53%).

**Not fixed, flagged as residual limitation.** `ania.it` (distance 1 from
`ansa.it`) and `libera.it`/`liberta.it` (distance 1/2 from `libero.it`) are
false positives that survive at *any* usable distance threshold — they are
genuinely one edit away from a real brand name (Italian near-synonyms in
`libero`'s case). `voanews.com` (distance 2 from `foxnews.com`, 11 chars) and
`kn-online.de`/`rp-online.de` (distance 2 from `t-online.de`, 11 chars)
survive because those brands are long enough to keep the ≤2 window. Fixing
these would need an explicit confusable-pair exception list, which is a more
invasive change than this maintenance pass's scope — left as a known
limitation, consistent with the module's own "high precision, not perfect
precision" framing.

## Finding 3 — `MAJOR_BRANDS` was missing 7 real Doppelganger targets

`MAJOR_BRANDS` is drawn from `data/disinfo_sources.csv`'s `authentic_domain`
column (every existing entry matches a value there). Cross-checking the full
column found 7 real, documented brands the original extraction missed:
`nd-aktuell.de` (Neues Deutschland, 3 clones), `rbc.ua` (RBK Ukraine, 2),
`obozrevatel.com` (1), `delfi.lt`/`delfi.lv`/`delfi.ee` (the Baltic states'
largest news portal, 1), `lsm.lv` (Latvia's public broadcaster, 1). Added all
7 — same extraction methodology as the existing 21 entries, not a new
leakage surface (these are the *authentic* brands being protected, mined from
public threat-intel documentation of real clone campaigns, independent of
`data/disinfo_sources.csv` domain-membership checks at scoring time).

`rbc.ua` (6 characters) is itself short enough to need Finding 2's fix — see
above.

## Finding 4 — stale docstring: "not wired into scoring"

`cats/signals/domain_provenance.py`'s module docstring said "Status:
standalone, not wired into scoring," but `cats.scoring.engine.apply_domain_penalty`
has applied it as ENGINE 1.4's asymmetric penalty since July. Corrected in
passing (see the diff) — a bookkeeping fix, not a behaviour change.

## Coefficient re-check — `DOMAIN_PENALTY_WEIGHT` remains 0.6, unchanged

| weight | concordance | Spearman |
|--:|--:|--:|
| 0.0 | 0.750 | 0.554 |
| 0.1 | 0.760 | 0.573 |
| 0.2 | 0.761 | 0.575 |
| 0.3–2.0 | **0.762** | **0.578** |

Sign-stable and on a wide plateau — 0.6 sits comfortably in the middle of a
range (0.3 through at least 2.0) that all produce the identical result on
this holdout, unlike the sign-flipping patterns that disqualified other
candidates this cycle. **No change made** — this is the same "checked and
confirmed, no action needed" outcome as the earlier silence-threshold
plateau, not a null result.

## Re-validation (`research/validate_domain_penalty.py`)

With the real Tranco table present (`make tranco-download`):

```
Future holdout n=53  (domain penalty fired on 3 source(s))
                             concordance  spearman
behavioural (calibrated)           0.750     0.554
behavioural + domain penalty       0.762     0.578

Corrections (sources the penalty moved):
  label=10.0   53.61 ->  17.61   https://notiziepericolose.blogspot.com
  label=10.0   29.25 ->   0.00   https://strafattiquotidiani.wordpress.com
  label=10.0   64.53 ->  40.53   https://empiresports.co
```

Identical concordance/Spearman to before this pass (0.762/0.578) — the
`empiresports.co` correction is smaller in magnitude (40.53 vs the prior
31.53, since it no longer double-fires `low_popularity_corroboration`
alongside `ambiguous_cctld_unranked`) but does not change any pairwise rank
comparison on this holdout.

Without the Tranco table (the default state — not committed, not
auto-fetched anywhere in this repo):

```
Future holdout n=53  (domain penalty fired on 2 source(s))
                             concordance  spearman
behavioural (calibrated)           0.750     0.554
behavioural + domain penalty       0.750     0.554
```

The `empiresports.co` catch requires Tranco data and is silently absent here
— see the tradeoff note in Finding 1.

## A latent test bug this audit surfaced (fixed)

Running `make tranco-download` locally to test the above broke two existing
tests (`tests/unit/test_lite.py::test_clone_url_penalises_and_reports_domain`,
`tests/unit/test_adversarial.py::TestR4AdversarialEvasion::test_domain_penalty_catches_regular_cadence_clone`)
that had relied on the *ambient absence* of `data/tranco_top1m.csv` (documented
in their own comments) rather than mocking the popularity table like every
test in `tests/unit/test_domain_provenance.py` correctly does. This is the
same class of bug as the pre-existing SBERT/BERT backend-availability test
fragility documented all week — a test that assumes an optional dependency is
absent, rather than pinning its state. Both fixed to `monkeypatch` a
deterministic (ranked) table, so they pass regardless of whether the real
Tranco file happens to be present in a given environment.

## Summary of changes

- `cats/signals/domain_provenance.py`: `co`/`in`/`me`/`ws` moved from
  `SUSPICIOUS_TLDS` to `AMBIGUOUS_CCTLDS` (Tranco-unranked-gated); typosquat
  distance threshold length-tiered (≤7-char brands need distance 1); 7 brands
  added to `MAJOR_BRANDS`; stale "not wired into scoring" docstring corrected.
- `cats/signals/types.py`: new `ambiguous_cctld_unranked` field on
  `DomainProvenanceResult`.
- `tests/unit/test_domain_provenance.py`: new tests for both fixes.
- `tests/unit/test_lite.py`, `tests/unit/test_adversarial.py`: fixed the
  latent Tranco-ambient-state test fragility above.
- `DOMAIN_PENALTY_WEIGHT` (0.6): unchanged, re-confirmed stable.

## Recommendation

1. Ship as-is — false-positive rate on the real legitimate catalogue drops
   from 0.68% to 0.53% (36 → 28 of 5 275), no holdout regression when Tranco
   is present, and a stale docstring is corrected.
2. Follow-up worth a human decision, not done here: automate the Tranco
   refresh (a scheduled workflow, analogous to `collect-rss.yml`) so the
   corroboration mechanism — both this pass's `ambiguous_cctld_unranked` and
   August's standalone bonus — isn't silently inert in a deployment that
   never runs `make tranco-download` by hand.
3. Not fixed, left as a documented residual limitation: `ania.it` vs
   `ansa.it`, `libera.it`/`liberta.it` vs `libero.it`, and the two
   `foxnews.com`/`t-online.de` distance-2 collisions. Fixing these would need
   an explicit confusable-pair exception list — a larger, more invasive
   change than this maintenance pass, and arguably a job for a future audit
   once there's evidence these specific pairs matter in practice (none of
   the 5 275-source catalogue false positives found here look adversarial —
   all are coincidental).
