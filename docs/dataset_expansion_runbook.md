# Dataset expansion runbook — growing and maintaining the labelled registry

**Goal.** Grow the labelled source set toward the ≥100-source future-holdout
target (v2.0), prioritising the scarce cell — **Italian high-reliability
outlets** — and keeping the collection healthy. The Italian high tail is thin:
only a handful of Italian nationals are both labelled and collected today. Pair
this with the feed-health repair loop in
[feed_health_2026-07.md](feed_health_2026-07.md), so dead feeds are not silently
dropping sources from every collection.

**This needs a network session** (RSS + MBFC access) — the default *Trusted*
network level does not reach arbitrary feeds/MBFC, so run it under *Full* or a
*Custom* allowlist (see [cloud_setup.md](cloud_setup.md) §3). Everything below
is verified against the current CLIs and data model; nothing here fabricates
feeds or ratings.

## ⚠️ BLOCKED (verified 2026-07-23): spaCy Italian model needs a session-scoped
## GitHub grant, not just *Full* network

A *Full*-network session is **not sufficient** to run step 6 below at full
fidelity. `it_core_news_lg` is fetched by `python -m spacy download
it_core_news_lg`, which pulls a release asset from
`github.com/explosion/spacy-models`. In a *Full*-network cloud session
(general egress confirmed working — e.g. a plain `curl` to an arbitrary HTTPS
host succeeds) the download still fails:

```
$ python -m spacy download it_core_news_lg
ERROR: HTTP error 403 while getting
https://github.com/explosion/spacy-models/releases/download/it_core_news_lg-3.8.0/...
```

The response body is not a generic network block, it is this session's GitHub
integration declining an out-of-scope repo:
`{"message":"GitHub access to this repository is not enabled for this
session. Use add_repo to request access."}`. **This is a per-repo GitHub
grant, orthogonal to the network level** — *Full* network gets you to
github.com's edge, but `explosion/spacy-models` still needs to be in this
session's GitHub scope (normally via `add_repo`, and only on explicit user
request — it is not part of the CATS repo and should not be added
autonomously).

**Gotcha:** the `SessionStart` hook (`.claude/hooks/*.sh`) wraps this download
in `... || true` — a flaky/blocked fetch must never fail the whole session
startup — so `cats session-start: environment ready.` prints regardless of
whether the model actually landed. **"environment ready" is not evidence the
spaCy model is present.** Verify with `python -c "import it_core_news_lg"`
before trusting NER-coherence fidelity in a calibration run.

Alternatives checked (2026-07-23) and ruled out from this session:
- Hugging Face mirror (`huggingface.co/explosion/it_core_news_lg`) — needs
  authentication in this environment (`401`, `"Invalid username or
  password."`), no token available here.
- Direct PyPI (`pypi.org/simple/it-core-news-lg/`) — `404`; spaCy trained
  pipelines are not published as ordinary PyPI packages.
- No cached wheel found anywhere on the container filesystem or in `pip
  cache`.

**To unblock:** either (a) a session where `explosion/spacy-models` has
already been granted GitHub scope (ask the user before calling `add_repo` —
it is unusual to add a model repo rather than a code repo, and may not even
work since it is release *assets*, not the repo's git history), or (b) the
model supplied another way (manual upload into the container, a private
mirror with credentials, or a pre-baked image/layer that already has
`it_core_news_lg` installed). Until then, `build_dataset` (step 6) can still
run — coherence just degrades to the neutral, zero-confidence NER value per
CLAUDE.md's graceful-degradation rule — but **do not calibrate production
weights (`data/calibrated_weights.json`) from a degraded run**; the
coherence signal would be uninformative and the calibration would not be
sound to ship.

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

# 3. Confirm the new feeds are healthy BEFORE calibrating (network).
python research/feed_health_audit.py   # the new sources should be 'ok', not dead/not-xml

# 4. Merge all snapshots into cumulative histories.
python -m cats.calibration.merge_snapshots \
  --inputs data/snapshots/labelled_sources_*.jsonl \
  --out data/labelled_sources.jsonl

# 5. Temporal split (calibrate on past, validate on the future snapshot).
python -m cats.calibration.split --input data/labelled_sources.jsonl \
  --holdout-fraction 0.2 --train-out data/train_sources.jsonl \
  --holdout-out data/holdout_sources.jsonl

# 6. Build the signal datasets (needs the spaCy model for full-fidelity
#    coherence — see the BLOCKED note above if `it_core_news_lg` isn't
#    installed; verify with `python -c "import it_core_news_lg"` first).
python -m cats.calibration.build_dataset --input data/train_sources.jsonl   --out data/train.jsonl
python -m cats.calibration.build_dataset --input data/holdout_sources.jsonl --out data/holdout_future.jsonl
```

## Exit criteria

- Italian sources present across the label bands (not clustered only in the low
  tail), and no dead feeds among the new sources (`research/feed_health_audit.py`).
- ≥ 100 sources with collected text.

Only then is it sound to recalibrate (with the diagnosis inputs — volatility
threshold, silence 96 h, gaming redesign) and re-validate on the new future
holdout, each per the CLAUDE.md discipline.
