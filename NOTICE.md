# NOTICE

> **Draft, pending maintainer and legal review.** Every factual line here was
> checked against the repository on 2026-11-07. Items marked **TODO (legal)**
> are open questions for the maintainer or a lawyer. They are not
> determinations, and nothing in this file grants rights the project does not
> hold.

CATS's **source code** is released under the [MIT License](LICENSE),
© 2026 Leapfrog-LSA. That license covers the code only. The data files in this
repository, and the third-party components CATS downloads or depends on, have
their own owners and terms, listed below. How each data file is licensed, or
why it is not, is set out in [`DATA_LICENSE`](DATA_LICENSE).

## 1. Third-party texts (RSS feed items)

| Item | Owner | Where |
|---|---|---|
| Headlines, summaries and, for some feeds, full article bodies, collected from public RSS feeds, with a `metadata.link` to each original item | **The respective publishers.** © belongs to each outlet. CATS holds no licence to them. | `data/labelled_sources.jsonl`, `data/train_sources.jsonl`, `data/holdout_sources.jsonl`, `data/snapshots/*.jsonl` (67 files, 2026-07-02 → 2026-09-30), and the separate `Leapfrog-LSA/cats-snapshots` repository |

Scale, measured with `python research/text_inventory.py` on 2026-11-07, over
the 70 files above in this repository:

- 110 sources from 100 publisher domains;
- 152,666 unique texts, about 89.8 million characters;
- by length, 103,674 texts are ≤ 300 characters and 4,099 are > 5,000
  characters;
- one source, `eldiario.es`, accounts for about 34.0 million characters (38%),
  mostly full article bodies.

Run the script for the per-publisher table. The `cats-snapshots` repository is
not included in these figures and grows daily.

- **TODO (legal):** decide whether raw texts may stay public (roadmap,
  item 1), and on what legal basis. See the questions in `DATA_LICENSE` §3.
- **TODO (legal):** the texts may contain personal data, such as names of
  people in the news. Assess whether GDPR Art. 85 or another basis applies
  (roadmap, item 18).

## 2. Third-party reference data shipped in `data/`

| File | Owner / origin | Terms as recorded in this repository |
|---|---|---|
| `ratings.csv`, `ratings_provenance.csv` | Factual Reporting ratings by **Media Bias/Fact Check (MBFC)**, one MBFC page and retrieval date per domain | © Media Bias/Fact Check; used as reference data with attribution (`data/README.md`). **TODO (legal):** check MBFC's terms before any redistribution beyond this repository, Zenodo included. |
| `cred1_current.csv` | **CRED-1**, © Alexander Loth, which aggregates OpenSources.co (Melissa Zimdars et al.) and the Iffy.news Index (Reynolds Journalism Institute) | CRED-1: **CC BY 4.0**. OpenSources.co: **CC BY 4.0**. Iffy.news Index: **MIT**. Attribution is required. Not used in any pipeline. |
| `disinfo_sources.csv` | Compiled by this project from published investigations: Qurium (2022-09-27), DFRLab, the US Department of Justice (2024), VIGINUM, BUTAC/Bufalopedia, la Repubblica (cited per row in its `source` / `attribution` columns) | Facts (domain names, attributions) with per-row citation. The selection and arrangement are the project's. |
| `Fonti_OSINT.csv`, `Fonti_OSINT_CONSOLIDATO.md` | Source catalogue compiled by this project | Names, URLs and feed addresses of third-party outlets. The selection and arrangement are the project's. |

## 3. Components CATS downloads but does not redistribute

| Component | Owner | Licence | Note |
|---|---|---|---|
| spaCy model `it_core_news_lg` 3.8.0 (default Italian NER) | Explosion; trained on UD Italian ISDT v2.8 (Bosco, Lenci, Montemagni, Simi), WikiNER (Nothman et al.) and Explosion fastText vectors | **CC BY-NC-SA 3.0** (model). Sources: ISDT CC BY-NC-SA 3.0, WikiNER CC BY 4.0, vectors CC0. Read from the installed model's `meta.json`. | Installed by `make nlp-download` and the Docker build, not stored in this repository. **TODO (legal):** the NonCommercial (NC) clause may restrict commercial deployments of CATS that use this model. Assess this, and decide whether to document an alternative model. |
| Tranco top-1M list (`data/tranco_top1m.csv`) | Tranco project, KU Leuven / imec-DistriNet (Le Pochat et al., NDSS 2019) | **TODO (legal):** not verified. No licence was found on 2026-11-07 (roadmap, item 15). | Downloaded by `make tranco-download`. Git-ignored and never committed. |
| TextBlob corpora (NLTK data) | NLTK project and the corpora's own authors | Per corpus | Downloaded by `make nlp-download`. |
| Optional `sbert` / `bert` model weights | Their respective model authors | Per model card | Downloaded only when those backends are enabled. |

## 4. Python dependencies

CATS installs its dependencies from PyPI (`requirements*.txt`,
`pyproject.toml`). Each is distributed under its own licence, and none is
vendored into this repository. A licence lister such as `pip-licenses`, run
in an installed environment, gives the full list.

## 5. Maintenance

- Update this file whenever a data file, a downloaded model or a reference
  dataset is added, removed or replaced.
- Keep the figures in §1 current by re-running
  `python research/text_inventory.py`.
- **TODO (maintainer):** if `cats-snapshots` stays public, give it its own
  `NOTICE` / `DATA_LICENSE`, because it carries the same third-party texts.
