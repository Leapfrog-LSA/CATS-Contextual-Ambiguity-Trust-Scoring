# CATS — Analisi della repository, piano di sviluppo e roadmap (luglio 2026)

> Fotografia dello stato della repo alla **v1.5.0 / ENGINE 1.4** (9 luglio 2026),
> con le criticità rilevate e una roadmap numerata. Le fonti primarie restano
> [`architecture.md`](architecture.md), i findings di calibrazione
> ([giu-lug](calibration_findings_2026-07.md) e
> [validazione futura](calibration_findings_2026-07-28.md)) e la
> [ricerca sui segnali](signal_research_2026-07.md); questo documento li
> sintetizza e ne deriva il piano.

---

## 1. Che cosa c'è nella repo

CATS assegna a una fonte OSINT un punteggio ordinale di affidabilità (0–100 +
banda) calcolato da quattro **segnali comportamentali** sulla storia dei
messaggi — `coherence`, `volatility`, `silence`, `gaming` — invertiti su un
asse di affidabilità e combinati con media pesata, più una **penalità
asimmetrica di domain-provenance** (ENGINE 1.4) per i domini clone. Due
superfici condividono lo stesso codice dei segnali:

| Superficie | Ingresso | Cosa aggiunge |
|---|---|---|
| **Libreria** `cats.lite` / `cats.calibration` | `pip install cats-scoring` | Scoring puro, zero infrastruttura; toolkit di calibrazione GA |
| **API FastAPI** (`cats.api`) | Docker + nginx + Postgres 16 + Redis 7 | Pipeline a 9 fasi, audit AES-256-GCM, endpoint GDPR Art. 13–22, multi-tenant, `/metrics` Prometheus |

Componenti principali: `cats/signals/` (i quattro segnali + `domain_provenance`
+ backend opzionali SBERT/BERT), `cats/scoring/` (aggregazione, pesi,
explainer), `cats/calibration/` (raccolta RSS, dataset, GA, report),
`cats/api/` + `cats/core/` + `cats/audit/` (deployment), `alembic/`
(migrazioni 001–003), `data/` (catalogo 5 275 fonti di cui 311 con RSS, rating
MBFC per 104 domini, snapshot settimanali, pesi calibrati), `docs/` (inclusa
l'impalcatura EU AI Act) e `research/` (spike riproducibili).

### 1.1 Stato di salute (verificato in sessione, 9 lug 2026)

- **Test: 191/191 verdi** — 174 unit + 17 integration (con Postgres/Redis
  attivi), in ~3 s complessivi.
- **Lint: pulito** — black, isort, flake8, mypy esattamente come il job CI.
- **Versioni allineate**: `pyproject.toml` e `cats.__version__` entrambi 1.5.0.
- **Automazioni attive**: CI (lint+test+docker) su PR verso `main`; raccolta
  RSS settimanale (lunedì 06:00 UTC) che accumula snapshot; publish PyPI
  automatico alla creazione di una GitHub Release (trusted publishing).
- Nessuna issue né PR aperta al momento dell'analisi.

### 1.2 Dove si trova il progetto sul piano empirico

La validazione temporale del 28 lug 2026 (calibrazione sugli snapshot 02/03/05
lug, valutazione sullo snapshot 06 lug mai visto) è **passata**: concordanza a
coppie 0.755 (> obiettivo 0.70), Spearman +0.553, accordo di banda entro una
banda 79.2%. Con la penalità di dominio (ENGINE 1.4): **0.775 / +0.595**, con
ogni correzione su un clone a bassa affidabilità. I pesi calibrati spediti in
`data/calibrated_weights.json` sono quindi validati in avanti nel tempo.

## 2. Punti di forza

1. **Disciplina metodologica rara per un progetto a questo stadio**: holdout
   futuro genuino, disciplina anti-leakage (mai punteggiare dalla lista disinfo
   etichettata), decisioni di design documentate con la loro storia (fix di
   polarità v1.3.0, penalità asimmetrica vs quinto segnale pesato).
2. **Onestà dichiarativa**: limiti WP 4.1/4.3 ovunque, punteggi dichiarati
   ordinali, findings che riportano anche i numeri scomodi (§3.1).
3. **Explainability di serie**: `/explain` decompone il punteggio per segnale
   sull'asse di affidabilità, con `engine_version` per non ri-decomporre righe
   di motori vecchi.
4. **Operazioni curate**: audit cifrato, rate-limiting per chiave, purge GDPR
   schedulata, container non-root, nginx con header di sicurezza, metriche.
5. **Degradazione elegante dell'NLP**: senza `it_core_news_lg` la coherence NER
   torna neutra a confidenza zero; SBERT/BERT ripiegano su NER/TextBlob.

## 3. Criticità

### 3.1 Il rischio dominante: la discriminazione poggia su un solo segnale

Sull'holdout futuro la correlazione di rango col label è: **silence −0.43**;
coherence +0.06, volatility −0.05, gaming −0.01. Tre segnali su quattro non
portano informazione di rango, e i pesi calibrati `news` (silence 0.469,
coherence 0.395, volatility 0.077, gaming 0.059) caricano coherence più di
quanto il suo ρ giustifichi (lieve overfitting SBERT sul train). Un avversario
che pubblica a cadenza regolare neutralizza silence e fa collassare CATS verso
il caso; la penalità di dominio chiude solo il sotto-caso "clone
infrastrutturale" (3 sorgenti su 53 nell'holdout, recall ~20% sulla coda
bassa). **È il problema numero uno del progetto** e motiva la fase C della
roadmap.

