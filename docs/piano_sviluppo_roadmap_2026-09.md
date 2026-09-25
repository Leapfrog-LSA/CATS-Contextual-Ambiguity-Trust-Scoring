# CATS — Roadmap di sviluppo (aggiornamento settembre 2026)

> Aggiornamento della [roadmap di luglio](piano_sviluppo_roadmap_2026-07.md)
> allo stato della **v1.7.0 / ENGINE 1.4** (25 settembre 2026). Le voci già
> chiuse a luglio non sono ripetute. I numeri vengono dai documenti citati
> accanto a ciascuno; i punteggi CATS restano **ordinali**, non probabilità
> calibrate (WP 4.1/4.3).

In sintesi: il collo di bottiglia non è il codice. La discriminazione poggia
soprattutto su `silence`, e sulla coda bassa CATS riconosce 5 fonti
inaffidabili su 15. Per migliorare servono **dati e utenti**, non nuovi
segnali.

## Stato attuale

- **Tre superfici sullo stesso codice dei segnali:**
  - la libreria (`cats.lite`, con `score_feed(url)`) e la CLI `cats score <url>`;
  - il server MCP ([`mcp.md`](mcp.md));
  - l'API FastAPI, con audit cifrato, `/explain`, `/contest`, multi-tenant e
    `/metrics` ([`api.md`](api.md)).
- **Validazione sull'holdout futuro** (53 fonti mai viste in calibrazione,
  [`calibration.md`](calibration.md)):

  | Metrica | Valore |
  |---|---|
  | Concordanza a coppie | 0,750 (0,762 con la penalità di dominio) |
  | Spearman | +0,554 |
  | Entro una banda | 79,2% |
  | Macro-F1 | 0,692 |
  | Coda bassa: precisione / recall | 1,000 / 0,333 (5 su 15) |

- **Segnali sistemati ad agosto**, ciascuno con ricalibrazione e
  rivalidazione: `gaming` ridisegnato
  ([`gaming_redesign_2026-08.md`](gaming_redesign_2026-08.md)), `volatility` a
  0,3 ([`volatility_retune_2026-08.md`](volatility_retune_2026-08.md)),
  `silence` a 96 h ([`silence_retune_2026-08.md`](silence_retune_2026-08.md)).
  Scartati dopo lo spike: credibilità del contenuto e corroborazione tra fonti.
- **Protezioni attive:** avviso sulla lingua (rischio R3), soglia minima di
  evidenza (R5), suite di test avversariali.
- **Qualità:**
  - 350 test unitari verdi (5 saltati) e 17 di integrazione; copertura
    unitaria 86%, con `signals/coherence.py` al 100% e `scoring/weights.py` al
    98%;
  - la CI esegue `lint`, `test` e `docker` su ogni PR verso `main`;
  - la pubblicazione su PyPI parte alla creazione di una GitHub Release.
- **Dati:**
  - circa 100 fonti etichettate (rating MBFC più registro delle fonti di
    disinformazione);
  - 62 snapshot in `data/snapshots/` al 25 settembre, uno al giorno;
  - **99 fonti utilizzabili** dopo il filtro sui timestamp, una sotto la soglia
    di 100 ([`snapshot_history_audit_2026-09.md`](snapshot_history_audit_2026-09.md));
  - **0 etichette umane** in `data/human_labels.jsonl`.
- **Documentazione:** whitepaper v1.1 pronto e corretto dalle affermazioni
  eccessive; impalcatura EU AI Act completa, ma classificazione, responsabile
  del rischio e firme restano **TODO umani** ([`eu_ai_act/`](eu_ai_act/)).

Dalla roadmap di luglio sono chiusi la Fase A, i punti 6–9 e i punti 10–11
(scartati). Restano aperti il 5 (dataset ≥ 100 fonti), il 12 (manutenzione
della penalità di dominio, in parte), il 13–14 (ricalibrazione e v2.0) e il 15
(TODO legali).

## Fase 1 — breve termine (0–4 settimane): chiudere il lavoro aperto

Legenda: **S** / **M** / **L** = sforzo piccolo / medio / grande.

