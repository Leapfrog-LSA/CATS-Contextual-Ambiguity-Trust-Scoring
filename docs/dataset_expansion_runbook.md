# Dataset expansion runbook — breaking the language confound

**Goal.** Add enough **Italian high-reliability** sources that language stops
predicting the label, unblocking the content-credibility signal and the
≥100-source future-holdout target (v2.0). The gap is quantified in
[content_credibility_findings_2026-07.md](content_credibility_findings_2026-07.md)
(reproduce with `research/dataset_language_balance.py`): ρ(is_italian, label)
= −0.265; the scarce cell is **high-reliability Italian** (3 today vs 35
English).

**This needs a network session** (RSS + MBFC access) — the default *Trusted*
network level does not reach arbitrary feeds/MBFC, so run it under *Full* or a
*Custom* allowlist (see [cloud_setup.md](cloud_setup.md) §3). Everything below
is verified against the current CLIs and data model; nothing here fabricates
feeds or ratings.

## The real bottleneck (verified, network-free)

`data/Fonti_OSINT.csv` currently holds **only 3 Italian (`Lingua=IT`) sources
with an RSS feed** (`avvenire.it`, `ilmanifesto.it`, and one already rated). So
the work is *not* "run the collector on existing feeds" — it is **add ~30
Italian outlets to the catalogue and their MBFC ratings**, then run the
pipeline. Separately, `data/ratings.csv` has **no Low/Very Low** entries, so the
low tail also needs a few known-unreliable Italian feeds.

## Data model (what a new source needs)

1. **Catalogue row** in `data/Fonti_OSINT.csv` — columns:
   `Macro-categoria, Sottosezione, Fonte, URL, RSS Feed, Lingua, Paese / Area, Accesso, Note`.
   Set `Lingua=IT`, a working `RSS Feed` URL, and the homepage in `URL`.
2. **Rating row** in `data/ratings.csv` — `domain,rating` on the MBFC *Factual
   Reporting* scale (`Very High | High | Mostly Factual | Mixed | Low | Very Low`).
   `domain` must match the catalogue `URL`'s host (no `www.`).

The joiner drops any catalogue source with no matching rating, so both rows are
required.

## Candidates to VERIFY (do not assume ratings or feeds)

Well-known Italian national outlets to consider adding. **Each row's RSS URL and
MBFC Factual-Reporting rating must be looked up and verified** before it is
committed — they are left blank here on purpose (no invented data):

| Outlet | Homepage | RSS (verify) | MBFC rating (look up) |
|---|---|---|---|
| Corriere della Sera | corriere.it | — | — |
| La Repubblica | repubblica.it | — | — |
| Il Sole 24 Ore | ilsole24ore.com | — | — |
| ANSA | ansa.it | — | — |
| La Stampa | lastampa.it | — | — |
| Il Post | ilpost.it | — | — |
| Rai News | rainews.it | — | — |
| Il Fatto Quotidiano | ilfattoquotidiano.it | — | — |
| Open | open.online | — | — |
| Wired Italia | wired.it | — | — |

For the low tail, add a few documented Italian low-reliability feeds (e.g. from
the disinformation registry in `data/disinfo_sources.csv` that expose RSS) —
same two-row procedure, rating `Low`/`Very Low`.

> Leakage discipline (CLAUDE.md): ratings come from MBFC (or the documented
> disinfo registry), never invented; the labelled set is never used as a
> scoring feature. Re-verify each MBFC page — ratings change over time.

## Pipeline (verified CLI sequence)

Run from the repo root after editing the two CSVs:

```bash
# 1. Join catalogue + ratings into the label registry.
python -m cats.calibration.label_from_ratings \
  --sources data/Fonti_OSINT.csv --ratings data/ratings.csv \
  --scale mbfc --out data/labels.jsonl

# 2. Collect a dated snapshot of each feed's recent messages (NETWORK).
mkdir -p data/snapshots
python -m cats.calibration.collect_rss \
  --labels data/labels.jsonl \
  --out "data/snapshots/labelled_sources_$(date -u +%F).jsonl" \
  --workers 8 --timeout 20 \
  --user-agent "Mozilla/5.0 (X11; Linux x86_64) CATS-calibration/1.0"

# 3. Re-check the balance BEFORE calibrating (network-free).
python research/dataset_language_balance.py   # rho(is_italian,label) should shrink toward 0

# 4. Merge all snapshots into cumulative histories.
python -m cats.calibration.merge_snapshots \
  --inputs data/snapshots/labelled_sources_*.jsonl \
  --out data/labelled_sources.jsonl

# 5. Temporal split (calibrate on past, validate on the future snapshot).
python -m cats.calibration.split --input data/labelled_sources.jsonl \
  --holdout-fraction 0.2 --train-out data/train_sources.jsonl \
  --holdout-out data/holdout_sources.jsonl

# 6. Build the signal datasets (needs the spaCy model for full-fidelity coherence).
python -m cats.calibration.build_dataset --input data/train_sources.jsonl   --out data/train.jsonl
python -m cats.calibration.build_dataset --input data/holdout_sources.jsonl --out data/holdout_future.jsonl
```

## Exit criteria

- `research/dataset_language_balance.py` → ρ(is_italian, label) near 0 (language
  no longer separates the tails), with Italian sources present in every band.
- ≥ 100 sources with text; a real Italian low **and** high tail.

Only then is it sound to (a) re-run `research/content_credibility_spike.py` and
read the within-Italian number as decisive, and (b) recalibrate with the
diagnosis inputs (volatility threshold, silence 96 h, gaming redesign) and
re-validate on the new future holdout — each per the CLAUDE.md discipline.