### 3.2 Dataset piccolo e distant supervision

Train 56 sorgenti / 3 643 messaggi, holdout 53 / 1 753; label MBFC (distant
supervision) con copertura 104/310 domini RSS, sbilanciata verso testate
internazionali in inglese e povera sulla coda lunga italiana. I numeri sono
indicativi, non un'accuratezza certificata — e ogni miglioria dei segnali sarà
invisibile finché il set di validazione non cresce (fase B).

### 3.3 Soglie non validate

Le soglie di banda (80/60/40/20), la soglia silence (72 h per ogni tipo di
sorgente) e i pesi statici WP 4.1 restano stime iniziali non validate. Vincolo
già codificato in CLAUDE.md: cambiare soglie o roster dei segnali invalida i
pesi calibrati e richiede ricalibrazione + rivalidazione su holdout futuro.

### 3.4 Compliance: decisioni umane in sospeso

`docs/eu_ai_act/` è un'impalcatura seria ma con i `TODO` deliberati che
bloccano tutto il resto: **la classificazione high-risk (Art. 6/Annex III) non
è decisa**, manca il risk-owner nominato, i sign-off, la metodologia di data
governance. Sono decisioni umane/legali: nessuna sessione automatica deve
compilarle (regola di repo).

### 3.5 Incoerenze minori trovate durante questa analisi

| # | Incoerenza | Dove |
|---|---|---|
| a | `CONTRIBUTING.md` dice di aprire le PR verso `develop`, ma il branch non esiste e CLAUDE.md/CI usano `main` | `CONTRIBUTING.md` §Development workflow |
| b | `alembic/env.py` legge solo l'URL statico di `alembic.ini` (DB `cats`) e ignora `DATABASE_URL`: `alembic upgrade head` fallisce negli ambienti test/cloud documentati (i test passano solo perché creano lo schema da soli) | `alembic/env.py:19`, `alembic.ini:3` |
| c | `docs/cloud_setup.md` afferma che la repo «spedisce» un hook `SessionStart` in `.claude/hooks/session-start.sh`, ma la directory `.claude/` non esiste | `docs/cloud_setup.md` §1 |
| d | Il link licenza del README punta a `LICENSE/` (con slash: 404 su GitHub); la datazione "28 luglio" dei findings è successiva alla release 1.5.0 (8 lug) che li cita | `README.md`, `docs/calibration_findings_2026-07-28.md` |

> **Aggiornamento (9 lug 2026):** tutte e quattro le incoerenze sono state
> risolte con la Fase A della roadmap (stesso branch di questo documento). La
> data reale della validazione è il **6 luglio 2026** (commit `2b41982`); il
> nome file dei findings resta invariato per stabilità dei link.

## 4. Principi del piano (vincoli non negoziabili)

- **Ogni modifica alla semantica dello scoring** (segnali, soglie, coefficienti)
  passa per ricalibrazione + rivalidazione su holdout futuro prima del rilascio,
  con bump di `ENGINE_VERSION`.
- **Anti-leakage**: i segnali si calcolano da struttura generale, mai
  dall'appartenenza a `data/disinfo_sources.csv`.
- **I dati prima dei modelli**: l'ampliamento del set di validazione (fase B)
  precede e abilita il lavoro sui segnali (fase C) — su n=53 una miglioria vera
  è indistinguibile dal rumore.
- **I TODO legali restano umani**; le release PyPI richiedono conferma
  esplicita del maintainer.

## 5. Roadmap

### Fase A — Igiene di repository (v1.5.x, effort basso) — ✅ completata il 9 lug 2026

1. ✅ **Allineare `CONTRIBUTING.md` al flusso reale**: PR verso `main`, rimozione
   dei riferimenti a `develop` (anche dal trigger `push` della CI, oggi inerte).
2. ✅ **Far onorare `DATABASE_URL` ad Alembic** (`alembic/env.py`), così
   `make db-migrate` e la procedura di `docs/cloud_setup.md` funzionano su
   qualunque database configurato, non solo sul DB `cats` hardcoded.
3. ✅ **Aggiungere l'hook `.claude/hooks/session-start.sh` + `.claude/settings.json`
   promessi da `docs/cloud_setup.md`**, così le sessioni cloud fredde si
   auto-configurano davvero (idempotente, solo cloud, fallback dello script di setup).