- [x] Allineare `docs/compliance.md` alle soglie del codice (volatility 0,3,
  silence 96 h) — **S** — [#153](https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring/pull/153).
- [x] Rendere robusti i due test di fallback SBERT/BERT, forzando l'assenza
  della dipendenza invece di presumerla — **S** — [#153](https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring/pull/153).
- [x] Alzare la copertura unitaria di `signals/coherence.py` (52% → 100%) e
  `scoring/weights.py` (64% → 98%) — **M** — [#154](https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring/pull/154).
- [x] Far ricadere sui pesi statici un file di pesi strutturalmente errato,
  invece di sollevare `AttributeError` a ogni valutazione — **S** — [#155](https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring/pull/155)
  (loader di produzione) e [#156](https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring/pull/156) (loader offline di `cats.calibration.evaluate`).
- [ ] Spostare la raccolta degli snapshot nel repo dati `cats-snapshots` — **M**
  — [#151](https://github.com/Leapfrog-LSA/CATS-Contextual-Ambiguity-Trust-Scoring/pull/151), in attesa che il maintainer crei il repo. Al cutover vanno
  aggiornati conteggio e data di chiusura degli snapshot rimasti in
  `data/snapshots/`.
- [ ] Allineare le dichiarazioni sul TLS — **S** — decisione del maintainer.
  `compliance.md` e il rischio R8 citano "TLS 1.3 (nginx)", ma in
  `deploy/nginx.conf` il blocco HTTPS è commentato. Due strade: attivarlo con i
  certificati, oppure dichiarare il TLS responsabilità di chi installa CATS.
- [ ] Automatizzare `make tranco-download` (workflow periodico o build Docker)
  — **S/M** — prima va verificata la licenza della lista Tranco. Senza la
  tabella, la componente "popolarità" della penalità di dominio non si attiva.
- [ ] Pubblicare la demo su Hugging Face Spaces e mettere l'URL nel README —
  **S** — umano.
- [ ] Esportare il PDF del whitepaper v1.1, depositarlo su Zenodo, poi inserire
  il concept DOI in `CITATION.cff` e il badge nel README — **S** — umano
  ([`zenodo_deposit_checklist.md`](zenodo_deposit_checklist.md)).
- [ ] Correggere la descrizione del repo su GitHub, che dice ancora "GDPR & EU
  AI Act compliant" — **S** — umano.
- [ ] Verificare che `technical@cats-system.org` riceva davvero — **S** — umano.

## Fase 2 — medio termine (1–3 mesi, ottobre–dicembre 2026): dati, primi utenti, API più solida

- [ ] Portare l'holdout futuro oltre le 100 fonti con storia di più mesi —
  **L** — richiede la raccolta attiva e tempo di calendario. Aggiungere fonti
  italiane regionali e istituzionali con rating verificati, seguendo
  [`dataset_expansion_runbook.md`](dataset_expansion_runbook.md); `labels.jsonl`
  non si rigenera mai.
- [x] Spostare il filtro sui timestamp anomali dentro la pipeline di
  calibrazione — **M**. Prima viveva solo in
  `research/snapshot_history_audit_2026-09.py`, e le date del 1970 o del
  2022–2024 falsano `silence`. Ora è in `merge_snapshots`, con le opzioni
  `--not-before` / `--not-after` disattivate di default. Tocca solo il dataset,
  non lo scoring live. Con i dati al 25 settembre il filtro dà 100 fonti con
  almeno 10 messaggi puliti (erano 99 al 13 settembre).
- [ ] Raccogliere almeno 20 etichette umane in `data/human_labels.jsonl`
  (modulo di feedback sul punteggio, redazioni di fact-checking) — **M** —
  dipende dal lancio.
- [ ] Lancio pubblico e prime "good first issue" — **M** — umano; dopo demo e
  DOI. Il piano di lancio resta fuori da questo repo.
- [ ] Rafforzare l'API — **M**:
  - [x] proteggere `/metrics`: il proxy nginx ora risponde `403`, e Prometheus
    legge le metriche direttamente da `app:8000` sulla rete interna;
  - [ ] test di carico su `/evaluate` e `/batch`;
  - [x] documentare i limiti di dimensione del payload, i rate limit e i codici
    di errore (`docs/api.md` → *Limits and errors*).
- [ ] Threat model e pen-test leggero (rischio R8) — **M** — il pen-test
  richiede un revisore esterno.
- [ ] Bozza tecnica del piano di monitoraggio post-market (Art. 72) — **M** —
  le soglie le decide un umano. Metriche candidate: distribuzione delle bande,
  quota di `requires_review`, quota di input non italiano.
- [ ] **Vincolo:** nessuno spike su nuovi segnali fino a metà dicembre 2026. Si
  riapre solo con più dati **e** un utente che lo chieda.

## Fase 3 — lungo termine (3–6+ mesi, gennaio–giugno 2027): ricalibrazione v2.0, conformità, pubblicazione

- [ ] **Ricalibrazione completa, primo tentativo il 12 gennaio 2027** — **L** —
  dipende dai dati della Fase 2.
  - Cosa: pesi, bande 80/60/40/20, `silence` per tipo di fonte, coefficiente
    della penalità di dominio.
  - Criterio di uscita: concordanza ≥ 0,78 su un holdout futuro ≥ 100 fonti e
    recall della coda bassa in miglioramento. Se non è soddisfatto, nuovo
    tentativo in primavera.
- [ ] Release v2.0 — **M** — dipende dalla ricalibrazione; la GitHub Release
  (che pubblica su PyPI) richiede la conferma del maintainer.
  - `ENGINE_VERSION` 2.0 e changelog di rottura (punteggi non comparabili);
  - `/explain` segnala le valutazioni fatte con un motore precedente;
  - accuracy declaration aggiornata con i numeri misurati.
- [ ] Terza fetta di validazione sulle etichette umane, riportata separata da
  quella MBFC — **M** — servono almeno 20 etichette.
- [ ] Stack NLP per l'inglese dentro la stessa ricalibrazione — **M/L** —
  dipende da un holdout più ampio. Lo spike era promettente ma non spedito (34
  fonti inglesi su 53); serve prima una vera categoria "english" nel
  rilevatore di lingua.
- [ ] Classificazione EU AI Act con un legale, nomina del responsabile del
  rischio e firme — **L** — umano/legale. Se l'esito è "alto rischio": Annex IV
  completo, sistema di gestione della qualità, valutazione di conformità.
- [ ] Vista opzionale dell'output sulla griglia Admiralty (A–F), per la
  leggibilità da parte degli analisti, senza cambiare il punteggio — **M**.
- [ ] Preprint o paper dopo la v2.0, con nuova versione su Zenodo; valutare una
  validazione esterna con un gruppo di ricerca sulle testate italiane — **M**.
- [ ] Nuovi segnali OSINT (credibilità del contenuto basata su modello,
  corroborazione tra fonti) — **L** — solo con un set di validazione in grado
  di distinguerli dal rumore e un utente che li chieda.
- [ ] Scalabilità (coda di worker per `/batch`, cache degli embedding SBERT) —
  **L** — solo quando esiste un deployment esterno reale.

## Rischi principali

- **Calibrazione:** la discriminazione dipende da `silence`. Una fonte ostile
  che pubblica a ritmo regolare passa inosservata: oggi 2 fonti inaffidabili su
  3 sfuggono.
- **Dati:** campione piccolo (53 fonti nell'holdout) ed etichette MBFC
  sbilanciate verso l'inglese. I numeri sono indicativi, non un'accuratezza
  certificata.
- **Tecnico:** i pesi calibrati presuppongono il backend SBERT. Con
  l'installazione di base (NER) la concordanza scende verso 0,62: chi installa
  CATS senza extra ottiene un sistema peggiore di quello documentato.
- **Normativo:** la classificazione EU AI Act non è determinata. L'uso in
  ambito forze dell'ordine, migrazione o giustizia può farlo rientrare
  nell'alto rischio. Affermazioni di conformità non verificate (descrizione del
  repo, TLS) sono un rischio legale e reputazionale.
- **Diritti sui dati:** gli snapshot pubblici ridistribuiscono testi di feed di
  terzi, e nessun documento indica ancora su quale base giuridica — decisione
  umana.
- **Adozione:** 0 etichette umane e nessun utente esterno. Se la Fase 2 non
  porta dati, la ricalibrazione di gennaio avrà poco di nuovo su cui lavorare.
- **Operativo:** un solo maintainer, e automazioni che si possono disattivare
  senza che nessuno se ne accorga (la raccolta giornaliera degli snapshot).
