# NOTICE

> **Draft, pending maintainer and legal review.** Every factual line here was
> checked against the repository on 2026-11-07. Items marked **TODO (legal)**
> or **TODO (maintainer)** are open questions. They are not determinations,
> and nothing in this file grants any right.

CATS's **source code** is released under the [MIT License](LICENSE),
© 2026 Leapfrog-LSA. That license covers the code only. The data files in this
repository, and the third-party components CATS downloads or depends on, come
from the owners listed below and carry their own terms. The status of each
data file is set out in [`DATA_LICENSE`](DATA_LICENSE).

## 1. Third-party texts (RSS feed items)

| Item | Origin | Where |
|---|---|---|
| Headlines, summaries and, for some feeds, full article bodies, copied from public RSS feeds, each with a `metadata.link` to the original item | **The respective publishers.** This project grants no licence to these texts. | `data/labelled_sources.jsonl`, `data/train_sources.jsonl`, `data/holdout_sources.jsonl`, `data/snapshots/*.jsonl` (67 files, 2026-07-02 → 2026-09-30), and the separate `Leapfrog-LSA/cats-snapshots` repository |

Scale, measured with `python research/text_inventory.py` on 2026-11-07, over
the 70 files above in this repository:

- 110 sources from 100 publisher domains;
- 152,065 distinct texts, about 89.6 million characters;
- by length, counting per source, 103,674 texts are ≤ 300 characters and
  4,099 are over 5,000 characters;
- one source, `eldiario.es`, accounts for about 34.0 million characters
  (38%), mostly full article bodies.

Run the script for the per-publisher table. These figures do not include the
`cats-snapshots` repository, which grows daily.

- **TODO (maintainer):** decide whether the raw texts stay public. The
  questions to settle first are in `DATA_LICENSE` §3.
- **TODO (legal):** whether a given text is protected at all (a short
  headline may not be), and who holds the rights, varies by publisher. Some
  sources in the inventory, for example `theconversation.com`,
  `calmatters.org` and `texastribune.org`, publish republication or Creative
  Commons terms. Check, per publisher, whether such terms already cover what
  this repository does.
- **TODO (legal):** the texts may contain personal data, such as names of
  people in the news. See `DATA_LICENSE` §3 (e).

## 2. Third-party reference data in `data/`

| File | Origin | Terms recorded in this repository |
|---|---|---|
| `ratings.csv`, `ratings_provenance.csv` | Factual Reporting ratings by **Media Bias/Fact Check (MBFC)**. `ratings_provenance.csv` records the MBFC page and retrieval date for each domain. | © Media Bias/Fact Check, used as reference data with attribution (`data/README.md`). **TODO (legal):** MBFC's terms have not been checked. See `DATA_LICENSE` §2. |
| `cred1_current.csv` | **CRED-1**, © Alexander Loth. It aggregates OpenSources.co (Melissa Zimdars et al.) and the Iffy.news Index (Reynolds Journalism Institute). | CRED-1: **CC BY 4.0**. OpenSources.co: **CC BY 4.0**. Iffy.news Index: **MIT**. Attribution is required. Not used in any pipeline. |
| `disinfo_sources.csv` | Compiled by this project from published investigations. These include Qurium (2022-09-27), Correctiv (2024), DFRLab (2024-09-06), BUTAC, Bufalopedia, la Repubblica, Il Tirreno and ENPA Milano. Attribution to state actors cites VIGINUM and the US Department of Justice. | Each row cites its sources in the `source`, `attribution` and `notes` columns. **TODO (legal):** whether the compilation itself is protected; see `DATA_LICENSE` §1. |
| `Fonti_OSINT.csv`, `Fonti_OSINT_CONSOLIDATO.md` | Source catalogue compiled by this project | Names, homepages and feed addresses of third-party outlets. **TODO (legal):** whether the compilation itself is protected; see `DATA_LICENSE` §1. |

## 3. Components CATS downloads

| Component | Origin | Licence | Note |
|---|---|---|---|
| spaCy model `it_core_news_lg` 3.8.0 (default Italian NER) | Explosion. Trained on UD Italian ISDT v2.8 (Bosco, Lenci, Montemagni, Simi), WikiNER (Nothman et al.) and Explosion fastText vectors. | **CC BY-NC-SA 3.0** for the model. Its sources: ISDT CC BY-NC-SA 3.0, WikiNER CC BY 4.0, vectors CC0. Read from the installed model's `meta.json`. | Not stored in this repository. `make nlp-download` installs it, and the `Dockerfile` bakes it into the image it builds. No workflow publishes that image today. **TODO (legal):** assess what the NonCommercial (NC) clause means for commercial deployments, and for publishing a Docker image that contains the model. |
| Tranco top-1M list (`data/tranco_top1m.csv`) | Tranco project, KU Leuven / imec-DistriNet (Le Pochat et al., NDSS 2019) | **TODO (legal):** not verified. No licence text was found on 2026-11-07. Also open in `docs/piano_sviluppo_roadmap_2026-09.md` ("prima va verificata la licenza della lista Tranco"). | Downloaded by `make tranco-download`, git-ignored, never committed. |
| TextBlob corpora (NLTK data) | NLTK project and each corpus's authors | Per corpus | Downloaded by `make nlp-download` and the `Dockerfile`. |
| Optional `sbert` / `bert` model weights | Their model authors | Per model card | Downloaded only when those backends are enabled. |

## 4. Python dependencies

CATS installs its dependencies from PyPI (`requirements*.txt`,
`pyproject.toml`). Each is distributed under its own licence, and none is
vendored into this repository. A licence lister such as `pip-licenses`, run
in an installed environment, gives the full list.

## 5. Maintenance

- Update this file whenever a data file, a downloaded model or a reference
  dataset is added, removed or replaced.
- Refresh the figures in §1 with `python research/text_inventory.py`.
- **TODO (maintainer):** if `cats-snapshots` stays public, give it its own
  notice, because it carries the same third-party texts.
