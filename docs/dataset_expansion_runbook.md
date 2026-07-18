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

## ⚠️ SAFETY: `data/labels.jsonl` is curated — never regenerate it destructively

`data/labels.jsonl` is **not** reproducible from `Fonti_OSINT.csv` + `ratings.csv`
alone. Verified (18 Jul 2026): `label_from_ratings --ratings data/ratings.csv
--scale mbfc --out data/labels.jsonl` produces **141** records vs the committed
**160**, silently **dropping the entire low tail** (e.g. *Corriere del Corsaro*
label 10, *Activist Post*/*Before It's News* label 30). Those low-reliability
labels come from the **documented-disinformation registry**
(`data/disinfo_sources.csv`), which is merged in separately — MBFC's
`ratings.csv` has no Low/Very Low entries. **Regenerating the file straight to
`data/labels.jsonl` deletes the ground-truth low tail — the core of the
validation.** Always write MBFC output to a *separate* file and merge, or append
new rows to the curated `labels.jsonl` (as the worked example below does).

## The real state of the registry (verified, network-free — corrects an earlier premise)

An earlier draft said the catalogue held "only 3 Italian RSS feeds". That was an
artefact of filtering on `Lingua=IT`; the column is mostly blank and the
catalogue has **duplicate rows per outlet**. In reality the major Italian
nationals are **already present** — `ansa.it`, `ilfattoquotidiano.it`,
`ilgiornale.it` are labelled *and* collected; `corriere.it` and
`ilsole24ore.com` are labelled (85 / 70) but **not collected**, because the
duplicate catalogue row that wins the join has an empty `RSS Feed`. So the real
work is smaller and different than "add ~30":

1. **A few genuinely-missing outlets** — done in this session: `repubblica.it`
   and `open.online` added (MBFC **High**, read from source; feeds verified 200).
2. **Catalogue data-quality** — deduplicate the rows so the feed-bearing row
   wins, or set the RSS on the winning row, so already-labelled outlets
   (`corriere.it`, `ilsole24ore.com`) actually get collected.
3. **Low tail** — MBFC has no Low/Very Low; Italian low-reliability sources come
   from the disinfo registry. Growing the Italian *high* tail is the scarce
   need, but the pool of Italian high-reliability nationals is itself limited.

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
# 1. Join catalogue + ratings into the MBFC registry — to a SEPARATE file, then
#    merge with the disinfo-registry low tail. NEVER --out data/labels.jsonl
#    directly (it drops the curated low tail — see the SAFETY section above).
python -m cats.calibration.label_from_ratings \
  --sources data/Fonti_OSINT.csv --ratings data/ratings.csv \
  --scale mbfc --out data/labels_mbfc.jsonl
# then merge data/labels_mbfc.jsonl with the disinfo-registry labels into
# data/labels.jsonl (union by source; keep the existing low tail).

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