4. ✅ **Micro-fix documentali**: link `LICENSE/` → `LICENSE` nel README; datazione
   dei findings corretta al **6 lug 2026** (data del commit di validazione) nei
   documenti vivi e nei commenti del codice, nome file invariato per i link.

### Fase B — Dati e misura (continua, prerequisito di tutto il resto)

5. **Far crescere il set di validazione con gli snapshot settimanali** (già
   automatici): obiettivo un holdout futuro ≥ 100 sorgenti con storia
   per-sorgente multi-mese; allargare la coda bassa e la coda lunga italiana
   (oggi MBFC copre 104/310 domini, quasi nessuna testata regionale).
   *(processo continuo — gli snapshot si accumulano ogni lunedì)*
6. ✅ **Trasformare il risk register in test eseguibili** (9 lug 2026): suite
   avversariale `tests/unit/test_adversarial.py` per i TODO R3/R4/R5 di
   `risk_management_art9.md` — clone a cadenza regolare (il caso che batte
   silence, contrastato solo dalla penalità di dominio), gaming spam/burst,
   messaggio singolo che oggi aggrega a banda "high" a confidenza zero (floor
   dello schema API: 1 messaggio), input non italiano degradato in silenzio.
   I test *fissano* il comportamento attuale, debolezze incluse: hardening o
   regressioni emergono come modifiche deliberate ai test.

### Fase C — Hardening dei segnali (v1.6 → v1.9, il cuore tecnico)

7. **Diagnosi dei tre segnali muti prima di inventarne di nuovi** — *diagnosi
   quantitativa completata il 9 lug 2026* (`research/signal_ablation_spike.py`,
   findings in `docs/signal_diagnosis_2026-07.md`): coherence (SBERT) è
   portante come tie-breaker (LOSO −0.139 di concordanza), i pesi morti veri
   sono volatility (−0.013) e gaming (−0.005, solo = caso); i segnali sono
   quasi ortogonali. Il backend SBERT è un requisito operativo dei pesi
   calibrati. *Restano da fare* (richiedono ricomputo a livello messaggio con
   gli asset NLP): ablation per sub-score di gaming e sweep della soglia spike
   di volatility.
8. **Rilevazione lingua + flag input non italiano (R3)**: confidenza ridotta
   esplicita invece di degrado silenzioso dei punteggi.
9. **Soglia minima di evidenza (R5)**: esporre un requisito minimo di
   messaggi/estensione temporale e una confidenza complessiva del punteggio.
10. **Segnale content-credibility** (il lavoro NLP maggiore, già a roadmap
    v2.0): densità di claim, sensazionalismo, pattern di citazione — copre la
    fake news su domini ordinari, invisibile sia ai segnali comportamentali sia
    a domain-provenance. Percorso: spike in `research/` (come per
    domain-provenance) → decisione → calibrazione → rivalidazione.
11. **Spike di corroborazione cross-sorgente** (candidato indicato dai
    findings del 28 lug): verificare fattibilità e valore incrementale prima di
    impegnarsi — richiede un registro condiviso tra sorgenti, quindi un design
    dati nuovo.
12. **Manutenzione di domain-provenance**: aggiornamento periodico delle liste
    TLD/free-hosting/brand, ricalibrazione del coefficiente 0.6 quando il
    dataset cresce, rivalidazione via `research/validate_domain_penalty.py`.

### Fase D — Ricalibrazione e v2.0 (2027)

13. **Ricalibrazione completa sul dataset ampliato**: pesi, soglie di banda
    80/60/40/20 e soglie silence per tipo di sorgente (oggi tutte 72 h),
    coefficiente della penalità di dominio; criterio di uscita: **concordanza /
    AUC ≥ 0.78 su holdout futuro ≥ 100 sorgenti** e coda bassa che discrimina.
    Aggiornare l'accuracy declaration (Art. 15) con i numeri misurati.
14. **Release v2.0**: bump `ENGINE_VERSION`, changelog di rottura (punteggi non
    comparabili), `/explain` che segnala l'engine mismatch, release PyPI con
    conferma esplicita del maintainer.

### Fase E — Compliance e operazioni (in parallelo, richiede umani)

15. **Sbloccare i TODO umani/legali**: decisione di classificazione EU AI Act
    con consulenza legale (determina se Annex IV/Art. 9-10 sono obbligatori o
    volontari), nomina del risk-owner e sign-off; pen-test/threat model (R8);
    piano di post-market monitoring; TLS 1.3 attivo in ogni deployment non
    locale.

---

**Sequenza consigliata**: A completata (9 lug 2026); B parte ora e non
si ferma; C in ordine 7→8→9→10 con 11 come spike opzionale; D quando B ha
prodotto un holdout ≥ 100 sorgenti; E appena disponibile l'interlocutore
legale. Il criterio che tiene insieme tutto: **nessun segnale nuovo entra in
produzione senza il proprio ciclo spike → calibrazione → rivalidazione su
holdout futuro**, come già fatto per domain-provenance.
