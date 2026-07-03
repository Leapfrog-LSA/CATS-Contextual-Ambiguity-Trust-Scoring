# Fonti OSINT — Database Consolidato
**Versione:** 5.25 — 17/06/2026  
**Totale fonti uniche:** 5275  
**File sorgente analizzati:** 40 (19 Markdown + 16 CSV + 2 documenti)  
**Deduplicazione:** per URL normalizzato (host senza `www`, path senza slash finale), con merge dei metadati complementari  
**Schema tabella:** Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note  
**Autore:** Lina — consolidamento assistito da Claude

---

## Indice

1. [📰 Media & Testate Giornalistiche](#1-media-testate-giornalistiche) — 2233
2. [📊 Statistiche & Dati Macroeconomici](#2-statistiche-dati-macroeconomici) — 403
3. [🏢 Registri Aziendali & Corporate Intelligence](#3-registri-aziendali-corporate-intelligence) — 270
4. [⚖️ Sanzioni, PEP & Compliance](#4-sanzioni-pep-compliance) — 86
5. [🔓 Open Data & Trasparenza](#5-open-data-trasparenza) — 509
6. [✅ Fact-Checking & Disinformazione](#6-fact-checking-disinformazione) — 32
7. [🎓 Geopolitica & Intelligence](#7-geopolitica-intelligence) — 154
8. [🕊️ Diritti Umani & Giudiziario](#8-diritti-umani-giudiziario) — 35
9. [🔐 Cybersecurity & Digital OSINT](#9-cybersecurity-digital-osint) — 181
10. [📡 Social Media & Media Monitoring](#10-social-media-media-monitoring) — 82
11. [🌿 Sostenibilità & ESG](#11-sostenibilità-esg) — 47
12. [🧩 Settori Specifici](#12-settori-specifici) — 1243

---

## Riepilogo per Categoria

| # | Macro-categoria | Sottocategoria | Fonti |
|---|-----------------|----------------|------:|
| 1 | 📰 Media & Testate Giornalistiche | Globali & Internazionali | 224 |
|  |  | Giornalismo Investigativo | 221 |
|  |  | Italia | 277 |
|  |  | Europa Occidentale | 264 |
|  |  | Europa Orientale & Nord Europa | 199 |
|  |  | America Latina & Caraibi | 204 |
|  |  | Africa | 314 |
|  |  | Medio Oriente & Nord Africa (MENA) | 100 |
|  |  | Asia & Pacifico | 300 |
|  |  | Nord America — Stampa Statale & Locale | 67 |
|  |  | Agenzie di Stampa Nazionali | 38 |
|  |  | Emittenti Pubbliche & Radio | 25 |
| 2 | 📊 Statistiche & Dati Macroeconomici | Banche Centrali & Autorità Monetarie | 164 |
|  |  | Istituti di Statistica Nazionali | 187 |
|  |  | Organizzazioni Internazionali & Banche di Sviluppo | 26 |
|  |  | Sondaggi, Barometri & Dataset Comparativi | 26 |
| 3 | 🏢 Registri Aziendali & Corporate Intelligence | Camere di Commercio | 123 |
|  |  | Risk Management & Business Intelligence | 37 |
|  |  | Registri & Ownership | 80 |
|  |  | Catasti & Registri Immobiliari | 30 |
| 4 | ⚖️ Sanzioni, PEP & Compliance | AML, Sanzioni & PEP | 61 |
|  |  | Crimine Organizzato & Traffici Illeciti | 25 |
| 5 | 🔓 Open Data & Trasparenza | Portali Open Data & Database | 196 |
|  |  | Gazzette Ufficiali & Legislazione | 95 |
|  |  | Istituzioni, Trasparenza & Open Government | 50 |
|  |  | Parlamenti & Organi Elettorali | 51 |
|  |  | Open Data Subnazionale & Città | 59 |
|  |  | Esteri, Governi & Diplomazia | 33 |
|  |  | Corti dei Conti, Tesori & Vigilanza Pubblica | 25 |
| 6 | ✅ Fact-Checking & Disinformazione | Fact-Checking & Disinformazione | 32 |
| 7 | 🎓 Geopolitica & Intelligence | Geopolitica & Intelligence | 154 |
| 8 | 🕊️ Diritti Umani & Giudiziario | Diritti Umani & Giudiziario | 35 |
| 9 | 🔐 Cybersecurity & Digital OSINT | Threat Intelligence & Cybersecurity | 67 |
|  |  | OSINT Tools & Intelligence | 114 |
| 10 | 📡 Social Media & Media Monitoring | Social Media & Media Monitoring | 82 |
| 11 | 🌿 Sostenibilità & ESG | Sostenibilità & ESG | 47 |
| 12 | 🧩 Settori Specifici | Finanza, Economia & Business | 58 |
|  |  | Autorità di Vigilanza Finanziaria & Regolatori | 66 |
|  |  | AI, LLM & Ricerca Scientifica | 92 |
|  |  | Automazione, Dev & Produttività | 149 |
|  |  | Borse Valori & Mercati | 67 |
|  |  | Autorità Data Protection & Privacy | 46 |
|  |  | Dogane, Trade & Export Control | 28 |
|  |  | Marittimo, Aviazione & Trasporti | 51 |
|  |  | Energia & Materie Prime | 50 |
|  |  | Salute & Regolatori Farmaceutici | 28 |
|  |  | Proprietà Intellettuale & Brevetti | 27 |
|  |  | Standard & Normazione Tecnica | 26 |
|  |  | Antitrust & Concorrenza | 29 |
|  |  | Agenzie Fiscali & Entrate | 33 |
|  |  | Law Enforcement & Giustizia | 27 |
|  |  | Spazio, Geoscienze & Meteo | 31 |
|  |  | Archivi, Biblioteche & Patrimonio Documentale | 25 |
|  |  | Ricerca Economica & Policy | 39 |
|  |  | Telecomunicazioni & Regolatori Media | 27 |
|  |  | Agricoltura & Sicurezza Alimentare | 25 |
|  |  | Lavoro & Welfare | 25 |
|  |  | Difesa & Procurement Pubblico | 25 |
|  |  | Cultura, Arte & Patrimonio | 25 |
|  |  | Sport & Governance Sportiva | 26 |
|  |  | Ordini & Associazioni Professionali | 29 |
|  |  | Fondazioni, Filantropia & Nonprofit | 26 |
|  |  | Promozione Investimenti & Fondi Sovrani | 34 |
|  |  | Ambiente & Vigilanza Ambientale | 25 |
|  |  | Associazioni Bancarie & Infrastrutture di Mercato | 34 |
|  |  | Associazioni Industriali, di Categoria & Turismo | 70 |
| | **TOTALE** | | **5275** |

---

## 1. 📰 Media & Testate Giornalistiche

### 1.1 Globali & Internazionali (224)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ABC News (USA) | https://abcnews.go.com | — | EN | — | — | TV USA |
| Acento DR | https://acento.com.do | — | — | DO | — | Online |
| AdWeek | https://www.adweek.com | https://www.adweek.com/feed/ | EN | — | — | Advertising |
| AFP Fact Check | https://factcheck.afp.com | — | — | Globale | — | Fact-checking AFP |
| AFP News | https://www.afp.com | https://www.afp.com/en/rss | EN | — | — | Wire globale — Wire service Europa |
| Africa Check | https://africacheck.org | — | — | Pan-Africa | — | Fact-checking africano — Africa |
| Agenda Digitale | https://www.agendadigitale.eu | https://www.agendadigitale.eu/feed/ | — | — | Online | PA digitale — Tech |
| AllSides | https://www.allsides.com | — | — | US | — | Bias comparazione — USA |
| Amandala Belize | https://www.amandala.com.bz | — | — | BZ | — | Belize |
| Anchorage Daily News | https://www.adn.com | — | EN | — | — | Alaska |
| Aos Fatos | https://www.aosfatos.org | — | PT | — | — | Fact-checking BR — Brasile |
| AP Fact Check | https://apnews.com/hub/ap-fact-check | — | — | — | — | Fact-checking AP — USA |
| Arizona Republic | https://www.azcentral.com | — | EN | — | — | Arizona |
| Associated Press | https://apnews.com | — | EN | — | — | Wire service USA |
| Axios | https://www.axios.com | — | EN | — | — | News concise |
| Axios Future | https://www.axios.com/future | https://www.axios.com/rss | EN | — | — | Tech/Future |
| Barbados Today | https://barbadostoday.bb | — | EN | — | — | Barbados |
| BBC News | https://www.bbc.com/news | — | EN | — | — | Copertura globale — homepage |
| BBC News World | https://www.bbc.com/news/world | — | EN | — | — | Copertura globale |
| BIRN Balkan | https://birn.eu.com | — | — | Balcani | — | Network |
| Boston Globe | https://www.bostonglobe.com | — | EN | — | — | Boston |
| Breaking Defense | https://breakingdefense.com | — | EN | — | — | Difesa globale |
| Bridge Michigan | https://www.bridgemi.com | — | EN | — | — | Michigan investigativo |
| Bulletin of Atomic Scientists | https://thebulletin.org | — | — | US | — | Sicurezza nucleare — USA |
| BuzzFeed News | https://www.buzzfeednews.com | — | EN | — | — | Investigativo + viral |
| CalMatters | https://calmatters.org | https://calmatters.org/feed/ | EN | — | — | California Policy |
| Canary Media | https://www.canarymedia.com | — | — | — | — | Energia pulita — USA — News |
| CBC News | https://www.cbc.ca/news | — | EN | — | — | Canada |
| CBS News | https://www.cbsnews.com | — | EN | — | — | TV USA |
| Chalkbeat | https://www.chalkbeat.org | — | EN | — | — | Educazione USA |
| Chicago Tribune | https://www.chicagotribune.com | — | EN | — | — | Chicago |
| Climate Signals | https://www.climatesignals.org | — | — | US | — | Scienza clima — USA |
| CNET | https://www.cnet.com | https://www.cnet.com/rss/news/ | EN | — | — | Tech Consumer |
| CNN International | https://edition.cnn.com | — | EN | — | — | Breaking news USA |
| Colorado Sun | https://coloradosun.com | — | EN | — | — | Colorado investigativo |
| CoronaVirusFacts Alliance | https://www.poynter.org/ifcn/covid-19-misinformation | — | — | Globale | — | FC COVID |
| Credit report of individuals and companies | https://u.ae/en/information-and-services/business/financial-credibility-for-individuals-and-companies | — | — | — | — | Bibliografia |
| Current Affairs | https://www.currentaffairs.org | — | EN | — | — | Analisi critica |
| Daily Sabah | https://www.dailysabah.com | — | EN | — | — | Turchia pro-gov |
| Data Journalism Awards | https://datajournalismawards.org | — | — | Globale | — | Awards |
| DataJournalism.com | https://datajournalism.com | — | — | Globale | — | Risorse data journalism |
| Deadline | https://deadline.com | https://deadline.com/feed/ | EN | — | — | Entertainment |
| Defense News | https://www.defensenews.com | https://www.defensenews.com/rss/ | EN | — | — | Difesa USA |
| Defense One | https://www.defenseone.com | — | EN | — | — | Difesa USA |
| Demagog | https://demagog.org | — | — | PL | — | Fact-checking PL — Polonia |
| Demagog CZ | https://demagog.cz | — | — | CZ | — | Fact-checking CZ — Rep. Ceca |
| Denver Post | https://www.denverpost.com | — | EN | — | — | Colorado |
| Detroit Free Press | https://www.freep.com | — | EN | — | — | Michigan |
| Diario Libre DR | https://www.diariolibre.com | — | — | DO | — | — |
| Digital4Biz | https://www.digital4.biz | https://www.digital4.biz/feed/ | — | — | — | B2B IT |
| DKAN | https://getdkan.org | — | — | — | — | Alternativa open source a CKAN basata su Drupal — Gratuito — Software/portale |
| Documented NY | https://documentedny.com | — | EN | — | — | Immigrazione USA |
| Dropsite News | https://www.dropsitenews.com | — | EN | — | — | Investigativo USA |
| DW News | https://www.dw.com | — | EN | — | — | Prospettiva tedesca |
| El Nacional DR | https://elnacional.com.do | — | — | DO | — | — |
| Emeequis | https://www.m-x.com.mx | — | — | MX | — | Inv. — Messico |
| Energymonitor.ai | https://energymonitor.ai | — | — | Globale | — | Energia e transizione |
| Engadget | https://www.engadget.com | https://www.engadget.com/rss.xml | EN | — | — | Tech Gadget |
| EU vs Disinfo | https://euvsdisinfo.eu | — | — | EU | — | Disinformazione pro-Kremlin |
| EUfactcheck | https://eufactcheck.eu | — | — | EU | — | — |
| Euractiv | https://www.euractiv.com | — | EN | — | — | UE policy |
| Eurasia Group | https://www.eurasiagroup.net | — | — | US | — | Rischio politico — USA |
| Euronews | https://www.euronews.com | — | EN/IT | — | — | Prospettiva europea |
| Expansión política MX | https://politica.expansion.mx | — | — | MX | — | Messico |
| FactCheck.org | https://www.factcheck.org | — | — | US | — | Fact-checking USA |
| FinanzaOnline | https://www.finanzaonline.com | — | — | — | — | Community — Finanza |
| First Draft | https://firstdraftnews.org | — | — | Globale | — | Verifica e media literacy |
| FiveThirtyEight | https://fivethirtyeight.com | — | — | US | — | Data e statistiche — USA |
| Floodlight News | https://floodlightnews.org | — | EN | — | — | Investigativo USA |
| Foreign Affairs | https://www.foreignaffairs.com | — | EN | — | — | Policy internazionale |
| Foreign Policy | https://foreignpolicy.com | — | EN | — | — | Geopolitica |
| FPRI | https://www.fpri.org | — | — | US | — | Policy — USA |
| Full Fact | https://fullfact.org | — | UK | — | — | Fact-checking britannico |
| Gatopardo MX | https://gatopardo.com | — | — | MX | — | Long-form — Messico |
| Gizmodo | https://gizmodo.com | https://gizmodo.com/rss | EN | — | — | Tech Culture |
| Global Fishing Watch | https://globalfishingwatch.org | — | — | Globale | — | Pesca illegale |
| Global Health Expenditure DB | https://apps.who.int/nha/database | — | — | — | — | Gratuito — Spesa sanitaria |
| Globe and Mail | https://www.theglobeandmail.com | — | EN | — | — | Canada premium |
| Google Dataset Search | https://datasetsearch.research.google.com | — | — | — | — | Motore di ricerca dedicato ai dataset da tutto il web — Gratuito — Motore ricerca |
| Google Open Images | https://storage.googleapis.com/openimages/web | — | — | — | — | 9 milioni immagini annotate (Google) — Gratuito — Dataset |
| Gothamist | https://gothamist.com | https://gothamist.com/feed | EN | — | — | New York |
| Grid News | https://gridnews.com | — | EN | — | — | Contesto news |
| Guyana Chronicle | https://www.guyanachronicle.com | — | — | GY | — | Guyana |
| Harper's Magazine | https://harpers.org | — | EN | — | — | USA — mensile storico |
| Heatmap News | https://heatmap.news | — | — | — | — | Clima e politica — USA — News |
| Hildebrandt en sus trece | https://hildebrandtensustrece.pe | — | — | PE | — | Long-form — Perù |
| Hollywood Reporter | https://www.hollywoodreporter.com | https://www.hollywoodreporter.com/feed/ | EN | — | — | Entertainment |
| Honolulu Civil Beat | https://www.civilbeat.org | — | EN | — | — | Hawaii investigativo |
| Houston Chronicle | https://www.houstonchronicle.com | — | EN | — | — | Texas |
| Hoy Digital DR | https://hoy.com.do | — | — | DO | — | — |
| HuffPost | https://www.huffpost.com | — | EN | — | — | USA progressista |
| Humanitarian Data Exchange | https://data.humdata.org | — | — | — | — | Dataset crisi umanitarie OCHA/ONU — Gratuito — Repository |
| Hurriyet Daily News | https://www.hurriyetdailynews.com | — | EN | — | — | Turchia |
| IEA – Agenzia Int. Energia | https://www.iea.org/data-and-statistics | — | — | — | — | Energia globale, CO2, rinnovabili dal 1973 — Freemium — Portale ufficiale |
| IFCN | https://ifcncodeofprinciples.poynter.org | — | — | Globale | — | Network fact-checkers |
| IPCC Data Distribution Centre | https://www.ipcc-data.org | — | — | — | — | Dati climatici per i report IPCC — Gratuito — Repository |
| IRE (Investigative Reporters) | https://www.ire.org | — | — | US | — | Associazione — USA |
| IRL North Macedonia | https://irl.mk | — | — | MK | — | Inv. — Macedonia N. |
| Jacobin | https://jacobin.com | — | EN | — | — | Sinistra radicale |
| Jacques Delors Centre | https://www.delorscentre.eu | — | — | EU | — | Berlino |
| Janes Defence | https://www.janes.com | — | EN | — | — | Difesa (Paywall) |
| Kansas City Star | https://www.kansascity.com | — | EN | — | — | Kansas/Missouri |
| Knight Center | https://knightcenter.utexas.edu | — | — | US | — | Giornalismo — USA |
| L'Usine Nouvelle | https://www.usinenouvelle.com | https://www.usinenouvelle.com/rss | FR | — | — | Industria FR |
| La Croix | https://www.la-croix.com | https://www.la-croix.com/rss | FR | — | — | Cattolico FR |
| La Jornada Maya | https://www.lajornadamaya.mx | — | — | MX | — | Regionale — Messico |
| LA Times | https://www.latimes.com | https://www.latimes.com/rss2.0.xml | EN | — | — | California |
| La Tribune | https://www.latribune.fr | — | FR | — | — | Francia economia |
| LAION Datasets | https://laion.ai/projects | — | — | — | — | Dataset immagini-testo per AI generativa — Gratuito — Repository |
| Les Echos | https://www.lesechos.fr | — | FR | — | — | Francia economia |
| Logically Facts | https://www.logicallyfacts.com | — | — | Globale | — | AI fact-checking |
| Maclean's | https://macleans.ca | — | EN | — | — | Canada — newsmagazine nazionale |
| Maldita.es | https://maldita.es | — | — | ES | — | Fact-checking ES — Spagna |
| MarineTraffic AIS Data | https://www.marinetraffic.com/en/ais/details | — | — | — | — | Freemium — Navi |
| Mashable | https://mashable.com | https://mashable.com/feed/ | EN | — | — | Digital Culture |
| Media Bias/Fact Check | https://mediabiasfactcheck.com | — | — | Globale | — | Bias dei media |
| Meta.mk (N. Macedonia) | https://meta.mk | — | — | MK | — | Online — Macedonia N. |
| Miami Herald | https://www.miamiherald.com | — | EN | — | — | Florida USA |
| Milenio | https://www.milenio.com | — | — | MX | — | Messico |
| Minneapolis Star Tribune | https://www.startribune.com | — | EN | — | — | Minnesota |
| Misbar | https://misbar.com | — | — | MENA | — | Fact-checking arabo — Medio Oriente |
| Mississippi Today | https://mississippitoday.org | — | EN | — | — | Mississippi investigativo |
| MIT Technology Review | https://www.technologyreview.com | — | EN | — | — | Tech e innovazione |
| Monocle | https://monocle.com | — | EN | — | — | Globale — affari e cultura |
| Mother Jones | https://www.motherjones.com | — | EN | — | — | Investigativo progressista |
| Nation | https://www.thenation.com | — | EN | — | — | Sinistra USA |
| National Interest | https://nationalinterest.org | — | EN | — | — | Politica estera USA |
| National Review | https://www.nationalreview.com | — | EN | — | — | USA — conservatore |
| NBC News | https://www.nbcnews.com | — | EN | — | — | TV USA |
| New Orleans Times-Picayune | https://www.nola.com | — | EN | — | — | Louisiana |
| New York Times World | https://www.nytimes.com/section/world | — | EN | — | — | USA premium |
| New Yorker | https://www.newyorker.com | — | EN | — | — | Long-form USA |
| NewsGuard | https://www.newsguardtech.com | — | — | Globale | — | Rating affidabilità media |
| Newsweek | https://www.newsweek.com | — | EN | — | — | USA settimanale |
| NOAA Climate | https://www.noaa.gov/climate | — | — | US | — | Dati climatici USA |
| NPR News | https://www.npr.org | — | EN | — | — | Radio USA pubblico |
| OCSE iLibrary Statistics | https://www.oecd-ilibrary.org/statistics | — | — | — | Database | Statistiche OCSE su economia, finanza, migrazione — Gratuito |
| Open.canada.ca | https://open.canada.ca/en/open-data | — | — | CA | — | Gratuito |
| OpenML | https://www.openml.org | — | — | — | — | Piattaforma open per esperimenti ML — Gratuito |
| OpenRailwayMap | https://www.openrailwaymap.org | — | — | — | — | Gratuito — Ferrovie |
| OpenSecrets | https://www.opensecrets.org | — | — | — | Pubblico | Finanziamenti politici USA — Database |
| PBS NewsHour | https://www.pbs.org/newshour | — | EN | — | — | USA pubblico |
| PesaCheck | https://pesacheck.org | — | — | Africa Or. | — | Fact-checking finanza — Africa orientale |
| Philadelphia Inquirer | https://www.inquirer.com | — | EN | — | — | Philadelphia |
| Ploughshares Fund | https://www.ploughshares.org | — | — | US | — | Non-proliferazione — USA |
| Politico (USA) | https://www.politico.com | — | EN | — | — | Politica USA |
| Politico Europe | https://www.politico.eu | — | EN | — | — | Policy e UE |
| PolitiFact | https://www.politifact.com | — | — | US | — | Fact-checking politico USA |
| Portal do Governo BR | https://www.gov.br/governoaberto | — | — | BR | — | Gratuito |
| Poynter | https://www.poynter.org | — | — | US | — | Risorse per giornalisti — USA |
| Puck News | https://puck.news | — | EN | — | — | Power USA |
| PyTorch Datasets | https://pytorch.org/vision/stable/datasets.html | — | — | — | — | Dataset ufficiali PyTorch — Gratuito — Repository |
| Quartz | https://qz.com | — | EN | — | — | Business globale |
| Quotidiano Nazionale | https://www.quotidiano.net | https://www.quotidiano.net/rss | — | — | — | QN/Carlino/Nazione — Quotidiano — Gruppo |
| Radio 24 | https://www.radio24.ilsole24ore.com | https://www.radio24.ilsole24ore.com/rss | — | — | — | Business Radio — Radio |
| Radio Free Europe | https://www.rferl.org | — | EN | — | — | Europa dell'est |
| Radio Free Europe Balkans | https://www.slobodnaevropa.org | — | — | Balcani | — | RFE/RL |
| Reason | https://reason.com | — | EN | — | — | Libertarismo USA |
| Reuters | https://www.reuters.com | — | EN | — | — | Wire service primario |
| Reuters Climate | https://www.reuters.com/sustainability | — | — | — | — | Reuters clima — Globale — News |
| Reuters Fact Check | https://www.reuters.com/fact-check | — | — | Globale | — | Fact-checking Reuters |
| RFI | https://www.rfi.fr | — | FR | — | — | Radio FR internazionale |
| Rivista AI | https://www.rivista.ai | https://www.rivista.ai/feed/ | — | — | — | IA — Tech |
| RNZ (Radio NZ) | https://www.rnz.co.nz | — | EN | — | — | NZ radio pubblica |
| Rolling Stone (news) | https://www.rollingstone.com | — | EN | — | — | Cultura e politica |
| Salon | https://www.salon.com | — | EN | — | — | USA sinistra |
| Salt Lake Tribune | https://www.sltrib.com | — | EN | — | — | Utah investigativo |
| Salud con Lupa | https://saludconlupa.com | — | — | PE | — | Salute — Perù |
| San Francisco Chronicle | https://www.sfchronicle.com | — | EN | — | — | San Francisco |
| Sbilanciamoci | https://sbilanciamoci.info | https://sbilanciamoci.info/feed/ | — | — | Online | Economia critica — Economia e sociale |
| Seattle Times | https://www.seattletimes.com | — | EN | — | — | Seattle |
| Semanario Universidad CR | https://semanariouniversidad.com | — | — | CR | — | Universitario |
| SF Gate | https://www.sfgate.com | https://www.sfgate.com/rss/ | EN | — | — | Bay Area |
| Sigma Awards | https://sigmaawards.org | — | — | Globale | — | Data journalism awards |
| Snopes | https://www.snopes.com | — | — | US | — | Fact-checking globale — USA |
| SPJ (Society Prof. Journalists) | https://www.spj.org | — | — | US | — | Associazione — USA |
| Stabroek News | https://www.stabroeknews.com | — | — | GY | — | Indip. — Guyana |
| Stimson Center | https://www.stimson.org | — | — | US | — | Non-proliferazione — USA |
| TensorFlow Datasets | https://www.tensorflow.org/datasets | — | — | — | — | Dataset pronti per TF — Gratuito — Repository |
| Teyit | https://teyit.org | — | — | TR | — | Fact-checking TR — Turchia |
| The Age | https://www.theage.com.au | — | EN | — | — | Melbourne |
| The American Prospect | https://prospect.org | — | EN | — | — | Sinistra USA |
| The Atlantic | https://www.theatlantic.com | — | EN | — | — | Cultura e politica USA |
| The Bulwark | https://thebulwark.com | — | EN | — | — | Moderato USA |
| The Conversation (Global) | https://theconversation.com/global | — | EN | — | — | Accademia |
| The Daily Beast | https://www.thedailybeast.com | — | EN | — | — | USA tabloide premium |
| The Dispatch | https://thedispatch.com | — | EN | — | — | Centrodestra USA |
| The Drum | https://www.thedrum.com | https://www.thedrum.com/rss.xml | EN | — | — | Marketing Media |
| The Economist | https://www.economist.com | — | EN | — | — | Analisi settimanale |
| The Examination | https://theexamination.org | — | — | Globale | — | Sanità globale |
| The Hill | https://thehill.com | — | EN | — | — | USA Congresso |
| The Hill Tech | https://thehill.com/policy/technology | https://thehill.com/news/technology/feed | EN | — | — | Policy Tech |
| The Nevada Independent | https://thenevadaindependent.com | — | EN | — | — | Nevada investigativo |
| The New Republic | https://newrepublic.com | — | EN | — | — | USA — politica e cultura |
| The Pudding | https://pudding.cool | — | — | US | — | Visual essays — USA |
| The Trace | https://www.thetrace.org | — | EN | — | — | Armi USA |
| The Walrus | https://thewalrus.ca | — | EN | — | — | Canada — long-form |
| Time | https://time.com | — | EN | — | — | USA settimanale |
| Toronto Star | https://www.thestar.com | — | EN | — | — | Canada |
| Trinidad Express | https://trinidadexpress.com | — | — | TT | — | Trinidad |
| Trinidad Guardian | https://www.guardian.co.tt | — | EN | — | — | Trinidad |
| TRT World | https://www.trtworld.com | — | EN | — | — | Turchia pubblica |
| Truco (Argentina) | https://chequeado.com/truco | — | — | AR | — | Fact-check politico — Argentina |
| Truthout Environment | https://truthout.org/environment | — | — | US | — | Giustizia ambientale — USA |
| UNCTAD Stat | https://unctadstat.unctad.org | — | — | — | — | Commercio internazionale, investimenti esteri — Gratuito — Portale ufficiale |
| UNESCO Institute of Statistics | https://uis.unesco.org | — | — | — | — | Istruzione, cultura, scienza, comunicazione — Gratuito — Portale ufficiale |
| UNIDO Statistics Portal | https://stat.unido.org | — | — | — | — | Industria manifatturiera globale — Gratuito — Portale ufficiale |
| USA Today | https://www.usatoday.com | https://rss.usatoday.com/usatoday/news | EN | — | — | USA mass |
| Variety | https://variety.com | https://variety.com/feed/ | EN | — | — | Entertainment |
| VERA Files | https://verafiles.org | — | EN | — | — | Fact-checking PH — Filippine |
| Verificado MX | https://verificado.mx | — | — | — | — | Fact-check — FC |
| Vice News | https://www.vice.com/en/section/news | — | EN | — | — | News giovani |
| VICE World News | https://www.vice.com/en/section/world-news | — | EN | — | — | Conflitti globali |
| Voice of America | https://www.voanews.com | — | EN | — | — | USA governo |
| Vox | https://www.vox.com | — | EN | — | — | Spiegazioni policy |
| War on the Rocks | https://warontherocks.com | — | EN | — | — | Sicurezza difesa |
| Washington Blade | https://www.washingtonblade.com | — | EN | — | — | LGBTQ+ USA |
| Washington Post FC | https://www.washingtonpost.com/politics/fact-checker | — | — | US | — | Kessler — USA |
| Washington Post World | https://www.washingtonpost.com/world | — | EN | — | — | USA premium |
| Wired | https://www.wired.com | — | EN | — | — | Tech cultura |
| WNYC | https://www.wnyc.org | https://www.wnyc.org/rss/ | EN | — | — | New York Radio |
| World Politics Review | https://www.worldpoliticsreview.com | — | EN | — | — | Analisi globale |
| WWF News | https://www.worldwildlife.org/magazine | — | — | Globale | — | Conservazione |
| Zona Docs | https://zonadocs.mx | — | — | MX | — | Doc/inv. — Messico |

### 1.2 Giornalismo Investigativo (221)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| +972 Magazine | https://www.972mag.com | https://www.972mag.com/feed/ | EN | — | — | Conflitto israelo-palestinese — Israele/Palestina |
| 100Reporters | https://100r.org | — | — | Globale | — | Network reporter |
| Africa Is a Country | https://africasacountry.com | — | EN | — | — | Cultura e politica — Pan-Africa |
| African Arguments | https://africanarguments.org | — | EN | — | — | Analisi politica — Pan-Africa |
| Afrique XXI | https://afriquexxi.info | https://afriquexxi.info/spip.php?page=backend | FR | — | — | Investigativo AF — Africa Inv. FR |
| Agência Pública | https://apublica.org | — | PT | — | — | Investigativo brasiliano — Brasile |
| Al-Monitor | https://www.al-monitor.com | https://www.al-monitor.com/rss | EN | — | — | Medio Oriente — MENA |
| AllAfrica | https://allafrica.com | — | EN | — | — | Aggregatore notizie africane — Pan-Africa |
| AmaBhungane | https://amabhungane.org | — | EN | — | — | Corruzione, stato — Sudafrica |
| Anara | https://anara.com | — | — | Asia Centrale | — | Media indipendenti — Asia centrale |
| Animal Político | https://www.animalpolitico.com | — | ES | — | — | Politica e corruzione — Messico |
| Antimafia Duemila | https://www.antimafiaduemila.com | — | — | — | — | Rivista specializzata — Antimafia |
| AP Investigative | https://apnews.com/hub/ap-investigations | — | — | US | — | Inchieste AP — USA |
| Apache | https://www.apache.be | — | NL | — | — | Belgio — investigativo fiammingo |
| Armando.info | https://armando.info | — | ES | — | — | Corruzione, potere — Venezuela |
| Article 14 | https://www.article-14.com | — | EN | — | — | Diritti e costituzione — India |
| Atlatszo.hu | https://atlatszo.hu | https://atlatszo.hu/feed/ | HU | — | — | Investigativo ungherese — Ungheria Inv. |
| BBC Afrique | https://www.bbc.com/afrique | https://feeds.bbci.co.uk/afrique/rss.xml | FR | — | — | BBC Africa |
| Bellingcat | https://www.bellingcat.com | — | EN | — | — | OSINT, geolocalizzazione — Globale |
| Bellingcat Online Toolkit | https://docs.google.com/spreadsheets/d/18rtqh8EG2q1xBo2cLNyhIDuK9jrPGwYr9DI2UncoqJQ | — | — | Globale | — | Bellingcat tools list — Pubblico — Spreadsheet |
| Bellingcat OSINT Challenge | https://www.bellingcat.com/resources/how-tos | — | — | — | Pubblico | Training |
| Bellingcat Podcast | https://www.bellingcat.com/category/resources/podcasts | — | — | — | — | OSINT — Podcast |
| Bivol | https://bivol.bg | — | — | BG | — | Investigativo bulgaro — Bulgaria |
| Caixin | https://www.caixinglobal.com | — | EN | — | — | Business investigativo CN — Cina |
| CENOZO | https://cenozo.org | — | FR | — | — | Sahel/Africa Occ. — investigativo transfrontaliero |
| Center for Public Integrity | https://publicintegrity.org | — | — | US | — | Investigativo nonprofit — USA |
| Centre for Information Resilience | https://www.centreforinformationresilience.org | — | — | Globale | — | OSINT e diritti umani |
| Chequeado | https://chequeado.com | — | ES | — | — | Fact-checking — Argentina |
| CINS | https://www.cins.rs | — | SR/EN | — | — | Serbia — centro giornalismo investigativo |
| CIPER Chile | https://www.ciperchile.cl | — | ES | — | — | Investigativo cileno — Cile |
| CIRO | https://cironline.org | — | — | US | — | Investigativo USA |
| City Bureau | https://www.citybureau.org | — | EN | — | — | Giornalismo civico Chicago — USA |
| CJID | https://thecjid.org | — | EN | — | — | Nigeria/Africa Occ. — Centre for Journalism Innovation |
| Coconuts Media | https://coconuts.co | — | EN | — | — | Media digitale SE Asia |
| Confidencial | https://confidencial.digital | https://confidencial.digital/feed/ | ES | — | — | Indipendente nicaraguense — Nicaragua |
| Congo Research Group | https://www.congoresearchgroup.org | — | — | CG | — | Investigativo Congo — Africa |
| Connectas | https://connectas.org | — | — | — | — | Network giornalistico LATAM — Regionale |
| Context.ro | https://context.ro | — | RO | — | — | Romania — investigativo |
| Contextual | https://www.contextual.news | — | — | Europa | — | Cross-border journalism |
| Correctiv | https://correctiv.org | — | — | DE | — | Investigativo tedesco — Germania |
| Cuartoscuro | https://cuartoscuro.com.mx | — | — | MX | — | Fotoreportage — Messico |
| Cuestión Pública | https://cuestionpublica.com | — | ES | — | — | Investigativo colombiano — Colombia |
| Daily Maverick | https://www.dailymaverick.co.za | https://www.dailymaverick.co.za/feed/ | EN | — | — | Analisi e inchieste — Sudafrica |
| Danwatch | https://danwatch.dk | — | — | DK | — | Investigativo danese — Danimarca |
| Daraj Media | https://daraj.com | https://daraj.com/feed/ | AR | — | — | Investigativo arabo — Pan-Arab Inv. |
| Datasketch | https://www.datasketch.es | — | — | CO | — | Data journalism — Colombia |
| Dawn Investigations | https://www.dawn.com/investigations | — | — | PK | — | Investigativo pachistano — Pakistan |
| DDoSecrets | https://ddosecrets.com | — | — | Globale | — | Leak e dataset — Pubblico — Database |
| De Correspondent | https://www.decorrespondent.nl | — | — | NL | — | Giornalismo membro — Paesi Bassi |
| Desinformémonos | https://desinformemonos.org | — | — | MX | — | Movimenti sociali — Messico |
| DIG Awards | https://dig-awards.org | — | — | — | — | Festival giornalismo investigativo — Investigativo — Doc/investigativo |
| Direkt36 | https://www.direkt36.hu/en | — | — | HU | — | Corruzione, potere — Ungheria |
| Direktoro Media | https://direktoro.media | — | — | Europa | — | Network investigativo |
| Disclose | https://disclose.ngo | — | — | FR | — | Investigativo, ambiente — Francia |
| Dnevnik.si | https://www.dnevnik.si | https://www.dnevnik.si/?format=rss | SL | — | — | Investigativo sloveno — Slovenia |
| Ekspresso | https://ekspresso.ge | — | — | GE | — | Investigativo georgiano — Georgia |
| El CLIP | https://www.elclip.org | — | — | — | — | Centro investigativo LATAM — Regionale |
| El Confidencial | https://www.elconfidencial.com | — | ES | — | — | Investigativo spagnolo — Spagna |
| El Destape | https://www.eldestapeweb.com | — | ES | — | — | Investigativo — Argentina |
| El Diaro.es | https://www.eldiario.es | https://www.eldiario.es/rss/ | ES | — | — | Investigativo spagnolo — Spagna |
| El Faro | https://elfaro.net | https://elfaro.net/es/rss | ES | — | — | Investigativo salvadoregno — El Salvador |
| El Sabueso MX | https://www.animalpolitico.com/el-sabueso | — | — | — | — | Messico — FC |
| EUobserver | https://euobserver.com | — | — | EU | — | Giornalismo UE indipendente |
| Finance Uncovered | https://www.financeuncovered.org | — | — | GB/EU | — | Finanza investigativa |
| Follow The Money (NL) | https://www.ftm.nl | — | NL | — | — | Finanza crimine — Paesi Bassi |
| Follow The Money (USA) | https://followthemoney.org | — | — | — | Pubblico | Finanziamenti politici USA — Database |
| Follow The Money NL | https://www.ftm.nl/dossiers | — | — | — | Freemium | Economia NL — Database |
| Foundation Investigative Journalism | https://fij.ng | — | EN | — | — | Nigeria investigativo |
| FragDenStaat | https://fragdenstaat.de | — | — | DE | — | FOIA tedesco — Germania |
| Frontier Myanmar | https://www.frontiermyanmar.net | — | EN | — | — | Analisi politica — Myanmar |
| Fund for Investigative Journalism | https://fij.org | — | — | — | — | USA — Funding |
| Fundacja Reporterów | https://fundacjareporterow.org | — | PL/EN | — | — | Polonia — fondazione reporter (VSquare) |
| GIJN | https://gijn.org | — | — | Globale | — | Risorse per giornalisti |
| GK | https://gk.city | — | ES | — | — | Investigativo digitale — Ecuador |
| Global Witness | https://www.globalwitness.org | — | — | Globale | — | Corruzione e ambiente — Pubblico — Database |
| Grounded News | https://grounded.news | — | — | — | — | Comparazione fonti — Media bias analysis |
| Himal Southasian | https://www.himalmag.com | — | EN | — | — | Analisi regionale — Asia meridionale |
| ICIJ | https://www.icij.org | — | — | Globale | — | Panama Papers, offshore |
| ICIJ Offshore Leaks | https://offshoreleaks.icij.org | — | — | — | Pubblico | Società offshore — Database |
| ICJK — Ján Kuciak Investigative Center | https://icjk.sk | — | SK/EN | — | — | Slovacchia — investigativo |
| Il Narco | https://ilnarco.blogspot.com | — | — | — | — | Blog specializzato — Criminalità organizzata — Crimine org. |
| InfoAmazonia | https://infoamazonia.org | — | PT/EN | — | — | Amazzonia data journalism — Brasile |
| InfoCuria | https://infocuria.eu | — | — | EU | — | Giustizia europea |
| InfoLibre | https://www.infolibre.es | — | ES | — | — | Indipendente spagnolo — Spagna |
| InfoNile | https://infonile.org | — | EN | — | — | Bacino del Nilo — geo-giornalismo acqua |
| Initium Media | https://theinitium.com | — | ZH | — | — | Investigativo HK — Hong Kong |
| Inkyfada | https://inkyfada.com | https://inkyfada.com/en/feed/ | EN/AR | — | — | Investigativo tunisino — Tunisia Inv. |
| Insecurity Insight | https://insecurityinsight.org | — | — | Globale/Asia | — | Crisi umanitarie |
| InSight Crime | https://insightcrime.org | — | — | Americhe | — | Criminalità organizzata LATAM |
| International Justice Monitor | https://www.ijmonitor.org | — | — | — | — | Crimini di guerra — Globale — Monitor |
| Investigace.cz | https://www.investigace.cz | — | — | CZ | — | Investigativo ceco — Repubblica Ceca |
| Investigate Europe | https://www.investigate-europe.eu | — | — | Europa | — | Network investigativo EU |
| IRPI | https://irpi.eu | — | — | — | — | Istituto Reportage Investigativo |
| IRPI Media | https://irpimedia.irpi.eu | — | — | — | — | Rete giornalisti investigativi — Corruzione, criminalità — Criminalità org., corruzione |
| Istinomer | https://www.istinomer.rs | — | — | RS | — | Fact-checking serbo — Serbia |
| iStories | https://istories.media | — | EN/RU | — | — | Investigativo russo (indipendente) — Russia |
| Khaosod English | https://www.khaosodenglish.com | — | EN | — | — | Investigativo thai — Thailandia |
| Kloop | https://kloop.kg | — | — | KG | — | Investigativo Asia centrale — Kirghizistan |
| Kontekstuell | https://kontekstuell.no | — | — | NO | — | Investigativo norvegese — Norvegia |
| KRIK | https://www.krik.rs | — | — | RS | — | Investigativo balcanico — Serbia |
| L'Espresso Investigazioni | https://espresso.repubblica.it | — | — | — | — | Storico settimanale — Inchieste nazionali |
| La Barra Espaciadora | https://www.labarraespaciadora.com | — | ES | — | — | Investigativo — Ecuador |
| La Diaria | https://ladiaria.com.uy | — | ES | — | — | Investigativo cooperativo — Uruguay |
| La Lista | https://lalista.news | — | — | — | — | Inchieste sociali — Investigativo |
| La Silla Vacía | https://lasillavacia.com | — | ES | — | — | Politica colombiana — Colombia |
| LatAm Journalism Review | https://latamjournalismreview.org | — | — | — | — | Risorse per giornalisti — Regionale |
| Liberainformazione | https://www.liberainformazione.org | — | — | — | — | Associazione Libera — Antimafia |
| Lighthouse Reports | https://www.lighthousereports.com | — | — | Europa | — | Investigativo collaborativo |
| Linkiesta Inchieste | https://www.linkiesta.it/tag/inchieste | — | — | — | — | Approfondimenti — Investigativo |
| Mafia Export | https://www.mafiaexport.it | — | — | — | — | Inchieste sulla 'ndrangheta — Mafia internazionale — 'Ndrangheta int. |
| Mail & Guardian | https://mg.co.za | https://mg.co.za/feed/ | EN | — | — | Investigativo sudafricano — Sudafrica Inv. |
| Malaysiakini | https://www.malaysiakini.com | — | EN/MS | — | — | Investigativo malese — Malaysia |
| Mediapart | https://www.mediapart.fr | — | FR | — | — | Francia investigativo |
| Mediapart Afrique | https://www.mediapart.fr/journal/international/afrique | — | — | Africa | — | FR investigativo Africa |
| Mediazone | https://www.mediazone.cz | — | — | CZ | — | Analisi media — Rep. Ceca |
| Meduza | https://meduza.io | — | EN/RU | — | — | Media russo indipendente — Russia |
| MeridioNews | https://meridionews.it | — | — | IT-Sicilia | — | Sicilia — Locale/investigativo |
| Mnemonic | https://mnemonic.org | — | — | Globale | — | Diritti umani digitali |
| Mongabay Latam | https://es.mongabay.com | — | — | — | — | Ambiente e investigativo — Regionale |
| MuckRock | https://www.muckrock.com | — | — | US | — | FOIA e trasparenza — USA |
| Mzalendo | https://www.mzalendo.com | — | — | KE | — | Tracking parlamentare — Kenya |
| Nairobi Law Monthly | https://nairobilawmonthly.com | — | EN | — | — | Diritto e investigativo — Kenya |
| Narcomafie | https://narcomafie.it | — | — | — | — | Antimafia — Criminalità |
| Nation Africa | https://nation.africa | https://nation.africa/rss/ | EN | — | — | Kenya e Africa orientale |
| Netzwerk Recherche | https://netzwerkrecherche.org | — | DE | — | — | Germania — rete giornalisti investigativi |
| Newtral | https://www.newtral.es | — | — | ES | — | Fact-checking + investigativo — Spagna |
| Nexo Jornal | https://nexojornal.com.br | — | PT | — | — | Data journalism — Brasile |
| Nikkei Business | https://business.nikkei.com | — | — | JP | — | Business JP — Giappone |
| NordEst Economia | https://www.nordesteconomia.it | — | — | — | — | Triveneto — Locale |
| Novaya Gazeta Europe | https://novayagazeta.eu | — | EN/RU | — | — | Investigativo in esilio — Russia |
| Nómada | https://nomada.gt | — | ES | — | — | Investigativo digitale — Guatemala |
| OC Index Africa | https://ocindex.africa | — | — | Pan-Africa | — | Criminalità organizzata — Africa |
| OCCRP | https://www.occrp.org | — | EN | — | — | Criminalità organizzata — Globale |
| OCCRP Aleph | https://aleph.occrp.org | — | — | — | Freemium | Documenti, aziende, persone — Registrazione (Pro) — Database |
| OCCRP Data | https://data.occrp.org | — | — | — | Pubblico | Dataset investigativi — Database |
| OCCRP Podcast | https://www.occrp.org/en/podcasts | — | — | — | — | Investigativo — Podcast |
| Ojo Público | https://ojopublico.com | — | ES | — | — | Investigativo peruviano — Perù |
| Ojoconmipisto | https://ojoconmipisto.com | — | — | GT | — | Finanza pubblica GT — Guatemala |
| Open Democracy | https://www.opendemocracy.net | — | UK | — | — | Democrazia e potere — UK/Globale |
| Open Secrets Blog | https://www.opensecrets.org/news/feed | — | — | US | — | Finanziamenti politici — USA |
| openDemocracy Russia | https://www.opendemocracy.net/en/odr | — | — | RU | — | Russia |
| Openpolis | https://www.openpolis.it | — | — | — | — | Politici e dati — Data journalism |
| Ossigeno per l'Informazione | https://www.ossigeno.info | — | — | — | — | Minacce alla stampa — Giornalisti sotto tutela — Libertà stampa |
| Outlier Media | https://outliermedia.org | — | — | US | — | Investigativo locale — USA |
| Oštro | https://www.ostro.si | — | — | SI | — | Investigativo sloveno — Slovenia |
| Pambazuka News | https://www.pambazuka.org | — | EN | — | — | Giustizia sociale — Pan-Africa |
| PaperTrail Media | https://papertrail.media | — | — | — | — | Data journalism — Investigativo |
| Philippine Center for Investigative Journalism | https://pcij.org | — | EN | — | — | Filippine investigativo |
| Pie de Página | https://piedepagina.mx | — | ES | — | — | Diritti umani Messico |
| Platform Investico | https://www.platform-investico.nl | — | — | BE/NL | — | Investigativo fiammingo — Belgio |
| Plaza Pública | https://www.plazapublica.com.gt | — | ES | — | — | Investigativo centroamericano — Guatemala |
| PODER | https://poderlatam.org | — | — | — | — | Corporate accountability — Regionale |
| Poligrafi | https://www.poligrafi.si | — | — | SI | — | Fact-checking sloveno — Slovenia |
| POLITICO EU Parliament | https://www.politico.eu/section/politics | — | — | EU | — | Policy UE |
| Premium Times | https://www.premiumtimesng.com | https://www.premiumtimesng.com/feed/ | EN | — | — | Investigativo nigeriano — Nigeria Inv. |
| ProPublica | https://www.propublica.org | — | EN | — | — | Investigativo nonprofit |
| ProPublica Data | https://www.propublica.org/datastore | — | — | US | — | Dataset inv. — USA |
| ProPublica Local | https://www.propublica.org/local | — | EN | — | — | USA locale investigativo |
| Punch Nigeria | https://punchng.com | — | EN | — | — | Nigeria news |
| Público España | https://www.publico.es | — | ES | — | — | Progressista investigativo — Spagna |
| Quartz Africa | https://qz.com/africa | — | EN | — | — | Business Africa — Pan-Africa |
| Quinto Elemento Lab | https://quintoelab.org | — | ES | — | — | Investigativo messicano — Messico |
| Rappler | https://www.rappler.com | — | EN | — | — | Investigativo filippino — Filippine |
| Rappler Fact Check | https://www.rappler.com/newsbreak/fact-check | — | — | PH | — | Fact-check Rappler — Filippine |
| Re:Check | https://recheck.media | — | — | BG | — | Fact-checking — Bulgaria |
| Report Mainz | https://www.swr.de/report | — | — | DE | — | TV investigativa — Germania |
| Report RAI | https://www.report.rai.it | — | — | — | — | Programma RAI — TV investigativa |
| Reporters United | https://reportersunited.gr | — | — | GR | — | Investigativo greco — Grecia |
| Republik | https://www.republik.ch | — | — | CH | — | Giornalismo membro (no RSS) — Svizzera |
| Rest of World | https://restofworld.org | — | EN | — | — | Tech e impatto globale — Globale (Sud globale) |
| Reuters Investigates | https://www.reuters.com/investigates | — | — | Globale | — | Inchieste Reuters |
| Reveal News | https://revealnews.org | — | — | US | — | Investigativo radio — USA |
| RFI Afrique | https://www.rfi.fr/fr/afrique | https://www.rfi.fr/fr/afrique/rss | FR | — | — | Radio francofona — Radio FR |
| Rise Project | https://www.riseproject.ro | — | — | RO | — | Criminalità organizzata — Romania |
| Sahara Reporters | https://saharareporters.com | — | EN | — | — | Corruzione e governance — Nigeria |
| SCOOP (Serbia) | https://scoop.rs | — | — | RS | — | Investigativo serbo — Serbia |
| Scroll.in | https://scroll.in | — | EN | — | — | Investigativo progressista — India |
| Sicilian Post | https://www.sicilianpost.it | — | — | IT-Sicilia | — | Sicilia — Locale/investigativo |
| Siena.lt | https://siena.lt | — | LT | — | — | Lituania — centro investigativo |
| Solomon | https://solomonews.gr | — | — | GR | — | Investigativo greco — Grecia |
| Status | https://statesman.com | — | — | US | — | Investigativo — USA |
| Taktika Media | https://taktikamedia.com | — | — | Caucaso | — | Media caucaso indipendente |
| Tamedia Investigativ | https://www.tamedia.ch | — | — | CH | — | Multi-titolo svizzero — Svizzera |
| Tansa | https://tansajp.org | — | JA/EN | — | — | Giappone — investigativo indipendente |
| Telejato | https://www.telejato.it | — | — | IT-Sicilia | — | Sicilia — TV locale/investigativa |
| Tempo | https://en.tempo.co | — | EN | — | — | Investigativo indonesiano — Indonesia |
| Texas Tribune | https://www.texastribune.org | https://www.texastribune.org/rss.xml | EN | — | — | Investigativo Texas — Texas Inv. |
| The 19th | https://19thnews.org | — | EN | — | — | Donne e politica — USA |
| The Africa Report | https://www.theafricareport.com | https://www.theafricareport.com/feed/ | EN | — | — | Business e politica — Pan-Africa |
| The Bureau of Investigative Journalism | https://www.thebureauinvestigates.com | — | UK | — | — | Droni, conflitti, corruzione |
| The Cable | https://www.thecable.ng | https://www.thecable.ng/feed | EN | — | — | Investigativo — Nigeria Inv. |
| The Caravan | https://caravanmagazine.in | — | EN | — | — | Long-form investigativo — India |
| The Continent | https://thecontinent.org | — | EN | — | — | Settimanale africano — Pan-Africa |
| The Conversation | https://theconversation.com | — | — | Globale | — | Ricerca accademica |
| The Dial | https://thedial.media | — | — | — | — | Inchieste USA/Italia — Investigativo — Investigativo USA/IT |
| The East African | https://www.theeastafrican.co.ke | https://www.theeastafrican.co.ke/rss/ | EN | — | — | Africa orientale — Africa Est |
| The Elephant | https://www.theelephant.info | — | EN | — | — | Analisi politica africana — Kenya |
| The Ferret | https://theferret.scot | — | — | GB-SCT | — | Investigativo scozzese — Scozia |
| The Guardian NG | https://guardian.ng | https://guardian.ng/feed/ | EN | — | — | Investigativo nigeriano — Nigeria |
| The Insider (Russia) | https://theins.ru | — | RU | — | — | Investigativo russo — Russia |
| The Intercept | https://theintercept.com | — | EN | — | — | Surveillance, intelligence — USA |
| The Intercept Brasil | https://theintercept.com/brasil | — | PT | — | — | Brasile investigativo |
| The Irrawaddy | https://www.irrawaddy.com | — | EN | — | — | Investigativo birmano — Myanmar |
| The Kashmir Walla | https://thekashmirwalla.com | — | EN | — | — | Kashmir investigativo |
| The Ken | https://the-ken.com | — | EN | — | — | Business investigativo — India |
| The Kyiv Independent | https://kyivindependent.com | — | EN | — | — | Guerra e politica ucraina — Ucraina |
| The Markup | https://themarkup.org | — | — | US | — | Tech accountability — USA |
| The Marshall Project | https://www.themarshallproject.org | — | EN | — | — | Giustizia penale — USA |
| The Sentry | https://thesentry.org | — | EN | — | — | Crimini di guerra e finanza — Africa |
| The Sentry Data | https://thesentry.org/tools | — | — | — | Database | Crimini di guerra — Pubblico |
| The Signals Network | https://thesignalsnetwork.org | — | — | Globale | — | Protezione fonti |
| The Standard | https://www.standardmedia.co.ke | https://www.standardmedia.co.ke/rss/all | EN | — | — | Investigativo keniota — Kenya |
| Toscana Media News | https://www.toscanamedia.it | — | — | — | — | Toscana — Locale |
| Transitions | https://tol.org | — | — | CEE | — | Notizie dall'Europa dell'est |
| TW Reporter | https://www.twreporter.org | — | ZH/EN | — | — | Investigativo taiwanese — Taiwan |
| Type Investigations | https://www.typeinvestigations.org | — | — | US | — | Investigativo indipendente — USA |
| VSquare | https://vsquare.org | — | — | CEE | — | Visegrad investigativo |
| WikiLeaks | https://wikileaks.org | — | — | Globale | — | Leak e documenti |
| WikiLeaks Library | https://wikileaks.org/library | — | — | — | Pubblico | Documenti classificati — Archivio |
| Wire India | https://thewire.in | https://thewire.in/feed | EN | — | — | Investigativo indiano — India Inv. |
| Yemen Data Project | https://yemendataproject.org | — | EN | — | — | Conflitto Yemen — Yemen Ricerca |

### 1.3 Italia (277)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AbruzzoWeb | https://www.abruzzoweb.it | — | IT | — | — | Abruzzo — testata digitale |
| ACN Italia | https://www.acn.gov.it | — | — | — | — | Agenzia Cyber Naz. — CERT/NL IT |
| Actionaid Italia | https://www.actionaid.it | — | — | — | — | Advocacy — Italia |
| Adnkronos | https://www.adnkronos.com | https://www.adnkronos.com/rss | — | — | — | Wire Service — Agenzia |
| Affaritaliani | https://www.affaritaliani.it | https://www.affaritaliani.it/rss | — | — | Online | Politica |
| AGCOM | https://www.agcom.it | — | — | IT | — | Regolatore comunicazioni — Italia |
| AGI | https://www.agi.it | https://www.agi.it/rss | — | — | — | Semi-pubblica — Wire Service — Agenzia |
| AGI Economia | https://www.agi.it/economia | — | — | — | — | Wire |
| AgrigentoNotizie | https://www.agrigentonotizie.it | — | IT | — | — | Agrigento — network Citynews |
| Altalex | https://www.altalex.com | https://www.altalex.com/feed | — | — | — | Legale |
| Altreconomia | https://altreconomia.it | https://altreconomia.it/feed/ | — | — | — | Economia critica — Economia sostenibile — Rivista |
| ANAC | https://www.anticorruzione.it | — | — | — | — | Anticorruzione — Italia — Regolatore |
| Analisi Difesa | https://www.analisidifesa.it | https://www.analisidifesa.it/feed/ | — | — | Online | Militare — Difesa |
| AnconaToday | https://www.anconatoday.it | — | IT | — | — | Ancona — network Citynews |
| ANSA | https://www.ansa.it | https://www.ansa.it/sito/ansait_rss.xml | — | — | — | Principale — Wire Service — Agenzia |
| Antimafia2000 | https://www.antimafia2000.com | — | — | — | — | Antimafia |
| AostaSera | https://aostasera.it | — | IT | — | — | Valle d'Aosta — testata digitale |
| ArezzoNotizie | https://www.arezzonotizie.it | — | IT | — | — | Arezzo — network Citynews |
| Articolo 21 | https://www.articolo21.org | — | — | — | — | Libertà stampa |
| Autorità Garante Concorrenza | https://www.agcm.it | — | — | — | — | Antitrust IT — Italia — Regolatore |
| Avvenire | https://www.avvenire.it | https://www.avvenire.it/rss | IT | — | — | Cattolico — Quotidiano |
| Avviso Pubblico | https://www.avvisopubblico.it | — | — | — | — | Legalità enti locali — Italia |
| Bari Today | https://www.baritoday.it | — | — | IT-Puglia | — | Bari online — Puglia |
| Basilicata24 | https://www.basilicata24.it | — | IT | — | — | Basilicata — testata digitale |
| BlogSicilia | https://www.blogsicilia.it | — | IT | — | — | Sicilia — portale regionale |
| Bologna Today | https://www.bolognatoday.it | — | — | IT-Emilia-Romagna | — | Bologna online — Emilia |
| Borsa Italiana News | https://www.borsaitaliana.it | — | — | — | — | LSE Group — Finanza |
| Brescia Oggi | https://www.bresciaoggi.it | — | — | IT-Lombardia | — | Brescia |
| BresciaToday | https://www.bresciatoday.it | — | IT | — | — | Brescia — network Citynews |
| BrindisiReport | https://www.brindisireport.it | — | IT | — | — | Brindisi — network Citynews |
| Calcio &Finanza | https://www.calcioefinanza.it | https://www.calcioefinanza.it/feed/ | — | — | — | Calcio economia — Sport/Business |
| Carmilla | https://www.carmillaonline.com | https://www.carmillaonline.com/feed/ | — | — | — | Contro-cultura — Cultura |
| Carta di Roma | https://www.cartadiroma.org | https://www.cartadiroma.org/feed/ | — | — | Online | Migrazioni |
| Casteddu Online | https://www.castedduonline.it | — | IT | — | — | Cagliari — testata digitale |
| CataniaToday | https://www.cataniatoday.it | — | IT | — | — | Catania — network Citynews |
| ChietiToday | https://www.chietitoday.it | — | IT | — | — | Chieti — network Citynews |
| Class CNBC | https://www.classcnbc.it | — | — | — | — | Business TV — TV |
| Commonware | https://www.commonware.org | — | — | — | — | Movimenti — Politica |
| Consob | https://www.consob.it | — | — | — | — | Regolatore mercati — Italia |
| Corriere del Mezzogiorno | https://corrieredelmezzogiorno.corriere.it | — | — | Sud | — | Sud Italia — Locale |
| Corriere del Ticino | https://www.cdt.ch | — | IT/DE | — | — | Svizzera italiana |
| Corriere dell'Umbria | https://www.corrieredellaumbria.it | — | — | IT-Umbria | — | Perugia — Umbria |
| Corriere della Calabria | https://www.corrieredellacalabria.it | — | IT | — | — | Calabria — testata digitale |
| Corriere della Sera Milano | https://milano.corriere.it | — | — | IT-Lombardia | — | Milano — Lombardia |
| Corriere delle Alpi | https://corrierealpi.gelocal.it | — | IT | — | — | Belluno — gruppo GEDI |
| Corriere dello Sport | https://www.corrieredellosport.it | https://www.corrieredellosport.it/rss | — | — | — | Roma/Napoli — Sport |
| Corriere di Bologna | https://corrieredibologna.corriere.it | — | — | IT-Emilia-Romagna | — | Bologna CdS — Emilia |
| Corriere di Firenze | https://corrierefiorentino.corriere.it | — | — | IT-Toscana | — | Firenze CdS — Toscana |
| Corriere di Torino | https://torino.corriere.it | — | — | IT-Piemonte | — | Torino CdS — Piemonte |
| Corriere Economia | https://www.corriere.it/economia | — | — | — | — | Supplemento |
| Corriere Immigrazione | https://www.corriereimmigrazione.it | — | — | — | Online | Migrazioni |
| Corriere Immigrazione | https://www.corriere.it/immigrazione | — | — | — | — | Sezione CdS — Migrazioni |
| Corriere Roma | https://roma.corriere.it | — | — | IT-Lazio | — | Roma CdS — Lazio |
| Corte Costituzionale IT | https://www.cortecostituzionale.it | — | — | IT | — | Giustizia costituzionale — Italia |
| Corte dei Conti IT | https://www.corteconti.it | — | — | — | — | Controllo pubblico — Italia |
| Critica Liberale | https://www.criticaliberale.it | — | — | — | — | Liberalismo — Politica |
| Cronache Maceratesi | https://www.cronachemaceratesi.it | — | IT | — | — | Macerata — testata digitale |
| Dagospia | https://www.dagospia.com | — | — | — | Online | Retroscena |
| DDay.it | https://www.dday.it | https://www.dday.it/rss | — | — | Online | Tech |
| Demos | https://www.demos.it | — | — | IT | — | Analisi politica/sociologia — Italia |
| Digi24 Romania | https://www.digi24.ro | https://www.digi24.ro/rss.xml | RO | — | — | Romania news |
| Dillinger News | https://www.dillingernews.it | — | — | — | Online | Crime e cronaca |
| Dinamopress | https://www.dinamopress.it | https://www.dinamopress.it/feed/ | — | — | — | Movimenti — Politica |
| Dire | https://www.dire.it | https://www.dire.it/feed/ | — | — | — | Parlamentare — Agenzia |
| Diritto.it | https://www.diritto.it | https://www.diritto.it/rss | — | — | — | Legale |
| Dolomiten | https://www.dolomiten.it | — | — | — | — | Tedesco AA |
| Domani | https://www.editorialedomani.it | https://www.editorialedomani.it/feed | — | — | Online | Investigativo |
| Doppiozero | https://www.doppiozero.com | https://www.doppiozero.com/rss.xml | — | — | Online | Cultura |
| East Journal | https://www.eastjournal.net | https://www.eastjournal.net/feed | — | — | Online | Est Europa — Geopolitica |
| Eastwest | https://eastwest.eu | https://eastwest.eu/feed/ | — | — | — | Geopolitica — Rivista |
| Eco di Bergamo | https://www.ecodibergamo.it | https://www.ecodibergamo.it/rss | — | IT-Lombardia | — | Bergamo — Locale |
| Effimera | https://effimera.org | — | — | — | — | Filosofia — Cultura |
| Emergency | https://www.emergency.it | — | — | — | — | Umanitario |
| EUnews | https://www.eunews.it | https://www.eunews.it/feed/ | — | EU | — | UE in italiano — Notizie europee in italiano — UE |
| Euromaidan Press | https://euromaidanpress.com | https://euromaidanpress.com/feed/ | EN | — | — | Ucraina |
| Facta.news | https://www.facta.news | — | — | IT | — | Fact-checking italiano — Italia |
| Famiglia Cristiana | https://www.famigliacristiana.it | https://www.famigliacristiana.it/rss | — | — | — | Cattolico — Settimanale |
| Fanpage | https://www.fanpage.it | https://www.fanpage.it/feed/ | — | — | Online | News |
| Fanpage Sport | https://sport.fanpage.it | — | — | — | — | Online — Sport |
| Farmacista33 | https://www.farmacista33.it | — | — | — | — | Farmacia — Sanità |
| Filodiritto | https://www.filodiritto.com | — | — | — | — | Legale |
| FirenzeToday | https://www.firenzetoday.it | — | IT | — | — | Firenze — network Citynews |
| Fnsi | https://www.fnsi.it | — | — | — | — | Sindacato — Giornalismo |
| FoggiaToday | https://www.foggiatoday.it | — | IT | — | — | Foggia — network Citynews |
| FondazioneMeeting | https://www.meetingrimini.org | — | — | IT | — | Cultura e società — Italia |
| ForlìToday | https://www.forlitoday.it | — | IT | — | — | Forlì-Cesena — network Citynews |
| Formiche | https://formiche.net | https://formiche.net/feed/ | — | — | Online | Policy/Difesa — Geopolitica/Policy |
| FrosinoneToday | https://www.frosinonetoday.it | — | IT | — | — | Frosinone — network Citynews |
| FTSV (Italia) | https://www.parlamento.it/parlam/leggi/deleghe/97276dl.htm | — | — | — | Pubblico | Lobby register IT — Archivio |
| G4Media | https://www.g4media.ro | https://www.g4media.ro/feed/ | RO | — | — | Romania Inv. |
| Garante Privacy | https://www.garanteprivacy.it | — | — | — | — | Privacy IT — Italia — Regolatore |
| Gazzetta del Sud | https://www.gazzettadelsud.it | — | — | IT-Calabria/Sicilia | — | Sicilia-Calabria — Locale |
| Gazzetta dello Sport | https://www.gazzetta.it | https://www.gazzetta.it/rss | — | — | — | Principale IT — Sport |
| Gazzetta di Mantova | https://gazzettadimantova.gelocal.it | — | IT | — | — | Mantova — gruppo GEDI, quotidiano più antico d'Italia |
| Gazzetta di Parma | https://www.gazzettadiparma.it | — | — | IT-Emilia-Romagna | — | Parma — Emilia |
| Gazzetta di Reggio | https://www.gazzettadireggio.it | — | — | IT-Emilia-Romagna | — | Reggio Emilia |
| Genova24 | https://www.genova24.it | — | IT | — | — | Liguria — testata digitale |
| GenovaToday | https://www.genovatoday.it | — | IT | — | — | Genova — network Citynews |
| Giornale di Brescia | https://www.giornaledibrescia.it | — | — | IT-Lombardia | — | Brescia — Lombardia |
| Giornale di Calabria | https://www.giornaledicalabria.it | — | — | IT-Calabria | — | Calabria — Locale |
| Giornale di Sicilia | https://gds.it | https://gds.it/rss | — | IT-Sicilia | — | Palermo — Sicilia |
| Giornale di Vicenza | https://www.giornalediviencenza.it | — | — | IT-Veneto | — | Vicenza — Veneto |
| GiornalistiItalia | https://www.giornalistiitalia.it | — | — | — | — | Giornalismo |
| Global Project | https://www.globalproject.info | https://www.globalproject.info/rss | — | — | — | Sinistra radicale — Politica |
| GoNews | https://www.gonews.it | — | IT | — | — | Toscana — testata digitale regionale |
| Governo Italiano | https://governo.it | — | — | — | — | Governo IT — Italia — Istituzione |
| HDBlog | https://www.hdblog.it | https://www.hdblog.it/rss/ | — | — | Online | Tech |
| HotNews | https://www.hotnews.ro | — | RO | — | — | Romania online |
| Hromadske Ukraine | https://hromadske.ua | — | — | UA | — | Public media — Ucraina |
| Huffpost Italia | https://www.huffingtonpost.it | https://www.huffingtonpost.it/rss | — | — | Online | Opinion |
| HWUpgrade | https://www.hwupgrade.it | https://www.hwupgrade.it/rss/ | — | — | Online | Hardware — Tech |
| ICE Agenzia | https://www.ice.it | — | — | IT | — | Commercio estero — Italia |
| ICT4Executive | https://www.ict4executive.it | — | — | — | — | Management — ICT |
| Il Bo Live (Padova) | https://ilbolive.unipd.it | https://ilbolive.unipd.it/it/rss.xml | — | — | — | UniPD — Università — Universitario |
| Il Centro | https://www.ilcentro.it | — | IT | — | — | Abruzzo — quotidiano regionale |
| Il Cittadino MB | https://www.ilcittadinomb.it | — | — | IT-Lombardia | — | Monza Brianza — Lombardia |
| Il Corriere del Veneto | https://corrieredelveneto.corriere.it | — | — | IT-Veneto | — | Venezia CdS — Veneto |
| Il Corriere della Sera | https://www.corriere.it | https://www.corriere.it/rss/primo_piano.xml | IT | — | — | 1° quotidiano — già in cat. 2 — Quotidiano |
| Il Fatto Quotidiano | https://www.ilfattoquotidiano.it | https://www.ilfattoquotidiano.it/feed/ | — | — | — | Investigativo — Quotidiano |
| Il Foglio | https://www.ilfoglio.it | https://www.ilfoglio.it/rss | — | — | — | Liberale — Quotidiano |
| Il Friuli | https://www.ilfriuli.it | — | IT | — | — | Friuli — settimanale e portale |
| Il Gazzettino | https://www.ilgazzettino.it | https://www.ilgazzettino.it/rss | — | IT-Veneto | — | Veneto — Locale |
| Il Giornale | https://www.ilgiornale.it | https://www.ilgiornale.it/rss | — | — | — | Centro-destra — Quotidiano |
| il Giornale dell'Architettura | https://www.tgarch.it | — | — | — | — | Architettura |
| Il Giorno | https://www.ilgiorno.it | https://www.ilgiorno.it/rss | — | IT-Lombardia | — | Lombardia — Quotidiano |
| Il Libraio | https://www.illibraio.it | https://www.illibraio.it/feed/ | — | — | — | Libri — Cultura |
| Il Manifesto | https://ilmanifesto.it | https://ilmanifesto.it/feed/ | IT | — | — | Sinistra — Quotidiano |
| Il Mattino | https://www.ilmattino.it | https://www.ilmattino.it/rss | — | IT-Campania | — | Napoli/Sud — Quotidiano |
| Il Messaggero | https://www.ilmessaggero.it | https://www.ilmessaggero.it/rss | — | — | — | Roma — Quotidiano |
| Il Messaggero Veneto | https://www.messaggeroveneto.it | https://www.messaggeroveneto.it/rss | — | IT-FVG | — | Udine — Locale |
| Il Piccolo | https://www.ilpiccolo.it | https://www.ilpiccolo.it/rss | — | IT-FVG | — | Trieste — Locale |
| Il Post | https://www.ilpost.it | https://www.ilpost.it/feed/ | — | — | Online | Qualità |
| Il Quotidiano del Sud | https://www.quotidianodelsud.it | — | — | Sud | — | Cosenza |
| Il Quotidiano di Sicilia | https://www.quotidianodisicilia.it | — | — | IT-Sicilia | — | Sicilia |
| Il Quotidiano Giuridico | https://www.ilquotidianogiuridico.it | — | — | — | — | Legale |
| Il Resto del Carlino | https://www.ilrestodelcarlino.it | https://www.ilrestodelcarlino.it/rss | — | IT-Emilia-Romagna | — | Emilia — Quotidiano |
| Il Riformista | https://www.ilriformista.it | https://www.ilriformista.it/feed | — | — | — | Garantista — Quotidiano |
| Il Secolo XIX | https://www.ilsecoloxix.it | https://www.ilsecoloxix.it/rss | — | IT-Liguria | — | Liguria — Quotidiano |
| Il Sole 24 Ore | https://www.ilsole24ore.com | https://www.ilsole24ore.com/rss/italia.xml | — | — | — | Finanza — Economia |
| Il Sole 24 Ore Tech | https://www.ilsole24ore.com/tecnologia | — | — | — | — | FT24 — Tech |
| Il Tascabile | https://www.iltascabile.com | https://www.iltascabile.com/feed/ | — | — | Online | Cultura |
| Il Tempo | https://www.iltempo.it | https://www.iltempo.it/rss | — | IT-Lazio | — | Roma — Lazio — Quotidiano |
| Il Tirreno | https://www.iltirreno.it | https://www.iltirreno.it/rss | — | IT-Toscana | — | Livorno/Grosseto — Locale |
| Il Trentino | https://www.ildolomiti.it | https://www.ildolomiti.it/rss | — | IT-TAA | — | Trentino — Quotidiano |
| IlNapolista | https://ilnapolista.it | https://ilnapolista.it/feed/ | — | — | — | Calcio critico — Sport |
| IlPescara | https://www.ilpescara.it | — | IT | — | — | Pescara — network Citynews |
| IlPiacenza | https://www.ilpiacenza.it | — | IT | — | — | Piacenza — network Citynews |
| InsideOver | https://it.insideover.com | https://it.insideover.com/feed/ | — | — | Online | Geopolitica |
| Internazionale | https://www.internazionale.it | — | — | — | — | Traduzioni da media esteri — Settimanale |
| InvestireOggi | https://www.investireoggi.it | https://www.investireoggi.it/feed/ | — | — | — | Finanza Personale |
| isNews | https://www.isnews.it | — | IT | — | — | Isernia/Molise — testata digitale |
| ISTAT | https://www.istat.it | — | — | — | Pubblico | Statistiche IT — Italia — Database |
| ITV News | https://www.itv.com/news | https://www.itv.com/news/rss | EN | — | — | TV UK |
| Jacobin Italia | https://jacobinitalia.it | https://jacobinitalia.it/feed/ | — | — | Online | Sinistra radicale — Politica |
| Key4biz | https://www.key4biz.it | https://www.key4biz.it/feed/ | — | — | Online | TLC/PA — Tech |
| Kumu | https://kumu.io | — | — | — | Freemium | Mappe relazionali — Network Mapping |
| L'Adige | https://www.ladige.it | — | IT | — | — | Trento — quotidiano storico |
| L'Alto Adige | https://www.altoadige.it | — | — | IT-TAA | — | Alto Adige — Trentino-AA — Quotidiano |
| L'Arena | https://www.larena.it | https://www.larena.it/rss | — | IT-Veneto | — | Verona — Locale |
| L'Espresso | https://lespresso.it | https://lespresso.it/feed/ | — | — | — | Investigativo — Settimanale |
| L'Essenziale | https://www.lessenziale.it | https://www.lessenziale.it/rss | — | — | Online | Migrazioni |
| L'Indipendente | https://www.lindipendente.online | https://www.lindipendente.online/feed/ | — | — | Online | No-pub |
| L'Unione Sarda | https://www.unionesarda.it | https://www.unionesarda.it/rss | — | IT-Sardegna | — | Sardegna — Locale |
| La Gazzetta del Mezzogiorno | https://www.lagazzettadelmezzogiorno.it | https://www.lagazzettadelmezzogiorno.it/rss | — | IT-Puglia/Basilicata | — | Bari — Puglia-Basilicata |
| La Guida | https://www.laguida.it | — | IT | — | — | Cuneo — settimanale locale |
| La Lettura (CdS) | https://www.corriere.it/la-lettura | — | — | — | — | Settimanale — Cultura |
| La Nazione | https://www.lanazione.it | https://www.lanazione.it/rss | — | IT-Toscana | — | Toscana — Locale |
| La Nuova del Sud | https://www.lanuova.net | — | IT | — | — | Basilicata — quotidiano |
| La Nuova Ferrara | https://lanuovaferrara.gelocal.it | — | IT | — | — | Ferrara — gruppo GEDI |
| La Nuova Sardegna | https://www.lanuovasardegna.it | https://www.lanuovasardegna.it/rss | — | IT-Sardegna | — | Sassari — Locale |
| La Nuova Venezia | https://nuovavenezia.gelocal.it | — | IT | — | — | Venezia — gruppo GEDI |
| La Prealpina | https://www.prealpina.it | — | — | IT-Lombardia | — | Varese — Lombardia |
| La Provincia (CO-CR-LC) | https://laprovinciacr.it | — | — | IT-Lombardia | — | Cremona/Como/LC — Lombardia |
| La Provincia Pavese | https://laprovinciapavese.gelocal.it | — | IT | — | — | Pavia — gruppo GEDI |
| La Repubblica | https://www.repubblica.it | — | — | — | — | Homepage — Quotidiano |
| La Repubblica Economia | https://www.repubblica.it/economia | — | — | — | — | — |
| La Repubblica Firenze | https://firenze.repubblica.it | — | — | IT-Toscana | — | Firenze — Toscana |
| La Sentinella del Canavese | https://lasentinella.gelocal.it | — | IT | — | — | Piemonte (Ivrea) — gruppo GEDI |
| La Sicilia | https://www.lasicilia.it | https://www.lasicilia.it/rss.xml | — | IT-Sicilia | — | Sicilia — Quotidiano |
| La Stampa | https://www.lastampa.it | — | — | — | — | Torino e nazionale — Quotidiano |
| La Tribuna di Treviso | https://tribunatreviso.gelocal.it | — | IT | — | — | Treviso — gruppo GEDI |
| La Verità | https://www.laverita.info | https://www.laverita.info/feed/ | — | — | — | Sovranista — Quotidiano |
| La7 | https://www.la7.it/tg-la7 | — | — | — | — | Cairo — Cairoeditore — TV |
| LaC News24 | https://www.lacnews24.it | — | IT | — | — | Calabria — network all-news |
| Latina Oggi | https://www.latinaoggi.eu | — | IT | — | — | Latina — quotidiano locale |
| LeccePrima | https://www.lecceprima.it | — | IT | — | — | Lecce — network Citynews |
| LeccoToday | https://www.leccotoday.it | — | IT | — | — | Lecco — network Citynews |
| Leggo | https://www.leggo.it | https://www.leggo.it/rss | — | — | Gratuito | Free press — Quotidiano |
| Lettera43 | https://www.lettera43.it | https://www.lettera43.it/feed/ | — | — | Online | Investigativo |
| Libera | https://www.libera.it | — | — | — | — | Antimafia — Italia |
| Libero | https://liberoquotidiano.it | https://liberoquotidiano.it/rss | — | — | — | Destra — Quotidiano |
| Libertatea | https://www.libertatea.ro | — | RO | — | — | Romania |
| Libertà | https://www.liberta.it | — | IT | — | — | Piacenza — quotidiano storico |
| Limes | https://www.limesonline.com | https://www.limesonline.com/feed/ | — | — | — | Geopolitica — Rivista |
| Linkiesta | https://www.linkiesta.it | https://www.linkiesta.it/rss/ | — | — | Online | Liberale |
| Live Sicilia | https://www.livesicilia.it | — | — | IT-Sicilia | — | Online — Sicilia |
| Lsdi (Libertà di Stampa) | https://www.lsdi.it | — | IT | — | — | Monitor |
| Mangialibri | https://www.mangialibri.com | — | — | — | — | Recensioni — Cultura |
| Mattino di Padova | https://mattinopadova.gelocal.it | — | — | IT-Veneto | — | Padova — Veneto |
| Medici Senza Frontiere IT | https://www.msf.it | — | — | — | — | Umanitario |
| Messaggero Umbria | https://www.ilmessaggero.it/umbria | — | — | IT-Umbria | — | Perugia — Umbria |
| MessinaToday | https://www.messinatoday.it | — | IT | — | — | Messina — network Citynews |
| Micromega | https://www.micromega.net | https://www.micromega.net/feed/ | — | — | — | Cultura/Politica — Rivista |
| Milano Finanza | https://www.milanofinanza.it | https://www.milanofinanza.it/rss | — | — | — | Finanza — Economia |
| MilanoToday | https://www.milanotoday.it | — | — | IT-Lombardia | — | Milano online — Lombardia |
| Minima &Moralia | https://www.minimaetmoralia.it | https://www.minimaetmoralia.it/feed/ | — | — | — | Letteratura — Cultura |
| ModenaToday | https://www.modenatoday.it | — | IT | — | — | Modena — network Citynews |
| MonzaToday | https://www.monzatoday.it | — | IT | — | — | Monza-Brianza — network Citynews |
| Napoli Today | https://www.napolitoday.it | — | — | IT-Campania | — | Napoli online — Campania |
| Network Digital 360 | https://www.networkdigital360.it | https://www.networkdigital360.it/feed/ | — | — | Online | Business IT — Tech |
| Normattiva | https://www.normattiva.it | — | — | IT | — | Leggi italiane — Pubblico — Testi delle leggi italiane — Database |
| Notizie Radicali | https://www.radicali.it/notizie | — | — | — | — | Liberali — Politica |
| NovaraToday | https://www.novaratoday.it | — | IT | — | — | Novara — network Citynews |
| Nuovo Quotidiano di Puglia | https://www.quotidianodipuglia.it | — | IT | — | — | Puglia — gruppo Caltagirone |
| Nurse Times | https://www.nursetimes.org | https://www.nursetimes.org/feed/ | — | — | — | Infermieri — Sanità |
| Open Fact Check | https://www.open.online/categoria/fact-checking | — | — | IT | — | FC Open.online — Italia |
| Open.online | https://www.open.online | https://www.open.online/feed/ | — | — | Online | Antimafia |
| OpenParlamento | https://openparlamento.it | — | — | — | — | Parlamento italiano — Pubblico — Database |
| Ordine Giornalisti | https://www.odg.it | — | — | — | — | Ordine — Giornalismo |
| Osservatore Romano | https://www.osservatoreromano.va | — | — | VA | — | Prospettiva Santa Sede — Vaticano |
| Osservatorio Balcani | https://www.balcanicaucaso.org | https://www.balcanicaucaso.org/rss | — | — | Online | Balcani — Geopolitica |
| PadovaOggi | https://www.padovaoggi.it | — | IT | — | — | Padova — network Citynews |
| Pagella Politica | https://pagellapolitica.it | — | — | IT | — | Fact-checking politico — Italia |
| Palermo Today | https://www.palermotoday.it | — | — | IT-Sicilia | — | Palermo online — Sicilia |
| Pandora Rivista | https://www.pandorarivista.it | https://www.pandorarivista.it/feed/ | — | — | — | Politica — Rivista |
| Panorama | https://www.panorama.it | https://www.panorama.it/rss/ | — | — | — | Business — Settimanale |
| ParmaToday | https://www.parmatoday.it | — | IT | — | — | Parma — network Citynews |
| PCM | https://www.governo.it/it/dipartimenti/dipartimento-informazione-editoria | — | — | IT | — | DIE — Italia |
| PerugiaToday | https://www.perugiatoday.it | — | IT | — | — | Perugia — network Citynews |
| Primocanale | https://www.primocanale.it | — | IT | — | — | Liguria — emittente all-news regionale |
| Primonumero | https://www.primonumero.it | — | IT | — | — | Campobasso/Molise — testata digitale |
| ProTV Romania | https://stirileprotv.ro | — | RO | — | — | Romania TV |
| Punto Informatico | https://www.punto-informatico.it | https://www.punto-informatico.it/rss/ | — | — | Online | Tech diritti — Tech |
| QuiComo | https://www.quicomo.it | — | IT | — | — | Como — network Citynews |
| Quirinale | https://www.quirinale.it | — | — | IT | — | Presidenza Repubblica — Italia |
| Quotidiano Sanità | https://www.quotidianosanita.it | https://www.quotidianosanita.it/rss | — | — | — | Sanità |
| Rai News 24 | https://www.rainews.it | https://www.rainews.it/rss | — | — | Online | RAI — TV/Online |
| Rai Tre | https://www.raiplay.it/programmi/report | — | — | — | — | Report RAI — TV |
| RavennaToday | https://www.ravennatoday.it | — | IT | — | — | Ravenna — network Citynews |
| Redattore Sociale | https://www.redattoresociale.it | https://www.redattoresociale.it/rss | — | — | Online | Sociale |
| Reggio Today | https://www.reggiotoday.it | — | — | IT-Emilia-Romagna | — | Reggio online — Emilia |
| Registro Imprese IT | https://www.registroimprese.it | — | — | — | Database | Aziende italiane — Freemium |
| RiminiToday | https://www.riminitoday.it | — | IT | — | — | Rimini — network Citynews |
| Roars | https://www.roars.it | https://www.roars.it/feed/ | — | — | — | Università — Blog |
| Roma Today | https://www.romatoday.it | https://www.romatoday.it/rss | — | IT-Lazio | — | Roma online — Lazio |
| SalernoToday | https://www.salernotoday.it | — | IT | — | — | Salerno — network Citynews |
| Salto.bz | https://salto.bz | — | IT/DE | — | — | Alto Adige — testata indipendente bilingue |
| Sardinia Post | https://www.sardiniapost.it | — | — | IT-Sardegna | — | Online — Sardegna |
| Scenari Economici | https://scenarieconomici.it | https://scenarieconomici.it/feed/ | — | — | — | Economia — Blog |
| Sky Sport | https://sport.sky.it | — | — | — | — | Sport — TV |
| Sky TG24 | https://tg24.sky.it | https://tg24.sky.it/rss.xml | — | — | Online | Sky — TV/Online |
| Sole 24 Ore Norme & Tributi | https://www.ilsole24ore.com/norme-e-tributi | — | — | — | — | Legale-fiscale |
| SondrioToday | https://www.sondriotoday.it | — | IT | — | — | Sondrio — network Citynews |
| Sport Mediaset | https://sportmediaset.mediaset.it | — | — | — | — | Mediaset — Sport |
| Stampa e Regime | https://www.stamparegime.it | — | — | — | — | Critica media |
| StartupBusiness | https://www.startupbusiness.it | https://www.startupbusiness.it/feed/ | — | — | Online | Startup — Tech |
| TGCom24 | https://www.tgcom24.mediaset.it | https://www.tgcom24.mediaset.it/rss | — | — | Online | Mediaset — TV/Online |
| TMNews | https://www.tmnews.it | — | — | — | — | Ex Agenzia — Online |
| Today.it | https://www.today.it | https://www.today.it/rss | — | — | Online | Mass |
| Torino Oggi | https://www.torinooggi.it | — | — | IT-Piemonte | — | Torino — Piemonte |
| TPI | https://www.tpi.it | https://www.tpi.it/feed/ | — | — | Online | International |
| Trentino | https://www.trentino.corriere.it | — | — | IT-TAA | — | Trentino-AA — Locale |
| TrentoToday | https://www.trentotoday.it | — | IT | — | — | Trento — network Citynews |
| TriestePrima | https://www.triesteprima.it | — | IT | — | — | Trieste — network Citynews |
| Tuttosport | https://www.tuttosport.com | https://www.tuttosport.com/rss/home.xml | — | — | — | Torino/Juventus — Sport |
| UdineToday | https://www.udinetoday.it | — | IT | — | — | Udine — network Citynews |
| Valigia Blu | https://www.valigiablu.it | https://www.valigiablu.it/feed/ | — | — | Online | Qualità — Fact-checking, inchieste |
| Valigia Blu FC | https://www.valigiablu.it/tag/fact-checking | — | — | IT | — | Italia |
| Valori | https://valori.it | https://valori.it/feed/ | — | — | Online | Finanza etica — Economia |
| VeneziaToday | https://www.veneziatoday.it | — | IT | — | — | Venezia — network Citynews |
| VeronaSera | https://www.veronasera.it | — | IT | — | — | Verona — network Citynews |
| Virgilio Notizie | https://notizie.virgilio.it | — | — | — | — | Aggregatore — Portale |
| Volere la Luna | https://volerelaluna.it | — | — | — | — | Analisi critica — Politica — Blog |
| VoxEurop Italia | https://voxeurop.eu/it | https://voxeurop.eu/it/feed/ | — | — | Online | Europa — Prospettiva europea |
| Whistleblower.it | https://www.whistleblower.it | — | — | IT | — | Protezione whistleblower — Italia |
| Wired Italia | https://www.wired.it | https://www.wired.it/feed/ | — | — | Online | Tech/Cultura — Tech/Culture |
| ZeroUno | https://www.zerounoweb.it | https://www.zerounoweb.it/feed/ | — | — | — | Enterprise — ICT |

### 1.4 Europa Occidentale (264)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| 192.com | https://www.192.com | — | — | — | — | Ricerca persone UK — Freemium — People Search |
| 20minutos | https://www.20minutos.es | — | ES | — | — | Spagna free press |
| 24 heures | https://www.24heures.ch | — | FR | — | — | Vaud — Losanna |
| ABC España | https://www.abc.es | — | ES | — | — | Spagna conservatore |
| AD.nl | https://www.ad.nl | — | NL | — | — | Paesi Bassi |
| Alternatives Économiques | https://www.alternatives-economiques.fr | — | FR | — | — | Francia — mensile economico eterodosso |
| ANSSI France | https://www.ssi.gouv.fr | — | — | — | — | Francia — CERT |
| Antena 3 Noticias | https://www.antena3.com | — | ES | — | — | Spagna — TV commerciale principale |
| Ara | https://www.ara.cat | — | CA | — | — | Catalogna |
| Atlantico | https://www.atlantico.fr | — | FR | — | — | Online FR |
| Augsburger Allgemeine | https://www.augsburger-allgemeine.de | — | DE | — | — | Baviera — Augusta |
| Badische Zeitung | https://www.badische-zeitung.de | — | DE | — | — | Baden-Württemberg — Friburgo |
| Banco de España | https://www.bde.es | — | — | — | — | Spagna — Banca centrale |
| Belfast Telegraph | https://www.belfasttelegraph.co.uk | — | EN | — | — | Irlanda del Nord |
| Berliner Zeitung | https://www.berliner-zeitung.de | — | DE | — | — | Berlino — quotidiano |
| Berner Zeitung | https://www.bernerzeitung.ch | — | DE | — | — | Berna |
| BFM TV | https://www.bfmtv.com | — | FR | — | — | TV news FR |
| Bild | https://www.bild.de | https://www.bild.de/rssfeeds.rss | DE | — | — | Tabloide DE |
| Birmingham Mail | https://www.birminghammail.co.uk | — | EN | — | — | UK — Birmingham |
| Blick | https://www.blick.ch | — | DE | — | — | Svizzera tabloide |
| BR24 | https://www.br.de | — | DE | — | — | Baviera — emittente pubblica |
| BristolLive / Bristol Post | https://www.bristolpost.co.uk | — | EN | — | — | UK — Bristol |
| BSI Germany | https://www.bsi.bund.de | — | — | — | — | Germania — CERT |
| Canarias7 | https://www.canarias7.es | — | ES | — | — | Canarie — Las Palmas |
| Capital | https://www.capital.fr | — | FR | — | — | Francia — mensile economico |
| Capital.de | https://www.capital.de | — | DE | — | — | Finanza DE |
| Capital.gr | https://www.capital.gr | — | — | GR | — | Business — Grecia |
| CERI Sciences Po | https://www.sciencespo.fr/ceri | — | — | FR | — | Ricerca politica — Francia |
| Channel 4 FactCheck | https://www.channel4.com/news/factcheck | — | UK | — | — | FC UK |
| Channel 5 News | https://www.channel5.com/news | — | EN | — | — | TV UK |
| Charente Libre | https://www.charentelibre.fr | — | FR | — | — | Francia — Charente |
| Charlie Hebdo | https://charliehebdo.fr | — | FR | — | — | Satira FR |
| ChronicleLive | https://www.chroniclelive.co.uk | — | EN | — | — | UK — Newcastle/Nord-Est |
| CIRCL (Luxembourg) | https://www.circl.lu | — | — | — | — | Lussemburgo — CERT |
| CNN Greece | https://www.cnngreece.gr | — | — | GR | — | Online — Grecia |
| Companies House UK | https://find-and-update.company-information.service.gov.uk | — | — | — | Database | Aziende UK — Pubblico |
| Corse-Matin | https://www.corsematin.com | — | FR | — | — | Corsica |
| Courrier International | https://www.courrierinternational.com | — | FR | — | — | Traduzioni globali |
| Courrier Picard | https://www.courrier-picard.fr | — | FR | — | — | Francia — Piccardia, Amiens |
| Daily Record | https://www.dailyrecord.co.uk | — | EN | — | — | Scozia — tabloid principale |
| Daily Telegraph | https://www.telegraph.co.uk | — | EN | — | — | UK conservatore |
| De Morgen | https://www.demorgen.be | — | NL | — | — | Belgio |
| De Standaard | https://www.standaard.be | https://www.standaard.be/rss.xml | NL | — | — | Belgio |
| De Telegraaf | https://www.telegraaf.nl | — | NL | — | — | Paesi Bassi tabloide |
| De Tijd | https://www.tijd.be | — | NL | — | — | Belgio — economico fiammingo |
| De Volkskrant | https://www.volkskrant.nl | — | NL | — | — | Paesi Bassi |
| Deia | https://www.deia.eus | — | ES/EU | — | — | Spagna — Bilbao |
| Der Spiegel | https://www.spiegel.de | — | DE | — | — | Germania |
| Diari de Tarragona | https://www.diaridetarragona.com | — | ES/CA | — | — | Spagna — Tarragona |
| Diario Córdoba | https://www.diariocordoba.com | — | ES | — | — | Spagna — Cordova |
| Diario de Cádiz | https://www.diariodecadiz.es | — | ES | — | — | Spagna — Cadice (Grupo Joly) |
| Diario de Ibiza | https://www.diariodeibiza.es | — | ES | — | — | Spagna — Baleari, Ibiza |
| Diario de León | https://www.diariodeleon.es | — | ES | — | — | Spagna — León |
| Diario de Mallorca | https://www.diariodemallorca.es | — | ES/CA | — | — | Baleari |
| Diario de Navarra | https://www.diariodenavarra.es | — | ES | — | — | Spagna — Navarra |
| Diario de Sevilla | https://www.diariodesevilla.es | — | ES | — | — | Andalusia — Siviglia |
| Diario Sur | https://www.diariosur.es | — | ES | — | — | Andalusia — Malaga |
| Die Zeit | https://www.zeit.de | — | DE | — | — | Germania settimanale |
| Diário de Notícias | https://www.dn.pt | — | PT | — | — | Portogallo |
| DNA — Dernières Nouvelles d'Alsace | https://www.dna.fr | — | FR | — | — | Alsazia — Strasburgo |
| Documento Greece | https://www.documentonews.gr | — | — | GR | — | Settimanale inv. — Grecia |
| Doğruluk Payı | https://dogrulukpayi.com | — | — | TR | — | FC TR — Turchia |
| DPA International | https://www.dpa-international.com | https://www.dpa-international.com/feed | EN | — | — | Wire Germania |
| Dublin Live | https://www.dublinlive.ie | https://www.dublinlive.ie/rss.xml | EN | — | — | Irlanda |
| DW English | https://www.dw.com/en | — | EN | — | — | Germania |
| Eastern Daily Press | https://www.edp24.co.uk | — | EN | — | — | UK — East Anglia, Norwich |
| EFE Verifica | https://verifica.efe.com | — | — | ES | — | FC ES — Spagna |
| Efimerida ton Syntakton | https://www.efsyn.gr | — | — | GR | — | Sinistra — Grecia |
| El Comercio | https://www.elcomercio.es | — | ES | — | — | Spagna — Asturie, Gijón |
| El Correo | https://www.elcorreo.com | — | ES | — | — | Paesi Baschi — Bilbao |
| El Diario Montañés | https://www.eldiariomontanes.es | — | ES | — | — | Cantabria |
| El Diario Vasco | https://www.diariovasco.com | — | ES | — | — | Paesi Baschi — San Sebastián |
| El Día | https://www.eldia.es | — | ES | — | — | Canarie — Tenerife |
| El Economista | https://www.eleconomista.es | — | ES | — | — | Spagna — economico |
| El Mundo | https://www.elmundo.es | — | ES | — | — | Spagna |
| El Norte de Castilla | https://www.elnortedecastilla.es | — | ES | — | — | Castiglia e León — Valladolid |
| El País | https://elpais.com | — | ES | — | — | Spagna |
| El Periódico de Aragón | https://www.elperiodicodearagon.com | — | ES | — | — | Spagna — Aragona |
| El Periódico España | https://www.elperiodico.com | https://www.elperiodico.com/es/rss/rss_portada.xml | ES | — | — | Catalogna — Spagna |
| El Punt Avui | https://www.elpuntavui.cat | — | CA | — | — | Spagna — Catalogna, catalanofono |
| European Policy Centre | https://www.epc.eu | — | — | BE | — | UE policy — Belgio |
| Express & Star | https://www.expressandstar.com | — | EN | — | — | UK — Midlands, Wolverhampton |
| Expresso | https://expresso.pt | — | PT | — | — | Portogallo |
| Falter | https://www.falter.at | — | DE | — | — | Austria — settimanale viennese |
| Faro de Vigo | https://www.farodevigo.es | — | ES/GL | — | — | Galizia — Vigo, il più antico di Spagna |
| FAZ | https://www.faz.net | — | DE | — | — | Germania conservatore |
| Focus Online | https://www.focus.de | https://www.focus.de/rss/index.rss | DE | — | — | Magazine DE |
| France 24 | https://www.france24.com | — | EN/FR | — | — | Prospettiva francese |
| France 24 Français | https://www.france24.com/fr | https://www.france24.com/fr/rss | FR | — | — | Francia |
| France Info | https://www.francetvinfo.fr | — | FR | — | — | Radio/TV pubblica |
| Frankfurter Rundschau | https://www.fr.de | — | DE | — | — | Germania sinistra |
| Freie Presse | https://www.freiepresse.de | — | DE | — | — | Sassonia — Chemnitz |
| Granada Hoy | https://www.granadahoy.com | — | ES | — | — | Spagna — Granada |
| Guernsey Press | https://guernseypress.com | — | EN | — | — | Guernsey |
| Hamburger Abendblatt | https://www.abendblatt.de | — | DE | — | — | Amburgo — quotidiano principale |
| Handelsblatt | https://www.handelsblatt.com | — | DE | — | — | Economia DE |
| Hannoversche Allgemeine | https://www.haz.de | — | DE | — | — | Bassa Sassonia — Hannover |
| Herald Scotland | https://www.heraldscotland.com | — | EN | — | — | Scozia |
| Heraldo de Aragón | https://www.heraldo.es | — | ES | — | — | Aragona — Saragozza |
| Het Nieuwsblad | https://www.nieuwsblad.be | — | NL | — | — | Belgio |
| Het Parool | https://www.parool.nl | — | NL | — | — | Amsterdam |
| Huelva Información | https://www.huelvainformacion.es | — | ES | — | — | Spagna — Huelva |
| Ideal | https://www.ideal.es | — | ES | — | — | Andalusia — Granada |
| IHEDN | https://www.ihedn.fr | — | — | FR | — | Difesa FR — Francia |
| In.gr | https://www.in.gr | — | — | GR | — | Online — Grecia |
| Información | https://www.informacion.es | — | ES | — | — | Spagna — Alicante |
| Irish Examiner | https://www.irishexaminer.com | https://www.irishexaminer.com/feed/ | EN | — | — | Irlanda |
| Irish Independent | https://www.independent.ie | — | EN | — | — | Irlanda |
| Irish Times | https://www.irishtimes.com | — | EN | — | — | Irlanda |
| Jersey Evening Post | https://jerseyeveningpost.com | — | EN | — | — | Jersey |
| Jornal de Noticias | https://www.jn.pt | https://www.jn.pt/rss/ | PT | — | — | Portogallo |
| Journalism.co.uk | https://www.journalism.co.uk | — | UK | — | — | Media industry news |
| Kathimerini Greece | https://www.ekathimerini.com | — | — | GR | — | Quality English — Grecia |
| Kieler Nachrichten | https://www.kn-online.de | — | DE | — | — | Schleswig-Holstein — Kiel |
| Kleine Zeitung | https://www.kleinezeitung.at | — | DE | — | — | Stiria/Carinzia — quotidiano principale |
| Kölner Stadt-Anzeiger | https://www.ksta.de | — | DE | — | — | NRW — Colonia |
| L'Echo | https://www.lecho.be | — | FR | — | — | Belgio — economico francofono |
| L'Est Républicain | https://www.estrepublicain.fr | — | FR | — | — | Grand Est — Nancy |
| L'Express | https://www.lexpress.fr | — | FR | — | — | Francia |
| L'Humanité | https://www.humanite.fr | — | FR | — | — | Francia sinistra |
| L'Indépendant | https://www.lindependant.fr | — | FR | — | — | Francia — Perpignan |
| L'Obs | https://www.nouvelobs.com | — | FR | — | — | Francia |
| L'Opinion | https://www.lopinion.fr | — | FR | — | — | Francia — liberale, economia |
| L'Union | https://www.lunion.fr | — | FR | — | — | Francia — Champagne, Reims |
| La Dépêche du Midi | https://www.ladepeche.fr | — | FR | — | — | Occitania — Tolosa |
| La Libre Belgique | https://www.lalibre.be | — | FR | — | — | Belgio |
| La Montagne | https://www.lamontagne.fr | — | FR | — | — | Alvernia — Clermont-Ferrand |
| La Nouvelle République | https://www.lanouvellerepublique.fr | — | FR | — | — | Centro — Tours |
| La Nueva España | https://www.lne.es | — | ES | — | — | Asturie — Oviedo |
| La Opinión de Murcia | https://www.laopiniondemurcia.es | — | ES | — | — | Spagna — Murcia |
| La Provence | https://www.laprovence.com | — | FR | — | — | PACA — Marsiglia |
| La Provincia | https://www.laprovincia.es | — | ES | — | — | Spagna — Las Palmas |
| La Razón | https://www.larazon.es | https://www.larazon.es/rss/ | ES | — | — | Spagna conservatore |
| La Rioja | https://www.larioja.com | — | ES | — | — | Spagna — La Rioja |
| La République des Pyrénées | https://www.larepubliquedespyrenees.fr | — | FR | — | — | Francia — Pau |
| La Vanguardia | https://www.lavanguardia.com | — | ES/CA | — | — | Catalogna |
| La Verdad | https://www.laverdad.es | — | ES | — | — | Murcia |
| La Voix du Nord | https://www.lavoixdunord.fr | — | FR | — | — | Alta Francia — Lille |
| La Voz de Galicia | https://www.lavozdegalicia.es | — | ES/GL | — | — | Galizia — quotidiano principale |
| Las Provincias | https://www.lasprovincias.es | — | ES | — | — | Comunità Valenciana |
| Le Dauphiné Libéré | https://www.ledauphine.com | — | FR | — | — | Alpi — Grenoble |
| Le Figaro | https://www.lefigaro.fr | — | FR | — | — | Francia |
| Le JDD | https://www.lejdd.fr | — | FR | — | — | Francia — domenicale nazionale |
| Le Monde | https://www.lemonde.fr | — | FR | — | — | Francia |
| Le Parisien | https://www.leparisien.fr | https://www.leparisien.fr/rss/ | FR | — | — | Parigi |
| Le Point | https://www.lepoint.fr | — | FR | — | — | Francia |
| Le Progrès | https://www.leprogres.fr | — | FR | — | — | Alvernia-Rodano-Alpi — Lione |
| Le Républicain Lorrain | https://www.republicain-lorrain.fr | — | FR | — | — | Francia — Lorena, Metz |
| Le Soir | https://www.lesoir.be | https://www.lesoir.be/arc/outboundfeeds/rss/ | FR | — | — | Belgio |
| Le Temps | https://www.letemps.ch | https://www.letemps.ch/feed.rss | FR | — | — | Svizzera |
| Le Télégramme | https://www.letelegramme.fr | — | FR | — | — | Bretagna — Brest |
| Les Décodeurs (Le Monde) | https://www.lemonde.fr/les-decodeurs | — | — | FR | — | Fact-checking FR — Francia |
| Levante-EMV | https://www.levante-emv.com | — | ES | — | — | Comunità Valenciana |
| Libération | https://www.liberation.fr | — | FR | — | — | Francia sinistra |
| Libération Désintox | https://www.liberation.fr/checknews | — | — | FR | — | Fact-checking FR — Francia |
| Liverpool Echo | https://www.liverpoolecho.co.uk | — | EN | — | — | UK — Liverpool |
| LSE Media Policy | https://blogs.lse.ac.uk/mediapolicyproject | — | — | — | — | London — Accademia |
| Luxembourg Times | https://luxembourgtimes.com | — | EN | — | — | Lussemburgo |
| Luxemburger Wort | https://www.wort.lu | https://www.wort.lu/rss/nachrichten.rss | DE | — | — | Lussemburgo |
| Luzerner Zeitung | https://www.luzernerzeitung.ch | — | DE | — | — | Svizzera centrale |
| LVZ — Leipziger Volkszeitung | https://www.lvz.de | — | DE | — | — | Sassonia — Lipsia |
| Manager Magazin | https://www.manager-magazin.de | — | DE | — | — | Business DE |
| Manchester Evening News | https://www.manchestereveningnews.co.uk | — | EN | — | — | UK — Manchester (Reach) |
| Marianne | https://www.marianne.net | — | FR | — | — | Francia |
| MDR | https://www.mdr.de | — | DE | — | — | Germania centrale — emittente pubblica |
| Media Lens | https://www.medialens.org | — | UK | — | — | Critica media UK |
| Mercator | https://www.merics.org | — | — | DE | — | Cina — Germania |
| Midi Libre | https://www.midilibre.fr | — | FR | — | — | Occitania — Montpellier |
| Minuten | https://www.20min.ch | — | DE/FR | — | — | Svizzera tabloide |
| Mitteldeutsche Zeitung | https://www.mz.de | — | DE | — | — | Sassonia-Anhalt — Halle |
| Málaga Hoy | https://www.malagahoy.es | — | ES | — | — | Spagna — Malaga |
| Münchner Merkur | https://www.merkur.de | — | DE | — | — | Baviera — Monaco |
| n-tv | https://www.n-tv.de | — | DE | — | — | Germania — all-news |
| Naftemporiki Greece | https://www.naftemporiki.gr | — | — | GR | — | Business — Grecia |
| Naiz | https://www.naiz.eus | — | EU/ES | — | — | Spagna — Paesi Baschi (Gara) |
| NCSC UK | https://www.ncsc.gov.uk | — | UK | — | — | Gov UK — CERT UK — CERT |
| NDR | https://www.ndr.de | — | DE | — | — | Nord — emittente pubblica |
| New Statesman | https://www.newstatesman.com | — | EN | — | — | UK — settimanale progressista |
| Nice-Matin | https://www.nicematin.com | — | FR | — | — | PACA — Nizza |
| Nos.nl | https://nos.nl | — | NL | — | — | NL pubblica |
| Noticias de Navarra | https://www.noticiasdenavarra.com | — | ES | — | — | Spagna — Navarra |
| NRC Handelsblad | https://www.nrc.nl | — | NL | — | — | Paesi Bassi quality |
| NU.nl | https://www.nu.nl | — | NL | — | — | Online NL |
| NZZ | https://www.nzz.ch | — | DE | — | — | Svizzera |
| Nürnberger Nachrichten | https://www.nn.de | — | DE | — | — | Baviera — Norimberga |
| Observador | https://observador.pt | — | PT | — | — | Portogallo online |
| OpenEurope | https://openeurope.org.uk | — | UK | — | — | Brexit/UE |
| Ostsee-Zeitung | https://www.ostsee-zeitung.de | — | DE | — | — | Meclemburgo — Rostock |
| Ouest France | https://www.ouest-france.fr | https://www.ouest-france.fr/rss/une.xml | FR | — | — | Regionale FR |
| OÖNachrichten | https://www.nachrichten.at | — | DE | — | — | Alta Austria — Linz |
| Paris-Normandie | https://www.paris-normandie.fr | — | FR | — | — | Normandia — Rouen |
| Pressgazette | https://pressgazette.co.uk | — | UK | — | — | News industry |
| Private Eye | https://www.private-eye.co.uk | — | EN | — | — | UK — satira e investigazioni |
| Profil | https://www.profil.at | — | DE | — | — | Austria — newsmagazine |
| Proto Thema | https://www.protothema.gr | — | EL | — | — | Grecia — quotidiano più letto |
| Protothema Greece | https://en.protothema.gr | — | — | GR | — | English — Grecia |
| Publico PT | https://www.publico.pt | https://feeds.publico.pt/publico/rss | PT | — | — | Portogallo quality |
| Reuters Institute | https://reutersinstitute.politics.ox.ac.uk | — | UK | — | — | Ricerca media — Accademia |
| RFI English | https://www.rfi.fr/en | — | EN | — | — | Francia radio int. |
| RFI Français | https://www.rfi.fr/fr | — | FR | — | — | Radio int. FR |
| Rheinische Post | https://rp-online.de | — | DE | — | — | NRW — Düsseldorf |
| RTBF | https://www.rtbf.be | — | FR | — | — | Belgio pubblica |
| RTL Nieuws | https://www.rtlnieuws.nl | — | NL | — | — | TV NL |
| RTL.de | https://www.rtl.de | — | DE | — | — | Germania — TV commerciale |
| RTP Notícias | https://www.rtp.pt/noticias | — | PT | — | — | Portogallo pubblica |
| RTS Info | https://www.rts.ch/info | — | FR | — | — | Svizzera francese |
| RTVE Noticias | https://www.rtve.es/noticias | — | ES | — | — | Spagna pubblica |
| RTÉ News | https://www.rte.ie/news | — | EN | — | — | Irlanda pubblica |
| Saarbrücker Zeitung | https://www.saarbruecker-zeitung.de | — | DE | — | — | Saarland |
| Salzburger Nachrichten | https://www.sn.at | — | DE | — | — | Salisburgo |
| Schwäbische Zeitung | https://www.schwaebische.de | — | DE | — | — | Baden-Württemberg — Alta Svevia |
| Segre | https://www.segre.com | — | ES/CA | — | — | Spagna — Lleida |
| Sky News (UK) | https://news.sky.com | https://news.sky.com/rss | EN | — | — | TV UK |
| Slate.fr | https://www.slate.fr | — | FR | — | — | Online FR |
| Spectator World | https://spectatorworld.com | — | EN | — | — | Conservatore UK/USA |
| Spiegel International | https://www.spiegel.de/international | — | EN/DE | — | — | Germania |
| Spiked Online | https://www.spiked-online.com | — | EN | — | — | Libertà civile UK |
| St. Galler Tagblatt | https://www.tagblatt.ch | — | DE | — | — | Svizzera orientale |
| Stern | https://www.stern.de | https://www.stern.de/feed/standard/alle-nachrichten/ | DE | — | — | Magazine DE |
| Stuttgarter Zeitung | https://www.stuttgarter-zeitung.de | — | DE | — | — | Baden-Württemberg — Stoccarda |
| Sud Ouest | https://www.sudouest.fr | — | FR | — | — | Nuova Aquitania — Bordeaux |
| Sächsische Zeitung | https://www.saechsische.de | — | DE | — | — | Sassonia — Dresda |
| Süddeutsche Zeitung | https://www.sueddeutsche.de | — | DE | — | — | Germania |
| Süddeutsche Zeitung Magazin | https://sz-magazin.sueddeutsche.de | — | DE | — | — | Long-form DE |
| Tages-Anzeiger | https://www.tagesanzeiger.ch | https://www.tagesanzeiger.ch/standard.rss | DE | — | — | Svizzera |
| Tagesspiegel | https://www.tagesspiegel.de | — | DE | — | — | Berlino |
| taz | https://taz.de | — | DE | — | — | Germania sinistra |
| Telecinco / Informativos | https://www.telecinco.es | — | ES | — | — | Spagna — Mediaset España |
| TF1 Info | https://www.tf1info.fr | — | FR | — | — | Francia — news TF1/LCI |
| The Courier | https://www.thecourier.co.uk | — | EN | — | — | Scozia — Dundee |
| The Guardian World | https://www.theguardian.com/world | — | EN | — | — | Prospettiva UK |
| The Independent | https://www.independent.co.uk | — | EN | — | — | UK online |
| The Independent US | https://www.independent.co.uk/us | https://www.independent.co.uk/us/rss | EN | — | — | USA edition |
| The Irish News | https://www.irishnews.com | — | EN | — | — | Irlanda del Nord — Belfast |
| The Journal (IE) | https://www.thejournal.ie | — | EN | — | — | Irlanda online |
| The Mirror | https://www.mirror.co.uk | — | EN | — | — | UK tabloid |
| The National (Scotland) | https://www.thenational.scot | — | EN | — | — | Scozia — indipendentista |
| The Press and Journal | https://www.pressandjournal.co.uk | — | EN | — | — | Scozia — Aberdeen/Highlands |
| The Register | https://www.theregister.com | https://www.theregister.com/headlines.xml | EN | — | — | Tech UK |
| The Rest is History | https://therestishistory.com | — | — | — | — | Storia UK — Podcast |
| The Scotsman | https://www.scotsman.com | — | EN | — | — | Scozia |
| The Spectator | https://www.spectator.co.uk | — | EN | — | — | UK — settimanale conservatore |
| The Sun | https://www.thesun.co.uk | — | EN | — | — | UK tabloid |
| The Times of London | https://www.thetimes.co.uk | — | EN | — | — | UK premium |
| The Week | https://theweek.com | — | EN | — | — | Aggregatore UK/USA |
| Thüringer Allgemeine | https://www.thueringer-allgemeine.de | — | DE | — | — | Turingia — Erfurt |
| Tiroler Tageszeitung | https://www.tt.com | — | DE | — | — | Tirolo — Innsbruck |
| To Vima Greece | https://www.tovima.gr | — | — | GR | — | Quality — Grecia |
| Tribune de Genève | https://www.tdg.ch | — | FR | — | — | Ginevra |
| Trouw | https://www.trouw.nl | — | NL | — | — | Paesi Bassi |
| TV5 Monde | https://information.tv5monde.com | — | FR | — | — | TV francofono |
| UnHerd | https://unherd.com | — | EN | — | — | Opinion UK |
| Verificat | https://www.verificat.cat | — | — | ES-CT | — | Fact-checking CA — Catalogna |
| Visão | https://visao.sapo.pt | — | PT | — | — | Portogallo settimanale |
| Vorarlberger Nachrichten | https://www.vn.at | — | DE | — | — | Vorarlberg |
| VRT Nieuws | https://www.vrt.be/vrtnws | — | NL | — | — | Belgio pubblica |
| WalesOnline | https://www.walesonline.co.uk | — | EN | — | — | Galles |
| WAZ | https://www.waz.de | — | DE | — | — | NRW — Ruhr, Funke |
| WDR | https://www1.wdr.de | — | DE | — | — | NRW — emittente pubblica |
| Welt | https://www.welt.de | https://www.welt.de/services/rss-feeds/welt.xml | DE | — | — | Conservatore DE |
| Weser-Kurier | https://www.weser-kurier.de | — | DE | — | — | Brema — quotidiano |
| WirtschaftsWoche | https://www.wiwo.de | — | DE | — | — | Germania — settimanale economico |
| Yorkshire Post | https://www.yorkshirepost.co.uk | — | EN | — | — | UK — Yorkshire, Leeds |
| ZDF | https://www.zdf.de | — | DE | — | — | Germania |

### 1.5 Europa Orientale & Nord Europa (199)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| 15min.lt | https://www.15min.lt | https://www.15min.lt/naujienos/rss | LT | — | — | Lituania |
| 24.hu | https://24.hu | — | HU | — | — | Ungheria |
| 24.kg | https://24.kg | — | RU | — | — | Kirghizistan |
| 24sata | https://www.24sata.hr | — | HR | — | — | Croazia |
| 444.hu | https://444.hu | https://444.hu/rss | HU | — | — | Ungheria Indip. |
| 7x7 Russia | https://7x7-journal.ru | — | — | RU | — | Regionale — Russia |
| 7x7 — Horizontal Russia | https://semnasem.org | — | RU/EN | — | — | Russia — giornalismo regionale indipendente |
| A1Plus Armenia | https://a1plus.am | — | EN/HY | — | — | Armenia |
| Aamulehti | https://www.aamulehti.fi | https://www.aamulehti.fi/rss/uutiset.rss | FI | — | — | Finlandia |
| Adevărul | https://adevarul.ro | — | RO | — | — | Romania — quotidiano storico |
| Adresseavisen | https://www.adressa.no | — | NO | — | — | Norvegia — Trondheim |
| Aftenposten | https://www.aftenposten.no | — | NO | — | — | Norvegia quality |
| Aftonbladet | https://www.aftonbladet.se | — | SV | — | — | Svezia tabloide |
| Agenda.ge | https://agenda.ge | — | EN | — | — | Georgia — news in inglese |
| Agora | https://agora.md | — | RO | — | — | Moldavia — testata digitale |
| Aktuálně.cz | https://zpravy.aktualne.cz | — | CS | — | — | Rep. Ceca online |
| Albania Daily News | https://www.albaniadailynews.com | — | — | AL | — | English — Albania |
| Albinfo Kosovo | https://www.albinfo.com | — | — | XK | — | Albanian — Kosovo |
| Altinget | https://www.altinget.dk | https://www.altinget.dk/rss | DA | — | — | Danimarca Policy |
| APA | https://apa.az | — | AZ/EN | — | — | Azerbaigian — agenzia di stampa |
| Armenpress | https://armenpress.am | — | HY/EN/RU | — | — | Armenia — agenzia di stato |
| Asia-Plus | https://asiaplustj.info | — | EN | — | — | Tagikistan |
| Atlanta Journal-Constitution | https://www.ajc.com | — | EN | — | — | Georgia USA |
| Azatliq (Azerbaijan) | https://www.azadliq.info | — | AZ | — | — | Azerbaijan RFE/RL |
| Azattyq (Kazakhstan) | https://www.azattyq.org | — | KK/EN | — | — | Kazakhstan RFE |
| B92 | https://www.b92.net | https://www.b92.net/rss/ | SR | — | — | Serbia |
| Balkan Insight | https://balkaninsight.com | — | EN | — | — | Balcani in inglese |
| BBC Science & Environment | https://www.bbc.com/news/science_and_environment | — | UK | — | — | News |
| Belarus Zerkalo | https://zerkalo.io | — | RU | — | — | Bielorussia indip. |
| Belarusian Investigative Center | https://investigativecenter.by | — | — | BY | — | Inv. — Bielorussia |
| BelTA (English) | https://eng.belta.by | — | EN | — | — | Bielorussia gov |
| Bergens Tidende | https://www.bt.no | — | NO | — | — | Norvegia — Bergen |
| Berlingske | https://www.berlingske.dk | — | DA | — | — | Danimarca |
| Berlingske Business | https://www.berlingske.dk/business | https://www.berlingske.dk/service/rss | DA | — | — | Danimarca |
| Blic | https://www.blic.rs | — | SR | — | — | Serbia |
| Bulgarian National TV | https://bntnews.bg | — | BG | — | — | Bulgaria pubblica |
| Børsen | https://borsen.dk | — | DA | — | — | Danimarca — economico |
| Capital BG | https://www.capital.bg | — | BG | — | — | Bulgaria economia |
| Caucasus Survey | https://caucasussurvey.org | — | EN | — | — | Accademia Caucaso |
| Censor Ukraine | https://censor.net.ua | — | — | UA | — | War-focused — Ucraina |
| Chronicles (Turkmenistan) | https://www.chrono-tm.org | — | RU/EN | — | — | Turkmenistan |
| CivilNet | https://www.civilnet.am | — | HY/EN | — | — | Armenia — testata indipendente |
| Club Z | https://clubz.bg | — | BG | — | — | Bulgaria |
| Control Risks | https://www.controlrisks.com | — | UK | — | — | Risk consulting |
| Czech Radio (ČRo) | https://www.irozhlas.cz | — | CS | — | — | Rep. Ceca pubblica |
| Dagbladet | https://www.dagbladet.no | — | NO | — | — | Norvegia |
| Dagens Industri | https://www.di.se | https://www.di.se/rss | SV | — | — | Svezia Business |
| Dagens Nyheter | https://www.dn.se | — | SV | — | — | Svezia quality |
| Dan | https://www.dan.co.me | — | SR | — | — | Montenegro — quotidiano |
| Delfi Estonia | https://www.delfi.ee | — | ET | — | — | Estonia online |
| Delfi Latvia | https://www.delfi.lv | — | LV | — | — | Lettonia online |
| Delfi Latvia English | https://eng.lsm.lv | https://www.lsm.lv/rss/ | EN | — | — | Lettonia |
| Delfi Lithuania | https://www.delfi.lt | — | LT | — | — | Lituania online |
| Delo | https://www.delo.si | — | SL | — | — | Slovenia quality |
| Delo.ua | https://delo.ua | — | UK/RU | — | — | Ucraina — business |
| Denik N (BIH) | https://denikn.ba | — | BS | — | — | Bosnia investigativo |
| Denik Referendum | https://denikreferendum.cz | https://denikreferendum.cz/feed/ | CS | — | — | Ceca Indip. |
| Denník N | https://dennikn.sk | — | SK | — | — | Slovacchia quality |
| Dnevni Avaz | https://avaz.ba | — | BS | — | — | Bosnia — quotidiano più diffuso |
| Dnevnik BG | https://www.dnevnik.bg | — | BG | — | — | Bulgaria |
| Do Rzeczy | https://dorzeczy.pl | https://dorzeczy.pl/feed/ | PL | — | — | Polonia |
| Doxa Russia | https://doxajournal.ru | — | — | RU | — | Student media — Russia |
| DR Nyheder | https://www.dr.dk/nyheder | — | DA | — | — | Danimarca pubblica |
| E24 Norge | https://e24.no | https://e24.no/rss | NO | — | — | Norvegia Business |
| Ekstra Bladet | https://ekstrabladet.dk | — | DA | — | — | Danimarca tabloide |
| Environmental Investigation Agency | https://eia-international.org | — | UK | — | — | Crimini ambientali |
| ERR Uudised | https://www.err.ee | — | ET | — | — | Estonia pubblica |
| Espreso.tv Ukraine | https://espreso.tv | — | — | UA | — | Online — Ucraina |
| Eurasianet | https://eurasianet.org | — | EN | — | — | Asia centrale |
| EVN Report | https://evnreport.com | — | EN | — | — | Armenia — analisi e approfondimento |
| Exit News | https://exit.al/en | https://exit.al/en/feed/ | — | AL | — | English — Albania |
| Expressen | https://www.expressen.se | — | SV | — | — | Svezia tabloide |
| Faktabaari | https://faktabaari.fi | — | — | FI | — | Fact-checking FI — Finlandia |
| Faktacheck (Estonia) | https://faktacheck.err.ee | — | — | EE | — | FC EE — Estonia |
| Faktisk (Norway) | https://www.faktisk.no | — | — | NO | — | FC NO — Norvegia |
| Faktoje Albania | https://faktoje.al | — | — | AL | — | Fact-check — Albania |
| Finance.si | https://www.finance.si | — | SL | — | — | Slovenia — economico |
| Fontanka | https://www.fontanka.ru | — | RU | — | — | San Pietroburgo |
| Gazeta Polska | https://www.gazetapolska.pl | https://www.gazetapolska.pl/feed/ | PL | — | — | Polonia |
| Gazeta Wyborcza | https://wyborcza.pl | — | PL | — | — | Polonia quality |
| Georgian Dream Opposite | https://formula.ge | — | KA | — | — | Georgia TV |
| Göteborgs-Posten | https://www.gp.se | https://www.gp.se/feed | SV | — | — | Svezia |
| Helsingin Sanomat | https://www.hs.fi | — | FI | — | — | Finlandia quality |
| Hetq | https://hetq.am | — | EN | — | — | Armenia investigativo |
| Hospodářské noviny | https://hn.cz | — | CS | — | — | Economia CZ |
| HVG | https://hvg.hu | — | HU | — | — | Ungheria quality |
| Ilta-Sanomat | https://www.is.fi | — | FI | — | — | Finlandia tabloide |
| Iltalehti | https://www.iltalehti.fi | — | FI | — | — | Finlandia — tabloid |
| Index.hr | https://www.index.hr | https://www.index.hr/rss2.xml | HR | — | — | Croazia |
| Index.hu | https://index.hu | — | HU | — | — | Ungheria |
| Information | https://www.information.dk | — | DA | — | — | Danimarca — quotidiano indipendente |
| Interfax Ukraine | https://en.interfax.com.ua | — | EN | — | — | Ucraina agenzia |
| Interpressnews | https://www.interpressnews.ge | — | KA/EN | — | — | Georgia — agenzia di stampa |
| IPN — Info-Prim Neo | https://www.ipn.md | — | RO/RU/EN | — | — | Moldavia — agenzia di stampa |
| IWPR (Central Asia) | https://iwpr.net | — | EN | — | — | Asia centrale |
| JAMnews | https://jam-news.net | — | EN | — | — | Caucaso |
| Jutarnji list | https://www.jutarnji.hr | — | HR | — | — | Croazia |
| Jyllands-Posten | https://jyllands-posten.dk | — | DA | — | — | Danimarca |
| Kaleva | https://www.kaleva.fi | — | FI | — | — | Finlandia — Oulu/Nord |
| Kauppalehti | https://www.kauppalehti.fi | — | FI | — | — | Finlandia — economico |
| Kavkaz-Uzel | https://www.kavkaz-uzel.eu | — | RU | — | — | Caucaso |
| Kavkaz.Realii (RFE/RL) | https://www.kavkazr.com | — | RU | — | — | Caucaso del Nord — RFE/RL |
| KazInform | https://www.inform.kz | — | EN | — | — | Kazakhstan agenzia |
| Keskisuomalainen | https://www.ksml.fi | https://www.ksml.fi/rss/uutiset.rss | FI | — | — | Finlandia |
| Klassekampen | https://klassekampen.no | — | NO | — | — | Norvegia — quotidiano di sinistra |
| Koha Kosovo | https://www.koha.net | — | — | XK | — | Albanian — Kosovo |
| Kun.uz | https://kun.uz/en | — | UZ/EN | — | — | Uzbekistan |
| Kyiv Post | https://www.kyivpost.com | — | EN | — | — | Ucraina in inglese |
| Lidovky.cz | https://www.lidovky.cz | https://www.lidovky.cz/rss | CS | — | — | Rep. Ceca |
| Liga.net Ukraine | https://www.liga.net | — | — | UA | — | Business — Ucraina |
| LRT (Lituania) | https://www.lrt.lt | — | LT | — | — | Lituania pubblica |
| LTV7 Latvija | https://www.lsm.lv | — | LV | — | — | Lettonia pubblica |
| Magyar Hang | https://hang.hu | — | HU | — | — | Ungheria opposizione |
| Mediapool | https://www.mediapool.bg | — | BG | — | — | Bulgaria |
| Mediazona | https://en.zona.media | https://en.zona.media/rss | EN/RU | — | — | Russia carceri |
| Meydan TV | https://www.meydan.tv | — | EN | — | — | Azerbaijan indip. |
| MIA — Media Information Agency | https://mia.mk | — | MK/EN | — | — | Macedonia del Nord — agenzia nazionale |
| Monitor Montenegro | https://www.monitor.co.me | — | — | ME | — | Settimanale inv. — Montenegro |
| Morgunblaðið | https://www.mbl.is | — | IS | — | — | Islanda |
| N1 Info Croatia | https://n1info.hr | https://n1info.hr/feed/ | HR | — | — | Croazia |
| N1 Serbia | https://n1info.rs | — | SR | — | — | Serbia CNN affiliate |
| Nacional (HR) | https://www.nacional.hr | — | HR | — | — | Croazia quality |
| Nasha Niva | https://nashaniva.com | — | — | BE | — | Bielorussia |
| Netgazeti | https://netgazeti.ge | — | KA | — | — | Georgia — testata indipendente |
| NewsMaker | https://newsmaker.md | — | RU/RO | — | — | Moldavia — testata indipendente |
| NGS | https://ngs.ru | — | RU | — | — | Russia — Novosibirsk/Siberia |
| Nova.rs | https://nova.rs | — | SR | — | — | Serbia |
| Novaya Gazeta (Archivio) | https://novayagazeta.ru | — | RU | — | — | cessato IT — Russia (Censurato) |
| Novinky.cz | https://www.novinky.cz | — | CS | — | — | Rep. Ceca |
| NRK Beta | https://nrk.no/beta | https://nrk.no/beta/feed | NO | — | — | Norvegia Tech |
| NRK Nyheter | https://www.nrk.no/nyheter | — | NO | — | — | Norvegia pubblica |
| Nv.ua Ukraine | https://english.nv.ua | — | — | UA | — | Quality — Ucraina |
| Népszava | https://nepszava.hu | — | HU | — | — | Ungheria — quotidiano indipendente |
| OC Media Georgia | https://oc-media.org | — | EN | — | — | Caucaso investigativo |
| OKO.press | https://oko.press | — | PL | — | — | Polonia investigativo |
| Oslobođenje | https://www.oslobodjenje.ba | — | BS | — | — | Bosnia |
| OVD-Info | https://en.ovdinfo.org | — | — | RU | — | Politici prigionieri — Russia |
| Oxford Analytica | https://oxan.com | — | UK | — | — | Analisi globale |
| Pobjeda | https://www.pobjeda.me | — | SR | — | — | Montenegro — quotidiano nazionale |
| Politiken | https://politiken.dk | — | DA | — | — | Danimarca sinistra |
| Polityka | https://www.polityka.pl | — | PL | — | — | Polonia settimanale |
| Poslovni dnevnik | https://www.poslovni.hr | — | HR | — | — | Croazia — economico |
| Postimees | https://www.postimees.ee | — | ET | — | — | Estonia |
| Postoj | https://www.postoj.sk | — | SK | — | — | Slovacchia cattolico |
| Pravda.sk | https://spravy.pravda.sk | — | SK | — | — | Slovacchia |
| Prizma (BIRN) | https://prizma.mk | — | MK | — | — | Macedonia del Nord — investigativo BIRN |
| Puls Biznesu | https://www.pb.pl | — | PL | — | — | Polonia — economico |
| RBC Russia | https://www.rbc.ru | — | — | RU | — | Business — Russia |
| Recorder | https://recorder.ro | — | RO | — | — | Romania — video-giornalismo investigativo |
| Reporter.al | https://reporter.al | — | — | AL | — | Inv. — Albania |
| ReportUSA Albania | https://www.reportusa.com | — | — | AL | — | Albania |
| Republic.ru | https://republic.ru | — | — | RU | — | Premium — Russia |
| RFE/RL Central Asia | https://www.rferl.org/z/1529 | — | EN | — | — | Asia centrale |
| RT International | https://www.rt.com | — | EN | — | — | Russia |
| RUV English | https://www.ruv.is/english | https://www.ruv.is/rss/frettir | EN | — | — | Islanda |
| Rzeczpospolita | https://www.rp.pl | — | PL | — | — | Polonia business |
| RÚV Fréttir | https://www.ruv.is | — | IS | — | — | Islanda pubblica |
| Schemes (Ucraina) | https://www.radiosvoboda.org/z/10765 | — | — | UA | — | RFE/RL inv. — Ucraina |
| Schemes Ukraine | https://www.radiosvoboda.org | — | — | UA | — | già in lista — Ucraina |
| Sibir.Realii (RFE/RL) | https://www.sibreal.org | — | RU | — | — | Siberia — RFE/RL |
| Sloboden Pečat | https://www.slobodenpecat.mk | — | MK | — | — | Macedonia del Nord — quotidiano |
| Sme.sk | https://www.sme.sk | — | SK | — | — | Slovacchia |
| SME.sk Business | https://ekonomika.sme.sk | https://www.sme.sk/rss | SK | — | — | Slovacchia |
| Sputnik International | https://sputnikintermediarios.com | — | EN | — | — | Russia |
| STA Agency (Slovenia) | https://www.sta.si | — | SL | — | — | Slovenia agenzia |
| Stavanger Aftenblad | https://www.aftenbladet.no | — | NO | — | — | Norvegia — Stavanger (oil capital) |
| Svenska Dagbladet | https://www.svd.se | — | SV | — | — | Svezia conservatore |
| SVT Nyheter | https://www.svt.se/nyheter | — | SV | — | — | Svezia pubblica |
| Sydsvenskan | https://www.sydsvenskan.se | https://www.sydsvenskan.se/feed | SV | — | — | Svezia |
| Szabad Európa | https://www.szabadeuropa.hu | — | HU | — | — | Radio Free Europe HU |
| Televizija N1 BIH | https://ba.n1info.com | — | BS | — | — | Bosnia CNN affiliate |
| Telex.hu | https://telex.hu | — | HU | — | — | Ungheria indipendente |
| The Guardian Environment | https://www.theguardian.com/environment | — | UK | — | — | Ambiente Guardian — News |
| The Village Russia | https://www.the-village.ru | — | — | RU | — | lifestyle urb. — Russia |
| Turan Information Agency | https://turan.az | — | AZ/EN/RU | — | — | Azerbaigian — agenzia indipendente |
| Turun Sanomat | https://www.ts.fi | — | FI | — | — | Finlandia — Turku |
| TV Rain (Dozhd) | https://tvrain.ru | https://tvrain.ru/rss/ | RU | — | — | Russia Esilio |
| TVN24 | https://tvn24.pl | — | PL | — | — | Polonia TV |
| Tygodnik Powszechny | https://www.tygodnikpowszechny.pl | — | PL | — | — | Polonia — settimanale cattolico-liberale |
| Ukrainska Pravda | https://www.pravda.com.ua | https://www.pravda.com.ua/rss/ | UK | — | — | Ucraina quality |
| Ukrainska Pravda English | https://www.pravda.com.ua/eng | https://www.pravda.com.ua/rss/ | EN | — | — | Ucraina |
| Ukrinform | https://www.ukrinform.net | — | EN | — | — | Ucraina agenzia |
| Ura.ru | https://ura.news | — | RU | — | — | Russia — Urali, Ekaterinburg |
| Vedomosti | https://www.vedomosti.ru | — | — | RU | — | Business — Russia |
| Večer (Slovenia) | https://www.vecer.com | — | SL | — | — | Slovenia |
| Večernji list | https://www.vecernji.hr | — | HR | — | — | Croazia |
| VG (Norvegia) | https://www.vg.no | — | NO | — | — | Norvegia tabloide |
| Világgazdaság | https://www.vg.hu | — | HU | — | — | Ungheria — economico |
| Vreme | https://www.vreme.com | — | SR | — | — | Serbia quality |
| VTimes (Archivio) | https://vtimes.io | — | RU | — | — | Russia (Chiuso) |
| What's New in Publishing | https://whatsnewinpublishing.com | — | UK | — | — | Publishing digitale |
| Wprost | https://www.wprost.pl | — | PL | — | — | Polonia |
| Yle (Finlandia) | https://yle.fi/uutiset | — | FI | — | — | Finlandia pubblica |
| Zaborona | https://zaborona.com | — | — | UA | — | Crimen/diritti — Ucraina |
| Zeri Kosovo | https://zeri.info | — | — | XK | — | Albanian — Kosovo |
| Ziarul de Gardă | https://www.zdg.md | — | RO/RU | — | — | Moldavia — investigativo principale |
| Ziarul Financiar | https://www.zf.ro | — | RO | — | — | Romania — economico |
| ZN.UA Ukraine | https://zn.ua | — | — | UA | — | Policy — Ucraina |
| Коммерсантъ | https://www.kommersant.ru | — | — | RU | — | Business — Russia |

### 1.6 America Latina & Caraibi (204)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| 14ymedio | https://www.14ymedio.com | — | ES | — | — | già in lista |
| A dónde van los desaparecidos | https://adondevanlosdesaparecidos.org | — | — | MX | — | Desaparecidos — Messico |
| A Tarde | https://atarde.com.br | — | PT | — | — | Brasile — Bahia |
| ABC Color | https://www.abc.com.py | — | ES | — | — | Paraguay |
| Agência Brasil | https://agenciabrasil.ebc.com.br | — | PT | — | — | Brasile pubblica |
| Agência Lupa | https://piaui.folha.uol.com.br/lupa | — | PT | — | — | Fact-checking BR — Brasile |
| AlterPresse | https://www.alterpresse.org | — | FR | — | — | Haiti — rete alternativa d'informazione |
| Amazônia Real | https://amazoniareal.com.br | — | PT | — | — | Brasile — Amazzonia, investigativo |
| Ambito Financiero | https://www.ambito.com | — | ES | — | — | Finanza — Argentina Finanza |
| América Televisión | https://www.americatv.com.pe | — | ES | — | — | Perù — TV principale |
| ANCCOM | https://anccom.sociales.uba.ar | — | — | AR | — | Università UBA — Argentina |
| Antigua Observer | https://antiguaobserver.com | — | EN | — | — | Antigua e Barbuda — quotidiano |
| Antilliaans Dagblad | https://antilliaansdagblad.com | — | NL | — | — | Curaçao/Antille olandesi — quotidiano |
| AyiboPost | https://ayibopost.com | — | FR/HT | — | — | Haiti — testata indipendente |
| Banca Inter-Americana Sviluppo | https://data.iadb.org | — | — | — | — | Sviluppo America Latina e Caraibi — Gratuito — Portale ufficiale |
| Band News | https://www.band.uol.com.br/noticias | — | PT | — | — | Brasile — Brasile TV |
| BioBio Chile | https://www.biobiochile.cl | https://www.biobiochile.cl/rss.xml | ES | — | — | Cile |
| Boa Informação | https://www.boainformacao.com.br | — | PT | — | — | Brasile online |
| Bolivia.com | https://www.bolivia.com | — | ES | — | — | Bolivia |
| Breaking Belize News | https://www.breakingbelizenews.com | — | EN | — | — | Belize — testata digitale |
| Búsqueda (UY) | https://www.busqueda.com.uy | — | ES | — | — | Uruguay investigativo |
| Caribbean Journal | https://caribbeanjournal.com | — | — | Caraibi | — | Business/politic. |
| Caribbean Loop | https://www.loopnewscaribbean.com | — | EN | — | — | Caraibi |
| Caribbean National Weekly | https://www.caribbeannationalweekly.com | — | — | Caraibi | — | Diaspora USA |
| CartaCapital | https://www.cartacapital.com.br | — | PT | — | — | Brasile — settimanale progressista |
| Cayman Compass | https://www.caymancompass.com | — | EN | — | — | Isole Cayman — quotidiano |
| Centro de Periodismo Investigativo | https://periodismoinvestigativo.com | — | ES | — | — | Porto Rico — investigativo |
| Channel 5 Belize | https://www.channel5belize.com | — | EN | — | — | Belize — emittente nazionale |
| CiberCuba | https://www.cibercuba.com | https://www.cibercuba.com/feed | ES | — | — | Diaspora — Cuba Diaspora |
| Cinco Días | https://cincodias.elpais.com | — | ES | — | — | Economia ES |
| Clarimundo | https://clarimundo.com.br | — | PT | — | — | Brasile investigativo |
| Clarín | https://www.clarin.com | — | ES | — | — | Argentina |
| CNN Brasil | https://www.cnnbrasil.com.br | https://www.cnnbrasil.com.br/feed/ | PT | — | — | TV news — Brasile TV |
| Colombiacheck | https://colombiacheck.com | — | — | — | — | Colombia — FC |
| Contagio Radio | https://www.contagioradio.com | — | — | CO | — | Alternativo — Colombia |
| Contracorriente (Honduras) | https://contracorriente.red | — | — | HN | — | Inv. HN — Honduras |
| Contralinea | https://www.contralinea.com.mx | https://www.contralinea.com.mx/feed/ | ES | — | — | Inv. — Messico |
| Convoca.pe | https://convoca.pe | https://convoca.pe/feed/ | ES | — | — | Investigativo — Perù |
| Correio Braziliense | https://www.correiobraziliense.com.br | — | PT | — | — | già in lista |
| Cosecha Roja | https://cosecharoja.org | — | — | AR | — | Violenza/genere — Argentina |
| CR Hoy | https://www.crhoy.com | https://www.crhoy.com/feed/ | ES | — | — | Costa Rica |
| Criterio Honduras | https://criterio.hn | — | — | HN | — | Inv. — Honduras |
| Crusoé | https://crusoe.com.br | — | — | BR | — | Business inv. — Brasile |
| Cuarta Pared Bolivia | https://cuartapared.bo | — | — | BO | — | Inv. — Bolivia |
| Cuatro / Mediaset ES | https://www.cuatro.com | — | ES | — | — | TV privata ES |
| Curaçao Chronicle | https://www.curacaochronicle.com | — | EN | — | — | Curaçao — testata anglofona |
| De Ware Tijd | https://dwtonline.com | — | NL | — | — | Suriname — quotidiano |
| Delfino | https://delfino.cr | — | ES | — | — | Costa Rica — testata digitale |
| Despacho 505 Nicaragua | https://despacho505.com | — | — | NI | — | Inv. — Nicaragua |
| Diario de Cuba | https://diariodecuba.com | — | ES | — | — | Cuba — testata indipendente (Madrid) |
| Diario Financiero | https://www.df.cl | — | ES | — | — | Cile — economico |
| Diario Las Americas | https://www.diariolasamericas.com | https://www.diariolasamericas.com/rss/all.rss | ES | — | — | Diaspora USA — USA Latino |
| Divergentes | https://www.divergentes.com | — | ES | — | — | Centroamerica — investigativo indipendente |
| Diário do Nordeste | https://diariodonordeste.verdesmares.com.br | — | PT | — | — | Brasile — Ceará |
| Dominica News Online | https://dominicanewsonline.com | — | EN | — | — | Dominica — portale news |
| Dromómanos | https://dromomananos.com | — | — | MX | — | Migrazioni — Messico |
| Ecuador Chequea | https://ecuadorchequea.com | — | — | — | — | Ecuador — FC |
| Ecuavisa | https://www.ecuavisa.com | — | ES | — | — | Ecuador — TV principale |
| Efecto Cocuyo | https://efectococuyo.com | — | ES | — | — | Venezuela indip. |
| El Caribe (DR) | https://www.elcaribe.com.do | — | ES | — | — | Rep. Dominicana |
| El Comercio (PE) | https://elcomercio.pe | — | ES | — | — | Perù |
| El Comercio Ecuador | https://www.elcomercio.com | https://www.elcomercio.com/rss/ | ES | — | — | Ecuador |
| El Cronista | https://www.cronista.com | — | ES | — | — | Argentina — economico |
| El Deber | https://eldeber.com.bo | — | ES | — | — | Bolivia |
| El Diario de Juárez | https://diario.mx | — | ES | — | — | Messico — Ciudad Juárez/frontiera |
| El Economista (México) | https://www.eleconomista.com.mx | — | ES | — | — | Messico — economico |
| El Español | https://www.elespanol.com | — | ES | — | — | Online ES |
| El Espectador | https://www.elespectador.com | https://www.elespectador.com/arc/outboundfeeds/rss/ | ES | — | — | Colombia |
| El Financiero | https://www.elfinanciero.com.mx | https://www.elfinanciero.com.mx/rss | ES | — | — | Business — Messico Business |
| El Heraldo Honduras | https://www.elheraldo.hn | — | ES | — | — | Honduras |
| El Informador | https://www.informador.mx | — | ES | — | — | Messico — Guadalajara/Jalisco |
| El Mercurio | https://digital.elmercurio.com | — | ES | — | — | Cile quality |
| El Mostrador | https://www.elmostrador.cl | https://www.elmostrador.cl/feed/ | ES | — | — | Cile online |
| El Mundo Costa Rica | https://www.elmundo.cr | — | — | CR | — | Online |
| El Nacional | https://www.elnacional.com | — | ES | — | — | Venezuela — quotidiano storico |
| El Nuevo Día | https://www.elnuevodia.com | — | ES | — | — | Porto Rico — quotidiano principale |
| El Nuevo Herald | https://www.elnuevoherald.com | — | ES | — | — | Florida USA es |
| El Observador (UY) | https://www.elobservador.com.uy | — | ES | — | — | Uruguay |
| El Pais Argentina | https://www.elpaisargentina.com.ar | — | ES | — | — | Argentina |
| El País (BO) | https://www.elpaisonline.com | — | ES | — | — | Bolivia |
| El País Uruguay | https://www.elpais.com.uy | — | ES | — | — | Uruguay |
| El Pitazo | https://elpitazo.net | — | ES | — | — | Venezuela |
| El Salvador Times | https://www.elsalvadortimes.com | — | — | SV_C | — | English — El Salvador |
| El Salvador.com (EDH) | https://www.elsalvador.com | — | ES | — | — | El Salvador — El Diario de Hoy |
| El Surtidor | https://www.elsurtidor.com.py | — | ES | — | — | Paraguay investigativo |
| El Tiempo Colombia | https://www.eltiempo.com | — | ES | — | — | Colombia |
| El Toque | https://eltoque.com | https://eltoque.com/feed/ | ES | — | — | Cuba digital |
| El Universal (MX) | https://www.eluniversal.com.mx | — | ES | — | — | Messico |
| El Universo | https://www.eluniverso.com | — | ES | — | — | Ecuador |
| elestado.net | https://elestado.net | — | — | CU | — | Cuba |
| Estado de Minas | https://www.em.com.br | — | PT | — | — | Brasile — Minas Gerais |
| Estadão | https://www.estadao.com.br | — | PT | — | — | Brasile |
| Exame | https://exame.com | — | PT | — | — | Brasile — business magazine |
| Excelsior | https://www.excelsior.com.mx | — | ES | — | — | Messico |
| Expansión | https://www.expansion.com | — | ES | — | — | Finanza ES |
| Eyewitness News Bahamas | https://ewnews.com | — | EN | — | — | Bahamas — testata digitale |
| Factum | https://www.revistafactum.com | https://www.revistafactum.com/feed/ | ES | — | — | Inv. — El Salvador |
| Folha de S.Paulo | https://www.folha.uol.com.br | — | PT | — | — | Brasile quality |
| Folha SP investigativo | https://www1.folha.uol.com.br/poder | — | — | BR | — | Politica — Brasile |
| G1 (Globo) | https://g1.globo.com | — | PT | — | — | Brasile TV |
| Gato Encerrado Honduras | https://gatoencerrado.news | — | — | HN | — | Inv. — Honduras |
| Gazeta do Povo | https://www.gazetadopovo.com.br | — | PT | — | — | Brasile — Paraná |
| Gestión | https://gestion.pe | — | ES | — | — | Perù — economico |
| Granma Cuba | https://www.granma.cu | — | ES | — | — | Cuba gov |
| GZH — Zero Hora | https://gauchazh.clicrbs.com.br | — | PT | — | — | Brasile — Rio Grande do Sul |
| Haití Liberté | https://haitiliberte.com | — | FR/EN | — | — | Haiti |
| IDL Reporteros | https://idl-reporteros.pe | — | — | PE | — | Inv. PE — Perù |
| Infobae | https://www.infobae.com | — | ES | — | — | Argentina online |
| InfoMoney | https://www.infomoney.com.br | — | PT | — | — | Brasile — finanza e mercati |
| IstoÉ | https://istoe.com.br | — | PT | — | — | Brasile — settimanale |
| iWitness News | https://www.iwnsvg.com | — | EN | — | — | Saint Vincent e Grenadine — testata |
| Jamaica Gleaner | https://jamaica-gleaner.com | — | EN | — | — | Giamaica |
| Jamaica Observer | https://www.jamaicaobserver.com | — | — | JM | — | Giamaica |
| Jornal do Brasil | https://www.jb.com.br | — | PT | — | — | Brasile |
| Kaieteur News | https://www.kaieteurnewsonline.com | — | EN | — | — | Guyana — quotidiano |
| La Capital | https://www.lacapital.com.ar | — | ES | — | — | Argentina — Rosario |
| La Estrella Panama | https://www.laestrella.com.pa | — | — | PA | — | Quality — Panama |
| La Jornada | https://www.jornada.com.mx | — | ES | — | — | Messico sinistra |
| La Liga Contra el Silencio | https://www.laligacontraelsilencio.com | — | — | CO | — | Network inv. — Colombia |
| La Nación (AR) | https://www.lanacion.com.ar | — | ES | — | — | Argentina |
| La Nación (CR) | https://www.nacion.com | — | ES | — | — | Costa Rica |
| La Nación (PY) | https://www.lanacion.com.py | — | ES | — | — | Paraguay |
| La Opinión (USA) | https://laopinion.com | — | ES | — | — | California es |
| La Politica Online | https://www.lapoliticaonline.com | — | ES | — | — | Politica — Argentina |
| La Prensa (NI) | https://www.laprensa.com.ni | — | ES | — | — | Nicaragua |
| La Prensa (Nicaragua) | https://www.laprensani.com | — | ES | — | — | Nicaragua — quotidiano storico (esilio) |
| La Prensa (PE) | https://laprensa.pe | — | ES | — | — | Perù tabloide |
| La Prensa Grafica | https://www.laprensagrafica.com | — | ES | — | — | già in lista |
| La Prensa Libre Guatemala | https://www.prensalibre.com | — | — | GT | — | già in lista |
| La Prensa Panama | https://www.prensa.com | https://www.prensa.com/nacionales/feed/ | ES | — | — | Panama |
| La República (PE) | https://larepublica.pe | — | ES | — | — | Perù |
| La Tercera | https://www.latercera.com | — | ES | — | — | Cile |
| La Tribuna Honduras | https://www.latribuna.hn | — | — | HN | — | Honduras |
| La Voz del Interior | https://www.lavoz.com.ar | — | ES | — | — | Argentina — Córdoba |
| Le Nouvelliste (Haiti) | https://lenouvelliste.com | — | FR | — | — | Haiti |
| Listín Diario | https://listindiario.com | — | ES | — | — | Rep. Dominicana |
| Los Andes | https://www.losandes.com.ar | — | ES | — | — | Argentina — Mendoza |
| Los Tiempos (BO) | https://www.lostiempos.com | — | ES | — | — | Bolivia |
| Metropoles | https://www.metropoles.com | https://www.metropoles.com/feed | PT | — | — | Online — Brasile |
| MIL21 | https://mil21.es | — | — | AR | — | Inv. — Argentina |
| Montevideo Portal | https://www.montevideo.com.uy | — | ES | — | — | Uruguay |
| N+ (Televisa) | https://www.nmas.com.mx | — | ES | — | — | Messico — news Televisa |
| Nation News | https://www.nationnews.com | — | EN | — | — | Barbados — quotidiano principale |
| News Room Guyana | https://newsroom.gy | — | EN | — | — | Guyana — testata digitale |
| Newsday (T&T) | https://newsday.co.tt | — | EN | — | — | Trinidad & Tobago — quotidiano |
| Newsroom Panama | https://www.newsroompanama.com | — | — | PA | — | English — Panama |
| Nexos | https://nexos.com.mx | https://nexos.com.mx/feed/ | ES | — | — | Culture/policy — Messico Cultura |
| Noticias Caracol | https://www.noticiascaracol.com | — | ES | — | — | Colombia — TV principale |
| Noticias RCN | https://www.noticiasrcn.com | — | ES | — | — | Colombia — RCN |
| NOW Grenada | https://nowgrenada.com | — | EN | — | — | Grenada — testata digitale |
| NSC Total | https://www.nsctotal.com.br | — | PT | — | — | Brasile — Santa Catarina |
| O Antagonista | https://www.oantagonista.com | — | — | BR | — | Direita — Brasile |
| O Globo | https://oglobo.globo.com | — | PT | — | — | Brasile |
| O Povo | https://www.opovo.com.br | — | PT | — | — | Brasile — Ceará, Fortaleza |
| O Tempo | https://www.otempo.com.br | — | PT | — | — | Brasile — Minas Gerais |
| Ok Diario | https://okdiario.com | — | ES | — | — | Online conservatore |
| Pacifista | https://pacifista.tv | https://pacifista.tv/feed/ | ES | — | — | Inv. — Colombia Inv. |
| Perfil | https://www.perfil.com | — | ES | — | — | Argentina |
| Piauí | https://piaui.folha.uol.com.br | — | PT | — | — | Brasile long-form |
| Plan V | https://www.planv.com.ec | https://www.planv.com.ec/feed/ | ES | — | — | Inv. — Ecuador Inv. |
| Poder360 | https://www.poder360.com.br | — | PT | — | — | Brasile politica |
| Portafolio | https://www.portafolio.co | — | ES | — | — | Colombia — economico |
| Prensa Comunitaria | https://prensacomunitaria.org | — | ES | — | — | Guatemala — giornalismo comunitario |
| Proceso | https://www.proceso.com.mx | — | ES | — | — | Messico investigativo |
| Página 12 | https://www.pagina12.com.ar | — | — | AR | — | Sinistra — Argentina |
| Página Siete | https://www.paginasiete.bo | — | ES | — | — | Bolivia |
| Radio Progreso Honduras | https://radioprogresohn.net | — | — | HN | — | Honduras |
| Radio Televisión Martí | https://www.radiotelevisionmarti.com | — | ES | — | — | Cuba RFE/RL |
| RCI | https://rci.fm | — | FR | — | — | Antille francesi — radio news |
| Record News | https://recordnews.r7.com | — | — | — | — | Brasile — TV |
| Reforma | https://gruporeforma.com | — | ES | — | — | Messico quality |
| Reporter Brasil | https://reporterbrasil.org.br | — | PT | — | — | Lavoro e diritti |
| RPP Noticias | https://rpp.pe | — | ES | — | — | Perù |
| Rutas del Conflicto | https://rutasdelconflicto.com | — | — | CO | — | Conflitto — Colombia |
| SBT News | https://www.sbtnews.com.br | — | — | — | — | Brasile — TV |
| Searchlight | https://www.searchlight.vc | — | EN | — | — | Saint Vincent e Grenadine — settimanale |
| Semana | https://www.semana.com | — | — | CO | — | News settimanale — Colombia |
| SIC Notícias | https://sicnoticias.pt | — | PT | — | — | TV PT |
| Sin Embargo | https://www.sinembargo.mx | — | ES | — | — | Messico investigativo |
| Soy502 | https://www.soy502.com | — | ES | — | — | Guatemala — testata digitale |
| St. Kitts & Nevis Observer | https://www.thestkittsnevisobserver.com | — | EN | — | — | Saint Kitts e Nevis — settimanale |
| St. Lucia Times | https://stluciatimes.com | — | EN | — | — | Saint Lucia — testata digitale |
| Starnieuws | https://www.starnieuws.com | — | NL | — | — | Suriname — portale news principale |
| Sudestada Argentina | https://www.sudestada.com.ar | — | — | AR | — | Inv. — Argentina |
| Sumaúma | https://sumauma.com | — | PT | — | — | Brasile Amazzonia |
| Tal Cual | https://talcualdigital.com | — | ES | — | — | Venezuela |
| Teleamazonas | https://www.teleamazonas.com | — | ES | — | — | Ecuador — TV news |
| Telemundo Noticias | https://www.telemundo.com/noticias | — | ES | — | — | USA español TV |
| TerraBrasilis | https://terrabrasilis.dpi.inpe.br | — | — | — | — | Gratuito — Deforestazione Amazzonia |
| TerraBrasilis | https://terrabrasilis.info | — | — | — | Pubblico | Deforestazione Amazzonia — Database |
| The Clinic | https://www.theclinic.cl | — | ES | — | — | Cile satira+news |
| The Daily Herald | https://www.thedailyherald.sx | — | EN | — | — | Sint Maarten/Caraibi olandesi — quotidiano |
| The Nassau Guardian | https://thenassauguardian.com | — | EN | — | — | Bahamas — quotidiano storico |
| The Royal Gazette | https://www.royalgazette.com | — | EN | — | — | Bermuda — quotidiano nazionale |
| The Tribune (Bahamas) | https://www.tribune242.com | — | EN | — | — | Bahamas — quotidiano principale |
| Tiempo Argentino | https://www.tiempoar.com.ar | — | ES | — | — | Argentina sinistra |
| Télam | https://www.telam.com.ar | — | ES | — | — | Argentina agenzia |
| Univision Noticias | https://www.univision.com/noticias | — | ES | — | — | USA español TV |
| UOL Notícias | https://noticias.uol.com.br | — | PT | — | — | Brasile online |
| Valor Economico | https://valor.globo.com | — | PT | — | — | Business — Brasile Business |
| Vanguardia | https://vanguardia.com.mx | — | ES | — | — | Messico — Coahuila |
| Verdad Abierta | https://verdadabierta.com | — | — | CO | — | Conflitto armato — Colombia |
| Wayka | https://wayka.pe | https://wayka.pe/feed/ | ES | — | — | Indip. — Perù Indip. |
| Última Hora (PY) | https://www.ultimahora.com | — | ES | — | — | Paraguay |

### 1.7 Africa (314)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| +972 Arabic (Local Call) | https://www.972mag.com/arabic | — | — | PS/IL | — | Palestina/IL |
| 237online | https://www.237online.com | — | FR | — | — | Camerun |
| 24h au Bénin | https://www.24haubenin.info | — | FR | — | — | Benin — portale news |
| 7iber | https://www.7iber.com | — | AR | — | — | Giordania investigativo — Giordania Inv. |
| 7SUR7.CD | https://7sur7.cd | — | FR | — | — | RD Congo — portale news |
| @Verdade Mozambico | https://www.verdade.co.mz | — | — | MZ | — | Mozambico |
| Abidjan.net | https://www.abidjan.net | — | FR | — | — | Costa d'Avorio |
| Accra Dot Alt | https://accradotalt.com | — | — | GH | — | Online — Ghana |
| Actu Cameroun | https://actucameroun.com | — | FR | — | — | Camerun — portale news |
| Actualite.cd | https://actualite.cd | — | — | CD | — | DRC |
| ActuNiger | https://www.actuniger.com | — | FR | — | — | Niger — portale news |
| Addis Standard | https://addisstandard.com | — | EN | — | — | Etiopia quality |
| Africa Business | https://africabusiness.com | — | EN | — | — | Testata/portale — Pan-Africa · link verificato attivo 06/2026 (https) |
| Africa Confidential | https://www.africa-confidential.com | — | EN | — | — | Pan-Africa intelligence |
| Africa Feeds | https://africafeeds.com | — | — | Pan-Africa | — | Aggregatore |
| Africa Intelligence | https://www.africaintelligence.com | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| Africa Newsroom | https://www.africa-newsroom.com | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| Africa Portal | https://www.africaportal.org | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| Africa Times | https://africatimes.com | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| Africa Top Sports | https://www.africatopsports.com | — | FR | — | — | Sport Africa |
| Africa Uncensored | https://africauncensored.online | — | EN | — | — | Kenya investigativo |
| Africa.com | https://www.africa.com | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| Africaguinee | https://www.africaguinee.com | — | FR | — | — | Guinea — portale news |
| African Business | https://african.business | https://african.business/feed/ | EN | — | — | Pan-Africa Business |
| African Business Magazine | https://africanbusinessmagazine.com | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| African Independent | https://www.africanindependent.com | — | — | ZA | — | Online — Sud Africa |
| African Independent | https://www.africanindy.com | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| African Manager | https://africanmanager.com | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| Africanews | https://www.africanews.com | — | EN/FR | — | — | già in lista |
| Afrik.com | https://www.afrik.com | — | FR | — | — | Pan-Africa online |
| Ahora EG | https://ahoraeg.com | — | ES | — | — | Guinea Equatoriale — testata indipendente |
| AIIJ Uganda | https://aiij.org | — | — | UG | — | Inv. — Uganda |
| Al Arabiya (Arabo) | https://arabic.alarabiya.net | — | AR | — | — | KSA |
| Al Jazeera Africa | https://www.aljazeera.com/africa | https://www.aljazeera.com/xml/rss/all.xml | EN | — | — | Qatar Africa |
| Al Jazeera Arabic | https://www.aljazeera.net | https://www.aljazeera.net/xml/rss/all.xml | AR | — | — | Qatar |
| Al-Ahram (Egypt) | https://english.ahram.org.eg | — | EN | — | — | Egitto gov |
| Al-Jumhuriya (Syria) | https://aljumhuriya.net | — | AR | — | — | Siria indip. |
| Al-Watwan | https://alwatwan.net | — | FR/AR | — | — | Comore — quotidiano nazionale |
| Algeria Watch | https://www.algeria-watch.org | — | FR/DE | — | — | Algeria HR |
| Alqatiba | https://alqatiba.org | — | AR | — | — | Tunisia investigativo |
| Alwihda Info | https://www.alwihdainfo.com | — | FR/AR | — | — | Ciad — testata indipendente |
| Aminata.com (Guinée) | https://www.aminata.com | — | — | GN | — | Guinea Conakry |
| ANCIR (Africa) | https://ancir.org | — | — | Pan-Africa | — | Network |
| APA News | https://apanews.net | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| APS — Agence de Presse Sénégalaise | https://aps.sn | — | FR | — | — | Senegal — agenzia di stampa nazionale |
| Arab Reporters Inv. (ARIJ) | https://en.arij.net | — | EN/AR | — | — | Pan-Arab investigativo |
| Arab48 | https://www.arab48.com | — | AR | — | — | Arabi Israele |
| Arise News | https://www.arise.tv | — | EN | — | — | Nigeria — all-news |
| Asaase Radio | https://asaaseradio.com | — | — | GH | — | Radio — Ghana |
| Awoko | https://awokonewspaper.sl | — | EN | — | — | Sierra Leone — quotidiano indipendente |
| Awoko Sierra Leone | https://awoko.org | — | EN | — | — | Sierra Leone |
| Ayin Network | https://3ayin.com | — | AR/EN | — | — | Sudan — giornalismo indipendente |
| Bahrain Mirror | https://bhmirror.net | — | AR | — | — | Bahrain indip. |
| BBC Arabic | https://www.bbc.com/arabic | — | AR | — | — | UK/MENA |
| BizNews | https://www.biznews.com | — | EN | — | — | Testata nazionale — South Africa · fonte aggregatore, verifica consigliata |
| Burkina24 | https://burkina24.com | — | FR | — | — | Burkina Faso — testata digitale |
| Business & Financial Times | https://thebftonline.com | — | EN | — | — | Testata nazionale — Ghana · fonte aggregatore, verifica consigliata |
| Business Daily Africa | https://www.businessdailyafrica.com | — | EN | — | — | Africa Est business |
| Business Day | https://www.businesslive.co.za | https://www.businesslive.co.za/rss/ | EN | — | — | Sudafrica business |
| Business Today Kenya | https://businesstoday.co.ke | — | EN | — | — | Testata nazionale — Kenya · fonte aggregatore, verifica consigliata |
| BusinessDay | https://www.businessdayonline.com | — | EN | — | — | Testata/portale — Nigeria · fonte aggregatore, verifica consigliata |
| BusinessDay Nigeria | https://businessday.ng | — | EN | — | — | Nigeria — quotidiano economico |
| BusinessTech | https://businesstech.co.za | — | EN | — | — | Testata nazionale — South Africa · fonte aggregatore, verifica consigliata |
| Cameroon Tribune | https://www.cameroon-tribune.cm | — | — | CM | — | Gov — Camerun |
| Canal de Moçambique | https://www.canalmoz.co.mz | — | — | MZ | — | Mozambico |
| Cape Times | https://www.iol.co.za/cape-times | — | — | ZA | — | Città del Capo — Sudafrica |
| Cape Times | https://www.capetimes.co.za | — | EN | — | — | Testata nazionale — South Africa · fonte aggregatore, verifica consigliata |
| Capital FM | https://www.capitalfm.co.ke | https://www.capitalfm.co.ke/news/rss | EN | — | — | Kenya radio |
| Carta de Moçambique | https://cartamz.com | — | PT | — | — | Mozambico — testata indipendente |
| CENOZO | https://cenozo.net | — | FR | — | — | Africa Occ. inv. |
| Citifmonline Ghana | https://citifmonline.com | — | EN | — | — | Ghana radio |
| Citizen Digital Kenya | https://www.citizen.digital | — | — | KE | — | Digitale — Kenya |
| City Press SA | https://www.news24.com/citypress | — | — | ZA | — | Sudafrica |
| Club-K Angola | https://www.club-k.net | — | — | AO | — | Indip. — Angola |
| Code for Africa | https://codeforafrica.org | — | — | Africa | — | Data/FC |
| Corbeau News Centrafrique | https://corbeaunews-centrafrique.org | — | FR | — | — | RCA — testata online |
| Cridem | https://cridem.org | — | FR | — | — | Mauritania — aggregatore/portale news |
| Daily Independent | https://www.independent.ng | — | EN | — | — | Testata/portale — Nigeria · fonte aggregatore, verifica consigliata |
| Daily Maverick Opinionista | https://www.dailymaverick.co.za/opinionista | — | EN | — | — | SA opinion |
| Daily News Egypt | https://www.dailynewsegypt.com | — | EN | — | — | Testata nazionale — Egypt · fonte aggregatore, verifica consigliata |
| Daily News KZN | https://www.iol.co.za/daily-news | — | — | ZA | — | KwaZulu-Natal — Sudafrica |
| Daily News Tanzania | https://www.dailynews.co.tz | — | EN | — | — | Tanzania |
| Daily Sun | https://www.dailysun.co.za | — | EN | — | — | Testata nazionale — South Africa · fonte aggregatore, verifica consigliata |
| Daily Trust | https://dailytrust.com | https://dailytrust.com/feed/ | EN | — | — | Nigeria Nord |
| Dakar Actu | https://www.dakaractu.com | — | FR | — | — | Senegal |
| Defimedia | https://defimedia.info | — | FR | — | — | Mauritius — gruppo Le Défi |
| Diario Rombe | https://diariorombe.es | — | ES | — | — | Guinea Equatoriale — testata in esilio |
| Dispatch Live SA | https://www.dispatchlive.co.za | — | — | ZA | — | Est Capo — Sudafrica |
| Dubawa | https://dubawa.org | — | — | NG/GH | — | Fact-checking Nigeria/Ghana — Africa occ. |
| Ecofin Agency | https://www.agenceecofin.com | — | — | Pan-Africa | — | Economia |
| Economic Confidential | https://economicconfidential.com | — | EN | — | — | Testata/portale — Nigeria · fonte aggregatore, verifica consigliata |
| Egypt Independent | https://www.egyptindependent.com | https://www.egyptindependent.com/feed/ | EN | — | — | Egitto |
| Egypt Today | https://www.egypttoday.com | — | EN | — | — | Testata nazionale — Egypt · fonte aggregatore, verifica consigliata |
| Egyptian Streets | https://egyptianstreets.com | — | EN | — | — | Testata nazionale — Egypt · fonte aggregatore, verifica consigliata |
| El Watan | https://elwatan.com | — | FR | — | — | Algeria |
| Enab Baladi | https://english.enabbaladi.net | https://english.enabbaladi.net/feed/ | EN/AR | — | — | Siria |
| Enquête Plus Sénégal | https://www.enqueteplus.com | — | FR | — | — | Senegal investigativo |
| eSwatini News | https://swazilandnews.com | — | EN | — | — | Eswatini |
| Ethiopian Insider | https://www.ethiopianinsider.com | — | EN | — | — | Etiopia |
| Expresso das Ilhas | https://expressodasilhas.cv | — | PT | — | — | Capo Verde — settimanale principale |
| Eye Radio | https://www.eyeradio.org | — | EN | — | — | Sud Sudan — radio/news Juba |
| Eyewitness News (EWN) | https://ewn.co.za | — | EN | — | — | Testata nazionale — South Africa · fonte aggregatore, verifica consigliata |
| Fasozine | https://fasozine.com | — | FR | — | — | Burkina investigativo |
| Financial Mail | https://www.financialmail.co.za | — | EN | — | — | Testata nazionale — South Africa · fonte aggregatore, verifica consigliata |
| Forbes Africa | https://www.forbesafrica.com | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| Foreign Policy Africa | https://foreignpolicy.com/region/africa | https://foreignpolicy.com/feed/ | EN | — | — | Focus Africa |
| Foroyaa | https://foroyaa.net | — | EN | — | — | Gambia — quotidiano indipendente |
| Fraternité Matin | https://www.fratmat.info | — | FR | — | — | Costa d'Avorio gov |
| FrontPage Africa | https://frontpageafricaonline.com | — | EN | — | — | Liberia |
| Gabon Review | https://www.gabonreview.com | — | — | GA_C | — | Gabon |
| Garowe Online | https://www.garoweonline.com | — | SO/EN | — | — | Somalia/Puntland — testata indipendente |
| GBC Ghana | https://www.gbcghana.com | — | EN | — | — | Testata nazionale — Ghana · fonte aggregatore, verifica consigliata |
| Ghana News Agency | https://ghananewsagency.org | — | EN | — | — | Testata nazionale — Ghana · fonte aggregatore, verifica consigliata |
| Ghanaian Chronicle | https://thechronicle.com.gh | — | EN | — | — | Testata nazionale — Ghana · fonte aggregatore, verifica consigliata |
| Ghanaian Times | https://www.ghanaiantimes.com.gh | — | EN | — | — | Testata nazionale — Ghana · fonte aggregatore, verifica consigliata |
| GhanaWeb | https://www.ghanaweb.com | — | EN | — | — | Ghana |
| Goobjoog News | https://goobjoog.com | — | SO/EN | — | — | Somalia — network news |
| Graphic Online | https://www.graphic.com.gh | https://www.graphic.com.gh/feeds | EN | — | — | Quotidiano — Ghana |
| GroundUp | https://www.groundup.org.za | — | EN | — | — | Sudafrica civico |
| Guineenews | https://guineenews.org | — | FR | — | — | Guinea — portale storico |
| HeraldLIVE SA | https://www.heraldlive.co.za | — | — | ZA | — | Port Elizabeth — Sudafrica |
| Hespress | https://www.hespress.com | — | AR | — | — | Marocco mass |
| Hiiraan Online | https://www.hiiraan.com | — | SO/EN | — | — | Somalia — portale storico |
| HORN Diplomat | https://www.thehorndiplomacy.com | — | EN | — | — | Corno Africa |
| Huffington Post SA | https://www.huffingtonpost.co.za | — | — | ZA | — | Online — Sudafrica |
| HumAngle | https://humanangle.ng | — | EN | — | — | Nigeria sicurezza |
| iAfrikan | https://www.iafrikan.com | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| ICIR Nigeria | https://www.icirnigeria.org | — | EN | — | — | Nigeria investigativo |
| Igihe Rwanda | https://www.igihe.com | — | — | RW | — | Kinyarwanda — Rwanda |
| Independent Uganda | https://www.independent.co.ug | — | — | UG | — | Quality — Uganda |
| Inforpress | https://inforpress.cv | — | PT | — | — | Capo Verde — agenzia di stampa nazionale |
| INK Zambia | https://www.inkzambia.org | — | EN | — | — | Zambia investigativo |
| IOL | https://www.iol.co.za | — | EN | — | — | Testata nazionale — South Africa · fonte aggregatore, verifica consigliata |
| Iran International | https://www.iranintl.com | https://www.iranintl.com/en/rss | EN | — | — | Iran indip. |
| Iraq Oil Report | https://www.iraqoilreport.com | — | EN | — | — | Iraq petrolio |
| ITNewsAfrica | https://www.itnewsafrica.com | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| iWatch Africa | https://iwatchafrica.org | — | EN | — | — | Ghana investigativo |
| Jeune Afrique | https://www.jeuneafrique.com | https://www.jeuneafrique.com/feed | FR | — | — | Pan-Africa francofono — Pan-Africa FR |
| Jeune Afrique Eco | https://www.jeuneafrique.com/economie | — | FR | — | — | Business Africa fr — Business FR |
| Jordan Times | https://www.jordantimes.com | https://www.jordantimes.com/rss | EN | — | — | Giordania |
| Jornal de Angola Online | https://www.jornaldeangola.ao | — | — | AO | — | Gov — Angola |
| Journal du Cameroun | https://www.journalducameroun.com | — | — | CM | — | Online — Camerun |
| Journal du Mali | https://www.journaldumali.com | — | FR | — | — | Mali — testata indipendente |
| Joy Online | https://www.myjoyonline.com | https://www.myjoyonline.com/feed/ | EN | — | — | Ghana |
| Kayhan London | https://kayhan.london | — | FA/EN | — | — | Iran diaspora |
| KBC Channel 1 | https://www.kbc.co.ke | — | — | KE | — | Pubblica — Kenya |
| Kenyan Wall Street | https://kenyanwallstreet.com | — | EN | — | — | Testata nazionale — Kenya · fonte aggregatore, verifica consigliata |
| Kenyans.co.ke | https://www.kenyans.co.ke | — | EN | — | — | Testata nazionale — Kenya · fonte aggregatore, verifica consigliata |
| Khaleej Times | https://www.khaleejtimes.com | — | EN | — | — | Dubai |
| Koaci | https://www.koaci.com | — | FR | — | — | Costa d'Avorio — news Africa occidentale |
| KT Press Rwanda | https://www.ktpress.rw | — | — | RW | — | Indip. — Rwanda |
| Kurdistan 24 | https://www.kurdistan24.net | — | EN/KU | — | — | Kurdistan |
| L'Express de Madagascar | https://lexpress.mg | — | FR/MG | — | — | Madagascar — quotidiano principale |
| L'Observateur Paalga | https://www.lobservateur.bf | — | FR | — | — | Burkina Faso — quotidiano storico |
| L'Opinion Maroc | https://www.lopinion.ma | — | FR | — | — | Marocco |
| L'Orient Today | https://www.lorientlejour.com | https://www.lorientlejour.com/rss/lol.rss | EN/FR | — | — | Libano |
| La Nation (Djibouti) | https://www.lanation.dj | — | FR | — | — | Gibuti — quotidiano nazionale |
| La Nouvelle Tribune | https://lanouvelletribune.info | — | FR | — | — | Benin — quotidiano indipendente |
| La Presse (Tunisia) | https://www.lapresse.tn | — | FR | — | — | Tunisia |
| Le Calame | https://lecalame.info | — | FR | — | — | Mauritania — settimanale indipendente |
| Le Desk Maroc | https://ledesk.ma | — | FR | — | — | Marocco investigativo — Marocco Inv. |
| Le Mauricien | https://www.lemauricien.com | — | FR | — | — | Mauritius |
| Le Monde Afrique | https://www.lemonde.fr/afrique | https://www.lemonde.fr/afrique/rss_full.xml | FR | — | — | Africa Le Monde |
| Le Monde du Togo | https://www.lemondedutogo.info | — | FR | — | — | Togo |
| Le Potentiel | https://lepotentiel.cd | — | FR | — | — | RD Congo — quotidiano Kinshasa |
| Le Soleil | https://www.lesoleil.sn | — | FR | — | — | Senegal — quotidiano nazionale |
| Ledjely | https://ledjely.com | — | FR | — | — | Guinea — testata digitale |
| Lefaso.net | https://lefaso.net | — | FR | — | — | Burkina Faso |
| Legit | https://www.legit.ng | — | EN | — | — | Testata/portale — Nigeria · fonte aggregatore, verifica consigliata |
| Les Dépêches de Brazzaville (ADIAC) | https://www.adiac-congo.com | — | FR | — | — | Congo-Brazzaville — quotidiano principale |
| Lesotho Times | https://lestimes.com | — | EN | — | — | Lesotho — settimanale principale |
| Liberian Observer | https://www.liberianobserver.com | — | EN | — | — | Liberia — quotidiano storico |
| Libya Herald | https://www.libyaherald.com | https://www.libyaherald.com/feed/ | EN | — | — | già in lista |
| Mada Masr | https://www.madamasr.com | https://www.madamasr.com/en/feed/ | EN/AR | — | — | Egitto indip. |
| Madagascar Tribune | https://www.madagascar-tribune.com | — | FR | — | — | Madagascar — testata online |
| Maeen Yemen | https://maeen.com | — | AR | — | — | Yemen |
| Maka Angola | https://www.makaangola.org | https://www.makaangola.org/feed/ | — | AO | — | Inv. — Angola |
| Makanday (Zambia) | https://www.makanday.com | — | EN | — | — | Zambia investigativo |
| Malawi24 | https://malawi24.com | — | EN | — | — | Malawi |
| Maliweb | https://www.maliweb.net | — | — | ML | — | Online — Mali |
| Masrawy | https://www.masrawy.com | — | AR | — | — | Egitto |
| Mediacongo | https://www.mediacongo.net | — | FR | — | — | RD Congo — portale e aggregatore |
| Megaphone | https://megaphone.news | — | AR | — | — | già in lista |
| Mercury SA | https://www.iol.co.za/mercury | — | — | ZA | — | Durban — Sudafrica |
| Midi Madagasikara | https://midi-madagasikara.mg | — | FR/MG | — | — | Madagascar — quotidiano |
| Miniflux | https://miniflux.app | — | — | — | Open Source | RSS minimalista — RSS Reader |
| Mmegi | https://www.mmegi.bw | https://www.mmegi.bw/rss/rss.xml | EN | — | — | Botswana |
| Modern Ghana | https://www.modernghana.com | — | EN | — | — | Testata nazionale — Ghana · fonte aggregatore, verifica consigliata |
| Moneyweb | https://www.moneyweb.co.za | — | EN | — | — | Testata nazionale — South Africa · fonte aggregatore, verifica consigliata |
| MUSEBA Journalism | https://www.musebajournalism.net | — | FR/EN | — | — | Camerun investigativo |
| Mwananchi Tanzania | https://www.mwananchi.co.tz | — | SW | — | — | Tanzania swahili |
| Médias24 | https://medias24.com | — | FR | — | — | Marocco |
| Naija News | https://www.naijanews.com | — | EN | — | — | Testata/portale — Nigeria · fonte aggregatore, verifica consigliata |
| Nairametrics | https://nairametrics.com | — | EN | — | — | Nigeria — finanza e dati |
| Nairobi News | https://nairobinews.nation.africa | — | — | KE | — | Lifestyle — Kenya |
| Nawaat | https://nawaat.org | — | AR/FR | — | — | Tunisia |
| New African | https://newafricanmagazine.com | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| New Dawn Liberia | https://thenewdawnliberia.com | — | EN | — | — | Liberia |
| New Era | https://neweralive.na | — | EN | — | — | Namibia — quotidiano di stato |
| New Narratives | https://newnarratives.org | — | EN | — | — | Liberia investigativo |
| New Vision Uganda | https://www.newvision.co.ug | — | EN | — | — | Uganda gov |
| News Diggers | https://diggers.news | — | EN | — | — | Zambia — quotidiano investigativo |
| News Ghana | https://www.newsghana.com.gh | — | EN | — | — | Testata nazionale — Ghana · fonte aggregatore, verifica consigliata |
| News24 | https://www.news24.com | https://feeds.news24.com/articles/news24/TopStories/rss | EN | — | — | Sudafrica online |
| NewsDay | https://www.newsday.co.zw | https://www.newsday.co.zw/feed/ | EN | — | — | Zimbabwe |
| Nigerian Tribune | https://tribuneonlineng.com | — | EN | — | — | Testata/portale — Nigeria · fonte aggregatore, verifica consigliata |
| Niqash | https://www.niqash.org | — | EN/AR | — | — | Iraq investigativo — Iraq Inv. |
| North Africa Journal | https://north-africa.com | — | EN | — | — | Testata/portale — Pan-Africa · link verificato attivo 06/2026 (https) |
| Novo Jornal | https://novojornal.co.ao | — | PT | — | — | Angola — settimanale indipendente |
| NTV Kenya | https://ntvkenya.co.ke | — | EN/SW | — | — | Kenya — Nation Media TV |
| Nyasa Times | https://www.nyasatimes.com | — | EN | — | — | Malawi |
| O Democrata | https://odemocratagb.com | — | PT | — | — | Guinea-Bissau — testata indipendente |
| O País (Mozambico) | https://opais.co.mz | — | PT | — | — | Mozambico — quotidiano indipendente |
| Observer Uganda | https://www.observer.ug | — | — | UG | — | Indip. — Uganda |
| OpenSecrets ZA | https://www.opensecrets.org.za | — | — | — | Pubblico | Politica sudafricana — Database |
| Orient XXI Africa | https://orientxxi.info | — | FR | — | — | MENA-Africa |
| Oxpeckers | https://oxpeckers.org | https://oxpeckers.org/feed/ | — | — | — | Africa ambiente — Sudafrica — Investigativo |
| Panafrican News Agency (PANA) | https://www.panapress.com | — | EN | — | — | Testata/portale — Pan-Africa · link verificato attivo 06/2026 (https) |
| Petra (Jordan) | https://petra.gov.jo | — | EN/AR | — | — | Giordania agenzia |
| PM News | https://pmnewsnigeria.com | — | EN | — | — | Testata/portale — Nigeria · fonte aggregatore, verifica consigliata |
| Politico SL | https://www.politicosl.com | — | EN | — | — | Sierra Leone — testata indipendente |
| PoliticsWeb | https://www.politicsweb.co.za | — | EN | — | — | Testata nazionale — South Africa · fonte aggregatore, verifica consigliata |
| Pretoria News | https://www.iol.co.za/pretoria-news | — | — | ZA | — | Pretoria — Sudafrica |
| Public Eye (Lesotho) | https://publiceyenews.com | — | EN | — | — | Lesotho — settimanale indipendente |
| Pulse Ghana | https://www.pulse.com.gh | — | EN | — | — | Testata nazionale — Ghana · fonte aggregatore, verifica consigliata |
| Pulse Nigeria | https://www.pulse.ng | — | EN | — | — | Testata/portale — Nigeria · fonte aggregatore, verifica consigliata |
| QNA (Qatar) | https://www.qna.org.qa | — | EN | — | — | Qatar agenzia |
| Radio Dabanga | https://www.dabangasudan.org | https://www.dabangasudan.org/en/feed | EN | — | — | Sudan |
| Radio Ndeke Luka | https://www.radiondekeluka.org | — | — | FR/SG | — | Rep. Centrafricana — Fondation Hirondelle |
| Radio Okapi | https://www.radiookapi.net | — | — | CD | — | ONU — DRC |
| Radio Tamazuj | https://www.radiotamazuj.org | — | EN/AR | — | — | Sud Sudan — testata indipendente |
| Radio Zamaneh | https://www.radiozamaneh.com | https://www.radiozamaneh.com/feed | FA/EN | — | — | Iran |
| Raseef22 | https://raseef22.net | https://raseef22.net/feed/ | AR | — | — | Pan-Arab youth |
| Reporters (Tunisia) | https://www.reporters.tn | — | FR | — | — | Tunisia |
| Republic of Togo | https://www.republicoftogo.com | — | FR | — | — | Togo — portale ufficiale news |
| Reuters Africa | https://af.reuters.com | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| RFI Mali | https://www.rfi.fr/fr/afrique/mali | — | FR | — | — | Mali |
| Rudaw | https://www.rudaw.net/english | https://www.rudaw.net/english/rss | EN | — | — | Kurdistan iracheno |
| Rwanda Focus | https://www.focus.rw | — | — | RW | — | Business — Rwanda |
| Sahara Médias | https://www.saharamedias.net | — | AR/FR | — | — | Mauritania — testata principale |
| Salone Messenger | https://salonemessenger.com | — | EN | — | — | Sierra Leone |
| Saudi Gazette | https://saudigazette.com.sa | — | EN | — | — | Arabia Saudita |
| SenePlus | https://www.seneplus.com | — | FR | — | — | Senegal — opinione e analisi |
| Seneweb | https://www.seneweb.com | — | FR | — | — | Senegal — portale più visitato |
| Seychelles Nation | https://www.nation.sc | — | EN/FR | — | — | Seychelles — quotidiano nazionale |
| Seychelles News Agency | https://www.seychellesnewsagency.com | — | EN | — | — | Seychelles |
| Shabait (Eritrea Profile) | https://shabait.com | — | EN/TI/AR | — | — | Eritrea — media di stato (Min. Informazione) |
| Sidwaya | https://www.sidwaya.info | — | FR | — | — | Burkina Faso — quotidiano di stato |
| Sky News Arabia | https://www.skynewsarabia.com | https://www.skynewsarabia.com/rss | AR | — | — | Abu Dhabi |
| Somali Guardian | https://somaliguardian.com | — | EN | — | — | Somalia — testata anglofona |
| SOS Médias Burundi | https://www.sosmediasburundi.org | — | FR | — | — | Burundi — rete giornalisti indipendenti |
| Sowetan | https://www.sowetanlive.co.za | — | EN | — | — | Sudafrica township |
| Sowt (Lebanon) | https://sowt.com | — | AR | — | — | Libano podcast |
| State Information Service | https://sis.gov.eg | — | EN | — | — | Testata nazionale — Egypt · fonte aggregatore, verifica consigliata |
| Studio Kalangou | https://www.studiokalangou.org | — | FR/HA | — | — | Niger — radio/news (Fondation Hirondelle) |
| Studio Tamani | https://www.studiotamani.org | — | — | ML | — | Radio — Mali |
| Sudan Tribune | https://sudantribune.com | https://sudantribune.com/rss | EN | — | — | Sudan |
| Sudans Post | https://www.sudanspost.com | — | EN | — | — | Sud Sudan — testata online |
| Sunday Standard Botswana | https://www.sundaystandard.info | — | EN | — | — | Botswana |
| Sunday Times SA | https://www.timeslive.co.za/sunday-times | — | — | ZA | — | Settimanale — Sudafrica |
| Syria Direct | https://syriadirect.org | https://syriadirect.org/feed/ | EN | — | — | Siria investigativo — Siria Inv. |
| Tchadinfos | https://tchadinfos.com | — | FR | — | — | Ciad — portale news principale |
| Tel Quel | https://telquel.ma | — | FR | — | — | Marocco quality |
| Tell Magazine | https://tell.ng | — | EN | — | — | Testata/portale — Nigeria · fonte aggregatore, verifica consigliata |
| The Citizen | https://www.thecitizen.co.tz | https://www.thecitizen.co.tz/feed | EN | — | — | Tanzania |
| The Conversation Africa | https://theconversation.com/africa | — | EN | — | — | Africa accademica |
| The Egyptian Gazette | https://egyptian-gazette.com | — | EN | — | — | Testata nazionale — Egypt · fonte aggregatore, verifica consigliata |
| The Fourth Estate Ghana | https://thefourthestategh.com | — | EN | — | — | Ghana investigativo |
| The Guardian Nigeria | https://www.ngrguardiannews.com | — | EN | — | — | Testata/portale — Nigeria · fonte aggregatore, verifica consigliata |
| The Independent Mauritius | https://www.lexpress.mu | — | FR/EN | — | — | Mauritius |
| The Libya Observer | https://www.libyaobserver.ly | https://www.libyaobserver.ly/feed | EN | — | — | già in lista |
| The Monitor | https://www.monitor.co.ug | https://www.monitor.co.ug/rss | EN | — | — | Quality |
| The Namibian | https://www.namibian.com.na | https://www.namibian.com.na/rss/ | EN | — | — | Quality — Namibia |
| The Nation | https://thenationonlineng.net | — | EN | — | — | Testata/portale — Nigeria · fonte aggregatore, verifica consigliata |
| The Nation (Malawi) | https://mwnation.com | — | EN | — | — | Malawi — quotidiano principale |
| The New Times Rwanda | https://www.newtimes.co.rw | — | — | RW | — | Gov-leaning — Rwanda |
| The News Ghana | https://thenewsghana.com.gh | — | EN | — | — | Ghana online |
| The Point | https://thepoint.gm | — | EN | — | — | Gambia — quotidiano principale |
| The Public Source | https://thepublicsource.org | — | EN/AR | — | — | già in lista |
| The Reporter Ethiopia | https://www.thereporterethiopia.com | — | EN/AM | — | — | Etiopia |
| The South African | https://www.thesouthafrican.com | — | EN | — | — | Testata nazionale — South Africa · fonte aggregatore, verifica consigliata |
| The Standard (Gambia) | https://standard.gm | — | EN | — | — | Gambia — quotidiano |
| The Standard Zimbabwe | https://www.standardnewspaper.co.zw | — | — | ZW | — | Settimanale — Zimbabwe |
| The Star | https://www.the-star.co.ke | — | EN | — | — | Testata nazionale — Kenya · fonte aggregatore, verifica consigliata |
| The Star SA | https://www.iol.co.za/the-star | — | — | ZA | — | Johannesburg — Sudafrica |
| The Statesman | https://www.thestatesmanonline.com | — | EN | — | — | Testata nazionale — Ghana · fonte aggregatore, verifica consigliata |
| The Sun | https://www.sunnewsonline.com | — | EN | — | — | Testata/portale — Nigeria · fonte aggregatore, verifica consigliata |
| The Witness | https://thewitnessnigeria.com | — | — | NG | — | Inv. — Nigeria |
| The Zimbabwean | https://www.thezimbabwean.co | https://www.thezimbabwean.co/feed/ | EN | — | — | Zimbabwe indip. |
| TheWill | https://www.thewillnigeria.com | — | EN | — | — | Testata/portale — Nigeria · fonte aggregatore, verifica consigliata |
| This Day Nigeria | https://www.thisdaylive.com | — | EN | — | — | Nigeria business |
| Times of Eswatini | https://www.times.co.sz | — | EN | — | — | Eswatini — quotidiano principale |
| Times of Oman | https://www.timesofoman.com | https://www.timesofoman.com/rss | EN | — | — | Oman |
| TimesLIVE | https://www.timeslive.co.za | — | EN | — | — | Sudafrica |
| Togo First | https://www.togofirst.com | — | FR/EN | — | — | Togo — economia e business |
| TRT Africa | https://www.trtworld.com/africa | https://www.trtworld.com/rss | EN | — | — | Turchia Africa |
| Tuko.co.ke | https://www.tuko.co.ke | — | — | KE | — | Online — Kenya |
| Tunisia Live | https://www.tunisia-live.net | — | EN | — | — | Tunisia |
| TV5 Monde Afrique | https://information.tv5monde.com/afrique | — | FR | — | — | TV Africa francofona |
| Téla Nón | https://www.telanon.info | — | PT | — | — | São Tomé e Príncipe — testata principale |
| Vanguard Nigeria | https://www.vanguardngr.com | — | EN | — | — | Nigeria |
| Ventures Africa | https://venturesafrica.com | — | EN | — | — | Testata/portale — Pan-Africa · fonte aggregatore, verifica consigliata |
| Vrye Weekblad | https://www.vrye.co.za | — | — | ZA | — | Afrikaans inv. — Sudafrica |
| Watani | https://en.wataninet.com | — | EN | — | — | Testata nazionale — Egypt · fonte aggregatore, verifica consigliata |
| Weekend Argus | https://www.iol.co.za/weekend-argus | — | — | ZA | — | Sudafrica |
| WestAfricaLeaks | https://westafricaleaks.org | — | — | — | Pubblico | Leak Africa occidentale — Database |
| Windhoek Observer | https://www.namibianobserver.com | — | — | NA | — | Namibia |
| Youm7 | https://www.youm7.com | — | AR | — | — | Egitto mass |
| Zambia Daily Mail | https://www.daily-mail.co.zm | — | EN | — | — | Zambia |
| ZELA Zimbabwe | https://www.zela.org | — | EN | — | — | Zimbabwe diritti |
| Zimbabwe Herald | https://www.herald.co.zw | — | — | ZW | — | Gov — Zimbabwe |
| Zimbabwe Independent | https://theindependent.co.zw | — | EN | — | — | Zimbabwe |
| ZimEye | https://www.zimeye.net | — | — | ZW | — | Diaspora — Zimbabwe |
| Zitamar News | https://www.zitamar.com | — | EN | — | — | Mozambico — economia e sicurezza |

### 1.8 Medio Oriente & Nord Africa (MENA) (100)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| 180post | https://180post.com | — | — | LB | — | Policy — Libano |
| Al Arabiya (English) | https://english.alarabiya.net | — | EN | — | — | Arabia Saudita |
| Al Jazeera English | https://www.aljazeera.com | — | EN | — | — | Medio Oriente e globale |
| Al-Masdar Online | https://almasdaronline.com | — | AR/EN | — | — | Yemen — testata indipendente |
| Al-Masry Al-Youm | https://www.almasryalyoum.com | — | — | EG | — | Mass media — Egitto |
| Al-Modon | https://www.almodon.com | — | — | Pan-Arab | — | Libano-based |
| Al-Quds | https://www.alquds.com | — | AR | — | — | Palestina — quotidiano storico |
| Al-Quds Al-Arabi | https://www.alquds.co.uk | — | — | — | — | Londra/Pan-Arab |
| AL24 News | https://al24news.dz | — | EN | — | — | Testata — Algeria · fonte aggregatore, verifica consigliata |
| Ammon News | https://en.ammonnews.net | — | — | JO | — | Online — Giordania |
| An-Nahar | https://www.annahar.com | — | AR | — | — | Libano — quotidiano storico |
| Anadolu Agency | https://www.aa.com.tr | — | TR/EN/Multi | — | — | Turchia — agenzia di stato |
| APS — Algérie Presse Service | https://www.aps.dz | — | FR | — | — | Testata — Algeria · fonte aggregatore, verifica consigliata |
| Arab News | https://www.arabnews.com | https://www.arabnews.com/rss.xml | EN | — | — | Arabia Saudita — KSA |
| Arab Times | https://www.arabtimesonline.com | — | EN | — | — | Kuwait — quotidiano anglofono |
| Arabian Business | https://www.arabianbusiness.com | — | — | Golfo | — | Business — Gulf |
| ARY News | https://arynews.tv | — | — | — | — | Pakistan — TV |
| Aujourd'hui le Maroc | https://aujourdhui.ma | — | FR | — | — | Testata — Morocco · testata nazionale nota, verifica consigliata |
| Bahrain Watch | https://bahrainwatch.org | — | — | BH | — | HR inv. — Bahrain |
| Bas News | https://www.basnews.com/en | — | — | — | — | Kurdistan |
| Bianet | https://bianet.org | — | TR/EN | — | — | Turchia — rete giornalismo indipendente |
| BirGün | https://www.birgun.net | — | TR | — | — | Turchia — quotidiano opposizione |
| BNA — Bahrain News Agency | https://www.bna.bh | — | AR/EN | — | — | Bahrein — agenzia di stato |
| Business News | https://www.businessnews.com.tn | — | FR | — | — | Testata — Tunisia · testata nazionale nota, verifica consigliata |
| Calcalist | https://www.calcalist.co.il | — | HE | — | — | Israele — economico principale |
| Cumhuriyet | https://www.cumhuriyet.com.tr | — | TR | — | — | Turchia — quotidiano laico storico |
| Daily Pakistan | https://en.dailypakistan.com.pk | — | — | PK | — | Online — Pakistan |
| Daily Star Lebanon | https://www.dailystar.com.lb | — | EN | — | — | Libano |
| Doha News | https://dohanews.co | — | EN | — | — | Qatar — testata digitale |
| Dünya | https://www.dunya.com | — | TR | — | — | Turchia — economico |
| Echorouk Online | https://www.echoroukonline.com | — | AR | — | — | Testata — Algeria · fonte aggregatore, verifica consigliata |
| El Khabar | https://www.elkhabar.com | — | AR | — | — | Testata — Algeria · testata nazionale nota, verifica consigliata |
| El Moudjahid | https://www.elmoudjahid.dz | — | FR | — | — | Testata — Algeria · testata nazionale nota, verifica consigliata |
| Gazete Duvar | https://www.gazeteduvar.com.tr | — | TR | — | — | Turchia — testata indipendente |
| Globes | https://en.globes.co.il | — | HE/EN | — | — | Israele — quotidiano economico |
| Gulf Business | https://gulfbusiness.com | — | — | Golfo | — | Business — Gulf |
| Gulf Daily News | https://www.gdnonline.com | — | EN | — | — | Bahrein — quotidiano anglofono |
| Gulf News | https://gulfnews.com | https://gulfnews.com/rss | EN | — | — | Dubai |
| Gulf Times | https://www.gulf-times.com | — | EN | — | — | Qatar — quotidiano anglofono |
| Haaretz English | https://www.haaretz.com | https://www.haaretz.com/rss/feed.xml | EN | — | — | Israele |
| HRANA Iran | https://www.en-hrana.org | — | HR | — | — | Iran |
| Hürriyet | https://www.hurriyet.com.tr | — | TR | — | — | Turchia — quotidiano principale |
| i24NEWS | https://www.i24news.tv | — | EN/FR/AR | — | — | Israele — all-news internazionale |
| Iran Focus | https://iranfocus.com | — | — | IR | — | Diaspora inv. — Iran |
| Iran Wire | https://iranwire.com | https://iranwire.com/feed/ | — | IR | — | Indip. — Iran |
| Iraqi News | https://www.iraqinews.com | — | — | IQ | — | English — Iraq |
| Jerusalem Post | https://www.jpost.com | https://www.jpost.com/rss/rssfeedsworld.aspx | EN | — | — | Israele |
| Jordan Fact Check | https://jordanfactcheck.com | — | — | JO | — | Fact-check Medio Oriente — Giordania |
| Jordan News | https://www.jordannews.jo | — | — | JO | — | English — Giordania |
| Kapitalis | https://kapitalis.com | — | FR | — | — | Testata — Tunisia · testata nazionale nota, verifica consigliata |
| KUNA | https://www.kuna.net.kw | — | AR/EN | — | — | Kuwait — agenzia di stato |
| Kurdistan24 | https://www.kurdistan24.net/en | — | — | — | — | Kurdistan |
| Kuwait Times | https://kuwaittimes.com | — | EN | — | — | Kuwait — quotidiano anglofono |
| L'Économiste | https://www.leconomiste.com | — | FR | — | — | Testata — Morocco · testata nazionale nota, verifica consigliata |
| LANA — Libyan News Agency | https://www.lana-news.ly | — | AR | — | — | Testata — Libya · fonte aggregatore, verifica consigliata |
| Le Matin | https://lematin.ma | — | FR | — | — | Testata — Morocco · testata nazionale nota, verifica consigliata |
| Le Quotidien d'Oran | https://www.lequotidien-oran.com | — | FR | — | — | Testata — Algeria · testata nazionale nota, verifica consigliata |
| Le360 | https://le360.ma | — | FR | — | — | Testata — Morocco · testata nazionale nota, verifica consigliata |
| Libya Monitor | https://www.libyamonitor.com | — | EN | — | — | Testata — Libya · fonte aggregatore, verifica consigliata |
| Libya Prospect | https://libyaprospect.com | — | EN | — | — | Testata — Libya · fonte aggregatore, verifica consigliata |
| Libyan Cloud News Agency | https://en.libyan-cna.net | — | EN | — | — | Testata — Libya · fonte aggregatore, verifica consigliata |
| Libyan Express | https://www.libyanexpress.com | — | EN | — | — | Testata — Libya · fonte aggregatore, verifica consigliata |
| MAP — Maghreb Arabe Presse | https://www.mapnews.ma | — | FR | — | — | Testata — Morocco · fonte aggregatore, verifica consigliata |
| Maroc Press | https://www.marocpress.com | — | AR | — | — | Testata — Morocco · fonte aggregatore, verifica consigliata |
| Marsad | https://www.marsad.ly | — | EN | — | — | Testata — Libya · fonte aggregatore, verifica consigliata |
| Medyascope | https://medyascope.tv | — | TR | — | — | Turchia — web TV indipendente |
| MENAFN | https://menafn.com | — | — | MENA | — | Finance news |
| Middle East Eye | https://www.middleeasteye.net | https://www.middleeasteye.net/rss | EN | — | — | Medio Oriente — MENA |
| Middle East Monitor | https://www.middleeastmonitor.com | — | — | GB/MENA | — | UK/MENA |
| Morocco World News | https://www.moroccoworldnews.com | — | — | MA | — | English — Marocco |
| Mosaïque FM | https://www.mosaiquefm.net | — | FR | — | — | Testata — Tunisia · testata nazionale nota, verifica consigliata |
| Muscat Daily | https://www.muscatdaily.com | — | EN | — | — | Oman — quotidiano |
| Naharnet | https://www.naharnet.com | — | EN | — | — | Libano — news in inglese |
| Oman Observer | https://www.omanobserver.om | — | EN | — | — | Oman — quotidiano di stato |
| Press TV | https://www.presstv.ir | — | EN | — | — | Iran |
| Radio Free Europe (Persia) | https://www.radiofarda.com | — | FA | — | — | Iran |
| Samaa TV | https://www.samaa.tv | — | — | — | — | Pakistan — TV |
| SANA | https://sana.sy | — | AR/EN | — | — | Siria — agenzia di stato |
| Shafaq News | https://shafaq.com | — | AR/EN/KU | — | — | Iraq — agenzia news |
| South24 | https://south24.net | — | AR/EN | — | — | Yemen — centro studi/news sud Yemen |
| SPA — Saudi Press Agency | https://www.spa.gov.sa | — | AR/EN | — | — | Arabia Saudita — agenzia di stato |
| Sözcü | https://www.sozcu.com.tr | — | TR | — | — | Turchia — quotidiano opposizione |
| T24 | https://t24.com.tr | — | TR | — | — | Turchia — testata digitale indipendente |
| TAP — Tunis Afrique Presse | https://www.tap.info.tn | — | FR | — | — | Testata — Tunisia · fonte aggregatore, verifica consigliata |
| The Gulf Intelligence | https://gulfintell.com | — | — | Golfo | — | Energy — Gulf |
| The National UAE | https://www.thenationalnews.com | https://www.thenationalnews.com/rss | EN | — | — | UAE |
| The Peninsula | https://thepeninsulaqatar.com | — | EN | — | — | Qatar — quotidiano anglofono |
| The Syria Report | https://syria-report.com | — | EN | — | — | Siria — economia e ricostruzione |
| The Tripoli Post | https://www.tripolipost.com | — | EN | — | — | Testata — Libya · fonte aggregatore, verifica consigliata |
| Times of Israel | https://www.timesofisrael.com | https://www.timesofisrael.com/feed/ | EN | — | — | Israele |
| TRT Haber | https://www.trthaber.com | — | TR | — | — | Turchia — all-news pubblica |
| TSA Algérie | https://www.tsa-algerie.com | https://www.tsa-algerie.com/feed/ | — | DZ | — | Online — Algeria |
| Tunisie Numérique | https://www.tunisienumerique.com | — | FR | — | — | Testata — Tunisia · testata nazionale nota, verifica consigliata |
| WAFA | https://english.wafa.ps | — | AR/EN | — | — | Palestina — agenzia ufficiale |
| WAM — Emirates News Agency | https://wam.ae | — | AR/EN/Multi | — | — | EAU — agenzia di stato |
| Yabiladi Morocco | https://www.yabiladi.com | — | — | MA | — | Diaspora — Marocco |
| Yemen Monitor | https://yemenmonitor.com | — | — | YE | — | English — Yemen |
| Ynetnews | https://www.ynetnews.com | — | EN | — | — | Israele — edizione inglese Yedioth |
| Zan Times | https://zantimes.com | — | — | IR/AF | — | Donne — Iran/Afghanistan |
| Zawya | https://www.zawya.com | — | — | Golfo | — | Business/Finance — Gulf |

### 1.9 Asia & Pacifico (300)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| 38 North (Stimson Center) | https://www.38north.org | — | EN | — | — | Corea del Nord — analisi |
| 7NEWS | https://7news.com.au | — | EN | — | — | Australia — Seven Network |
| 9News | https://www.9news.com.au | — | EN | — | — | Australia — Nine Network |
| Aaj Tak | https://www.aajtak.in | — | HI | — | — | India — all-news hindi più visto |
| ABC News (AU) | https://www.abc.net.au/news | — | EN | — | — | Australia |
| Afghanistan Analysts Network | https://www.afghanistan-analysts.org | — | — | AF | — | Afghanistan |
| AKIpress | https://akipress.com | — | EN/RU | — | — | Kirghizistan — agenzia regionale |
| Alt News | https://www.altnews.in | — | EN | — | — | Fact-checking India |
| Amar Ujala | https://www.amarujala.com | — | HI | — | — | India — hindi, UP/Uttarakhand |
| Anandabazar Patrika | https://www.anandabazar.com | — | BN | — | — | Bengala Occidentale — bengali principale |
| Apple Daily HK (archivio) | https://hk.appledaily.com | — | ZH | — | — | HK (cessato) |
| Asahi Shimbun | https://www.asahi.com/ajw | — | EN/JA | — | — | Giappone quality |
| ASD ACSC Australia | https://www.cyber.gov.au | — | — | — | — | Australia — CERT |
| Asia Sentinel | https://www.asiasentinel.com | — | — | Pan-Asia | — | Inv. |
| Australian Financial Review | https://www.afr.com | — | EN | — | — | Business — Australia Business |
| Bangkok Post | https://www.bangkokpost.com | https://www.bangkokpost.com/rss/data/topstories.xml | EN | — | — | Thailandia |
| BBS — Bhutan Broadcasting Service | https://www.bbs.bt | — | EN/DZ | — | — | Bhutan — emittente nazionale |
| bdnews24 | https://bdnews24.com | — | — | BD | — | English — Bangladesh |
| BenarNews | https://www.benarnews.org | — | — | SE Asia | — | RFE affiliate |
| Berita Harian Malaysia | https://www.bharian.com.my | — | — | MY | — | Malay-lang — Malaysia |
| Bernama Malaysia | https://www.bernama.com | — | — | MY | — | Agenzia gov — Malaysia |
| Bisnis Indonesia | https://www.bisnis.com | — | ID | — | — | Indonesia — economico |
| BOOM Fact Check | https://www.boomlive.in | — | — | IN | — | Fact-checking India |
| Borneo Bulletin | https://borneobulletin.com.bn | — | EN | — | — | Brunei — quotidiano principale |
| Borneo Post | https://www.theborneopost.com | — | — | — | — | Malesia/Borneo |
| Busan Ilbo | https://www.busan.com | — | KO | — | — | Corea — Busan, quotidiano regionale |
| Business Standard | https://www.business-standard.com | — | — | IN | — | Business — India |
| BusinessWorld | https://www.bworldonline.com | — | EN | — | — | Filippine — economico |
| CafeF | https://cafef.vn | — | VI | — | — | Vietnam — finanza e mercati |
| Caixin China | https://www.caixin.com | https://www.caixin.com/rss/ | ZH | — | — | Cina Business |
| Cambodia Daily | https://www.cambodiadaily.com | — | EN | — | — | Cambogia |
| CamboJA News | https://cambojanews.com | — | EN/KH | — | — | Cambogia — rete giornalisti indipendenti |
| Cek Fakta (Indonesia) | https://cekfakta.tempo.co | — | — | — | — | Indonesia — FC |
| CERT-In India | https://www.cert-in.org.in | — | — | — | — | India — CERT |
| CGTN English | https://www.cgtn.com | — | EN | — | — | Cina |
| Channel NewsAsia | https://www.channelnewsasia.com | — | — | SG | — | News — Singapore |
| China Daily | https://www.chinadaily.com.cn | — | EN | — | — | Cina gov |
| China Dialogue | https://chinadialogue.net | — | — | — | — | Cina ambiente — Analisi |
| China File | https://www.chinafile.com | https://www.chinafile.com/feed | EN | — | — | Cina Culture |
| Chosun Ilbo | https://www.chosun.com | — | KO | — | — | Corea conservatore |
| Chronicles of Turkmenistan | https://www.hronikatm.com | — | RU/EN | — | — | Turkmenistan — monitoraggio indipendente |
| Chunichi Shimbun | https://www.chunichi.co.jp | — | JA | — | — | Chubu — Nagoya |
| Colombo Gazette | https://colombogazette.com | — | EN | — | — | Sri Lanka |
| Colombo Telegraph | https://www.colombotelegraph.com | https://www.colombotelegraph.com/index.php/feed/ | EN | — | — | Sri Lanka |
| CommonWealth Magazine | https://english.cw.com.tw | — | EN | — | — | Taiwan quality |
| Crikey | https://www.crikey.com.au | — | EN | — | — | Australia — testata indipendente |
| Daily FT (Sri Lanka) | https://www.ft.lk | — | EN | — | — | Sri Lanka |
| Daily Mirror (Sri Lanka) | https://www.dailymirror.lk | — | EN | — | — | Sri Lanka — quotidiano anglofono |
| Daily News (Thailandia) | https://www.dailynews.co.th | — | TH | — | — | Thailandia — quotidiano |
| Daily NK | https://www.dailynk.com | — | EN/KO | — | — | Corea del Nord — fonti interne |
| Daily Star Bangladesh | https://www.thedailystar.net | — | EN | — | — | Bangladesh |
| Daily Thanthi | https://www.dailythanthi.com | — | TA | — | — | Tamil Nadu — tamil più diffuso |
| Dainik Bhaskar | https://www.bhaskar.com | — | HI | — | — | India — hindi, MP/Rajasthan/Nord |
| Dainik Jagran | https://www.jagran.com | — | HI | — | — | India — quotidiano hindi più diffuso (UP/Nord) |
| Dan Tri | https://dantri.com.vn | — | VI | — | — | Vietnam — portale news |
| Daryo | https://daryo.uz | — | UZ/RU | — | — | Uzbekistan — portale news |
| Dawn Pakistan | https://www.dawn.com | https://www.dawn.com/feeds/home | EN | — | — | già in lista |
| Deccan Chronicle | https://www.deccanchronicle.com | — | EN | — | — | Sud India — Hyderabad/Chennai |
| Deccan Herald | https://www.deccanherald.com | — | — | IN | — | South India |
| DeepSeek | https://www.deepseek.com | — | — | — | Freemium | Cina — LLM |
| Detik.com | https://news.detik.com | — | — | ID | — | Mass media — Indonesia |
| Dhaka Tribune | https://www.dhakatribune.com | https://www.dhakatribune.com/feed | EN | — | — | Bangladesh |
| Diamond Online | https://diamond.jp | — | JA | — | — | Giappone — business |
| Dinamalar | https://www.dinamalar.com | — | TA | — | — | Tamil Nadu — tamil |
| DVB Myanmar | https://english.dvb.no | https://english.dvb.no/feed/ | — | MM | — | Indip. — Myanmar |
| DVB — Democratic Voice of Burma | https://www.dvb.no | — | MY/EN | — | — | Myanmar — media in esilio |
| East Asia Forum | https://eastasiaforum.org | — | — | Pan-Asia | — | Policy |
| EastMojo | https://www.eastmojo.com | — | EN | — | — | Nord-Est India — testata digitale |
| EconomyNext Sri Lanka | https://economynext.com | — | — | LK | — | Economy — Sri Lanka |
| Eenadu | https://www.eenadu.net | — | TE | — | — | Andhra/Telangana — telugu principale |
| Etilaat-e Roz | https://www.etilaatroz.com | — | FA/EN | — | — | Afghanistan — giornalismo investigativo |
| Factor Daily | https://factordaily.com | — | — | IN | — | Tech — India |
| FBC News | https://www.fbcnews.com.fj | — | EN | — | — | Figi — emittente pubblica |
| Fergana News | https://fergana.agency | — | — | Asia Centrale | — |  |
| Fiji Times | https://www.fijitimes.com.fj | — | EN | — | — | Fiji |
| FijiVillage | https://www.fijivillage.com | — | EN | — | — | Figi — news e radio |
| Firstpost | https://www.firstpost.com | https://www.firstpost.com/rss | EN | — | — | News — India News |
| Focusing on Taiwan | https://focustaiwan.tw | — | EN | — | — | Taiwan agenzia |
| Fortify Rights | https://www.fortifyrights.org | — | — | SE Asia | — | Diritti |
| Free Malaysia Today | https://www.freemalaysiatoday.com | — | EN | — | — | Malaysia |
| Free Press Journal | https://www.freepressjournal.in | — | EN | — | — | Mumbai — quotidiano storico |
| Frontline | https://frontline.thehindu.com | — | EN | — | — | India — quindicinale (The Hindu) |
| Gandhara RFE/RL | https://gandhara.rferl.org | — | EN | — | — | Pakistan/Afghanistan |
| Gazeta.uz | https://www.gazeta.uz | — | RU/UZ | — | — | Uzbekistan — portale principale |
| Geo TV | https://www.geo.tv | https://www.geo.tv/rss | EN | — | — | Pakistan TV |
| Global Times | https://www.globaltimes.cn | — | EN | — | — | Cina gov |
| GMA News Online | https://www.gmanetwork.com/news | — | EN/TL | — | — | Filippine — network nazionale |
| Greater Kashmir | https://www.greaterkashmir.com | — | EN | — | — | Kashmir |
| Gujarat Samachar | https://www.gujaratsamachar.com | — | GU | — | — | Gujarat — gujarati principale |
| Hankyoreh | https://www.hani.co.kr | https://www.hani.co.kr/arti/rss.html | KO | — | — | Corea Progressista |
| Hankyung (KED) | https://www.hankyung.com | — | KO/EN | — | — | Corea — economico |
| Hasht-e Subh (8am Media) | https://8am.media | — | FA/EN | — | — | Afghanistan — testata in esilio |
| Hindu Business Line | https://www.thehindubusinessline.com | https://www.thehindubusinessline.com/feed/ | EN | — | — | India Business |
| Hindustan (Live Hindustan) | https://www.livehindustan.com | — | HI | — | — | India — hindi, gruppo HT |
| Hindustan Times | https://www.hindustantimes.com | — | EN | — | — | India |
| HK Free Press | https://hongkongfp.com | — | EN | — | — | HK indipendente |
| Hokkaido Shimbun | https://www.hokkaido-np.co.jp | — | JA | — | — | Hokkaido — Sapporo |
| IDN Times | https://www.idntimes.com | — | — | ID | — | Online — Indonesia |
| Ikon.mn | https://ikon.mn | — | MN | — | — | Mongolia — portale news |
| India Today | https://www.indiatoday.in | — | — | IN | — | News — India |
| Indian Express | https://indianexpress.com | — | EN | — | — | India quality |
| Inquirer (Philippines) | https://newsinfo.inquirer.net | — | EN | — | — | Filippine |
| InvestigateWest | https://investigatewest.org | — | — | — | — | USA Pacific NW — Investigativo |
| Island Times (Palau) | https://islandtimes.org | — | EN | — | — | Palau — testata nazionale |
| Islands Business | https://islandsbusiness.com | — | — | Pacifico | — | Business — Pacific |
| Jakarta Globe | https://jakartaglobe.id | https://jakartaglobe.id/feed/ | EN | — | — | Indonesia |
| Jakarta Post | https://www.thejakartapost.com | — | EN | — | — | Indonesia |
| Japan Times | https://www.japantimes.co.jp | — | EN | — | — | Giappone in inglese |
| Jawa Pos | https://www.jawapos.com | — | ID | — | — | Indonesia — Surabaya, gruppo nazionale |
| Jiemian News | https://www.jiemian.com | — | ZH | — | — | Cina — business news Shanghai |
| Jiji Press | https://www.jiji.com | — | JA | — | — | Giappone agenzia |
| JoongAng Ilbo | https://koreajoongangdaily.joins.com | — | EN/KO | — | — | Corea quality |
| JPCERT Japan | https://www.jpcert.or.jp | — | — | — | — | Giappone — CERT |
| JTBC | https://jtbc.co.kr | — | KO | — | — | Corea — network news |
| Kahoku Shimpo | https://kahoku.news | — | JA | — | — | Tohoku — Sendai |
| Kaktus.media | https://kaktus.media | — | RU | — | — | Kirghizistan — portale news |
| Katadata | https://katadata.co.id | — | ID | — | — | Indonesia — dati ed economia |
| Kathmandu Post | https://kathmandupost.com | https://kathmandupost.com/rss | EN | — | — | Nepal |
| KCNA Watch | https://kcnawatch.org | — | EN | — | — | Aggregatore media di stato nordcoreani |
| Khaama Press | https://www.khaama.com | — | EN | — | — | Afghanistan |
| Khmer Times | https://www.khmertimeskh.com | — | — | KH | — | Cambogia |
| Khovar | https://khovar.tj | — | TG/RU/EN | — | — | Tagikistan — agenzia di stato |
| Kobe Shimbun | https://www.kobe-np.co.jp | — | JA | — | — | Hyogo — Kobe |
| Kompas | https://www.kompas.com | — | — | ID | — | Quotidiano — Indonesia |
| Kompas TV | https://www.kompas.tv | — | ID | — | — | Indonesia — all-news (gruppo Kompas) |
| Kontan | https://www.kontan.co.id | — | ID | — | — | Indonesia — economico |
| Korea Bizwire | https://koreabizwire.com | https://koreabizwire.com/feed | EN | — | — | Corea Business |
| Korea Fact Check | https://www.factcheck.snu.ac.kr | — | — | KR | — | Fact-checking KR — Corea |
| Korea Herald | https://www.koreaherald.com | — | EN | — | — | Corea del Sud |
| Korea Times | https://www.koreatimes.co.kr | — | EN | — | — | Corea Sud |
| KrCERT Korea | https://www.krcert.or.kr | — | — | — | — | Corea — CERT |
| Kuensel | https://kuenselonline.com | — | EN/DZ | — | — | Bhutan — quotidiano nazionale |
| Kumparan | https://kumparan.com | — | ID | — | — | Indonesia — digitale |
| Kyodo News | https://www.kyodonews.net | — | EN | — | — | Giappone agenzia |
| Kyoto Shimbun | https://www.kyoto-np.co.jp | — | JA | — | — | Kyoto |
| Lanka Business Online | https://lankabusinessonline.com | — | — | LK | — | Business — Sri Lanka |
| Lao Dong | https://laodong.vn | — | VI | — | — | Vietnam — quotidiano sindacale |
| Laotian Times | https://laotiantimes.com | — | — | LA | — | Inglese — Laos |
| Les Nouvelles Calédoniennes | https://www.lnc.nc | — | FR | — | — | Nuova Caledonia — quotidiano |
| Livemint | https://www.livemint.com | — | — | IN | — | Business — India |
| Lokmat | https://www.lokmat.com | — | MR | — | — | Maharashtra — marathi principale |
| Loksatta | https://www.loksatta.com | — | MR | — | — | Maharashtra — marathi (Indian Express) |
| Macao News | https://macaonews.org | — | EN | — | — | Macao — testata indipendente |
| Macau Daily Times | https://macaudailytimes.com.mo | — | EN | — | — | Macao — quotidiano anglofono |
| Maeil Business (MK) | https://www.mk.co.kr | — | KO | — | — | Corea — economico principale |
| Mainichi Shimbun | https://mainichi.jp/english | — | EN/JA | — | — | Giappone |
| Malay Mail | https://www.malaymail.com | — | EN | — | — | Malaysia |
| Malayala Manorama | https://www.manoramaonline.com | — | ML | — | — | Kerala — malayalam più diffuso |
| Manila Bulletin | https://mb.com.ph | https://mb.com.ph/feed/ | EN | — | — | Filippine |
| Marianas Variety | https://www.mvariety.com | — | EN | — | — | Isole Marianne — quotidiano regionale |
| Matangi Tonga | https://matangitonga.to | — | EN/TO | — | — | Tonga — testata online |
| Mathrubhumi (Malayalam) | https://www.mathrubhumi.com | — | ML | — | — | Kerala — malayalam |
| Mathrubhumi (English) | https://english.mathrubhumi.com | — | EN | IN | — | Kerala — India |
| Matichon | https://www.matichon.co.th | — | TH | — | — | Thailandia — quotidiano |
| Media Indonesia | https://mediaindonesia.com | — | ID | — | — | Indonesia — quotidiano |
| Medianama | https://www.medianama.com | https://www.medianama.com/feed/ | — | IN | — | Tech policy — India |
| Mekong Eye | https://www.mekongeye.com | — | EN | — | — | Mekong investigativo |
| Metro TV | https://metrotvnews.com | — | ID | — | — | Indonesia — all-news |
| Mid-Day | https://www.mid-day.com | — | EN | — | — | Mumbai — quotidiano cittadino |
| Mihaaru | https://mihaaru.com | — | DV | — | — | Maldive — quotidiano principale |
| MindaNews | https://mindanews.com | — | EN | — | — | Filippine — Mindanao |
| Mizzima Myanmar | https://mizzima.com | — | — | MM | — | Indip. — Myanmar |
| MoneyControl | https://www.moneycontrol.com | — | — | IN | — | Finance — India |
| Mongabay Indonesia | https://www.mongabay.co.id | — | — | ID | — | Ambiente — Indonesia |
| Montsame | https://montsame.mn | — | MN/EN | — | — | Mongolia — agenzia di stampa nazionale |
| Morning | https://www.morning.com.np | — | EN | — | — | Nepal investigativo |
| Mothership | https://mothership.sg | — | EN | — | — | Singapore — testata digitale |
| Myanmar Now | https://myanmar-now.org | — | EN | — | — | Myanmar indipendente |
| Myanmar Times | https://www.mmtimes.com | — | EN | — | — | Myanmar |
| myRepública | https://myrepublica.nagariknetwork.com | — | EN | — | — | Nepal — quotidiano anglofono |
| Nazione Indiana | https://www.nazioneindiana.com | https://www.nazioneindiana.com/feed/ | — | — | — | Letteratura — Cultura |
| NDTV | https://www.ndtv.com | — | EN | — | — | India TV news |
| NDTV Profit | https://www.ndtvprofit.com | — | — | IN | — | Finance — India |
| Nepali Times | https://www.nepalitimes.com | — | EN | — | — | Nepal |
| Netra News | https://netranews.org | — | EN | — | — | Bangladesh investigativo |
| New Nation BD | https://thenewnation.net | — | — | BD | — | English — Bangladesh |
| New Zealand Herald | https://www.nzherald.co.nz | — | EN | — | — | Nuova Zelanda |
| News.mn | https://news.mn | — | MN | — | — | Mongolia — portale news |
| Newslaundry | https://www.newslaundry.com | — | EN | — | — | India media critica |
| Newsroom NZ | https://newsroom.co.nz | — | EN | — | — | Nuova Zelanda — giornalismo di approfondimento |
| NHK News Web Easy | https://www3.nhk.or.jp/news/easy | https://www3.nhk.or.jp/rss/news/cat0.xml | JA | — | — | Giappone Simple |
| NHK World Japan | https://www3.nhk.or.jp/nhkworld | — | EN | — | — | Giappone pubblica |
| Nikkei | https://www.nikkei.com | — | JA | — | — | Giappone economia |
| Nishinippon Shimbun | https://www.nishinippon.co.jp | — | JA | — | — | Kyushu — Fukuoka |
| NK News | https://www.nknews.org | — | EN | — | — | Corea del Nord — testata specialistica (Seoul) |
| OdishaTV | https://odishatv.in | — | OR/EN | — | — | Odisha — network principale |
| OhmyNews | https://www.ohmynews.com | — | KO | — | — | Corea investigativo |
| Okinawa Times | https://www.okinawatimes.co.jp | — | JA | — | — | Okinawa |
| Onlinekhabar | https://www.onlinekhabar.com | — | NE/EN | — | — | Nepal — portale più letto |
| Oorvani (India) | https://oorvani.org | — | EN | — | — | India investigativo |
| Orda.kz | https://orda.kz | — | RU | — | — | Kazakistan — testata indipendente |
| Otago Daily Times | https://www.odt.co.nz | — | EN | — | — | Nuova Zelanda — quotidiano regionale |
| Outlook India | https://www.outlookindia.com | — | — | IN | — | Settimanale — India |
| Pacific Beat ABC | https://www.abc.net.au/pacific | — | — | Pacifico | — | Pacific |
| Pacific Daily News (Guam) | https://www.guampdn.com | — | EN | — | — | Guam — quotidiano |
| Pacnews | http://www.pacnews.org | — | — | Pacifico | — | Pacific |
| Pajhwok Afghan News | https://pajhwok.com | — | EN/FA/PS | — | — | Afghanistan — agenzia indipendente |
| Philippine Star | https://www.philstar.com | — | EN | — | — | Filippine |
| Pikiran Rakyat | https://www.pikiran-rakyat.com | — | ID | — | — | Indonesia — Giava occidentale, Bandung |
| PNG Loop | https://www.pngloop.com | https://www.pngloop.com/feed | EN | — | — | Papua NG |
| PNG Post-Courier | https://www.postcourier.com.pg | — | — | PG | — | Papua NG |
| Prachatai | https://prachatai.com/english | https://prachatai.com/english/node/feed | — | TH | — | Diritti — Thailandia |
| Prajavani | https://www.prajavani.net | — | KN | — | — | Karnataka — kannada |
| Prothom Alo | https://www.prothomalo.com | — | BN | — | — | Bangladesh quality |
| Punjab Kesari | https://www.punjabkesari.in | — | HI/PA | — | — | Punjab — hindi/punjabi |
| Quartz India | https://qz.com/india | — | — | IN | — | Business — India |
| Quint | https://www.thequint.com | — | EN | — | — | India online |
| Radio Free Asia Myanmar | https://www.rfa.org/english/news/myanmar | — | — | MM | — | RFA — Myanmar |
| Radio New Zealand Pacific | https://www.rnz.co.nz/international/pacific-news | — | — | Pacifico | — | RNZ — Pacific |
| Republika Indonesia | https://www.republika.co.id | — | — | ID | — | Muslim — Indonesia |
| RNZ Pacific | https://www.rnz.co.nz/international | https://www.rnz.co.nz/rss | EN | — | — | Pacifico |
| Roar Media LK | https://roar.media/english | — | — | LK | — | Culture — Sri Lanka |
| RTHK News | https://news.rthk.hk | — | EN/ZH | — | — | Hong Kong — emittente pubblica |
| Ryukyu Shimpo | https://ryukyushimpo.jp | — | JA | — | — | Okinawa |
| Sakal | https://www.esakal.com | — | MR | — | — | Maharashtra — marathi, Pune |
| Sakshi | https://www.sakshi.com | — | TE | — | — | Andhra/Telangana — telugu |
| Samoa Observer | https://www.samoaobserver.ws | — | — | WS | — | Samoa |
| Sandesh | https://sandesh.com | — | GU | — | — | Gujarat — gujarati |
| Sankei News | https://www.sankei.com | https://www.sankei.com/rss/news.xml | JA | — | — | Giappone Cons. |
| Shinano Mainichi Shimbun | https://www.shinmai.co.jp | — | JA | — | — | Nagano |
| Shine (Shanghai Daily) | https://www.shine.cn | — | EN | — | — | Shanghai — anglofono |
| Sin Chew Daily | https://www.sinchew.com.my | — | ZH | — | — | Malaysia — sinofono principale |
| Sixth Tone | https://www.sixthtone.com | https://www.sixthtone.com/rss | EN | — | — | Cina Society |
| Solomon Star | https://www.solomonstarnews.com | — | — | SB | — | Solomon |
| Solomon Times | https://www.solomontimes.com | — | EN | — | — | Isole Salomone — testata online |
| South China Morning Post | https://www.scmp.com | — | EN | — | — | Asia-Pacifico |
| Strait Times | https://www.straitstimes.com | — | EN | — | — | Singapore |
| Suara Merdeka | https://www.suaramerdeka.com | — | ID | — | — | Indonesia — Giava centrale, Semarang |
| Sun Online | https://sun.mv | — | DV/EN | — | — | Maldive — portale news |
| Sun Star | https://www.sunstar.com.ph | https://www.sunstar.com.ph/rss | EN | — | — | Filippine |
| SupChina | https://supchina.com | https://supchina.com/feed/ | EN | — | — | Cina Analysis |
| Sydney Morning Herald | https://www.smh.com.au | — | EN | — | — | Australia |
| Tahiti Infos | https://www.tahiti-infos.com | — | FR | — | — | Polinesia Francese — portale news |
| Taipei Times | https://www.taipeitimes.com | — | EN | — | — | Taiwan |
| Taiwan FactCheck Center | https://tfc-taiwan.org.tw | — | — | — | — | Taiwan — FC |
| Taiwan News | https://www.taiwannews.com.tw | https://www.taiwannews.com.tw/en/rss | EN | — | — | Taiwan |
| Taiwan Plus | https://www.taiwanplus.com | https://www.taiwanplus.com/api/news/rss | EN | — | — | Taiwan Public |
| Tatoli | https://tatoli.tl | — | TET/PT/EN | — | — | Timor Est — agenzia di stampa nazionale |
| TBS News | https://newsdig.tbs.co.jp | — | JA | — | — | Giappone TV |
| Telangana Today | https://telanganatoday.com | — | EN | — | — | Telangana — Hyderabad |
| Tengrinews | https://tengrinews.kz | — | RU/KK | — | — | Kazakistan — portale news principale |
| Thai Enquirer | https://www.thaienquirer.com | — | — | TH | — | Indip. — Thailandia |
| Thai PBS World | https://www.thaipbsworld.com | — | EN | — | — | Thailandia |
| Thai Rath | https://www.thairath.co.th | — | TH | — | — | Thailandia — quotidiano più diffuso |
| The Assam Tribune | https://assamtribune.com | — | EN | — | — | Assam — Guwahati |
| The Astana Times | https://astanatimes.com | — | EN | — | — | Kazakistan — anglofono |
| The Australian | https://www.theaustralian.com.au | — | EN | — | — | Australia premium |
| The Bhutanese | https://thebhutanese.bt | — | EN | — | — | Bhutan — settimanale investigativo |
| The Conversation AU | https://theconversation.com/au | https://theconversation.com/au/articles/rss | EN | — | — | Accademia — Australia Accademia |
| The Edge Malaysia | https://theedgemalaysia.com | — | EN | — | — | Malaysia business |
| The Edition | https://edition.mv | — | EN | — | — | Maldive — edizione anglofona di Mihaaru |
| The Express Tribune | https://tribune.com.pk | https://tribune.com.pk/feed/latest | EN | — | — | già in lista |
| The Hindu | https://www.thehindu.com | — | EN | — | — | India quality |
| The Island | https://island.lk | — | EN | — | — | Sri Lanka — quotidiano |
| The Morning Context | https://themorningcontext.com | — | — | IN | — | Business — India |
| The Nation Thailand | https://www.nationthailand.com | — | EN | — | — | Thailandia |
| The National (PNG) | https://www.thenational.com.pg | — | EN | — | — | Papua Nuova Guinea — quotidiano |
| The News International | https://www.thenews.com.pk | — | EN | — | — | già in lista |
| The News Minute | https://www.thenewsminute.com | — | EN | — | — | Sud India — testata digitale |
| The Paper (澎湃) | https://www.thepaper.cn | — | ZH | — | — | Cina |
| The Phnom Penh Post | https://www.phnompenhpost.com | — | — | KH | — | Indip. — Cambogia |
| The Quint WebQoof | https://www.thequint.com/news/webqoof | — | — | — | — | India — FC |
| The Scoop (Brunei) | https://thescoop.co | — | EN | — | — | Brunei — testata digitale |
| The Shillong Times | https://theshillongtimes.com | — | EN | — | — | Meghalaya |
| The Standard (HK) | https://www.thestandard.com.hk | — | EN | — | — | Hong Kong — quotidiano gratuito |
| The Telegraph India | https://www.telegraphindia.com | — | — | IN | — | Kolkata — India |
| The UB Post | https://www.ubpost.mn | — | EN | — | — | Mongolia — quotidiano anglofono |
| The Week (India) | https://www.theweek.in | — | EN | — | — | India — settimanale |
| ThePrint | https://theprint.in | https://theprint.in/feed/ | EN | — | — | Policy — India Policy |
| Tirto | https://tirto.id | — | ID | — | — | Indonesia investigativo |
| Today Online Singapore | https://www.todayonline.com | — | — | SG | — | Singapore |
| Tokyo Shimbun | https://www.tokyo-np.co.jp | — | JA | — | — | Tokyo — quotidiano (Chunichi group) |
| Tolonews | https://tolonews.com | — | EN | — | — | Afghanistan |
| Toyo Keizai | https://toyokeizai.net | — | JA | — | — | Giappone — economico storico |
| Tribune India | https://www.tribuneindia.com | — | — | IN | — | North India |
| Tuoi Tre News | https://tuoitrenews.vn | — | EN | — | — | Vietnam |
| Turkmen.news | https://turkmen.news | — | RU/EN | — | — | Turkmenistan — testata indipendente in esilio |
| Turkmenportal | https://turkmenportal.com | — | RU/TK | — | — | Turkmenistan — portale news |
| TVB | https://www.tvb.com | — | ZH | — | — | Hong Kong — emittente principale |
| TVBS | https://news.tvbs.com.tw | — | ZH | — | — | Taiwan — network news |
| Utusan Malaysia | https://www.utusan.com.my | — | — | MY | — | Gov-leaning — Malaysia |
| UzA — Agenzia nazionale | https://uza.uz | — | UZ/RU/EN | — | — | Uzbekistan — agenzia di stato |
| Vanuatu Daily Post | https://www.dailypost.vu | — | — | VU | — | Vanuatu |
| Vientiane Times | https://www.vientianetimes.org.la | — | — | LA | — | Gov — Laos |
| Vietnam Investment Review | https://vir.com.vn | — | — | VN | — | Business — Vietnam |
| Vietnam News | https://vietnamnews.vn | — | EN | — | — | Vietnam |
| Vietnam Plus | https://en.vietnamplus.vn | https://en.vietnamplus.vn/rss | EN | — | — | Vietnam agenzia |
| VietnamNet | https://vietnamnet.vn/en | — | — | VN | — | Online — Vietnam |
| Vijaya Karnataka | https://vijaykarnataka.com | — | KN | — | — | Karnataka — kannada |
| Vishvas News | https://www.vishvasnews.com | — | — | — | — | India — FC |
| Vlast.kz | https://vlast.kz | — | RU | — | — | Kazakistan — testata indipendente |
| VnEconomy | https://vneconomy.vn | — | VI | — | — | Vietnam — economico |
| VnExpress | https://e.vnexpress.net | https://e.vnexpress.net/rss/news.rss | — | VN | — | Online — Vietnam |
| VOD Cambodia | https://vodenglish.news | — | EN | — | — | Cambogia indip. |
| VTV | https://vtv.vn | — | VI | — | — | Vietnam — TV di stato |
| WION | https://www.wionews.com | — | EN | — | — | India — all-news internazionale |
| Xinhua | https://www.xinhuanet.com/english | — | EN | — | — | Cina agenzia |
| Yicai Global | https://www.yicaiglobal.com | — | EN | — | — | Cina — economia (Shanghai Media Group) |
| Yomiuri Shimbun | https://www.yomiuri.co.jp | — | JA | — | — | Giappone, il più letto |
| Yonhap News | https://en.yna.co.kr | — | EN | — | — | Corea agenzia |

### 1.10 Nord America — Stampa Statale & Locale (67)

| Fonte | URL | RSS Feed | Lingua | Note |
|-------|-----|----------|--------|------|
| AL.com | https://www.al.com | — | EN | — | — | Alabama — gruppo Advance Local |
| Albuquerque Journal | https://www.abqjournal.com | — | EN | — | — | New Mexico — quotidiano principale |
| Argus Leader | https://www.argusleader.com | — | EN | — | — | South Dakota — quotidiano principale |
| Arkansas Democrat-Gazette | https://www.arkansasonline.com | — | EN | — | — | Arkansas — quotidiano statale |
| Baltimore Sun | https://www.baltimoresun.com | — | EN | — | — | Maryland — quotidiano storico |
| Billings Gazette | https://billingsgazette.com | — | EN | — | — | Montana — quotidiano principale |
| Bismarck Tribune | https://bismarcktribune.com | — | EN | — | — | North Dakota — capitale statale |
| Calgary Herald | https://calgaryherald.com | — | EN | — | — | Alberta — Calgary |
| Casper Star-Tribune | https://trib.com | — | EN | — | — | Wyoming — quotidiano statale |
| Charleston Gazette-Mail | https://www.wvgazettemail.com | — | EN | — | — | West Virginia — Pulitzer investigativo |
| Charlotte Observer | https://www.charlotteobserver.com | — | EN | — | — | North Carolina — Charlotte |
| Chicago Sun-Times | https://chicago.suntimes.com | — | EN | — | — | Illinois — secondo quotidiano Chicago |
| Cincinnati Enquirer | https://www.cincinnati.com | — | EN | — | — | Ohio — Cincinnati |
| Cleveland.com / Plain Dealer | https://www.cleveland.com | — | EN | — | — | Ohio — Cleveland |
| Courier-Journal | https://www.courier-journal.com | — | EN | — | — | Kentucky — Louisville |
| CT Mirror | https://ctmirror.org | — | EN | — | — | Connecticut — nonprofit |
| Dallas Morning News | https://www.dallasnews.com | — | EN | — | — | Texas — Dallas |
| Delaware News Journal | https://www.delawareonline.com | — | EN | — | — | Delaware — quotidiano principale |
| Des Moines Register | https://www.desmoinesregister.com | — | EN | — | — | Iowa — quotidiano statale |
| Deseret News | https://www.deseret.com | — | EN | — | — | Utah — quotidiano storico |
| Hartford Courant | https://www.courant.com | — | EN | — | — | Connecticut — più antico quotidiano USA |
| Honolulu Star-Advertiser | https://www.staradvertiser.com | — | EN | — | — | Hawaii — quotidiano principale |
| Idaho Statesman | https://www.idahostatesman.com | — | EN | — | — | Idaho — quotidiano principale |
| IndyStar | https://www.indystar.com | — | EN | — | — | Indiana — Indianapolis |
| Las Vegas Review-Journal | https://www.reviewjournal.com | — | EN | — | — | Nevada — quotidiano principale |
| Milwaukee Journal Sentinel | https://www.jsonline.com | — | EN | — | — | Wisconsin — quotidiano principale |
| MinnPost | https://www.minnpost.com | — | EN | — | — | Minnesota — nonprofit |
| Montana Free Press | https://montanafreepress.org | — | EN | — | — | Montana — nonprofit |
| Montreal Gazette | https://montrealgazette.com | — | EN | — | — | Québec — quotidiano anglofono |
| New Hampshire Union Leader | https://www.unionleader.com | — | EN | — | — | New Hampshire — quotidiano statale |
| Newsday | https://www.newsday.com | — | EN | — | — | New York — Long Island |
| NJ.com / Star-Ledger | https://www.nj.com | — | EN | — | — | New Jersey — Advance Local |
| Omaha World-Herald | https://omaha.com | — | EN | — | — | Nebraska — quotidiano principale |
| OPB — Oregon Public Broadcasting | https://www.opb.org | — | EN | — | — | Oregon — emittente pubblica |
| Orlando Sentinel | https://www.orlandosentinel.com | — | EN | — | — | Florida — Orlando |
| Pittsburgh Post-Gazette | https://www.post-gazette.com | — | EN | — | — | Pennsylvania — Pittsburgh |
| Portland Press Herald | https://www.pressherald.com | — | EN | — | — | Maine — quotidiano principale |
| Providence Journal | https://www.providencejournal.com | — | EN | — | — | Rhode Island — quotidiano statale |
| Richmond Times-Dispatch | https://richmond.com | — | EN | — | — | Virginia — capitale statale |
| Sacramento Bee | https://www.sacbee.com | — | EN | — | — | California — capitale statale |
| SaltWire | https://www.saltwire.com | — | EN | — | — | Atlantico canadese — gruppo regionale |
| San Antonio Express-News | https://www.expressnews.com | — | EN | — | — | Texas — San Antonio |
| San Diego Union-Tribune | https://www.sandiegouniontribune.com | — | EN | — | — | California — San Diego |
| Spotlight PA | https://www.spotlightpa.org | — | EN | — | — | Pennsylvania — nonprofit investigativo |
| St. Louis Post-Dispatch | https://www.stltoday.com | — | EN | — | — | Missouri — St. Louis |
| States Newsroom | https://statesnewsroom.com | — | EN | — | — | Rete nonprofit redazioni statali (50 stati) |
| Tampa Bay Times | https://www.tampabay.com | — | EN | — | — | Florida — Pulitzer, PolitiFact |
| The Baltimore Banner | https://www.thebaltimorebanner.com | — | EN | — | — | Maryland — nonprofit |
| THE CITY | https://www.thecity.nyc | — | EN | — | — | New York — nonprofit NYC |
| The Columbus Dispatch | https://www.dispatch.com | — | EN | — | — | Ohio — capitale statale |
| The Detroit News | https://www.detroitnews.com | — | EN | — | — | Michigan — Detroit |
| The Mercury News | https://www.mercurynews.com | — | EN | — | — | California — Silicon Valley |
| The News & Observer | https://www.newsobserver.com | — | EN | — | — | North Carolina — Raleigh |
| The Oklahoman | https://www.oklahoman.com | — | EN | — | — | Oklahoma — quotidiano principale |
| The Oregonian | https://www.oregonlive.com | — | EN | — | — | Oregon — quotidiano principale |
| The Post and Courier | https://www.postandcourier.com | — | EN | — | — | South Carolina — Charleston, investigativo |
| The State | https://www.thestate.com | — | EN | — | — | South Carolina — Columbia |
| The Tennessean | https://www.tennessean.com | — | EN | — | — | Tennessee — Nashville |
| The Virginian-Pilot | https://www.pilotonline.com | — | EN | — | — | Virginia — Norfolk |
| Times Union | https://www.timesunion.com | — | EN | — | — | New York — Albany, capitale statale |
| Tulsa World | https://tulsaworld.com | — | EN | — | — | Oklahoma — Tulsa |
| Vancouver Sun | https://vancouversun.com | — | EN | — | — | British Columbia — Vancouver |
| VTDigger | https://vtdigger.org | — | EN | — | — | Vermont — nonprofit investigativo |
| Wichita Eagle | https://www.kansas.com | — | EN | — | — | Kansas — quotidiano principale |
| Winnipeg Free Press | https://www.winnipegfreepress.com | — | EN | — | — | Manitoba — quotidiano principale |
| Wisconsin Watch | https://wisconsinwatch.org | — | EN | — | — | Wisconsin — nonprofit |
| WyoFile | https://wyofile.com | — | EN | — | — | Wyoming — nonprofit |

### 1.11 Agenzie di Stampa Nazionali (38)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Agerpres | https://www.agerpres.ro | — | RO/EN | RO | — | Agenzia di stampa rumena |
| AMNA — Athens-Macedonian News Agency | https://www.amna.gr | — | EL/EN | GR | — | Agenzia di stampa greca |
| Andina | https://andina.pe | — | ES | PE | — | Agenzia di stato peruviana |
| ANGOP | https://www.angop.ao | — | PT | AO | — | Agenzia di stato angolana |
| ANI | https://www.aninews.in | — | EN | IN | — | Asian News International |
| ANP | https://www.anp.nl | — | NL | NL | — | Agenzia di stampa olandese |
| APA — Austria Presse Agentur | https://apa.at | — | DE | AT | — | Agenzia di stampa austriaca |
| APP — Associated Press of Pakistan | https://www.app.com.pk | — | EN/UR | PK | — | Agenzia di stato pakistana |
| ATA — Albanian Telegraphic Agency | https://ata.gov.al | — | SQ/EN | AL | — | Agenzia di stampa albanese |
| Belga News Agency | https://www.belga.be | — | FR/NL | BE | — | Agenzia di stampa belga |
| BelTA | https://www.belta.by | — | RU/EN | BY | — | Agenzia di stato bielorussa |
| BSS — Bangladesh Sangbad Sangstha | https://www.bssnews.net | — | BN/EN | BD | — | Agenzia di stato bengalese |
| BTA | https://www.bta.bg | — | BG/EN | BG | — | Agenzia di stampa bulgara |
| CNA Taiwan (Central News Agency) | https://www.cna.com.tw | — | ZH | TW | — | Agenzia di stampa taiwanese |
| CNA — Cyprus News Agency | https://www.cna.org.cy | — | EL/EN | CY | — | Agenzia di stampa cipriota |
| ENA — Ethiopian News Agency | https://www.ena.et | — | AM/EN | ET | — | Agenzia di stato etiope |
| GNA — Ghana News Agency | https://gna.org.gh | — | EN | GH | — | Agenzia di stato ghanese |
| HINA | https://www.hina.hr | — | HR | HR | — | Agenzia di stampa croata |
| Keystone-SDA | https://www.keystone-sda.ch | — | DE/FR/IT | CH | — | Agenzia di stampa svizzera |
| KPL — Lao News Agency | https://kpl.gov.la | — | LO/EN | LA | — | Agenzia di stato laotiana |
| Lusa | https://www.lusa.pt | — | PT | PT | — | Agenzia di stampa portoghese |
| MAP — Maghreb Arabe Presse | https://www.map.ma | — | AR/FR | MA | — | Agenzia di stato marocchina |
| Moldpres | https://www.moldpres.md | — | RO/RU/EN | MD | — | Agenzia di stampa moldava |
| MTI (MTVA) | https://mti.hu | — | HU | HU | — | Agenzia di stampa ungherese |
| NAN — News Agency of Nigeria | https://nan.ng | — | EN | NG | — | Agenzia di stato nigeriana |
| NTB | https://www.ntb.no | — | NO | NO | — | Agenzia di stampa norvegese |
| PA Media | https://pamediagroup.com | — | EN | GB | — | Agenzia di stampa britannica |
| PAP | https://www.pap.pl | — | PL | PL | — | Agenzia di stampa polacca |
| PNA — Philippine News Agency | https://www.pna.gov.ph | — | EN | PH | — | Agenzia di stato filippina |
| PTI — Press Trust of India | https://www.ptinews.com | — | EN | IN | — | Principale agenzia indiana |
| Ritzau | https://ritzau.dk | — | DA | DK | — | Agenzia di stampa danese |
| SAnews | https://www.sanews.gov.za | — | EN | ZA | — | Agenzia governativa sudafricana |
| STT | https://stt.fi | — | FI | FI | — | Agenzia di stampa finlandese |
| Tanjug | https://www.tanjug.rs | — | SR/EN | RS | — | Agenzia di stampa serba |
| TASR | https://www.tasr.sk | — | SK | SK | — | Agenzia di stampa slovacca |
| The Canadian Press | https://www.thecanadianpress.com | — | EN/FR | CA | — | Agenzia di stampa canadese |
| TT Nyhetsbyrån | https://tt.se | — | SV | SE | — | Agenzia di stampa svedese |
| ČTK | https://www.ctk.eu | — | CS/EN | CZ | — | Agenzia di stampa ceca |

### 1.12 Emittenti Pubbliche & Radio (25)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| All India Radio (News on Air) | https://www.newsonair.gov.in | — | EN/HI | IN | — | Radio pubblica indiana |
| BBC World Service | https://www.bbc.co.uk/worldservice | — | EN/Multi | Globale | — | Servizio mondiale BBC — 40+ lingue |
| BNT | https://bnt.bg | — | BG | BG | — | Emittente pubblica bulgara |
| Deutschlandfunk | https://www.deutschlandfunk.de | — | DE | DE | — | Radio pubblica nazionale tedesca |
| EBU — European Broadcasting Union | https://www.ebu.ch | — | EN/FR | EU | — | Unione europea di radiodiffusione — standard e collaborazioni |
| GBC Ghana | https://www.gbcghanaonline.com | — | EN | GH | — | Emittente pubblica ghanese |
| HRT | https://www.hrt.hr | — | HR | HR | — | Emittente pubblica croata |
| KBS World | https://world.kbs.co.kr | — | Multi | KR | — | Servizio estero coreano |
| NTA — Nigerian Television Authority | https://nta.ng | — | EN | NG | — | Emittente pubblica nigeriana |
| ORF | https://orf.at | — | DE | AT | — | Emittente pubblica austriaca |
| Polskie Radio | https://www.polskieradio.pl | — | PL/Multi | PL | — | Radio pubblica polacca |
| PTS Taiwan | https://www.pts.org.tw | — | ZH | TW | — | Emittente pubblica taiwanese |
| Radio Pakistan | https://www.radio.gov.pk | — | UR/EN | PK | — | Radio di stato pakistana |
| Radio Prague International | https://english.radio.cz | — | EN/Multi | CZ | — | Servizio estero radio ceca |
| Radio Romania International | https://www.rri.ro | — | RO/Multi | RO | — | Servizio estero rumeno |
| RAI Internazionale | https://www.rainternational.rai.it | — | IT/Multi | IT | — | Servizio internazionale RAI per italiani nel mondo |
| RNW Media | https://www.rnw.org | — | EN/NL | Globale | — | Radio Paesi Bassi internazionale — media freedom |
| RTS — Radio-televizija Srbije | https://www.rts.rs | — | SR | RS | — | Emittente pubblica serba |
| STVR | https://www.stvr.sk | — | SK | SK | — | Emittente pubblica slovacca |
| Sveriges Radio | https://sverigesradio.se | — | SV | SE | — | Radio pubblica svedese |
| TVP Info | https://www.tvp.info | — | PL | PL | — | Emittente pubblica polacca |
| TVR | https://www.tvr.ro | — | RO | RO | — | Emittente pubblica rumena |
| TVRI | https://tvri.go.id | — | ID | ID | — | Emittente pubblica indonesiana |
| Vatican News | https://www.vaticannews.va | — | Multi | VA | — | Media vaticani |
| Česká televize | https://www.ceskatelevize.cz | — | CS | CZ | — | Emittente pubblica ceca |

## 2. 📊 Statistiche & Dati Macroeconomici

### 2.1 Banche Centrali & Autorità Monetarie (164)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Banca Centrale della Repubblica di San Marino | https://www.bcsm.sm | — | IT | — | — | Banca centrale — San Marino |
| Banco Central de Bolivia | https://www.bcb.gob.bo | — | ES | — | — | Banca centrale — Bolivia |
| Banco Central de Chile | https://www.bcentral.cl | — | ES | — | — | Banca centrale — Chile |
| Banco Central de Costa Rica | https://www.bccr.fi.cr | — | ES | — | — | Banca centrale — Costa Rica |
| Banco Central de Cuba | https://www.bc.gob.cu | — | ES | — | — | Banca centrale — Cuba |
| Banco Central de la República Argentina | https://www.bcra.gob.ar | — | ES | — | — | Banca centrale — Argentina |
| Banco Central de la República Dominicana | https://www.bancentral.gov.do | — | ES | — | — | Banca centrale — Dominican Republic |
| Banco Central de Nicaragua | https://www.bcn.gob.ni | — | ES | — | — | Banca centrale — Nicaragua |
| Banco Central de Reserva de El Salvador | https://www.bcr.gob.sv | — | ES | — | — | Banca centrale — El Salvador |
| Banco Central de Reserva del Perú | https://www.bcrp.gob.pe | — | ES | — | — | Banca centrale — Peru |
| Banco Central de São Tomé e Príncipe | https://bcstp.st | — | PT | — | — | Banca centrale — São Tomé and Príncipe |
| Banco Central de Timor-Leste | https://www.bancocentral.tl | — | PT | — | — | Banca centrale — Timor-Leste |
| Banco Central de Venezuela | https://www.bcv.org.ve | — | ES | — | — | Banca centrale — Venezuela |
| Banco Central del Ecuador | https://www.bce.fin.ec | — | ES | — | — | Banca centrale — Ecuador |
| Banco Central del Paraguay | https://www.bcp.gov.py | — | ES | — | — | Banca centrale — Paraguay |
| Banco Central del Uruguay | https://www.bcu.gub.uy | — | ES | — | — | Banca centrale — Uruguay |
| Banco Central do Brasil | https://www.bcb.gov.br | — | PT | — | — | Banca centrale — Brazil |
| Banco de Cabo Verde | https://www.bcv.cv | — | PT | — | — | Banca centrale — Cape Verde |
| Banco de Guatemala | https://www.banguat.gob.gt | — | ES | — | — | Banca centrale — Guatemala |
| Banco de la República | https://www.banrep.gov.co | — | ES | — | — | Banca centrale — Colombia |
| Banco de Moçambique | https://www.bancomoc.mz | — | PT | — | — | Banca centrale — Mozambique |
| Banco de México | https://www.banxico.org.mx | — | ES | — | — | Banca centrale — Mexico |
| Banco de Portugal | https://www.bportugal.pt | — | PT | — | — | Banca centrale — Portugal |
| Banco Nacional de Angola | https://www.bna.ao | — | PT | — | — | Banca centrale — Angola |
| Bangko Sentral ng Pilipinas | https://www.bsp.gov.ph | — | EN | — | — | Banca centrale — Philippines |
| Bangladesh Bank | https://www.bb.org.bd | — | EN | — | — | Banca centrale — Bangladesh |
| Bank Al-Maghrib | https://www.bkam.ma | — | AR | — | — | Banca centrale — Morocco |
| Bank Negara Malaysia | https://www.bnm.gov.my | — | MS | — | — | Banca centrale — Malaysia |
| Bank of Albania | https://www.bankofalbania.org | — | SQ | — | — | Banca centrale — Albania |
| Bank of Algeria | https://www.bank-of-algeria.dz | — | AR | — | — | Banca centrale — Algeria |
| Bank of Botswana | https://www.bankofbotswana.bw | — | EN | — | — | Banca centrale — Botswana |
| Bank of Canada | https://www.bankofcanada.ca | — | EN | — | — | Banca centrale — Canada |
| Bank of England | https://www.bankofengland.co.uk | — | EN | — | — | Banca centrale — United Kingdom |
| Bank of Eritrea | https://www.boe.gov.er | — | EN | — | — | Banca centrale — Eritrea |
| Bank of Finland | https://www.bof.fi | — | FI | — | — | Banca centrale — Finland |
| Bank of Ghana | https://www.bog.gov.gh | — | EN | — | — | Banca centrale — Ghana |
| Bank of Greece | https://www.bankofgreece.gr | — | EL | — | — | Banca centrale — Greece |
| Bank of Guyana | https://www.bankofguyana.org.gy | — | EN | — | — | Banca centrale — Guyana |
| Bank of Israel | https://www.boi.org.il | — | HE | — | — | Banca centrale — Israel |
| Bank of Jamaica | https://www.boj.org.jm | — | EN | — | — | Banca centrale — Jamaica |
| Bank of Japan | https://www.boj.or.jp | — | JA | — | — | Banca centrale — Japan |
| Bank of Korea | https://www.bok.or.kr | — | KO | — | — | Banca centrale — South Korea |
| Bank of Latvia | https://www.bank.lv | — | LV | — | — | Banca centrale — Latvia |
| Bank of Lithuania | https://www.lb.lt | — | LT | — | — | Banca centrale — Lithuania |
| Bank of Mauritius | https://www.bom.mu | — | EN | — | — | Banca centrale — Mauritius |
| Bank of Mongolia | https://www.mongolbank.mn | — | MN | — | — | Banca centrale — Mongolia |
| Bank of Namibia | https://www.bon.com.na | — | EN | — | — | Banca centrale — Namibia |
| Bank of Papua New Guinea | https://www.bankpng.gov.pg | — | EN | — | — | Banca centrale — Papua New Guinea |
| Bank of Sierra Leone | https://www.bsl.gov.sl | — | EN | — | — | Banca centrale — Sierra Leone |
| Bank of South Sudan | https://boss.gov.ss | — | EN | — | — | Banca centrale — South Sudan |
| Bank of Tanzania | https://www.bot.go.tz | — | EN | — | — | Banca centrale — Tanzania |
| Bank of Thailand | https://www.bot.or.th | — | TH | — | — | Banca centrale — Thailand |
| Bank of the Lao PDR | https://www.bol.gov.la | — | LO | — | — | Banca centrale — Laos |
| Bank of Uganda | https://www.bou.or.ug | — | EN | — | — | Banca centrale — Uganda |
| Bank of Zambia | https://www.boz.zm | — | EN | — | — | Banca centrale — Zambia |
| Banka Slovenije | https://www.bsi.si | — | SL | — | — | Banca centrale — Slovenia |
| Banky Foiben'i Madagasikara | https://www.banky-foibe.mg | — | FR | — | — | Banca centrale — Madagascar |
| Banque Centrale de Djibouti | https://www.banque-centrale.dj | — | FR | — | — | Banca centrale — Djibouti |
| Banque Centrale de la République de Guinée | https://www.bcrg-guinee.org | — | FR | — | — | Banca centrale — Guinea |
| Banque Centrale de Mauritanie | https://www.bcm.mr | — | FR | — | — | Banca centrale — Mauritania |
| Banque Centrale de Tunisie | https://www.bct.gov.tn | — | AR | — | — | Banca centrale — Tunisia |
| Banque Centrale des Comores | https://www.banque-comores.km | — | FR | — | — | Banca centrale — Comoros |
| Banque Centrale des États de l'Afrique de l'Ouest (BCEAO) | https://www.bceao.int | — | FR | — | — | Banca centrale — Senegal |
| Banque Centrale du Congo | https://www.bcc.cd | — | FR | — | — | Banca centrale — DR Congo |
| Banque centrale du Luxembourg | https://www.bcl.lu | — | FR | — | — | Banca centrale — Luxembourg |
| Banque de France | https://www.banque-france.fr | — | FR | — | — | Banca centrale — France |
| Banque de la République du Burundi | https://www.brb.bi | — | FR | — | — | Banca centrale — Burundi |
| Banque des États de l'Afrique Centrale (BEAC) | https://www.beac.int | — | EN | — | — | Banca centrale — Cameroon |
| Banque du Liban | https://www.bdl.gov.lb | — | AR | — | — | Banca centrale — Lebanon |
| Bermuda Monetary Authority | https://www.bma.bm | — | EN | — | — | Banca centrale — Bermuda |
| Brunei Darussalam Central Bank | https://www.bdcb.gov.bn | — | EN | — | — | Banca centrale — Brunei |
| Bulgarian National Bank | https://www.bnb.bg | — | BG | — | — | Banca centrale — Bulgaria |
| Cayman Islands Monetary Authority | https://www.cima.ky | — | EN | — | — | Banca centrale — Cayman Islands |
| Central Bank of Armenia | https://www.cba.am | — | HY | — | — | Banca centrale — Armenia |
| Central Bank of Aruba | https://www.cbaruba.org | — | NL | — | — | Banca centrale — Aruba |
| Central Bank of Azerbaijan | https://www.cbar.az | — | AZ/EN | AZ | — | Banca centrale azera |
| Central Bank of Azerbaijan (EN) | https://en.cbar.az | — | EN | AZ | — | Banca centrale — Azerbaijan — edizione inglese |
| Central Bank of Bahrain | https://www.cbb.gov.bh | — | AR | — | — | Banca centrale — Bahrain |
| Central Bank of Barbados | https://www.centralbank.org.bb | — | EN | — | — | Banca centrale — Barbados |
| Central Bank of Belize | https://www.centralbank.org.bz | — | EN | — | — | Banca centrale — Belize |
| Central Bank of Bosnia and Herzegovina | https://www.cbbh.ba | — | BS | — | — | Banca centrale — Bosnia and Herzegovina |
| Central Bank of Curaçao and Sint Maarten | https://www.centralbank.cw | — | NL | — | — | Banca centrale — Curaçao |
| Central Bank of Cyprus | https://www.centralbank.cy | — | EN | — | — | Banca centrale — Cyprus |
| Central Bank of Egypt | https://www.cbe.org.eg | — | AR | — | — | Banca centrale — Egypt |
| Central Bank of Eswatini | https://www.centralbank.org.sz | — | EN | — | — | Banca centrale — Eswatini |
| Central Bank of Ireland | https://www.centralbank.ie | — | EN | — | — | Banca centrale — Ireland |
| Central Bank of Jordan | https://www.cbj.gov.jo | — | AR | — | — | Banca centrale — Jordan |
| Central Bank of Kenya | https://www.centralbank.go.ke | — | EN | — | — | Banca centrale — Kenya |
| Central Bank of Kosovo | https://www.bqk-kos.org | — | SQ | — | — | Banca centrale — Kosovo |
| Central Bank of Kuwait | https://www.cbk.gov.kw | — | AR | — | — | Banca centrale — Kuwait |
| Central Bank of Lesotho | https://www.centralbank.org.ls | — | EN | — | — | Banca centrale — Lesotho |
| Central Bank of Liberia | https://www.cbl.org.lr | — | EN | — | — | Banca centrale — Liberia |
| Central Bank of Libya | https://www.cbl.gov.ly | — | AR | — | — | Banca centrale — Libya |
| Central Bank of Malta | https://www.centralbankmalta.org | — | EN | — | — | Banca centrale — Malta |
| Central Bank of Montenegro | https://www.cbcg.me | — | SR | — | — | Banca centrale — Montenegro |
| Central Bank of Myanmar | https://www.cbm.gov.mm | — | MY | — | — | Banca centrale — Myanmar |
| Central Bank of Nigeria | https://www.cbn.gov.ng | — | EN | — | — | Banca centrale — Nigeria |
| Central Bank of Oman | https://cbo.gov.om | — | AR | — | — | Banca centrale — Oman |
| Central Bank of Samoa | https://www.cbs.gov.ws | — | EN | — | — | Banca centrale — Samoa |
| Central Bank of Seychelles | https://www.cbs.sc | — | EN | — | — | Banca centrale — Seychelles |
| Central Bank of Solomon Islands | https://www.cbsi.com.sb | — | EN | — | — | Banca centrale — Solomon Islands |
| Central Bank of Somalia | https://www.centralbank.gov.so | — | EN | — | — | Banca centrale — Somalia |
| Central Bank of Sri Lanka | https://www.cbsl.gov.lk | — | EN | — | — | Banca centrale — Sri Lanka |
| Central Bank of Sudan | https://www.cbos.gov.sd | — | AR | — | — | Banca centrale — Sudan |
| Central Bank of Syria | https://www.cb.gov.sy | — | AR | — | — | Banca centrale — Syria |
| Central Bank of the Bahamas | https://www.centralbankbahamas.com | — | EN | — | — | Banca centrale — Bahamas |
| Central Bank of The Gambia | https://www.cbg.gm | — | EN | — | — | Banca centrale — Gambia |
| Central Bank of the Republic of China (Taiwan) | https://www.cbc.gov.tw | — | ZH | — | — | Banca centrale — Taiwan |
| Central Bank of the Republic of Turkey | https://www.tcmb.gov.tr | — | TR | — | — | Banca centrale — Turkey |
| Central Bank of the Russian Federation | https://www.cbr.ru | — | RU | — | — | Banca centrale — Russia |
| Central Bank of the UAE | https://www.centralbank.ae | — | AR | — | — | Banca centrale — United Arab Emirates |
| Central Bank of Trinidad and Tobago | https://www.central-bank.org.tt | — | EN | — | — | Banca centrale — Trinidad and Tobago |
| Central Bank of Turkmenistan | https://www.cbt.tm | — | RU | — | — | Banca centrale — Turkmenistan |
| Central Bank of Uzbekistan | https://www.cbu.uz | — | RU | — | — | Banca centrale — Uzbekistan |
| Central Bank of Yemen | https://www.centralbank.gov.ye | — | AR | — | — | Banca centrale — Yemen |
| Centrale Bank van Suriname | https://www.cbvs.sr | — | NL | — | — | Banca centrale — Suriname |
| Croatian National Bank | https://www.hnb.hr | — | HR | — | — | Banca centrale — Croatia |
| Czech National Bank | https://www.cnb.cz | — | CS | — | — | Banca centrale — Czech Republic |
| Da Afghanistan Bank | https://www.dab.gov.af | — | EN | — | — | Banca centrale — Afghanistan |
| Danmarks Nationalbank | https://www.nationalbanken.dk | — | DA | — | — | Banca centrale — Denmark |
| De Nederlandsche Bank | https://www.dnb.nl | — | NL | — | — | Banca centrale — Netherlands |
| Eastern Caribbean Central Bank (ECCB) | https://www.eccb-centralbank.org | — | EN | — | — | Banca centrale — West Indies |
| Eesti Pank | https://www.eestipank.ee | — | ET | — | — | Banca centrale — Estonia |
| Institut d'Émission d'Outre-Mer (IEOM) | https://www.ieom.fr | — | FR | — | — | Banca centrale — France |
| Maldives Monetary Authority | https://www.mma.gov.mv | — | EN | — | — | Banca centrale — Maldives |
| Monetary Authority of Macao | https://www.amcm.gov.mo | — | ZH | — | — | Banca centrale — Macau |
| Monetary Authority of Singapore | https://www.mas.gov.sg | — | EN | — | — | Banca centrale — Singapore |
| Narodowy Bank Polski | https://www.nbp.pl | — | PL | — | — | Banca centrale — Poland |
| National Bank of Belgium | https://www.nbb.be | — | NL | — | — | Banca centrale — Belgium |
| National Bank of Cambodia | https://www.nbc.gov.kh | — | KH/EN | KH | — | Banca centrale cambogiana |
| National Bank of Cambodia | https://www.nbc.org.kh | — | KM | — | — | Banca centrale — Cambodia |
| National Bank of Ethiopia | https://www.nbe.gov.et | — | EN | — | — | Banca centrale — Ethiopia |
| National Bank of Georgia | https://www.nbg.gov.ge | — | KA | — | — | Banca centrale — Georgia |
| National Bank of Kazakhstan | https://www.nationalbank.kz | — | RU | — | — | Banca centrale — Kazakhstan |
| National Bank of Moldova | https://www.bnm.md | — | RO | — | — | Banca centrale — Moldova |
| National Bank of North Macedonia | https://www.nbrm.mk | — | MK | — | — | Banca centrale — North Macedonia |
| National Bank of Romania | https://www.bnr.ro | — | RO | — | — | Banca centrale — Romania |
| National Bank of Rwanda | https://www.bnr.rw | — | EN | — | — | Banca centrale — Rwanda |
| National Bank of Serbia | https://www.nbs.rs | — | SR | — | — | Banca centrale — Serbia |
| National Bank of Tajikistan | https://www.nbt.tj | — | RU | — | — | Banca centrale — Tajikistan |
| National Bank of the Kyrgyz Republic | https://www.nbkr.kg | — | RU | — | — | Banca centrale — Kyrgyzstan |
| National Bank of the Republic of Belarus | https://www.nbrb.by | — | RU | — | — | Banca centrale — Belarus |
| National Bank of Ukraine | https://www.bank.gov.ua | — | UK | — | — | Banca centrale — Ukraine |
| National Reserve Bank of Tonga | https://www.reservebank.to | — | EN | — | — | Banca centrale — Tonga |
| Nepal Rastra Bank | https://www.nrb.org.np | — | NE | — | — | Banca centrale — Nepal |
| Norges Bank | https://www.norges-bank.no | — | NO | — | — | Banca centrale — Norway |
| Národná banka Slovenska | https://www.nbs.sk | — | SK | — | — | Banca centrale — Slovakia |
| Oesterreichische Nationalbank | https://www.oenb.at | — | DE | — | — | Banca centrale — Austria |
| Palestine Monetary Authority | https://www.pma.ps | — | AR | — | — | Banca centrale — Palestine |
| People's Bank of China | https://www.pbc.gov.cn | — | ZH | — | — | Banca centrale — China |
| Qatar Central Bank | https://www.qcb.gov.qa | — | AR | — | — | Banca centrale — Qatar |
| Reserve Bank of Australia | https://www.rba.gov.au | — | EN | — | — | Banca centrale — Australia |
| Reserve Bank of Fiji | https://www.rbf.gov.fj | — | EN | — | — | Banca centrale — Fiji |
| Reserve Bank of Malawi | https://www.rbm.mw | — | EN | — | — | Banca centrale — Malawi |
| Reserve Bank of New Zealand | https://www.rbnz.govt.nz | — | EN | — | — | Banca centrale — New Zealand |
| Reserve Bank of Vanuatu | https://www.rbv.gov.vu | — | EN | — | — | Banca centrale — Vanuatu |
| Reserve Bank of Zimbabwe | https://www.rbz.co.zw | — | EN | ZW | — | Banca centrale zimbabwese |
| Royal Monetary Authority of Bhutan | https://www.rma.org.bt | — | EN | — | — | Banca centrale — Bhutan |
| Saudi Central Bank (SAMA) | https://www.sama.gov.sa | — | AR | — | — | Banca centrale — Saudi Arabia |
| South African Reserve Bank | https://www.resbank.co.za | — | EN | — | — | Banca centrale — South Africa |
| State Bank of Pakistan | https://www.sbp.org.pk | — | EN | — | — | Banca centrale — Pakistan |
| State Bank of Vietnam | https://www.sbv.gov.vn | — | VI | — | — | Banca centrale — Vietnam |
| Sveriges Riksbank | https://www.riksbank.se | — | SV | — | — | Banca centrale — Sweden |
| Swiss National Bank | https://www.snb.ch | — | DE | — | — | Banca centrale — Switzerland |

### 2.2 Istituti di Statistica Nazionali (187)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Agence nationale de la statistique (ANSD) | https://www.ansd.sn | — | FR | — | — | Istituto nazionale di statistica — Senegal |
| Agency for Statistics of BiH (BHAS) | https://www.bhas.ba | — | BS | — | — | Istituto nazionale di statistica — Bosnia and Herzegovina |
| Agency on Statistics | https://www.stat.tj | — | RU | — | — | Istituto nazionale di statistica — Tajikistan |
| Algemeen Bureau voor de Statistiek | https://www.statistics-suriname.org | — | NL | — | — | Istituto nazionale di statistica — Suriname |
| Australian Bureau of Statistics (ABS) | https://www.abs.gov.au | — | EN | — | — | Istituto nazionale di statistica — Australia |
| Badan Pusat Statistik | https://www.bps.go.id | — | ID | — | — | Istituto nazionale di statistica — Indonesia |
| Bahamas National Statistics Institute | https://stats.gov.bs | — | EN | — | — | Istituto nazionale di statistica — Bahamas |
| Bangladesh Bureau of Statistics | https://www.bbs.gov.bd | — | EN | — | — | Istituto nazionale di statistica — Bangladesh |
| Barbados Statistical Service | https://stats.gov.bb | — | EN | — | — | Istituto nazionale di statistica — Barbados |
| Bureau of Economic Analysis (BEA) | https://www.bea.gov | — | EN | — | — | Istituto nazionale di statistica — United States |
| Bureau of Labor Statistics (BLS) | https://www.bls.gov | — | EN | — | — | Istituto nazionale di statistica — United States |
| Bureau of National Statistics | https://stat.gov.kz | — | RU | — | — | Istituto nazionale di statistica — Kazakhstan |
| Bureau of Statistics | https://www.bos.gov.ls | — | EN | — | — | Istituto nazionale di statistica — Lesotho |
| Bureau of Statistics and Census | https://bsc.ly | — | AR | — | — | Istituto nazionale di statistica — Libya |
| CAPMAS | https://www.capmas.gov.eg | — | AR | — | — | Istituto nazionale di statistica — Egypt |
| Census and Statistics Department | https://www.censtatd.gov.hk | — | ZH | — | — | Istituto nazionale di statistica — Hong Kong |
| Central Administration of Statistics | https://www.cas.gov.lb | — | AR | — | — | Istituto nazionale di statistica — Lebanon |
| Central Bureau of Statistics | https://www.cbs.gov.sd | — | AR | — | — | Istituto nazionale di statistica — Sudan |
| Central Bureau of Statistics | https://www.cbs.aw | — | NL | — | — | Istituto nazionale di statistica — Aruba |
| Central Bureau of Statistics | https://www.cbs.cw | — | NL | — | — | Istituto nazionale di statistica — Curaçao |
| Central Bureau of Statistics | https://www.cbssyr.sy | — | AR | — | — | Istituto nazionale di statistica — Syria |
| Central Organization of Statistics (COSIT) | https://cosit.gov.iq | — | AR | — | — | Istituto nazionale di statistica — Iraq |
| Central Statistical Bureau of Latvia | https://www.stat.gov.lv | — | LV | — | — | Istituto nazionale di statistica — Latvia |
| Central Statistical Office | https://stats.gov.gd | — | EN | — | — | Istituto nazionale di statistica — Grenada |
| Central Statistical Office | https://stats.gov.lc | — | EN | — | — | Istituto nazionale di statistica — Saint Lucia |
| Central Statistical Office | https://cso.gov.tt | — | EN | — | — | Istituto nazionale di statistica — Trinidad and Tobago |
| Central Statistical Organization | https://www.cso-yemen.org | — | AR | — | — | Istituto nazionale di statistica — Yemen |
| Central Statistics Office | https://stats.gov.dm | — | EN | — | — | Istituto nazionale di statistica — Dominica |
| Central Statistics Office (CSO) | https://www.cso.ie | — | EN | — | — | Istituto nazionale di statistica — Ireland |
| Croatian Bureau of Statistics (DZS) | https://www.dzs.hr | — | HR | — | — | Istituto nazionale di statistica — Croatia |
| Czech Statistical Office (ČSÚ) | https://www.csu.gov.cz | — | CS | — | — | Istituto nazionale di statistica — Czech Republic |
| DANE | https://www.dane.gov.co | — | ES | — | — | Istituto nazionale di statistica — Colombia |
| Department of Economic Planning and Statistics | https://www.deps.gov.bn | — | EN | — | — | Istituto nazionale di statistica — Brunei |
| Department of Statistics | https://www.estadistica.ad | — | ES | — | — | Istituto nazionale di statistica — Andorra |
| Department of Statistics | https://www.dos.gov.jo | — | AR | — | — | Istituto nazionale di statistica — Jordan |
| Department of Statistics Malaysia | https://www.dosm.gov.my | — | MS | — | — | Istituto nazionale di statistica — Malaysia |
| Department of Statistics Singapore | https://www.singstat.gov.sg | — | EN | — | — | Istituto nazionale di statistica — Singapore |
| DGBAS | https://www.stat.gov.tw | — | ZH | — | — | Istituto nazionale di statistica — Taiwan |
| Direction générale de la statistique | https://www.stat-gabon.org | — | FR | — | — | Istituto nazionale di statistica — Gabon |
| Energy Information Administration (EIA) | https://www.eia.gov | — | EN | — | — | Istituto nazionale di statistica — United States |
| Ethiopian Statistics Service | https://www.statsethiopia.gov.et | — | EN | — | — | Istituto nazionale di statistica — Ethiopia |
| Federal Competitiveness and Statistics Centre | https://fcsc.gov.ae | — | AR | — | — | Istituto nazionale di statistica — United Arab Emirates |
| Federal State Statistics Service (Rosstat) | https://www.gks.ru | — | RU | — | — | Istituto nazionale di statistica — Russia |
| Federal Statistical Office (Destatis) | https://www.destatis.de | — | DE | — | — | Istituto nazionale di statistica — Germany |
| Federal Statistical Office (FSO) | https://www.bfs.admin.ch | — | DE | — | — | Istituto nazionale di statistica — Switzerland |
| Fiji Bureau of Statistics | https://www.statsfiji.gov.fj | — | EN | — | — | Istituto nazionale di statistica — Fiji |
| General Authority for Statistics | https://www.stats.gov.sa | — | AR | — | — | Istituto nazionale di statistica — Saudi Arabia |
| Ghana Statistical Service | https://www.statsghana.gov.gh | — | EN | — | — | Istituto nazionale di statistica — Ghana |
| Guyana Bureau of Statistics | https://www.statisticsguyana.gov.gy | — | EN | — | — | Istituto nazionale di statistica — Guyana |
| Haut Commissariat au Plan | https://www.hcp.ma | — | AR | — | — | Istituto nazionale di statistica — Morocco |
| Hellenic Statistical Authority (ELSTAT) | https://www.statistics.gr | — | EL | — | — | Istituto nazionale di statistica — Greece |
| Hungarian Central Statistical Office (KSH) | https://www.ksh.hu | — | HU | — | — | Istituto nazionale di statistica — Hungary |
| ICASEES | https://www.icasees.org | — | FR | — | — | Istituto nazionale di statistica — Central African Republic |
| INEC | https://www.ecuadorencifras.gob.ec | — | ES | — | — | Istituto nazionale di statistica — Ecuador |
| INEGI | https://www.inegi.org.mx | — | ES | — | — | Istituto nazionale di statistica — Mexico |
| INIDE | https://www.inide.gob.ni | — | ES | — | — | Istituto nazionale di statistica — Nicaragua |
| INSEED | https://www.inseed.td | — | FR | — | — | Istituto nazionale di statistica — Chad |
| INSEED | https://www.inseed.tg | — | FR | — | — | Istituto nazionale di statistica — Togo |
| Institut de statistiques du Burundi (ISTEEBU) | https://www.isteebu.bi | — | FR | — | — | Istituto nazionale di statistica — Burundi |
| Institut des Statistiques de Djibouti | https://www.instad.dj | — | FR | — | — | Istituto nazionale di statistica — Djibouti |
| Institut national de la statistique | https://www.ins-rdc.org | — | FR | — | — | Istituto nazionale di statistica — DR Congo |
| Institut National de la Statistique | https://www.ins-congo.cg | — | FR | — | — | Istituto nazionale di statistica — Congo |
| Institut National de la Statistique | https://www.stat-guinee.org | — | FR | — | — | Istituto nazionale di statistica — Guinea |
| Institut National de la Statistique | https://www.ins.ci | — | FR | — | — | Istituto nazionale di statistica — Ivory Coast |
| Institut national de la statistique | https://www.instat-mali.org | — | FR | — | — | Istituto nazionale di statistica — Mali |
| Institut National de la Statistique | https://www.stat-niger.org | — | FR | — | — | Istituto nazionale di statistica — Niger |
| Institut National de la Statistique (INS) | https://www.ins.tn | — | AR | — | — | Istituto nazionale di statistica — Tunisia |
| Institut national de la statistique (INSD) | https://www.insd.bf | — | FR | — | — | Istituto nazionale di statistica — Burkina Faso |
| Institut national de la statistique (INSEE) | https://www.insee.fr | — | FR | — | — | Istituto nazionale di statistica — France |
| Institut national de la statistique (INSTAT) | https://www.instat.mg | — | FR | — | — | Istituto nazionale di statistica — Madagascar |
| Institute of Statistics (INSTAT) | https://www.instat.gov.al | — | SQ | — | — | Istituto nazionale di statistica — Albania |
| Instituto Brasileiro de Geografia e Estatística (IBGE) | https://www.ibge.gov.br | — | PT | — | — | Istituto nazionale di statistica — Brazil |
| Instituto Nacional de Estadística | https://www.inege.org | — | ES | — | — | Istituto nazionale di statistica — Equatorial Guinea |
| Instituto Nacional de Estadística | https://www.ine.gob.bo | — | ES | — | — | Istituto nazionale di statistica — Bolivia |
| Instituto Nacional de Estadística | https://www.ine.gob.gt | — | ES | — | — | Istituto nazionale di statistica — Guatemala |
| Instituto Nacional de Estadística | https://www.ine.gov.py | — | ES | — | — | Istituto nazionale di statistica — Paraguay |
| Instituto Nacional de Estadística | https://www.ine.gub.uy | — | ES | — | — | Istituto nazionale di statistica — Uruguay |
| Instituto Nacional de Estadística | https://www.ine.gov.ve | — | ES | — | — | Istituto nazionale di statistica — Venezuela |
| Instituto Nacional de Estadística (INE) | https://www.ine.es | — | ES | — | — | Istituto nazionale di statistica — Spain |
| Instituto Nacional de Estadística (INE) | https://www.ine.gob.hn | — | ES | — | — | Istituto nazionale di statistica — Honduras |
| Instituto Nacional de Estadística e Informática | https://www.inei.gob.pe | — | ES | — | — | Istituto nazionale di statistica — Peru |
| Instituto Nacional de Estadística y Censo | https://www.inec.gob.pa | — | ES | — | — | Istituto nazionale di statistica — Panama |
| Instituto Nacional de Estadística y Censos | https://www.inec.go.cr | — | ES | — | — | Istituto nazionale di statistica — Costa Rica |
| Instituto Nacional de Estadística y Censos (INDEC) | https://www.indec.gob.ar | — | ES | — | — | Istituto nazionale di statistica — Argentina |
| Instituto Nacional de Estadísticas | https://www.ine.cl | — | ES | — | — | Istituto nazionale di statistica — Chile |
| Instituto Nacional de Estatística | https://www.ine.gov.ao | — | PT | — | — | Istituto nazionale di statistica — Angola |
| Instituto Nacional de Estatística | https://ine.cv | — | PT | — | — | Istituto nazionale di statistica — Cape Verde |
| Instituto Nacional de Estatística | https://www.stat-guinebissau.com | — | PT | — | — | Istituto nazionale di statistica — Guinea-Bissau |
| Instituto Nacional de Estatística | https://www.ine.gov.mz | — | PT | — | — | Istituto nazionale di statistica — Mozambique |
| Instituto Nacional de Estatística | https://www.ine.st | — | PT | — | — | Istituto nazionale di statistica — São Tomé and Príncipe |
| Israel Central Bureau of Statistics | https://www.cbs.gov.il | — | HE | — | — | Istituto nazionale di statistica — Israel |
| Kenya National Bureau of Statistics | https://www.knbs.go.ke | — | EN | — | — | Istituto nazionale di statistica — Kenya |
| Kiribati Statistics Office | https://nso.gov.ki | — | EN | — | — | Istituto nazionale di statistica — Kiribati |
| Kosovo Agency of Statistics (ASK) | https://ask.rks-gov.net | — | SQ | — | — | Istituto nazionale di statistica — Kosovo |
| Kuwait Central Statistical Bureau | https://www.csb.gov.kw | — | AR | — | — | Istituto nazionale di statistica — Kuwait |
| Lao Statistics Bureau | https://www.lsb.gov.la | — | LO | — | — | Istituto nazionale di statistica — Laos |
| LISGIS | https://www.lisgis.gov.lr | — | EN | — | — | Istituto nazionale di statistica — Liberia |
| Maldives Bureau of Statistics | https://statisticsmaldives.gov.mv | — | EN | — | — | Istituto nazionale di statistica — Maldives |
| Monaco Statistics (IMSEE) | https://www.monacostatistics.mc | — | FR | — | — | Istituto nazionale di statistica — Monaco |
| Myanmar Statistical Information Service | https://www.mmsis.gov.mm | — | MY | — | — | Istituto nazionale di statistica — Myanmar |
| Namibia Statistics Agency | https://www.nsa.org.na | — | EN | — | — | Istituto nazionale di statistica — Namibia |
| National Agricultural Statistics Service | https://www.nass.usda.gov | — | EN | — | — | Istituto nazionale di statistica — United States |
| National Bureau of Statistics | https://www.nigerianstat.gov.ng | — | EN | — | — | Istituto nazionale di statistica — Nigeria |
| National Bureau of Statistics | https://www.ssnb.org | — | EN | — | — | Istituto nazionale di statistica — South Sudan |
| National Bureau of Statistics | https://www.nbs.go.tz | — | EN | — | — | Istituto nazionale di statistica — Tanzania |
| National Bureau of Statistics | https://statistics.gov.ag | — | EN | — | — | Istituto nazionale di statistica — Antigua and Barbuda |
| National Bureau of Statistics (BNS) | https://www.statistica.md | — | RO | — | — | Istituto nazionale di statistica — Moldova |
| National Bureau of Statistics of China | https://www.stats.gov.cn | — | ZH | — | — | Istituto nazionale di statistica — China |
| National Center for Education Statistics | https://nces.ed.gov | — | EN | — | — | Istituto nazionale di statistica — United States |
| National Centre for Statistics & Information | https://data.gov.om | — | AR | — | — | Istituto nazionale di statistica — Oman |
| National Institute of Statistics | https://www.statistics-cameroon.org | — | EN | — | — | Istituto nazionale di statistica — Cameroon |
| National Institute of Statistics | https://www.nis.gov.kh | — | KM | — | — | Istituto nazionale di statistica — Cambodia |
| National Institute of Statistics (INS) | https://www.insse.ro | — | RO | — | — | Istituto nazionale di statistica — Romania |
| National Institute of Statistics of Rwanda | https://www.statistics.gov.rw | — | EN | — | — | Istituto nazionale di statistica — Rwanda |
| National Statistical Committee | https://www.stat.kg | — | RU | — | — | Istituto nazionale di statistica — Kyrgyzstan |
| National Statistical Committee (BELSTAT) | https://www.belstat.gov.by/en | — | RU | — | — | Istituto nazionale di statistica — Belarus |
| National Statistical Institute (NSI) | https://www.nsi.bg/en | — | BG | — | — | Istituto nazionale di statistica — Bulgaria |
| National Statistical Office | https://www.nsomalawi.mw | — | EN | — | — | Istituto nazionale di statistica — Malawi |
| National Statistical Office | https://www.nso.go.th | — | TH | — | — | Istituto nazionale di statistica — Thailand |
| National Statistical Office (MoSPI) | https://www.mospi.gov.in | — | EN | — | — | Istituto nazionale di statistica — India |
| National Statistical Office of PNG | https://www.nso.gov.pg | — | EN | — | — | Istituto nazionale di statistica — Papua New Guinea |
| National Statistics and Information Authority | https://nsia.gov.af | — | EN | — | — | Istituto nazionale di statistica — Afghanistan |
| National Statistics Bureau | https://www.nbs.gov.sc | — | EN | — | — | Istituto nazionale di statistica — Seychelles |
| National Statistics Bureau | https://www.nsb.gov.bt | — | EN | — | — | Istituto nazionale di statistica — Bhutan |
| National Statistics Office | https://www.cbs.gov.np | — | NE | — | — | Istituto nazionale di statistica — Nepal |
| National Statistics Office | https://www.nso.gov.vn | — | VI | — | — | Istituto nazionale di statistica — Vietnam |
| National Statistics Office (NSO) | https://www.nso.gov.mt | — | EN | — | — | Istituto nazionale di statistica — Malta |
| National Statistics Office of Georgia (GeoStat) | https://www.geostat.ge | — | KA | — | — | Istituto nazionale di statistica — Georgia |
| National Statistics Office of Mongolia | https://www.nso.mn | — | MN | — | — | Istituto nazionale di statistica — Mongolia |
| Office for National Statistics (ONS) | https://www.ons.gov.uk | — | EN | — | — | Istituto nazionale di statistica — United Kingdom |
| Office national de la statistique | https://www.ons.mr | — | FR | — | — | Istituto nazionale di statistica — Mauritania |
| Office National des Statistiques | https://www.ons.dz | — | AR | — | — | Istituto nazionale di statistica — Algeria |
| Office of Statistics | https://www.as.llv.li | — | DE | — | — | Istituto nazionale di statistica — Liechtenstein |
| Oficina Nacional de Estadística | https://www.one.gob.do | — | ES | — | — | Istituto nazionale di statistica — Dominican Republic |
| Oficina Nacional de Estadísticas (ONEI) | https://www.onei.gob.cu | — | ES | — | — | Istituto nazionale di statistica — Cuba |
| Pakistan Bureau of Statistics | https://www.pbs.gov.pk | — | EN | — | — | Istituto nazionale di statistica — Pakistan |
| Palestinian Central Bureau of Statistics | https://www.pcbs.gov.ps | — | AR | — | — | Istituto nazionale di statistica — Palestine |
| Philippine Statistics Authority | https://psa.gov.ph | — | EN | — | — | Istituto nazionale di statistica — Philippines |
| Planning and Statistics Authority | https://www.psa.gov.qa | — | AR | — | — | Istituto nazionale di statistica — Qatar |
| Samoa Bureau of Statistics | https://www.sbs.gov.ws | — | EN | — | — | Istituto nazionale di statistica — Samoa |
| Solomon Islands Statistics | https://www.statistics.gov.sb | — | EN | — | — | Istituto nazionale di statistica — Solomon Islands |
| Somalia National Bureau of Statistics | https://www.nbs.gov.so | — | EN | — | — | Istituto nazionale di statistica — Somalia |
| State Committee on Statistics | https://www.stat.gov.tm | — | RU | — | — | Istituto nazionale di statistica — Turkmenistan |
| State Committee on Statistics | https://stat.uz | — | RU | — | — | Istituto nazionale di statistica — Uzbekistan |
| State Data Agency (LSD) | https://www.vda.lrv.lt | — | LT | — | — | Istituto nazionale di statistica — Lithuania |
| State Statistical Office | https://www.stat.gov.mk | — | MK | — | — | Istituto nazionale di statistica — North Macedonia |
| State Statistics Committee of Azerbaijan | https://www.stat.gov.az | — | AZ | — | — | Istituto nazionale di statistica — Azerbaijan |
| State Statistics Service of Ukraine | https://www.stat.gov.ua | — | UK | — | — | Istituto nazionale di statistica — Ukraine |
| STATEC | https://statistiques.public.lu | — | FR | — | — | Istituto nazionale di statistica — Luxembourg |
| Statistical Centre of Iran | https://www.amar.org.ir | — | FA | — | — | Istituto nazionale di statistica — Iran |
| Statistical Committee of Armenia | https://www.armstat.am | — | HY | — | — | Istituto nazionale di statistica — Armenia |
| Statistical Institute of Belize | https://www.sib.org.bz | — | EN | — | — | Istituto nazionale di statistica — Belize |
| Statistical Institute of Jamaica | https://statinja.gov.jm | — | EN | — | — | Istituto nazionale di statistica — Jamaica |
| Statistical Office of Montenegro (MONSTAT) | https://www.monstat.org | — | SR | — | — | Istituto nazionale di statistica — Montenegro |
| Statistical Office of Slovenia (SURS) | https://www.stat.si | — | SL | — | — | Istituto nazionale di statistica — Slovenia |
| Statistical Office of the Republic of Serbia | https://www.stat.gov.rs | — | SR | — | — | Istituto nazionale di statistica — Serbia |
| Statistical Office of the Slovak Republic | https://www.susr.sk | — | SK | — | — | Istituto nazionale di statistica — Slovakia |
| Statistical Service of Cyprus (CYSTAT) | https://www.cystat.gov.cy | — | EN | — | — | Istituto nazionale di statistica — Cyprus |
| Statistics and Census Service (DSEC) | https://www.dsec.gov.mo | — | ZH | — | — | Istituto nazionale di statistica — Macau |
| Statistics Austria | https://www.statistik.at | — | DE | — | — | Istituto nazionale di statistica — Austria |
| Statistics Belgium | https://www.statbel.fgov.be | — | NL | — | — | Istituto nazionale di statistica — Belgium |
| Statistics Botswana | https://www.statsbots.org.bw | — | EN | — | — | Istituto nazionale di statistica — Botswana |
| Statistics Bureau of Japan | https://www.stat.go.jp | — | JA | — | — | Istituto nazionale di statistica — Japan |
| Statistics Canada | https://www.statcan.gc.ca | — | EN | — | — | Istituto nazionale di statistica — Canada |
| Statistics Denmark | https://www.dst.dk | — | DA | — | — | Istituto nazionale di statistica — Denmark |
| Statistics Estonia | https://www.stat.ee | — | ET | — | — | Istituto nazionale di statistica — Estonia |
| Statistics Faroe Islands | https://www.hagstova.fo | — | FO | — | — | Istituto nazionale di statistica — Faroe Islands |
| Statistics Finland | https://www.stat.fi | — | FI | — | — | Istituto nazionale di statistica — Finland |
| Statistics Iceland | https://www.statice.is | — | IS | — | — | Istituto nazionale di statistica — Iceland |
| Statistics Korea (KOSTAT) | https://kostat.go.kr | — | KO | — | — | Istituto nazionale di statistica — South Korea |
| Statistics Mauritius | https://statsmauritius.govmu.org | — | EN | — | — | Istituto nazionale di statistica — Mauritius |
| Statistics Netherlands (CBS) | https://www.cbs.nl | — | NL | — | — | Istituto nazionale di statistica — Netherlands |
| Statistics New Zealand | https://www.stats.govt.nz | — | EN | — | — | Istituto nazionale di statistica — New Zealand |
| Statistics Norway (SSB) | https://www.ssb.no | — | NO | — | — | Istituto nazionale di statistica — Norway |
| Statistics Poland (GUS) | https://www.stat.gov.pl | — | PL | — | — | Istituto nazionale di statistica — Poland |
| Statistics Portugal (INE) | https://www.ine.pt | — | PT | — | — | Istituto nazionale di statistica — Portugal |
| Statistics Sierra Leone | https://www.statistics.sl | — | EN | — | — | Istituto nazionale di statistica — Sierra Leone |
| Statistics South Africa | https://www.statssa.gov.za | — | EN | — | — | Istituto nazionale di statistica — South Africa |
| Statistics Sweden (SCB) | https://www.scb.se | — | SV | — | — | Istituto nazionale di statistica — Sweden |
| The Gambia Bureau of Statistics | https://www.gbosdata.org | — | EN | — | — | Istituto nazionale di statistica — Gambia |
| Turkish Statistical Institute (TUIK) | https://www.turkstat.gov.tr | — | TR | — | — | Istituto nazionale di statistica — Turkey |
| Ufficio Tecnologia, Dati e Statistica | https://www.statistica.sm | — | IT | — | — | Istituto nazionale di statistica — San Marino |
| Uganda Bureau of Statistics | https://www.ubos.org | — | EN | — | — | Istituto nazionale di statistica — Uganda |
| United States Census Bureau | https://www.census.gov | — | EN | — | — | Istituto nazionale di statistica — United States |
| Vanuatu National Statistics Office | https://www.vnso.gov.vu | — | EN | — | — | Istituto nazionale di statistica — Vanuatu |
| Zambia Statistics Agency | https://www.zamstats.gov.zm | — | EN | — | — | Istituto nazionale di statistica — Zambia |
| Zimbabwe National Statistics Agency | https://www.zimstat.co.zw | — | EN | — | — | Istituto nazionale di statistica — Zimbabwe |

---

### 2.3 Organizzazioni Internazionali & Banche di Sviluppo (26)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ADB — Asian Development Bank | https://www.adb.org | — | EN | Asia | — | Banca asiatica di sviluppo, dati e report |
| AfDB — African Development Bank | https://www.afdb.org | — | EN/FR | Africa | — | Banca africana di sviluppo |
| AIIB | https://www.aiib.org | — | EN | Asia | — | Asian Infrastructure Investment Bank |
| BOAD — Banque Ouest Africaine de Développement | https://www.boad.org | — | FR | Africa Occ. | — | Banca sviluppo Africa Occidentale |
| CABEI — Central American Bank | https://www.bcie.org | — | ES | America Centrale | — | Banco Centroamericano de Integración Económica |
| CAF — Banco de Desarrollo de América Latina | https://www.caf.com | — | ES/EN | LatAm | — | Banca di sviluppo latinoamericana |
| CDB — Caribbean Development Bank | https://www.caribank.org | — | EN | Caraibi | — | Banca caraibica di sviluppo |
| EADB — East African Development Bank | https://www.eadb.org | — | EN | Africa Or. | — | Banca sviluppo Africa Orientale |
| EBRD | https://www.ebrd.com | — | EN | Europa | — | Banca europea per la ricostruzione e lo sviluppo |
| EIB — European Investment Bank | https://www.eib.org | — | EN | EU | — | Banca europea per gli investimenti |
| GCF — Green Climate Fund | https://www.greenclimate.fund | — | EN | Globale | — | Fondo verde per il clima ONU |
| GEF — Global Environment Facility | https://www.thegef.org | — | EN | Globale | — | Fondo globale per l'ambiente |
| IDA — International Development Association | https://ida.worldbank.org | — | EN | Globale | — | Braccio concessionale Banca Mondiale |
| IDB — Inter-American Development Bank | https://www.iadb.org | — | EN/ES | Americhe | — | Banca interamericana di sviluppo |
| IFAD | https://www.ifad.org | — | EN | Globale | — | Fondo sviluppo agricolo ONU |
| IFC — International Finance Corporation | https://www.ifc.org | — | EN | Globale | — | Braccio privato Banca Mondiale |
| IMO — International Maritime Organization | https://www.imo.org | — | EN | Globale | — | Organizzazione marittima internazionale ONU |
| IsDB — Islamic Development Bank | https://www.isdb.org | — | EN/AR | Globale | — | Banca islamica di sviluppo |
| ITU | https://www.itu.int | — | EN/Multi | Globale | — | Unione internazionale telecomunicazioni, dati ICT |
| MIGA | https://www.miga.org | — | EN | Globale | — | Garanzie investimenti, Banca Mondiale |
| NDB — New Development Bank | https://www.ndb.int | — | EN | BRICS | — | Banca di sviluppo BRICS |
| UNCTAD | https://unctad.org | — | EN | Globale | — | Conferenza ONU commercio e sviluppo — dati e report |
| UNESCO | https://www.unesco.org | — | EN/Multi | Globale | — | Educazione, scienza e cultura ONU |
| UNFCCC | https://unfccc.int | — | EN | Globale | — | Convenzione ONU cambiamenti climatici — NDC registry |
| UNIDO | https://www.unido.org | — | EN | Globale | — | Sviluppo industriale ONU |
| WFP — World Food Programme | https://www.wfp.org | — | EN/Multi | Globale | — | Programma alimentare mondiale |

### 2.4 Sondaggi, Barometri & Dataset Comparativi (26)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Arab Barometer | https://www.arabbarometer.org | — | EN/AR | MENA | — | Sondaggi mondo arabo |
| Asian Barometer | https://www.asianbarometer.org | — | EN | Asia | — | Sondaggi democrazia in Asia |
| Constitute Project | https://www.constituteproject.org | — | EN | Globale | — | Costituzioni mondiali comparate |
| Correlates of War | https://correlatesofwar.org | — | EN | Globale | — | Dataset storici guerre e alleanze |
| CSES — Comparative Study of Electoral Systems | https://cses.org | — | EN | Globale | — | Studio comparato sistemi elettorali — microdati 50+ Paesi |
| EIU Democracy Index | https://www.eiu.com/n/campaigns/democracy-index | — | EN | Globale | — | Indice democrazia Economist Intelligence Unit |
| Eurobarometer — Surveys | https://europa.eu/eurobarometer/surveys/browse/all | — | Multi | EU | — | Sondaggi periodici opinione pubblica UE per Paese |
| European Social Survey | https://www.europeansocialsurvey.org | — | EN | Europa | — | Survey sociale comparata europea |
| Fragile States Index | https://fragilestatesindex.org | — | EN | Globale | — | Fragilità statale (Fund for Peace) |
| FRED — Federal Reserve Economic Data | https://fred.stlouisfed.org | — | EN | Globale | Gratuito | Database macro time-series (St. Louis Fed) — 800k+ serie, API |
| Gallup World Poll | https://www.gallup.com/analytics/318875/global-research.aspx | — | EN | Globale | — | Sondaggi globali opinione pubblica — 140+ Paesi |
| Global Competitiveness Index — WEF | https://www.weforum.org/reports/the-global-competitiveness-report-2020 | — | EN | Globale | — | Indice competitività WEF per Paese |
| Global Innovation Index (WIPO) | https://www.globalinnovationindex.org | — | EN | Globale | — | Innovazione per Paese |
| Global Peace Index (IEP) | https://www.economicsandpeace.org | — | EN | Globale | — | Institute for Economics and Peace |
| Henley & Partners — Passport Index | https://www.henleyglobal.com | — | EN | Globale | — | Indice passaporti e mobilità |
| ISSP | https://issp.org | — | EN | Globale | — | Programma survey sociale internazionale |
| LAPOP — Latin American Public Opinion Project | https://www.vanderbilt.edu/lapop | — | EN/ES | LatAm | — | Sondaggi opinione pubblica latinoamericana — Vanderbilt |
| Latinobarómetro | https://www.latinobarometro.org | — | ES | LatAm | — | Opinione pubblica latinoamericana |
| Legatum Prosperity Index | https://www.prosperity.com | — | EN | Globale | — | Indice prosperità per Paese |
| Lowy Asia Power Index | https://power.lowyinstitute.org | — | EN | Asia | — | Potenza comparata in Asia |
| Mo Ibrahim Index (IIAG) | https://mo.ibrahim.foundation/iiag | — | EN | Africa | — | Indice governance africana per Paese |
| ND-GAIN Index | https://gain.nd.edu | — | EN | Globale | — | Adattamento climatico per Paese |
| Polity5 Project | https://www.systemicpeace.org/polityproject.html | — | EN | Globale | — | Dataset regime politico storico 1800-presente |
| QoG — Quality of Government Dataset | https://www.gu.se/en/quality-government/qog-data | — | EN | Globale | — | Dataset qualità governance per Paese — Università Göteborg |
| World Values Survey | https://www.worldvaluessurvey.org | — | EN | Globale | — | Valori comparati ~100 Paesi |
| YouGov International | https://yougov.co.uk/topics/international | — | EN | Globale | — | Sondaggi internazionali panel online |

## 3. 🏢 Registri Aziendali & Corporate Intelligence

### 3.1 Camere di Commercio (123)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AARGAU CHAMBER OF COMMERCE AND INDUSTRY | https://www.aihk.ch/ | — | — | — | — | Dataset strutturato: selezione dei membri della World Chambers Federation (WCF) |
| ABBOTSFORD CHAMBER OF COMMERCE | https://www.abbotsfordchamber.com/ | — | — | — | — | Dataset strutturato: selezione dei membri della World Chambers Federation (WCF) |
| ABHA CHAMBER OF COMMERCE | https://www.abhacci.org.sa/ | — | — | — | — | Dataset strutturato: selezione dei membri della World Chambers Federation (WCF) |
| Abu Dhabi Chamber of Commerce & Industry | https://www.abudhabichamber.ae/ | — | — | — | — | Dataset strutturato: selezione dei membri della World Chambers Federation (WCF) |
| African Chambers of Commerce | https://africanchambersofcommerce.org | — | EN | — | — | Rete africana — Pan-Africa |
| Albania — Union of Chambers | https://uccial.al | — | SQ/EN | AL | — | Unione camere albanesi |
| Algeria | https://caci.dz/en/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| Angola | https://ccia.ao/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| Argentina — CAC | https://www.cac.com.ar | — | ES | AR | — | Cámara Argentina de Comercio |
| ASCAME | https://www.ascame.org | — | EN/FR | — | — | Camere del Mediterraneo |
| Australia — ACCI | https://www.australianchamber.com.au | — | EN | AU | — | Camera di commercio e industria australiana |
| Austria | https://www.wko.at/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Bahrain — BCCI | https://www.bcci.bh | — | AR/EN | BH | — | Camera di commercio del Bahrein |
| Belarus — BelCCI | https://www.cci.by | — | RU/EN | BY | — | Camera di commercio bielorussa |
| Belgio | https://belgianchambers.be/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Benin | https://www.cci.bj/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| Bosnia — Spoljnotrgovinska komora BiH | https://komorabih.ba | — | BS/EN | BA | — | Camera di commercio estero BiH |
| Botswana | https://bb.org.bw/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| Brazil — CACB | https://cacb.org.br | — | PT | BR | — | Confederazione associazioni commerciali |
| Brazil — CNI | https://www.portaldaindustria.com.br | — | PT | BR | — | Confederazione nazionale industria |
| Bulgaria | https://www.bcci.bg/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Burkina Faso | https://cci.bf/?q=en | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| CACCI, accesso eseguito il giorno marzo 28, 2026, | https://www.cacci.biz/ | — | — | — | — | Bibliografia |
| Camerun | http://ccima.cm/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| Canada — Canadian Chamber of Commerce | https://chamber.ca | — | EN/FR | CA | — | Camera di commercio canadese |
| Chile — CNC | https://www.cnc.cl | — | ES | CL | — | Camera nazionale commercio cilena |
| China — CCPIT | https://www.ccpit.org | — | ZH/EN | CN | — | Consiglio promozione commercio internazionale |
| Cile | https://www.amchamchile.cl/ | — | — | — | — | Dataset strutturato: le Camere di Commercio Americane (AmChams) in America Latin |
| Cipro | http://www.ccci.org.cy/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Colombia — Confecámaras | https://confecamaras.org.co | — | ES | CO | — | Rete camere colombiane |
| Croazia | http://www.investincroatia.hr/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Côte d'Ivoire — CCI-CI | https://www.cci.ci | — | FR | CI | — | Camera di commercio ivoriana |
| Denmark — Dansk Erhverv | https://www.danskerhverv.dk | — | DA | DK | — | Camera di commercio danese |
| Dominican Rep. — Cámara Santo Domingo | https://camarasantodomingo.do | — | ES | DO | — | Camera di Santo Domingo |
| Ecuador | https://www.ecamcham.com | — | — | — | — | Dataset strutturato: le Camere di Commercio Americane (AmChams) in America Latin |
| Egitto | http://fedcoc.org.eg/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| El Salvador | https://www.amchamsal.com | — | — | — | — | Dataset strutturato: le Camere di Commercio Americane (AmChams) in America Latin |
| Estonia | https://www.koda.ee/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Etiopia | https://www.ethiopianchamber.com/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| Eurochambres | https://www.eurochambres.eu | — | EN | — | — | Rete camere europee — UE |
| Finlandia | https://www.kauppakamari.fi/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Francia | https://www.cci.fr/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| GCC Chambers | https://gcc-sg.org | — | AR/EN | — | — | Camere Consiglio Cooperazione Golfo |
| Georgia | http://www.gcci.ge/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Germania | https://www.dihk.de/de | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Ghana | http://ghanachamber.org/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| Grecia | http://www.uhc.gr/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Guatemala | https://www.amchamguate.com | — | — | — | — | Dataset strutturato: le Camere di Commercio Americane (AmChams) in America Latin |
| Hong Kong — HKGCC | https://www.chamber.org.hk | — | EN/ZH | HK | — | Camera generale di commercio HK |
| ICC — International Chamber of Commerce | https://iccwbo.org | — | EN | Globale | — | Camera di commercio internazionale (Parigi) |
| Iceland — Iceland Chamber of Commerce | https://www.chamber.is | — | IS/EN | IS | — | Camera di commercio islandese |
| India — CII | https://www.cii.in | — | EN | IN | — | Confederation of Indian Industry |
| India — FICCI | https://www.ficci.in | — | EN | IN | — | Federazione camere indiane |
| Indonesia — KADIN | https://kadin.id | — | ID/EN | ID | — | Camera di commercio indonesiana |
| Irlanda | https://www.chambers.ie/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Israel — Federation of Chambers | https://www.chamber.org.il | — | HE/EN | IL | — | Federazione camere israeliane |
| Italia | https://www.unioncamere.gov.it/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Japan — JCCI | https://www.jcci.or.jp | — | JA/EN | JP | — | Camera di commercio e industria giapponese |
| Jordan — Jordan Chamber of Commerce | https://www.jocc.org.jo | — | AR/EN | JO | — | Camera di commercio giordana |
| Kazakhstan — Atameken | https://atameken.kz | — | KK/RU/EN | KZ | — | Camera nazionale imprenditori |
| Kenya | https://www.kenyachamber.or.ke/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| Kuwait — KCCI | https://www.kcci.org.kw | — | AR/EN | KW | — | Camera di commercio kuwaitiana |
| Lebanon — CCIA Beirut | https://www.ccib.org.lb | — | AR/FR/EN | LB | — | Camera di Beirut e Monte Libano |
| Lettonia | https://www.chamber.lv/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Lituania | https://chambers.lt/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Lussemburgo | https://www.cc.lu/accueil/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Malta | https://www.maltachamber.org.mt/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Mauritius — MCCI | https://www.mcci.org | — | EN/FR | MU | — | Camera di commercio mauriziana |
| Messico | https://www.amcham.com | — | — | — | — | Dataset strutturato: le Camere di Commercio Americane (AmChams) in America Latin |
| Moldova — Camera de Comerț | https://chamber.md | — | RO/EN | MD | — | Camera di commercio moldava |
| Mongolia — MNCCI | https://mongolchamber.mn | — | MN/EN | MN | — | Camera di commercio mongola |
| Montenegro — Privredna komora | https://www.privrednakomora.me | — | SR/EN | ME | — | Camera di commercio montenegrina |
| Morocco — CGEM | https://www.cgem.ma | — | FR/AR | MA | — | Confederazione imprese marocchine |
| Mozambique — CTA | https://cta.org.mz | — | PT | MZ | — | Confederazione associazioni economiche |
| Namibia — NCCI | https://www.ncci.org.na | — | EN | NA | — | Camera di commercio namibiana |
| Nepal — FNCCI | https://fncci.org | — | EN/NE | NP | — | Federazione camere nepalesi |
| Nigeria | http://naccima.com/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| Nigeria — Lagos Chamber (LCCI) | https://lagoschamber.com | — | EN | NG | — | Camera di Lagos |
| North Macedonia — Economic Chamber | https://www.mchamber.mk | — | MK/EN | MK | — | Camera economica macedone |
| Norvegia | http://dnhf.no/home-en/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Oman — OCCI | https://chamberoman.om | — | AR/EN | OM | — | Camera di commercio omanita |
| PACCI (Pan-African Chambers) | https://pacci.org | — | EN/FR | — | — | Camere panafricane — Pan-Africa |
| Pakistan — FPCCI | https://fpcci.org.pk | — | EN | PK | — | Federazione camere pakistane |
| Panama | https://www.panamcham.com | — | — | — | — | Dataset strutturato: le Camere di Commercio Americane (AmChams) in America Latin |
| Paraguay | https://www.pamcham.com | — | — | — | — | Dataset strutturato: le Camere di Commercio Americane (AmChams) in America Latin |
| Peru — Cámara de Comercio de Lima | https://www.camaralima.org.pe | — | ES | PE | — | Camera di commercio di Lima |
| Philippines — PCCI | https://www.philippinechamber.com | — | EN | PH | — | Camera di commercio filippina |
| Polonia | https://kig.pl/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Portogallo | https://www.ccip.pt/pt/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Qatar Chamber — Comitato Sanità | https://www.qatarchamber.com/members | — | EN | — | — | Qatar Chamber — settore sanitario privato |
| Repubblica Ceca | https://www.komora.cz/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Romania | https://ccir.ro/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Ruanda | http://rwandachamber.org/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| Russia — TPP RF | https://tpprf.ru | — | RU/EN | RU | — | Camera di commercio e industria russa |
| Saudi Arabia — Council of Saudi Chambers | https://csc.org.sa | — | AR/EN | SA | — | Consiglio camere saudite |
| Senegal | https://cciad.sn/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| Serbia — Privredna komora Srbije | https://pks.rs | — | SR/EN | RS | — | Camera di commercio serba |
| Singapore — SBF | https://www.sbf.org.sg | — | EN | SG | — | Singapore Business Federation |
| Slovacchia | https://www.sopk.sk/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Slovenia | https://www.gzs.si/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| South Korea — KCCI | https://www.korcham.net | — | KO/EN | KR | — | Camera di commercio coreana |
| Spagna | https://www.camara.es/en | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Sri Lanka — Ceylon Chamber of Commerce | https://www.chamber.lk | — | EN | LK | — | Camera di commercio di Ceylon |
| Sudafrica | http://sacci.org.za/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| Svezia | https://www.swedishchambers.se/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Svizzera | https://www.sihk.ch/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Tanzania | http://tccia.com/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| Thailand — Thai Chamber of Commerce | https://www.thaichamber.org | — | TH/EN | TH | — | Camera di commercio thailandese |
| Trinidad e Tobago | https://www.amchamtt.com | — | — | — | — | Dataset strutturato: le Camere di Commercio Americane (AmChams) in America Latin |
| Tunisia | http://utica.org.tn/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| Turchia | https://www.tobb.org.tr | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| UAE — Dubai Chamber | https://www.dubaichamber.com | — | AR/EN | AE | — | Camera di commercio di Dubai |
| Ucraina | https://ucci.org.ua/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Uganda | https://www.chamberuganda.go.ug/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |
| UK — British Chambers of Commerce | https://www.britishchambers.org.uk | — | EN | GB | — | Federazione camerale britannica |
| Ungheria | https://mkik.hu/ | — | — | — | — | Dataset strutturato: membri effettivi e affiliati di Eurochambres |
| Uruguay | https://www.ccuruguayusa.com | — | — | — | — | Dataset strutturato: le Camere di Commercio Americane (AmChams) in America Latin |
| US — U.S. Chamber of Commerce | https://www.uschamber.com | — | EN | US | — | Camera di commercio statunitense |
| Uzbekistan — Chamber of Commerce | https://chamber.uz | — | UZ/RU/EN | UZ | — | Camera di commercio uzbeka |
| Venezuela — Fedecámaras | https://fedecamaras.org | — | ES | VE | — | Federazione camere venezuelane |
| Vietnam — VCCI | https://vcci.com.vn | — | VI/EN | VN | — | Camera di commercio vietnamita |
| World Chambers Federation (ICC) | https://worldchambers.com | — | EN | — | — | Federazione mondiale camere — Globale |
| Zambia | https://zambiachamber.org/ | — | — | — | — | Dataset strutturato: membri della Pan African Chamber of Commerce and Industry ( |

### 3.2 Risk Management & Business Intelligence (37)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Acerca de | https://www.burodecredito.com.mx/generales/acerca-de-bur%C3%B3.html | — | — | — | — | Bibliografia |
| ALIDE | https://www.alide.org.pe | — | ES | — | — | Assoc. latinoam. istituzioni finanziarie per sviluppo — Risk/Credit |
| Best IT Vendor Risk Management Solutions Reviews 2026 | https://www.gartner.com/reviews/market/it-vendor-risk-management-solutions | — | — | — | — | Bibliografia |
| Category: Members - BIIA.com | https://www.biia.com/category/members/ | — | — | — | — | Bibliografia |
| Coface | https://www.coface.com | — | — | FR | — | Risk economico — Francia |
| Companies List | https://www.consumerfinance.gov/consumer-tools/credit-reports-and-scores/consumer-reporting-companies/companies-list/ | — | — | — | — | Bibliografia |
| Confcommercio Milano | https://www.confcommerciomilano.it | — | IT | — | — | Associazione commercio Milano — Reti imprese · Italia |
| Corporate Crime & Investigations, USA, Global | https://chambers.com/legal-rankings/corporate-crime-investigations-usa-2:2385:225:1 | — | — | — | — | Bibliografia |
| Corporate Investigations/Anti-Corruption, Global: Multi-Jurisdictional, Global | https://chambers.com/legal-rankings/corporate-investigations-anti-corruption-global-multi-jurisdictional-2:2790:21180:1 | — | — | — | — | Bibliografia |
| CRIBIS | https://www.cribis.com/it | — | IT | — | — | Business information e credit risk Italia — Gruppo CRIF |
| CTOS Credit Malaysia | https://ctoscredit.com.my | — | EN | — | — | Credit reporting agency — Malaysia |
| D&B Cambodia | https://www.dnbcb.com | — | EN | — | — | Credit bureau Cambodia — Dun & Bradstreet |
| Datazn.ai | https://www.datazn.ai | — | EN | — | — | ESG data providers comparatore 2026 |
| Decisimo | https://decisimo.com | — | EN | — | — | Credit bureau data e risk scoring — Africa focus |
| Emerging Risks in Audit & Risk Management | https://www.gartner.com/en/audit-risk/trends/emerging-risks | — | — | — | — | Bibliografia |
| FATF | https://www.fatf-gafi.org | — | — | — | — | AML — Int. org. |
| FEBIS | https://www.febis.org | — | EN | — | — | Federation of Business Information Services — Globale |
| Forrester Wave™: Third-Party Risk Management Platforms, Q1 2026 | https://www.logicgate.com/resources/reports/forrester-wave-third-party-risk-management-platforms-q1-2026/ | — | — | — | — | Bibliografia |
| iDenfy | https://www.idenfy.com | — | EN | — | — | Fraud prevention e identity verification |
| Jamlab | https://jamlab.africa | — | — | Africa | — | Media innovation |
| Jones Day Lawyers and Practices Earn Top Rankings in Chambers Global 2026 | https://www.jonesday.com/en/news/2026/02/jones-day-lawyers-and-practices-earn-top-rankings-in-chambers-global-2026 | — | — | — | — | Bibliografia |
| Kroll | https://www.kroll.com/en | — | EN | — | — | Due diligence, investigazioni, compliance e risk intelligence — Globale |
| LexisNexis | https://www.lexisnexis.com | — | — | — | Commerciale | Legale e notizie — A pagamento — Database |
| MetricStream | https://www.metricstream.com | — | EN | — | — | Piattaforma GRC e cyber risk management — Leader Forrester 2026 |
| Moody's | https://www.moodys.com | — | — | — | — | Ratings — Research |
| Nexis Uni | https://www.lexisnexis.com/en-us/products/nexis-uni.page | — | — | — | — | Giornali archivio — Accademico — Database |
| ORBIS (Bureau van Dijk) | https://orbis.bvdinfo.com | — | — | — | Database | Dati aziende globali — A pagamento |
| Riskonnect | https://riskonnect.com | — | EN | — | — | Enterprise risk management platform — Band 1 Forrester 2026 |
| S&P Global | https://www.spglobal.com | — | — | — | — | Ratings — Research |
| Serasa Experian - Company, Brazil | https://www.swfinstitute.org/profile/5e39a651fcbe7e8ca72a2b94 | — | — | — | — | Bibliografia |
| Serasa S.A. Sao Paulo Company Profile - Brazil | https://www.emis.com/php/company-profile/BR/Serasa_SA__Sao_Paulo__en_1154489.html | — | — | — | — | Bibliografia |
| Stock Analysis | https://stockanalysis.com | — | EN | — | — | Dati finanziari e profili aziendali — Gratuito |
| Streamlit | https://streamlit.io | — | — | — | Open Source | Python — Data app |
| Sweep | https://www.sweep.net | — | EN | — | — | ESG reporting e sustainability software — SaaS |
| Top 10 Best Fraud Prevention Companies in 2025 | https://www.cryptika.com/top-10-best-fraud-prevention-companies-in-2025/ | — | — | — | — | Bibliografia |
| Top 10: Credit Rating Companies | https://fintechmagazine.com/articles/top-10-credit-rating-companies | — | — | — | — | Bibliografia |
| Top 12 sustainability reporting platforms (ESG) | https://www.energycap.com/blog/sustainability-reporting-platform/ | — | — | — | — | Bibliografia |

### 3.3 Registri & Ownership (80)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Argentina — IGJ | https://www.argentina.gob.ar/justicia/igj | — | ES | AR | — | Inspección General de Justicia |
| Armenia — e-Register | https://www.e-register.am | — | HY/EN | AM | — | Registro imprese armeno |
| Australia — ASIC | https://asic.gov.au | — | EN | AU | — | Regolatore + registro imprese |
| Austria — Firmenbuch (JustizOnline) | https://justizonline.gv.at | — | DE | AT | — | Registro imprese austriaco |
| Bahrain — Sijilat | https://www.sijilat.bh | — | AR/EN | BH | — | Registro commerciale del Bahrein |
| Belgium — KBO/BCE | https://kbopub.economie.fgov.be | — | NL/FR | BE | — | Banque-Carrefour des Entreprises |
| Bolivia — SEPREC | https://www.seprec.gob.bo | — | ES | BO | — | Registro di commercio boliviano |
| Botswana — CIPA | https://www.cipa.co.bw | — | EN | BW | — | Registro imprese del Botswana |
| Brazil — Consulta CNPJ (Receita Federal) | https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/cnpjreva_solicitacao.asp | — | PT | BR | — | Verifica CNPJ |
| Bulgaria — Trade Register (Registry Agency) | https://portal.registryagency.bg | — | BG/EN | BG | — | Registro commerciale bulgaro |
| Canada — Corporations Canada | https://ised-isde.canada.ca/cc/lgcy/fdrlCrpSrch.html | — | EN/FR | CA | — | Ricerca società federali |
| Chile — Registro de Empresas y Sociedades | https://www.registrodeempresasysociedades.cl | — | ES | CL | — | Registro imprese semplificato |
| China — GSXT (National Enterprise Credit) | https://www.gsxt.gov.cn | — | ZH | CN | — | Sistema nazionale credito imprese |
| Colombia — RUES | https://www.rues.org.co | — | ES | CO | — | Registro unico imprese e società |
| Costa Rica — Registro Nacional | https://www.rnpdigital.com | — | ES | CR | — | Registro nazionale costaricano |
| Croatia — Sudski registar | https://sudreg.pravosudje.hr | — | HR | HR | — | Registro giudiziario imprese |
| Cyprus — Companies Section (DRCOR) | https://www.companies.gov.cy | — | EL/EN | CY | — | Registro società cipriota |
| Czechia — Veřejný rejstřík (Justice.cz) | https://or.justice.cz | — | CS | CZ | — | Registro pubblico imprese ceco |
| Denmark — CVR (Virk) | https://datacvr.virk.dk | — | DA/EN | DK | — | Registro centrale imprese danese |
| Ecuador — Superintendencia de Compañías | https://www.supercias.gob.ec | — | ES | EC | — | Vigilanza e registro società ecuadoriano |
| Estonia — e-Business Register | https://ariregister.rik.ee | — | ET/EN | EE | — | Registro imprese estone |
| EU e-Justice — BRIS "Find a company" | https://e-justice.europa.eu/topics/registers-business-insolvency-land/business-registers-search-company-eu_en | — | Multi | EU+EEA | — | Interconnessione registri imprese UE |
| Finland — PRH / Virre | https://www.prh.fi | — | FI/EN | FI | — | Patent and Registration Office, registro imprese |
| France — Infogreffe | https://www.infogreffe.fr | — | FR | FR | — | Registro del commercio (RCS) |
| France — INPI Data (RNE) | https://data.inpi.fr | — | FR | FR | — | Registro nazionale imprese, open data |
| Georgia — NAPR | https://napr.gov.ge | — | KA/EN | GE | — | Registro pubblico georgiano |
| Germany — Handelsregister | https://www.handelsregister.de | — | DE | DE | — | Registro commerciale |
| Germany — Unternehmensregister | https://www.unternehmensregister.de/en | — | DE/EN | DE | — | Registro imprese federale |
| Ghana — Office of the Registrar of Companies | https://orc.gov.gh | — | EN | GH | — | Registro società ghanese |
| GLEIF — Legal Entity Identifier | https://www.gleif.org | — | EN | Globale | — | Database LEI globale |
| Greece — GEMI Business Portal | https://publicity.businessportal.gr | — | EL/EN | GR | — | Pubblicità registro imprese greco |
| Guatemala — Registro Mercantil | https://www.registromercantil.gob.gt | — | ES | GT | — | Registro mercantile guatemalteco |
| Hong Kong — Companies Registry | https://www.cr.gov.hk | — | EN/ZH | HK | — | ICRIS |
| Hungary — e-Cégjegyzék | https://www.e-cegjegyzek.hu | — | HU | HU | — | Registro società ungherese |
| India — MCA21 | https://www.mca.gov.in | — | EN | IN | — | Ministry of Corporate Affairs |
| Indonesia — AHU Online | https://ahu.go.id | — | ID | ID | — | Registro entità giuridiche (Min. Giustizia) |
| Ireland — CRO | https://www.cro.ie | — | EN | IE | — | Companies Registration Office |
| Japan — Hōjin Bangō (Corporate Number, NTA) | https://www.houjin-bangou.nta.go.jp | — | JA/EN | JP | — | Registro numeri societari giapponese |
| Kenya — Business Registration Service | https://brs.go.ke | — | EN | KE | — | Registro imprese keniota |
| Kompass | https://www.kompass.com | — | Multi | Globale | — | Directory B2B globale |
| Latvia — Uzņēmumu reģistrs | https://www.ur.gov.lv | — | LV/EN | LV | — | Registro imprese lettone |
| Lithuania — Registrų centras | https://www.registrucentras.lt | — | LT/EN | LT | — | Centro registri lituano |
| Luxembourg — LBR (RCS) | https://www.lbr.lu | — | FR/EN | LU | — | Registre de Commerce et des Sociétés |
| Malaysia — SSM | https://www.ssm.com.my | — | MS/EN | MY | — | Suruhanjaya Syarikat Malaysia |
| Malta — Malta Business Registry | https://mbr.mt | — | EN | MT | — | Registro imprese maltese |
| Mexico — SIGER / RPC | https://rpc.economia.gob.mx | — | ES | MX | — | Registro pubblico del commercio |
| Namibia — BIPA | https://www.bipa.na | — | EN | NA | — | Registro imprese e PI namibiano |
| Nepal — Office of Company Registrar | https://ocr.gov.np | — | NE/EN | NP | — | Registro società nepalese |
| Netherlands — KvK | https://www.kvk.nl | — | NL | NL | — | Camera di commercio/registro |
| New Zealand — Companies Office | https://companies-register.companiesoffice.govt.nz | — | EN | NZ | — | Registro società neozelandese |
| Nigeria — CAC Public Search | https://search.cac.gov.ng | — | EN | NG | — | Corporate Affairs Commission |
| North Data | https://www.northdata.com | — | EN/DE | Europa | — | Aggregatore dati societari DACH+ |
| Norway — Brønnøysundregistrene | https://www.brreg.no | — | NO/EN | NO | — | Registri nazionali norvegesi |
| Pakistan — SECP | https://www.secp.gov.pk | — | EN | PK | — | Securities & Exchange Commission Pakistan, registro società |
| Peru — SUNARP | https://www.sunarp.gob.pe | — | ES | PE | — | Sovrintendenza registri pubblici |
| Philippines — SEC Philippines | https://www.sec.gov.ph | — | EN | PH | — | Registro e regolatore societario |
| Poland — KRS (eKRS) | https://ekrs.ms.gov.pl | — | PL | PL | — | Registro giudiziario nazionale |
| Portugal — Publicações MJ | https://publicacoes.mj.pt | — | PT | PT | — | Pubblicazioni societarie obbligatorie |
| Qatar — MOCI | https://www.moci.gov.qa | — | AR/EN | QA | — | Ministero commercio, registro qatariota |
| Romania — ONRC | https://www.onrc.ro | — | RO | RO | — | Oficiul Național al Registrului Comerțului |
| Russia — EGRUL (FNS) | https://egrul.nalog.ru | — | RU | RU | — | Registro statale persone giuridiche |
| Rwanda — RDB Business Registration | https://rdb.rw | — | EN | RW | — | Registro imprese ruandese |
| Saudi Arabia — Ministry of Commerce | https://mc.gov.sa | — | AR/EN | SA | — | Registro commerciale saudita |
| Serbia — APR | https://www.apr.gov.rs | — | SR/EN | RS | — | Agenzia registri economici serba |
| Singapore — ACRA Bizfile | https://www.bizfile.gov.sg | — | EN | SG | — | Registro imprese |
| Slovakia — ORSR | https://www.orsr.sk | — | SK | SK | — | Registro commerciale slovacco |
| Slovenia — AJPES | https://www.ajpes.si | — | SL/EN | SI | — | Agenzia registri pubblici slovena |
| South Africa — CIPC | https://www.cipc.co.za | — | EN | ZA | — | Companies & IP Commission |
| Spain — Registradores | https://www.registradores.org | — | ES | ES | — | Registro Mercantil |
| Sweden — Bolagsverket | https://bolagsverket.se | — | SV/EN | SE | — | Ufficio registrazione società svedese |
| Switzerland — Zefix | https://www.zefix.ch | — | DE/FR/IT/EN | CH | — | Indice centrale ditte svizzero |
| Taiwan — FindBiz (MOEA) | https://findbiz.nat.gov.tw | — | ZH/EN | TW | — | Registro società taiwanese |
| Tanzania — BRELA | https://www.brela.go.tz | — | SW/EN | TZ | — | Registro imprese tanzaniano |
| Thailand — DBD | https://www.dbd.go.th | — | TH/EN | TH | — | Department of Business Development |
| Uganda — URSB | https://ursb.go.ug | — | EN | UG | — | Registro imprese ugandese |
| Ukraine — Unified State Register (USR) | https://usr.minjust.gov.ua | — | UK | UA | — | Registro statale unificato |
| US — Delaware Division of Corporations | https://icis.corp.delaware.gov | — | EN | US | — | Ricerca entità Delaware |
| US — SEC EDGAR (Company Search) | https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany | — | EN | US | — | Filing societari quotate |
| Vietnam — National Business Registration Portal | https://dangkykinhdoanh.gov.vn | — | VI/EN | VN | — | Portale registrazione imprese |
| Zambia — PACRA | https://www.pacra.org.zm | — | EN | ZM | — | Registro imprese zambiano |

### 3.4 Catasti & Registri Immobiliari (30)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ANCPI Romania | https://www.ancpi.ro | — | RO | RO | — | Catasto rumeno |
| BLM — Bureau of Land Management (USA) | https://www.blm.gov/programs/lands-and-realty | — | EN | US | — | Registro terreni pubblici federali USA |
| Cadastre Luxembourg | https://www.cadastre.lu | — | — | FR/LU/LU | — | Catasto ufficiale Lussemburgo |
| Cadastre.gouv.fr | https://www.cadastre.gouv.fr | — | FR | FR | — | Catasto francese |
| Canada Land Survey System | https://clss.nrcan.gc.ca | — | EN/FR | CA | — | Sistema catastale Canada — Natural Resources |
| Daeji Online (Korea) | https://www.eum.go.kr | — | KO | KR | — | Sistema informazioni catastali Corea del Sud |
| EuroGeographics | https://eurogeographics.org | — | EN | Europa | — | Rete catasti e cartografie nazionali |
| Geoportal.gov.pl | https://www.geoportal.gov.pl | — | PL | PL | — | Geoportale e catasto polacco |
| Geoportal.gov.sk | https://www.geoportal.sk | — | SK | SK | — | Portale geospaziale e catastale Slovacchia |
| GeoViewer Belgium (Geopunt) | https://www.geopunt.be | — | NL/FR | BE | — | Portale geospaziale e catasto Belgio |
| GUGiK — Land Registry Poland | https://www.gugik.gov.pl | — | PL | PL | — | Ufficio geodetico e cartografico Polonia |
| HM Land Registry | https://www.gov.uk/government/organisations/land-registry | — | EN | GB | — | Registro immobiliare Inghilterra/Galles |
| iGovSG — SLA Land Registry | https://www.sla.gov.sg | — | EN | SG | — | Singapore Land Authority — registro fondiario |
| Kadaster | https://www.kadaster.nl | — | NL/EN | NL | — | Catasto olandese |
| Kadastr.ru | https://kadastr.ru | — | RU | RU | — | Servizio federale catasto Russia (portale cittadino) |
| Kartverket | https://www.kartverket.no | — | NO/EN | NO | — | Catasto e cartografia norvegese |
| Land Portal | https://landportal.org | — | EN | Globale | — | Hub globale dati fondiari e accesso alla terra |
| Land Registry Ireland (PRAI) | https://www.prai.ie | — | EN | IE | — | Property Registration Authority Irlanda |
| Lantmäteriet | https://www.lantmateriet.se | — | SV/EN | SE | — | Catasto e cartografia svedese |
| LINZ — Land Information NZ | https://www.linz.govt.nz | — | EN | NZ | — | Catasto neozelandese |
| Maanmittauslaitos | https://www.maanmittauslaitos.fi | — | FI/EN | FI | — | Catasto finlandese |
| NSW Land Registry Services | https://www.nswlrs.com.au | — | EN | AU | — | Registro fondiario New South Wales Australia |
| Registers of Scotland | https://www.ros.gov.uk | — | EN | GB | — | Registro immobiliare scozzese |
| Rosreestr | https://rosreestr.gov.ru | — | RU | RU | — | Registro immobiliare russo |
| Sede Catastro | https://www.sedecatastro.gob.es | — | ES | ES | — | Catasto spagnolo |
| SNIG — Geoportal Portugal | https://snig.dgterritorio.gov.pt | — | PT | PT | — | Sistema nazionale informazione geografica Portogallo |
| Swisstopo — Cadastral Surveying | https://www.swisstopo.admin.ch/en/cadastral-surveying | — | EN/DE | CH | — | Catasto federale Svizzera |
| Tailte Éireann | https://www.tailte.ie | — | EN | IE | — | Catasto e registro immobiliare irlandese |
| TKGM — Land Registry Türkiye | https://www.tkgm.gov.tr | — | TR | TR | — | Catasto e registro fondiario Turchia |
| ČÚZK | https://cuzk.gov.cz | — | CS/EN | CZ | — | Catasto ceco |

## 4. ⚖️ Sanzioni, PEP & Compliance

### 4.1 AML, Sanzioni & PEP (61)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ACRC Korea | https://www.acrc.go.kr | — | KO/EN | KR | — | Anticorruzione e diritti civili coreana |
| AFA — Agence Française Anticorruption | https://www.agence-francaise-anticorruption.gouv.fr | — | FR | FR | — | Agenzia anticorruzione francese |
| AMLC Philippines | https://www.amlc.gov.ph | — | EN | PH | — | FIU filippina |
| AMLO Thailand | https://www.amlo.go.th | — | TH/EN | TH | — | FIU thailandese |
| ANI Romania | https://www.integritate.eu | — | RO/EN | RO | — | Agenzia nazionale integrità rumena |
| AUSTRAC | https://www.austrac.gov.au | — | EN | AU | — | FIU e regolatore AML australiano |
| Australia — DFAT Consolidated List | https://www.dfat.gov.au/international-relations/security/sanctions/consolidated-list | — | EN | AU | — | Sanzioni australiane |
| Basel Institute on Governance | https://baselgovernance.org | — | EN | Globale | — | Basel AML Index, asset recovery |
| Canada — Consolidated Autonomous Sanctions | https://www.international.gc.ca/world-monde/international_relations-relations_internationales/sanctions/consolidated-consolide.aspx | — | EN/FR | CA | — | Lista sanzioni canadese |
| Castellum.AI — Sanctions Search | https://www.castellum.ai/sanctions-list-search | — | EN | Globale | — | Aggregatore gratuito multi-lista |
| CBA Poland | https://www.cba.gov.pl | — | PL/EN | PL | — | Ufficio centrale anticorruzione polacco |
| CGU Brasil | https://www.gov.br/cgu | — | PT | BR | — | Controladoria-Geral da União |
| COAF | https://www.gov.br/coaf | — | PT | BR | — | FIU brasiliana |
| CPIB Singapore | https://www.cpib.gov.sg | — | EN | SG | — | Corrupt Practices Investigation Bureau |
| CTIF-CFI | https://www.ctif-cfi.be | — | FR/NL/EN | BE | — | FIU belga |
| CVC India | https://cvc.gov.in | — | EN/HI | IN | — | Central Vigilance Commission |
| EACC Kenya | https://eacc.go.ke | — | EN | KE | — | Ethics and Anti-Corruption Commission |
| EFCC Nigeria | https://www.efcc.gov.ng | — | EN | NG | — | Economic and Financial Crimes Commission |
| EPPO — European Public Prosecutor's Office | https://www.eppo.europa.eu | — | EN | EU | — | Procura europea |
| EU Sanctions Map | https://www.sanctionsmap.eu | — | EN | EU | — | Regimi sanzionatori UE per Paese |
| EU — Consolidated Financial Sanctions (FISMA) | https://finance.ec.europa.eu/eu-and-world/sanctions-restrictive-measures/overview-sanctions-and-related-resources_en | — | EN | EU | — | Lista consolidata asset freeze UE |
| FIC — Financial Intelligence Centre | https://www.fic.gov.za | — | EN | ZA | — | FIU sudafricana |
| FINTRAC | https://fintrac-canafe.canada.ca | — | EN/FR | CA | — | FIU canadese |
| FIU-IND | https://fiuindia.gov.in | — | EN | IN | — | FIU indiana |
| FIU-Nederland | https://www.fiu-nederland.nl | — | NL/EN | NL | — | FIU olandese |
| FRC Kenya | https://www.frc.go.ke | — | EN | KE | — | FIU keniota |
| GRECO — Group of States against Corruption | https://www.coe.int/en/web/greco | — | EN/FR | Europa | — | Monitoraggio anticorruzione Consiglio d'Europa |
| IACA — International Anti-Corruption Academy | https://www.iaca.int | — | EN | Globale | — | Accademia internazionale anticorruzione |
| ICAC Hong Kong | https://www.icac.org.hk | — | EN/ZH | HK | — | Independent Commission Against Corruption |
| INTERPOL — Notices (Red Notices) | https://www.interpol.int/How-we-work/Notices/View-Red-Notices | — | EN | Globale | — | Ricercati internazionali |
| JFIU Hong Kong | https://www.jfiu.gov.hk | — | EN/ZH | HK | — | FIU di Hong Kong |
| KNAB Latvia | https://www.knab.gov.lv | — | LV/EN | LV | — | Anticorruzione lettone |
| KoFIU | https://www.kofiu.go.kr | — | KO/EN | KR | — | FIU sudcoreana |
| KPK Indonesia | https://www.kpk.go.id | — | ID | ID | — | Commissione eradicazione corruzione |
| MACC Malaysia | https://www.sprm.gov.my | — | MS/EN | MY | — | Commissione anticorruzione malese |
| NAB Pakistan | https://nab.gov.pk | — | EN | PK | — | National Accountability Bureau |
| NABU Ukraine | https://nabu.gov.ua | — | UK/EN | UA | — | Ufficio nazionale anticorruzione ucraino |
| NACC Thailand | https://www.nacc.go.th | — | TH/EN | TH | — | Commissione anticorruzione thailandese |
| NFIU Nigeria | https://www.nfiu.gov.ng | — | EN | NG | — | FIU nigeriana |
| OFAC — Sanctions List Search | https://ofac.treasury.gov/sanctions-list-search-tool | — | EN | US | — | SDN + Consolidated List; ricerca fuzzy |
| OFAC — Sanctions List Service (download) | https://sanctionslist.ofac.treas.gov | — | EN | US | — | Dataset XML/CSV scaricabili |
| Office of the Ombudsman (Filippine) | https://www.ombudsman.gov.ph | — | EN | PH | — | Anticorruzione filippina |
| PPATK | https://www.ppatk.go.id | — | ID/EN | ID | — | FIU indonesiana |
| Rosfinmonitoring | https://www.fedsfm.ru | — | RU | RU | — | FIU russa |
| SEPBLAC | https://www.sepblac.es | — | ES/EN | ES | — | FIU spagnola |
| SFMS Ukraine | https://fiu.gov.ua | — | UK/EN | UA | — | FIU ucraina |
| SFO — Serious Fraud Office | https://www.sfo.gov.uk | — | EN | GB | — | Frodi gravi e corruzione UK |
| SIU South Africa | https://www.siu.org.za | — | EN | ZA | — | Special Investigating Unit |
| StAR — Stolen Asset Recovery Initiative | https://star.worldbank.org | — | EN | Globale | — | Recupero asset, Banca Mondiale/UNODC |
| STT Lithuania | https://www.stt.lt | — | LT/EN | LT | — | Servizio investigazioni speciali lituano |
| Switzerland — SECO Sanctions | https://www.seco.admin.ch/seco/en/home/Aussenwirtschaftspolitik_Wirtschaftliche_Zusammenarbeit/Wirtschaftsbeziehungen/exportkontrollen-und-sanktionen/sanktionen-embargos.html | — | EN/DE | CH | — | Sanzioni svizzere |
| TRACE International | https://www.traceinternational.org | — | EN | Globale | — | Anti-bribery compliance, TRACE Matrix |
| U4 Anti-Corruption Resource Centre | https://www.u4.no | — | EN | Globale | — | Ricerca anticorruzione, Bergen |
| UAF Chile | https://www.uaf.gob.cl | — | ES | CL | — | FIU cilena |
| UIF — Unità di Informazione Finanziaria (Italia) | https://uif.bancaditalia.it | — | IT | IT | — | FIU italiana, Banca d'Italia |
| UK OFSI — Consolidated List | https://www.gov.uk/government/publications/financial-sanctions-consolidated-list-of-targets | — | EN | GB | — | Asset freeze targets |
| UK Sanctions List (FCDO) | https://www.gov.uk/government/publications/the-uk-sanctions-list | — | EN | GB | — | Lista unica UK (dal 28/01/2026) |
| UN Security Council — Consolidated List | https://www.un.org/securitycouncil/content/un-sc-consolidated-list | — | EN | Globale | — | Lista consolidata Consiglio di Sicurezza |
| UN — Sanctions search (scsanctions) | https://scsanctions.un.org | — | EN | Globale | — | Ricerca/Download liste ONU |
| UNCAC Coalition | https://uncaccoalition.org | — | EN | Globale | — | Rete società civile convenzione ONU |
| World Bank — Debarred Firms | https://www.worldbank.org/en/projects-operations/procurement/debarred-firms | — | EN | Globale | — | Aziende escluse/sospese da appalti |


### 4.2 Crimine Organizzato & Traffici Illeciti (25)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ACAMS — AML Professionals | https://www.acams.org | — | EN | Globale | — | Associazione professionisti AML — risorse e standard |
| AMPI — AML Intelligence | https://www.amlintelligence.com | — | EN | Globale | — | Intelligence AML, sanzioni e crimine finanziario globale |
| Basel AML Index | https://index.baselgovernance.org | — | EN | Globale | — | Indice rischio riciclaggio per Paese — Basel Institute |
| C4ADS | https://c4ads.org | — | EN | Globale | — | Analisi reti criminali e traffici illeciti — approccio data-driven |
| ENACT Africa | https://enactafrica.org | — | EN | Africa | — | Ricerca criminalità organizzata in Africa subsahariana |
| Europol SOCTA | https://www.europol.europa.eu/publications-events/publications/socta-2021 | — | EN | EU | — | Serious & Organised Crime Threat Assessment UE, aggiornato ogni 4 anni |
| Financial Crime News | https://www.financialcrimenews.com | — | EN | Globale | — | News crimine finanziario, AML e sanzioni |
| FinTRACA — Financial Transactions Reporting (AF) | https://fintraca.gov.af | — | EN/FA | AF | — | Unità intelligence finanziaria Afghanistan |
| GITOC — Global Organized Crime Index | https://ocindex.net | — | EN | Globale | — | Indice globale crimine organizzato per paese (193 paesi) |
| Global Drug Policy Observatory | https://www.swansea.ac.uk/research/globaldrugpolicyobservatory | — | EN | Globale | — | Osservatorio politiche globali sulle droghe |
| Global Initiative Against Transnational Organized Crime | https://globalinitiative.net | — | EN | Globale | — | Think tank e rete globale su crimine organizzato transnazionale |
| ICCWC — Wildlife Crime | https://www.unodc.org/unodc/en/wildlife-crime/iccwc.html | — | EN | Globale | — | Consorzio contro crimini fauna selvatica — UNODC/Interpol |
| Interpol — Organized Crime | https://www.interpol.int/en/Crimes/Organised-Crime | — | EN | Globale | — | Portale INTERPOL criminalità organizzata transnazionale |
| Interpol — Tratta Esseri Umani | https://www.interpol.int/en/Crimes/Trafficking-in-human-beings | — | EN | Globale | — | INTERPOL tratta di esseri umani e smuggling |
| MENAFATF — FATF Middle East & North Africa | https://www.menafatf.org | — | AR/EN | MENA | — | Task force AML/CFT Medio Oriente e Nord Africa |
| OC-ACE | https://oc-ace.eu | — | EN | EU | — | Centro di eccellenza antimafia UE — network ricerca |
| OCCO — Organized Crime Corruption Observatory | https://occo.network | — | EN | Globale | — | Rete osservatori criminalità organizzata e corruzione |
| TRAC — Terrorism Research & Analysis Consortium | https://www.trackingterrorism.org | — | EN | Globale | — | Database terrorismo e gruppi estremisti |
| Transcrime | https://www.transcrime.it | — | IT/EN | IT | — | Ricerca su crimine organizzato, Università Cattolica Milano |
| UNODC World Drug Report | https://www.unodc.org/unodc/en/data-and-analysis/world-drug-report.html | — | EN | Globale | — | Report annuale ONU su produzione, traffico e uso di droghe |
| UNODC — Corruption | https://www.unodc.org/unodc/en/corruption/index.html | — | EN | Globale | — | Hub UNODC anticorruzione — dati, strumenti e rapporti |
| UNODC — CrimeStat | https://www.unodc.org/unodc/en/data-and-analysis/statistics.html | — | EN | Globale | — | Statistiche crimine UNODC — dati comparativi per Paese |
| UNODC — Drug Trafficking | https://www.unodc.org/unodc/en/drug-trafficking/index.html | — | EN | Globale | — | Traffico droghe e mercati illeciti UNODC |
| UNODC — Firearms Trafficking | https://www.unodc.org/unodc/en/firearms-protocol/firearms-trafficking.html | — | EN | Globale | — | Traffico armi da fuoco — UNODC Firearms Protocol |
| UNODC — Organized Crime | https://www.unodc.org/unodc/en/organized-crime/intro.html | — | EN | Globale | — | UNODC hub crimine organizzato e traffici illeciti |

## 5. 🔓 Open Data & Trasparenza

### 5.1 Portali Open Data & Database (196)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ACLED | https://acleddata.com | — | — | — | Pubblico | Conflitti armati — Freemium — Database |
| ADS-B Exchange | https://globe.adsbexchange.com | — | — | — | Pubblico | Voli militari — Voli in tempo reale — Database |
| ArcGIS Open Data | https://hub.arcgis.com/search | — | — | — | — | Freemium — Dati GIS |
| Arms Control Association | https://www.armscontrol.org | — | — | US | — | Controllo armi — USA |
| ART — Open Data Trasporti | https://bdt.autorita-trasporti.it/catalogo-opendata | — | IT | IT | — | Autorità Regolazione Trasporti: ferro, autostrade, mare — CC BY 4.0 |
| Arxiv | https://arxiv.org | — | — | — | — | Preprint accademici — Pubblico — Research — Accademia |
| Asia Times | https://asiatimes.com | — | — | Pan-Asia | — | Analisi |
| Banca Africana di Sviluppo | https://dataportal.opendataforafrica.org | — | — | — | — | Statistiche Africa da 50+ istituzioni — Gratuito — Portale ufficiale |
| Banca Asiatica di Sviluppo | https://data.adb.org | — | — | — | — | Sviluppo Asia e Pacifico — Gratuito — Portale ufficiale |
| Banca Mondiale Data360 | https://data360.worldbank.org | — | — | — | — | Nuova piattaforma curata BM con analisi tematiche — Gratuito — Portale ufficiale |
| Bertelsmann Transformation Index | https://bti-project.org | — | — | — | Database | Democrazia |
| bioRxiv | https://www.biorxiv.org | — | — | — | — | Bio pre-print — Accademia |
| Carabinieri | https://www.carabinieri.it | — | — | — | — | Polizia |
| Catalog.data.gov | https://catalog.data.gov | — | — | — | — | Gratuito — USA (catalogo) |
| CDC Data & Statistics | https://data.cdc.gov | — | — | — | — | Gratuito — Salute USA |
| CERN Open Data Portal | https://opendata.cern.ch | — | — | — | — | Dati esperimenti LHC (>3 petabyte) — Gratuito — Repository |
| CKAN | https://ckan.org | — | — | — | — | Piattaforma usata da data.gov, data.gov.uk, ecc. — Gratuito — Software/portale |
| Climate Watch | https://www.climatewatchdata.org | — | — | — | — | Gratuito — Clima e NDC |
| Clinical Trials Data | https://clinicaltrials.gov | — | — | — | Database | Dati studi clinici USA e internazionali — Gratuito |
| Consip — Dati Open | https://dati.consip.it | — | IT | IT | — | E-procurement PA, MePA — CKAN — IODL 2.0 |
| Copernicus Climate CDS | https://cds.climate.copernicus.eu | — | — | — | — | Gratuito — Clima EU |
| Copernicus Climate Change | https://climate.copernicus.eu | — | — | EU | — | Dati EU clima — Scienza |
| Copernicus CLMS | https://land.copernicus.eu | — | — | — | — | Gratuito — Copertura suolo EU |
| Copernicus EU | https://www.copernicus.eu | — | — | — | — | Osservazione terra EU — Pubblico — Satellite |
| Copernicus Data Space Ecosystem | https://dataspace.copernicus.eu | — | — | — | Pubblico | ESA immagini satellitari — portale ufficiale (sostituisce scihub, dismesso 11/2023) — Satellite |
| Corriere Adriatico | https://www.corriereadriatico.it | https://www.corriereadriatico.it/rss | — | IT-Marche | — | Ancona — Locale |
| COVIP — Open Data | https://www.covip.it | — | IT | IT | — | Vigilanza fondi pensione — IODL 2.0 |
| Dados.gov.br | https://dados.gov.br | — | — | BR | — | Gratuito |
| Data Commons | https://datacommons.org | — | — | — | — | Aggregatore dati pubblici da ONU, Banca Mondiale, governi — Gratuito |
| Data.europa.eu | https://data.europa.eu | — | — | EU | — | Open Data — Gratuito — Consolidamento EU Open Data Portal + European Data Portal |
| Data.go.jp | https://www.data.go.jp | — | — | JP | — | Gratuito |
| Data.go.kr | https://www.data.go.kr | — | — | KR | — | Gratuito |
| Data.gouv.fr | https://www.data.gouv.fr | — | — | FR | — | Gratuito |
| Data.gov (USA) | https://www.data.gov | — | — | — | — | USA — Open Data — Gratuito |
| Data.gov.au | https://www.data.gov.au | — | — | AU | — | Gratuito |
| Data.gov.in | https://data.gov.in | — | — | IN | — | Gratuito |
| Data.gov.ke | https://www.data.go.ke | — | — | KE | — | Gratuito |
| Data.gov.sg | https://data.gov.sg | — | — | SG | — | Gratuito |
| Data.gov.uk | https://www.data.gov.uk | — | UK | — | — | Gratuito |
| Data.govt.nz | https://www.data.govt.nz | — | — | NZ | — | Gratuito |
| Data.overheid.nl | https://data.overheid.nl | — | — | NL | — | Gratuito |
| DataHub.io | https://datahub.io | — | — | — | — | Dataset pubblicati e mantenuti da comunità globale — Gratuito — Repository |
| DataPortals.org | https://dataportals.org | — | — | — | — | Lista curata di 500+ portali open data nel mondo — Gratuito — Meta-portale |
| Datasette | https://datasette.io | — | — | — | Open Source | SQL+web — Tool |
| DatiGov | https://dati.gov.it | — | — | — | — | Open data governo — Italia — Gratuito — Portale ufficiale open data PA italiana |
| Datos.gob.es | https://datos.gob.es | — | — | ES | — | Gratuito |
| datos.gob.mx | https://datos.gob.mx | — | — | MX | — | Gratuito |
| DgStat — Min. Giustizia | https://datiestatistiche.giustizia.it | — | IT | IT | — | Statistiche giudiziarie civili/penali — Dati pubblici |
| DIA | https://diaweb.interno.gov.it | — | — | — | — | Antimafia |
| DPLA | https://dp.la | — | — | — | Pubblico | USA cultura digitale — Archivio |
| Dryad Digital Repository | https://datadryad.org | — | — | — | — | Dati sottostanti pubblicazioni scientifiche peer-reviewed — Freemium — Repository |
| Economic Times | https://economictimes.indiatimes.com | — | — | IN | — | Business — India |
| EIO | https://www.europol.europa.eu | — | — | — | — | Europol — Polizia |
| ENEA — Open Data | https://dati.enea.it | — | IT | IT | — | Energia e nuove tecnologie — CKAN |
| Enigma Public | https://enigma.com | — | — | — | Database | Dati governativi USA — Freemium |
| EU Commission | https://ec.europa.eu | — | — | — | — | Istituzione |
| EU CORDIS | https://cordis.europa.eu | — | — | — | Pubblico | Finanziamenti ricerca — Database |
| EU Council | https://www.consilium.europa.eu | — | — | — | — | Istituzione |
| EU Court of Auditors | https://www.eca.europa.eu | — | — | — | — | Controllo |
| EU Parliament | https://www.europarl.europa.eu | — | — | — | — | Istituzione |
| EU Whois | https://www.eurid.eu/en/whois | — | — | — | Database | Registro domini EU — Pubblico |
| EUDA — Agenzia UE Droghe | https://www.euda.europa.eu | — | EN | EU | — | Ex-EMCDDA: prevalenza, morti, sequestri droga — CC BY 4.0 — Database |
| Eurojust | https://www.eurojust.europa.eu | — | — | EU | — | Giustizia |
| Europeana | https://www.europeana.eu | — | — | — | Pubblico | Cultura europea — Archivio |
| Eurostat | https://ec.europa.eu/eurostat | — | — | — | Pubblico | UE statistiche — Database |
| Eurostat — Database | https://ec.europa.eu/eurostat/data/database | — | — | — | — | Statistiche ufficiali Unione Europea — Gratuito — Portale ufficiale |
| FAO – FAOSTAT | https://www.fao.org/faostat | — | — | — | — | Agricoltura, alimentazione, uso del suolo — Gratuito — Portale ufficiale |
| FBI Vault | https://vault.fbi.gov | — | — | — | Pubblico | Documenti FBI declassificati — Archivio |
| FEC (USA) | https://www.fec.gov | — | — | — | — | Elezioni USA — Regolatore |
| Figshare | https://figshare.com | — | — | — | — | Dataset, figure e output ricerca vari formati — Freemium — Repository |
| FIRMS NASA | https://firms.modaps.eosdis.nasa.gov | — | — | — | — | Incendi globali — Pubblico — Satellite |
| FlightAware | https://www.flightaware.com | — | — | — | Freemium | Voli — Database |
| FMI Data Portal | https://data.imf.org | — | — | — | — | Outlook economico globale, finanze pubbliche — Gratuito — Portale ufficiale |
| Forbidden Stories | https://forbiddenstories.org | — | — | Globale | — | Giornalisti minacciati |
| GADM | https://gadm.org | — | — | — | — | Gratuito — Confini amministrativi |
| Gapminder | https://www.gapminder.org | — | — | — | Pubblico | Sviluppo mondiale — Database |
| GBIF | https://www.gbif.org | — | — | — | — | Biodiversità globale: 2 miliardi+ occorrenze specie — Gratuito — Repository |
| GDELT Project | https://www.gdeltproject.org | — | — | — | Pubblico | News monitoring globale — Monitoraggio news — Database |
| GDPR Enforcement Tracker | https://www.enforcementtracker.com | — | — | — | Database | Sanzioni GDPR — Pubblico |
| GenBank (NCBI) | https://www.ncbi.nlm.nih.gov/genbank | — | — | — | — | Sequenze genetiche e genomiche — Gratuito — Repository |
| Geofabrik OSM Extracts | https://download.geofabrik.de | — | — | — | — | Gratuito — Dati OSM per area |
| GitHub | https://github.com | — | — | — | Freemium | Repository e script — Code Hosting |
| GitHub Innovation Graph | https://innovationgraph.github.com | — | EN | — | Pubblico | Sviluppo software per 215+ economie — CC0 — Database |
| Global Carbon Project | https://www.globalcarbonproject.org/carbonbudget | — | — | — | — | Gratuito — Emissioni CO2 |
| Global Open Data Index | https://index.okfn.org | — | — | — | — | Classifica apertura dati governi (Open Knowledge) — Gratuito — Ranking |
| Global Terrorism Database | https://www.start.umd.edu/gtd | — | — | — | Pubblico | Terrorismo globale — Terrorismo — Database |
| Global Voices | https://globalvoices.org | — | — | — | Pubblico | Media civici — Archivio |
| GNI (Google News Initiative) | https://newsinitiative.withgoogle.com | — | — | — | — | Google — Funding |
| GovData.de | https://www.govdata.de | — | — | DE | — | Gratuito |
| GovTrack | https://www.govtrack.us | — | — | — | — | Legislazione USA — Pubblico — Database |
| GRAIN | https://grain.org | — | — | — | — | Terra e cibo — ONG |
| Guardia di Finanza | https://www.gdf.gov.it | — | — | — | — | Finanziari — Polizia |
| Harvard Dataverse | https://dataverse.harvard.edu | — | — | — | — | Accademia — Gratuito — Dataset ricerca accademica (UH) |
| Hugging Face Spaces | https://huggingface.co/spaces | — | — | — | — | App AI demo — Freemium — Demo Hub |
| HuggingFace | https://huggingface.co | — | — | — | Freemium | Modelli open source — ML Hub |
| IATI d-Portal | https://d-portal.org | — | — | — | — | Aiuti internazionali da 100+ organizzazioni — Gratuito — Aggregatore |
| ICPSR | https://www.icpsr.umich.edu | — | — | — | — | Scienze sociali, sondaggi, dati storici USA — Freemium — Repository |
| IEEE Dataport | https://ieee-dataport.org | — | — | — | — | Dataset ingegneria e tecnologia — Freemium — Repository |
| IHME GHDx | https://ghdx.healthdata.org | — | — | — | — | Gratuito — Burden of Disease |
| IMF Data | https://www.imf.org/en/Data | — | — | — | Pubblico | Dati finanziari — Database |
| INAIL — Open Data | https://dati.inail.it | — | IT | IT | — | Infortuni e malattie professionali — IODL 2.0 |
| InfluenceWatch | https://www.influencewatch.org | — | — | — | Database | USA |
| INPS — Open Data | https://www.inps.it | — | IT | IT | — | Pensioni, CIG, contributi — IODL 2.0 |
| International Aid Transparency | https://iatistandard.org/en/iati-tools-and-resources | — | — | — | — | Standard trasparenza aiuti allo sviluppo — Gratuito |
| International Budget Partnership | https://internationalbudget.org | — | — | — | — | Bilanci — ONG — Bilanci pubblici — Gratuito |
| ISPRA Catasto Rifiuti | https://www.catasto-rifiuti.isprambiente.it | — | IT | IT | — | Catasto nazionale rifiuti urbani/speciali — banca dati ISPRA — Database |
| ISPRA IdroGEO | https://idrogeo.isprambiente.it | — | IT | IT | — | Dissesto idrogeologico: frane (IFFI), alluvioni (PIR) — CC BY 4.0 |
| iVision | https://ivision.com | — | — | — | Pubblico | Risorse |
| Journalists Toolbox | https://www.journaliststoolbox.org | — | — | — | Pubblico | Risorse per reporter — Risorse |
| Kaggle Datasets | https://www.kaggle.com/datasets | — | — | — | — | Dataset — Freemium — Oltre 50.000 dataset pubblici; community ML/AI |
| MapWarper | https://mapwarper.net | — | — | — | — | Geolocalizzazione storica — Pubblico — Tool |
| Marine Traffic | https://www.marinetraffic.com | — | — | — | Freemium | Navi AIS — Database |
| MediaCloud | https://mediacloud.org | — | — | — | Database | Analisi media news — Pubblico |
| Mendeley Data | https://data.mendeley.com | — | — | — | — | 20 milioni+ dataset indicizzati (Elsevier) — Gratuito — Repository |
| MIMIT — Prezzi Carburanti | https://www.mimit.gov.it | — | IT | IT | — | Prezzi carburanti praticati — IODL 2.0 |
| Min. Istruzione — Dati Scuola | https://dati.istruzione.it | — | IT | IT | — | Portale Unico Dati della Scuola — IODL 2.0 |
| Min. Lavoro — Open Data | https://dati.lavoro.gov.it | — | IT | IT | — | Rapporti di lavoro, tirocini — IODL 2.0 — in manutenzione (2026) |
| Min. Salute — Open Data | https://www.dati.salute.gov.it | — | IT | IT | — | Open data sanitari — IODL 2.0 |
| MIT — Open Data Trasporti | https://dati.mit.gov.it | — | IT | IT | — | Infrastrutture e trasporti — CKAN — IODL 2.0 |
| MUR / USTAT — Open Data | https://dati-ustat.mur.gov.it | — | IT | IT | — | Università e ricerca — CKAN — IODL 2.0 |
| NASA Open Data Portal | https://data.nasa.gov | — | — | — | — | Dati spaziali, astronomici, atmosferici NASA — Gratuito — Repository |
| Natural Earth | https://www.naturalearthdata.com | — | — | — | — | Gratuito — Mappe vettoriali |
| New Naratif | https://newnaratif.com | — | EN | — | — | Investigativo ASEAN — Sud-est asiatico |
| Nikkei Asia | https://asia.nikkei.com | — | EN | — | — | Business e politica asiatica — Giappone |
| NOAA Data | https://www.ncdc.noaa.gov/cdo-web | — | — | — | — | Dati climatici e oceanografici USA — Gratuito — Repository |
| NSA Document Archive | https://www.nsa.gov/news-features/declassified-documents | — | — | — | Pubblico | NSA declassificati — Archivio |
| Nuclear Threat Initiative | https://www.nti.org | — | — | US | — | Rischi nucleari — USA |
| OMS – Global Health Observatory | https://www.who.int/data/gho | — | — | — | — | Salute globale, malattie, mortalità, vaccinazioni — Gratuito — Portale ufficiale |
| Open Data Barometer | https://opendatabarometer.org | — | — | — | — | Valutazione readiness open data governi — Gratuito — Ranking |
| Open Data Inception | https://opendatainception.io | — | — | — | — | 2.600+ portali open data globali con mappa — Gratuito — Meta-portale |
| Open Data Network | https://www.opendatanetwork.com | — | — | — | — | Rete data.gov + città USA — Gratuito |
| Open Data Soft Explorer | https://data.opendatasoft.com/explore | — | — | — | — | Catalogo con 2.900+ dataset da portali locali — Gratuito |
| Open Government Partnership | https://www.opengovpartnership.org | — | — | — | — | Gov aperto — Org. — Gratuito — 75+ governi aderenti a standard open gov |
| Open Government Russia | https://data.gov.ru | — | — | RU | — | Gratuito |
| Open Sanctions | https://www.opensanctions.org | — | — | — | Database | Sanzioni e PEP — Pubblico |
| Open Science Framework (OSF) | https://osf.io | — | — | — | — | Gestione progetto + dati aperti; no-profit — Gratuito — Piattaforma |
| Open States | https://openstates.org | — | — | — | — | USA stati — Data |
| OpenAFRICA | https://africaopendata.org | — | — | Africa | — | Gratuito |
| OpenAIRE | https://explore.openaire.eu | — | — | — | — | Aggregatore ricerca europea aperta — Gratuito |
| OpenBudgets.eu | https://openbudgets.eu | — | — | — | — | Bilanci UE — Data — Gratuito — Bilanci pubblici europei |
| OpenContracting | https://www.open-contracting.org | — | — | — | Pubblico | Appalti globali — Database |
| OpenCorporates | https://opencorporates.com | — | — | — | Freemium | Registro aziende globale — Database |
| OpenData Hong Kong | https://data.gov.hk | — | — | HK | — | Gratuito |
| Opendata.swiss | https://opendata.swiss | — | — | CH | — | Gratuito |
| OpenDataSoft | https://public.opendatasoft.com | — | — | — | — | Globale — Open Data — Gratuito — Catalogo con 2.900+ dataset da portali globali |
| OpenFlights | https://openflights.org | — | — | — | Pubblico | Dati voli — Database |
| OpenFlights — Dati | https://openflights.org/data.html | — | — | — | — | Gratuito — Aviazione |
| OpenOil | https://openoil.net | — | — | — | Pubblico | Contratti petrolio — Database |
| OpenOwnership Register | https://register.openownership.org | — | — | — | Pubblico | Titolari effettivi — Database |
| OpenPNRR | https://openpnrr.it | — | IT | IT | — | Monitoraggio Piano Nazionale Ripresa e Resilienza — CC BY 4.0 |
| OpenSpending | https://openspending.org | — | — | — | Pubblico | Spesa pubblica globale — Database |
| OpenStreetMap | https://www.openstreetmap.org | — | — | — | — | Mappe open source — Pubblico — Mappe collaborative — Mappa |
| OSINT Combine | https://www.osintcombine.com | — | — | — | Pubblico | OSINT tools — Risorse |
| OSINT Techniques | https://www.osinttechniques.com | — | — | — | Pubblico | Blog OSINT — Risorse |
| Our World in Data | https://ourworldindata.org | — | — | Globale | — | Data visualization — Multi-tematico — Gratuito |
| Our World in Data – Health | https://ourworldindata.org/health-meta | — | — | — | — | Gratuito — Salute globale |
| PANGAEA | https://www.pangaea.de | — | — | — | — | Dati ambientali e geoscientifici — Gratuito — Repository |
| Parlamento Italiano | https://www.parlamento.it | — | — | — | — | Istituzione |
| Parlameter (UE) | https://parlameter.eu | — | — | — | — | Voti PE — Data |
| PressReader | https://www.pressreader.com | — | — | — | Freemium | Giornali globali — Archivio |
| Prison Policy Initiative | https://www.prisonpolicy.org | — | — | US | — | Carceri USA |
| Procura Nazionale Antimafia | https://www.dna.it | — | — | — | — | Magistratura |
| Public Intelligence | https://publicintelligence.net | — | — | — | Pubblico | Documenti governativi — Archivio |
| PubMed Central | https://www.ncbi.nlm.nih.gov/pmc | — | — | — | — | Articoli biomedici in open access — Gratuito — Repository |
| Re3data | https://www.re3data.org | — | — | — | — | Registro globale di 2.000+ repository di ricerca — Gratuito |
| Registry of Open Data on AWS | https://registry.opendata.aws | — | — | — | — | Dataset pubblici ospitati su Amazon Web Services — Gratuito — Registro |
| Sequence Read Archive (SRA) | https://www.ncbi.nlm.nih.gov/sra | — | — | — | — | Dati sequenziamento DNA/RNA — Gratuito — Repository |
| SNPA — Protezione Ambiente | https://www.snpambiente.it | — | IT | IT | — | Sistema Nazionale Protezione Ambiente (L.132/2016) — dati ambientali ufficiali |
| Socrata Open Data | https://dev.socrata.com/data | — | — | — | — | Portali città USA (Chicago, NYC, ecc.) — Gratuito — Piattaforma |
| SSRN | https://www.ssrn.com | — | — | — | — | Pre-print — Accademia |
| Technisette Toolkit | https://technisette.com/p/tools | — | — | — | Pubblico | OSINT tools — Risorse |
| TerraServer | https://www.terraserver.com | — | — | — | — | Immagini satellitari — Freemium — Satellite |
| The Diplomat | https://thediplomat.com | — | EN | — | — | Geopolitica asiatica — Asia-Pacifico |
| They Work For You | https://www.theyworkforyou.com | — | UK | — | — | Parlamento UK |
| Times of India | https://timesofindia.indiatimes.com | — | EN | — | — | India mass |
| Trace Labs | https://www.tracelabs.org | — | — | — | Pubblico | Missing persons — Risorse |
| Trace Labs OSINT VM | https://www.tracelabs.org/initiatives/osint-vm | — | — | — | Pubblico | VM |
| UN Comtrade | https://comtradeplus.un.org | — | — | — | Database | Dati commercio internazionale 130+ paesi — Gratuito/Reg. |
| UN Data | https://data.un.org | — | — | — | Pubblico | Statistiche ONU — 60 milioni di punti dati da agenzie ONU — Database |
| UN SDG Indicators (UNSD) | https://unstats.un.org/sdgs | — | EN | Globale | — | Indicatori Obiettivi Sviluppo Sostenibile — Accesso aperto — Database |
| UNECE — Statistiche Trasporti | https://w3.unece.org/PXWeb2015/pxweb/en/STAT/STAT__40-TRTRANS/ | — | EN | Globale | — | Commissione Economica ONU per l'Europa — Accesso aperto — Database |
| UNHCR | https://www.unhcr.org | — | — | Globale | — | Rifugiati |
| UniProt | https://www.uniprot.org | — | — | — | — | Database proteine e sequenze — Gratuito — Repository |
| UNODC Statistics | https://www.unodc.org/unodc/en/data-and-analysis | — | — | — | Database | Criminalità e droghe — Pubblico — Criminalità, droghe, traffici illeciti |
| Uppsala Conflict Data | https://ucdp.uu.se | — | — | — | Pubblico | Conflitti globali — Conflitti — Database |
| USGS EarthExplorer | https://earthexplorer.usgs.gov | — | — | — | — | Immagini satellitari e dati geografici USA — Gratuito — Repository |
| VoteView USA | https://voteview.com | — | — | — | — | Congresso USA — Data |
| VoteWatch Europe | https://www.votewatch.eu | — | — | — | Database | Voti PE |
| WHOIS Lookup | https://lookup.icann.org | — | — | — | Database | Info domini internet — Pubblico |
| Wikidata | https://www.wikidata.org | — | Multi | Globale | — | Base di conoscenza strutturata libera — pivot OSINT — CC0 — Database |
| World Bank Data | https://data.worldbank.org | — | — | — | Pubblico | Dati economici globali — Sviluppo globale, PIL, povertà, educazione — Database |
| World Justice Project | https://worldjusticeproject.org | — | — | — | — | Rule of law — Org. |
| World Open Data | https://worldopendata.com | — | — | — | — | 7.300+ indicatori da Banca Mondiale, FMI, OMS, FAO — Gratuito — Aggregatore |
| Zenodo | https://zenodo.org | — | — | — | — | CERN — Accademia — Gratuito — Repository CERN per dati e pubblicazioni scientifiche |
| Zero Day Initiative | https://www.zerodayinitiative.com | — | — | — | — | Trend Micro — Vulnerabilità |
| INFORM Risk Index | https://drmkc.jrc.ec.europa.eu/inform-index | — | EN | Globale | — | Indice rischio umanitario per paese (JRC-EU), aggiornamento annuale |


### 5.2 Gazzette Ufficiali & Legislazione (95)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Andorra — BOPA | https://www.bopa.ad | — | CA | AD | — | Bollettino ufficiale andorrano |
| Argentina — Boletín Oficial | https://www.boletinoficial.gob.ar | — | ES | AR | — | Gazzetta ufficiale argentina |
| Australia — Federal Register of Legislation | https://www.legislation.gov.au | — | EN | AU | — | Legislazione federale |
| Austria — RIS (Rechtsinformationssystem) | https://www.ris.bka.gv.at | — | DE | AT | — | Diritto federale e Bundesgesetzblatt |
| Belgium — Moniteur Belge / Belgisch Staatsblad | https://www.ejustice.just.fgov.be | — | FR/NL | BE | — | Gazzetta ufficiale belga |
| Bolivia — Gaceta Oficial | https://gacetaoficialdebolivia.gob.bo | — | ES | BO | — | Gazzetta ufficiale |
| Brazil — Diário Oficial da União | https://www.in.gov.br | — | PT | BR | — | Imprensa Nacional, DOU |
| Brunei — Attorney General's Chambers | https://www.agc.gov.bn | — | MS/EN | BN | — | Legislazione e gazzetta del Brunei |
| Bulgaria — Darzhaven Vestnik | https://dv.parliament.bg | — | BG | BG | — | Gazzetta ufficiale bulgara |
| Canada — Canada Gazette | https://gazette.gc.ca | — | EN/FR | CA | — | Gazzetta ufficiale canadese |
| Chile — Diario Oficial | https://www.diariooficial.interior.gob.cl | — | ES | CL | — | Gazzetta ufficiale cilena |
| Chile — LeyChile (BCN) | https://www.bcn.cl/leychile | — | ES | CL | — | Legislazione consolidata, Biblioteca del Congreso |
| China — Gov.cn Zhengce (政策) | https://www.gov.cn/zhengce | — | ZH | CN | — | Atti e politiche del Consiglio di Stato |
| Colombia — SUIN-Juriscol | https://www.suin-juriscol.gov.co | — | ES | CO | — | Sistema unico informazione normativa |
| Costa Rica — La Gaceta (Imprenta Nacional) | https://www.imprentanacional.go.cr | — | ES | CR | — | Gazzetta ufficiale costaricana |
| Croatia — Narodne novine | https://narodne-novine.nn.hr | — | HR | HR | — | Gazzetta ufficiale croata |
| Cuba — Gaceta Oficial | https://www.gacetaoficial.gob.cu | — | ES | CU | — | Gazzetta ufficiale cubana |
| Cyprus — CyLaw | http://www.cylaw.org | — | EL/EN | CY | — | Legislazione e giurisprudenza cipriota |
| Czechia — e-Sbírka (Sbírka zákonů) | https://www.e-sbirka.cz | — | CS | CZ | — | Raccolta leggi ceca (digitale dal 2024) |
| Denmark — Retsinformation | https://www.retsinformation.dk | — | DA | DK | — | Legislazione danese e Lovtidende |
| Ecuador — Registro Oficial | https://www.registroficial.gob.ec | — | ES | EC | — | Gazzetta ufficiale ecuadoriana |
| Estonia — Riigi Teataja | https://www.riigiteataja.ee | — | ET/EN | EE | — | Gazzetta ufficiale estone |
| EU — N-Lex (diritto nazionale) | https://n-lex.europa.eu | — | Multi | EU | — | Portale verso le gazzette nazionali UE |
| Finland — Finlex | https://www.finlex.fi | — | FI/SV | FI | — | Banca dati legislativa finlandese |
| France — Journal Officiel | https://www.journal-officiel.gouv.fr | — | FR | FR | — | Gazzetta ufficiale francese |
| France — Légifrance | https://www.legifrance.gouv.fr | — | FR | FR | — | Diritto francese |
| Gazettes.Africa | https://gazettes.africa | — | EN | Africa | — | Archivio gazzette ufficiali africane (Laws.Africa) |
| Germany — Bundesanzeiger | https://www.bundesanzeiger.de | — | DE | DE | — | Gazzetta federale |
| Germany — Gesetze im Internet | https://www.gesetze-im-internet.de | — | DE | DE | — | Leggi federali consolidate |
| GlobaLex (NYU) | https://www.nyulawglobal.org/globalex | — | EN | Globale | — | Guide ai sistemi legali nazionali |
| Greece — Ethniko Typografeio (ET/FEK) | https://www.et.gr | — | EL | GR | — | Gazzetta ufficiale greca |
| Guatemala — Diario de Centro América | https://dca.gob.gt | — | ES | GT | — | Gazzetta ufficiale guatemalteca |
| Hong Kong — eLegislation | https://www.elegislation.gov.hk | — | EN/ZH | HK | — | Legislazione consolidata HK |
| Hong Kong — Government Gazette | https://www.gld.gov.hk/egazette | — | EN/ZH | HK | — | Gazzetta ufficiale HK |
| Hungary — Magyar Közlöny | https://magyarkozlony.hu | — | HU | HU | — | Gazzetta ufficiale ungherese |
| India — eGazette | https://egazette.gov.in | — | EN/HI | IN | — | Gazette of India digitale |
| India — India Code | https://www.indiacode.nic.in | — | EN | IN | — | Legislazione centrale e statale |
| Indonesia — Peraturan.go.id (JDIH) | https://peraturan.go.id | — | ID | ID | — | Banca dati normativa nazionale |
| Ireland — Iris Oifigiúil | https://www.irisoifigiuil.ie | — | EN/GA | IE | — | Gazzetta ufficiale irlandese |
| Ireland — Irish Statute Book | https://www.irishstatutebook.ie | — | EN | IE | — | Legislazione consolidata irlandese |
| Israel — Reshumot (Gov.il) | https://www.gov.il/he/departments/dynamiccollectors/reshumot | — | HE | IL | — | Gazzetta ufficiale israeliana |
| Italy — Gazzetta Ufficiale | https://www.gazzettaufficiale.it | — | IT | IT | — | Gazzetta ufficiale italiana |
| Japan — e-Gov Laws (e-LAWS) | https://elaws.e-gov.go.jp | — | JA | JP | — | Legislazione giapponese consolidata |
| Japan — Kanpō (Gazzetta) | https://www.kanpou.npb.go.jp | — | JA | JP | — | Gazzetta ufficiale giapponese |
| Kenya — Kenya Law (Gazette & Laws) | https://kenyalaw.org | — | EN | KE | — | Kenya Gazette e legislazione |
| Latvia — Latvijas Vēstnesis | https://www.vestnesis.lv | — | LV | LV | — | Gazzetta ufficiale lettone |
| Latvia — Likumi.lv | https://likumi.lv | — | LV/EN | LV | — | Legislazione consolidata lettone |
| Laws.Africa | https://laws.africa | — | EN | Africa | — | Legislazione africana digitalizzata, open |
| Liechtenstein — Gesetze.li (LILEX) | https://www.gesetze.li | — | DE | LI | — | Legislazione del Liechtenstein |
| Lithuania — TAR (e-tar) | https://www.e-tar.lt | — | LT | LT | — | Registro atti giuridici lituano |
| Luxembourg — Legilux | https://legilux.public.lu | — | FR | LU | — | Journal officiel lussemburghese |
| Malaysia — Federal Legislation (LoM) | https://lom.agc.gov.my | — | MS/EN | MY | — | Leggi federali, Attorney General's Chambers |
| Malta — Legislation.mt | https://legislation.mt | — | MT/EN | MT | — | Leggi di Malta consolidate |
| Mexico — Diario Oficial de la Federación | https://www.dof.gob.mx | — | ES | MX | — | Gazzetta ufficiale messicana |
| Monaco — LégiMonaco | https://legimonaco.mc | — | FR | MC | — | Legislazione monegasca |
| Nepal — Law Commission | https://lawcommission.gov.np | — | NE/EN | NP | — | Legislazione nepalese consolidata |
| Netherlands — Officiële Bekendmakingen | https://www.officielebekendmakingen.nl | — | NL | NL | — | Pubblicazioni ufficiali |
| New Zealand — Legislation.govt.nz | https://www.legislation.govt.nz | — | EN | NZ | — | Legislazione neozelandese |
| New Zealand — NZ Gazette | https://gazette.govt.nz | — | EN | NZ | — | Gazzetta ufficiale neozelandese |
| Norway — Lovdata | https://lovdata.no | — | NO | NO | — | Legislazione e Norsk Lovtidend |
| Panama — Gaceta Oficial | https://www.gacetaoficial.gob.pa | — | ES | PA | — | Gazzetta ufficiale panamense |
| Peru — El Peruano (Normas Legales) | https://busquedas.elperuano.pe | — | ES | PE | — | Gazzetta ufficiale peruviana |
| Philippines — Official Gazette | https://www.officialgazette.gov.ph | — | EN | PH | — | Gazzetta ufficiale filippina |
| Poland — Dziennik Ustaw | https://dziennikustaw.gov.pl | — | PL | PL | — | Gazzetta ufficiale polacca |
| Poland — ISAP (Sejm) | https://isap.sejm.gov.pl | — | PL | PL | — | Sistema informativo atti giuridici |
| Portugal — Diário da República | https://diariodarepublica.pt | — | PT | PT | — | Gazzetta ufficiale portoghese |
| Qatar — Al-Meezan | https://www.almeezan.qa | — | AR/EN | QA | — | Portale legale del Qatar |
| Romania — Monitorul Oficial | https://monitoruloficial.ro | — | RO | RO | — | Gazzetta ufficiale rumena |
| Russia — Pravo.gov.ru | https://pravo.gov.ru | — | RU | RU | — | Portale ufficiale informazione giuridica |
| Saudi Arabia — Umm Al-Qura | https://www.uqn.gov.sa | — | AR | SA | — | Gazzetta ufficiale saudita |
| Serbia — Pravno-informacioni sistem | https://www.pravno-informacioni-sistem.rs | — | SR | RS | — | Službeni glasnik, legislazione serba |
| Singapore — eGazette | https://www.egazette.gov.sg | — | EN | SG | — | Gazzetta ufficiale di Singapore |
| Singapore — Statutes Online (SSO) | https://sso.agc.gov.sg | — | EN | SG | — | Legislazione consolidata |
| Slovakia — Slov-Lex | https://www.slov-lex.sk | — | SK | SK | — | Raccolta leggi slovacca |
| Slovenia — Uradni list | https://www.uradni-list.si | — | SL | SI | — | Gazzetta ufficiale slovena |
| South Africa — Government Gazette (GPW) | https://www.gpwonline.co.za | — | EN | ZA | — | Government Printing Works |
| South Korea — Korea Law (law.go.kr) | https://www.law.go.kr | — | KO | KR | — | Centro nazionale informazione giuridica |
| Spain — BOE | https://www.boe.es | — | ES | ES | — | Boletín Oficial del Estado |
| Sri Lanka — Government Documents (Gazette) | https://documents.gov.lk | — | SI/TA/EN | LK | — | Gazzetta ufficiale srilankese |
| Sweden — Svensk författningssamling | https://svenskforfattningssamling.se | — | SV | SE | — | Raccolta ufficiale leggi svedesi |
| Switzerland — Fedlex | https://www.fedlex.admin.ch | — | DE/FR/IT | CH | — | Raccolta diritto federale |
| Taiwan — Laws & Regulations DB (MOJ) | https://law.moj.gov.tw | — | ZH/EN | TW | — | Banca dati legislativa taiwanese |
| Thailand — Royal Thai Government Gazette | https://www.ratchakitcha.soc.go.th | — | TH | TH | — | Gazzetta ufficiale thailandese |
| Turkey — Resmî Gazete | https://www.resmigazete.gov.tr | — | TR | TR | — | Gazzetta ufficiale turca |
| UAE — UAE Legislation | https://uaelegislation.gov.ae | — | AR/EN | AE | — | Portale legislativo federale EAU |
| UK — Legislation.gov.uk | https://www.legislation.gov.uk | — | EN | GB | — | Legislazione UK |
| UK — The Gazette | https://www.thegazette.co.uk | — | EN | GB | — | Gazzetta ufficiale del Regno Unito |
| Ukraine — Zakon (Verkhovna Rada) | https://zakon.rada.gov.ua | — | UK | UA | — | Legislazione ucraina |
| Uruguay — IMPO | https://www.impo.com.uy | — | ES | UY | — | Diario Oficial e normativa uruguaiana |
| US — Congress.gov | https://www.congress.gov | — | EN | US | — | Legislazione federale |
| US — Federal Register | https://www.federalregister.gov | https://www.federalregister.gov/documents/current.rss | EN | US | — | Atti federali quotidiani |
| US — GovInfo (GPO) | https://www.govinfo.gov | — | EN | US | — | Documenti governativi ufficiali |
| Vietnam — Công Báo (Gazzetta) | https://congbao.chinhphu.vn | — | VI | VN | — | Gazzetta ufficiale vietnamita |
| WIPO Lex | https://www.wipo.int/wipolex | — | EN | Globale | — | Leggi PI e trattati di ~200 giurisdizioni |
| WorldLII | https://www.worldlii.org | — | EN | Globale | — | Aggregatore legislazione/giurisprudenza |

### 5.3 Istituzioni, Trasparenza & Open Government (50)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AgID Open Data | https://www.agid.gov.it/it/ambiti-intervento/open-data | — | — | — | — | Gratuito — Linee guida e politiche open data PA — Regolatore |
| ANAC Open Data | https://www.anticorruzione.it/-/open-data | — | — | — | Database | Gratuito — Appalti pubblici, trasparenza |
| AskTheEU | https://www.asktheeu.org | — | — | — | Pubblico | FOIA UE — Database |
| Banca d'Italia Statistics | https://infostat.bancaditalia.it | — | — | — | Database | Gratuito — Statistiche monetarie e finanziarie BdI |
| BDAP (Banca Dati AP) | https://bdap-opendata.rgs.mef.gov.it | — | — | — | Database | Gratuito — Bilanci enti locali e PA |
| Camera dei Deputati | https://www.camera.it | — | — | IT | — | Parlamento IT — Italia |
| CIA FOIA | https://www.cia.gov/library/readingroom | — | — | — | Pubblico | Documenti CIA declassificati — Archivio |
| Contract KFOR | https://contracts.osce.org | — | — | — | Pubblico | Appalti OSCE — Database |
| Copernicus Browser | https://browser.dataspace.copernicus.eu | — | — | — | — | Gratuito — Immagini satellitari ESA (nuovo portale 2024) — Satellite |
| Court of Justice EU | https://curia.europa.eu | — | — | EU | — | Giustizia UE |
| ECB Statistical Data Warehouse | https://sdw.ecb.europa.eu | — | — | — | Database | Gratuito — Statistiche monetarie e finanziarie BCE |
| EEA Data | https://www.eea.europa.eu/data-and-maps | — | — | — | — | Gratuito — Dati ambientali Agenzia Europea Ambiente — Portale |
| ENISA | https://www.enisa.europa.eu | — | — | — | — | Agenzia sicurezza UE — ENISA EU — CERT |
| EU CORDIS — Open Data | https://cordis.europa.eu/en/opendata | — | — | — | Database | Gratuito — Risultati ricerca finanziata UE dal 1990 |
| EU Integrity Watch | https://integritywatch.eu | — | — | — | Database | Gratuito — Pubblico — Conflitti interesse parlamento UE |
| EU TED (appalti) | https://ted.europa.eu | — | — | — | Pubblico | Appalti UE — Appalti pubblici europei — Database |
| Europa.eu Legislation | https://eur-lex.europa.eu | — | — | EU | — | Legislazione UE — Pubblico — Database |
| European Commission Press | https://ec.europa.eu/commission/presscorner | — | — | EU | — | Commissione UE |
| European Parliament News | https://www.europarl.europa.eu/news/en | — | — | EU | — | Parlamento UE |
| Europeana — Collezioni | https://www.europeana.eu/en/collections | — | — | — | — | Gratuito — Patrimonio culturale europeo digitale |
| FOI Directory UK | https://foi.directory | — | — | — | Pubblico | FOIA UK — Database |
| FOIA.gov (USA) | https://www.foia.gov | — | — | — | Pubblico | Richieste FOIA — Archivio |
| ISTAT Dati | https://dati.istat.it | — | — | — | Database | Gratuito — Statistiche ufficiali italiane — Open Data |
| ISTAT I.Stat | https://esploradati.istat.it | — | — | — | Database | Gratuito — Nuovo portale dati ISTAT (2024) |
| Little Sis | https://littlesis.org | — | — | — | Database | Network potere USA — Pubblico |
| Lobbyfacts EU | https://www.lobbyfacts.eu | — | — | — | Database | Gratuito — Pubblico — Trasparenza lobbisti UE |
| MANS Montenegro | https://www.mans.co.me | — | — | ME | — | Anti-corruzione — Montenegro |
| NUTS Geodata EU | https://ec.europa.eu/eurostat/web/gisco/geodata | — | — | — | — | Gratuito — Dati geospaziali unità statistiche europee — GIS |
| OLAF | https://anti-fraud.ec.europa.eu | — | — | EU | — | Antifrode UE |
| Open Data Comune di Milano | https://dati.comune.milano.it | — | — | — | — | Gratuito — Dataset Comune di Milano — Comunale |
| Open Data Comune di Roma | https://dati.comune.roma.it | — | — | — | — | Gratuito — Dataset Comune di Roma — Comunale |
| Open Data Comune di Torino | https://opendata.comune.torino.it | — | — | — | — | Gratuito — Dataset Comune di Torino — Comunale |
| Open Data Monitor EU | https://opendatamonitor.eu | — | — | — | — | Gratuito — Classifica apertura dati paesi europei — Aggregatore |
| Open Data Regione Lazio | https://dati.lazio.it | — | — | — | — | Gratuito — Dataset Regione Lazio — Regionale |
| Open Data Regione Lombardia | https://www.dati.lombardia.it | — | — | — | — | Gratuito — Dataset Regione Lombardia — Regionale |
| OpenCoesione | https://opencoesione.gov.it | — | — | — | Database | Gratuito — Fondi strutturali europei in Italia |
| OpenCUP | https://opencup.gov.it | — | — | — | Database | Gratuito — Codice Unico Progetto — investimenti pubblici |
| Portale Open Data MEF | https://www.rgs.mef.gov.it/VERSIONE-I/opendata | — | — | — | Database | Gratuito — Finanza pubblica, bilancio dello Stato |
| Portale Trasparenza PA | https://www.trasparenza.gov.it | — | — | — | — | Gratuito — Dati obbligatori trasparenza D.Lgs. 33/2013 |
| Registro Trasparenza UE | https://www.transparencyregister.eu | — | — | — | Pubblico | Lobby UE — Database |
| Senato della Repubblica | https://www.senato.it | — | — | IT | — | Senato IT — Italia |
| SIOPE – Finanza Locale | https://www.siope.it | — | — | — | Database | Gratuito — Incassi e pagamenti tesoreria enti pubblici |
| Sunlight Foundation | https://sunlightfoundation.com | — | — | — | — | Trasparenza governativa — Pubblico — Risorse — ONG |
| Transparency Intl. Italia | https://www.transparency.it | — | — | — | — | Anti-corruzione IT — Italia |
| Transparency IT | https://www.transparency.it/legge-anticorruzione | — | — | — | Pubblico | FOIA Italia — Archivio |
| WhatDoTheyKnow UK | https://www.whatdotheyknow.com | — | — | — | Pubblico | FOIA UK — Database |
| WTO Data | https://stats.wto.org | — | — | — | — | Commercio mondiale, tariffe, dispute — Gratuito — Portale ufficiale |

| Contracts Finder (UK) | https://www.contractsfinder.service.gov.uk | — | EN | GB | — | Portale appalti pubblici UK (contratti >£10.000) |
| EU Funding & Tenders Portal | https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/home | — | EN | EU | — | Bandi e opportunità di finanziamento UE, accesso a tutti i programmi |
| USASpending.gov | https://www.usaspending.gov | — | EN | US | — | Spesa federale USA: contratti, sussidi, prestiti — open data |

---

### 5.4 Parlamenti & Organi Elettorali (51)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Abgeordnetenwatch | https://www.abgeordnetenwatch.de | — | DE | DE | — | Monitoraggio eletti tedeschi |
| ACE Electoral Knowledge Network | https://aceproject.org | — | EN/Multi | Globale | — | Enciclopedia amministrazione elettorale |
| AEC — Australian Electoral Commission | https://www.aec.gov.au | — | EN | AU | — | Commissione elettorale australiana |
| Assemblée nationale | https://www.assemblee-nationale.fr | — | FR | FR | — | Camera bassa francese |
| Bundestag | https://www.bundestag.de | — | DE/EN | DE | — | Parlamento federale tedesco |
| CEC Ukraine | https://www.cvk.gov.ua | — | UK/EN | UA | — | Commissione elettorale centrale ucraina |
| COMELEC Philippines | https://comelec.gov.ph | — | EN | PH | — | Commissione elettorale filippina |
| Congreso de los Diputados | https://www.congreso.es | — | ES | ES | — | Camera bassa spagnola |
| Câmara dos Deputados | https://www.camara.leg.br | — | PT | BR | — | Camera bassa brasiliana, open data |
| ECI — Election Commission of India | https://www.eci.gov.in | — | EN/HI | IN | — | Commissione elettorale indiana |
| ECP Pakistan | https://www.ecp.gov.pk | — | EN | PK | — | Commissione elettorale pakistana |
| Eduskunta | https://www.eduskunta.fi | — | FI/SV/EN | FI | — | Parlamento finlandese |
| EISA | https://www.eisa.org | — | EN | Africa | — | Istituto elettorale per la democrazia sostenibile in Africa |
| ElectionGuide | https://www.electionguide.org | — | EN | Globale | — | Calendario elezioni mondiale (IFES) |
| Elections Canada | https://www.elections.ca | — | EN/FR | CA | — | Commissione elettorale canadese |
| Electoral Commission UK | https://www.electoralcommission.org.uk | — | EN | GB | — | Commissione elettorale britannica |
| Eligendo (Ministero Interno) | https://elezioni.interno.gov.it | — | IT | IT | — | Risultati elettorali italiani |
| Folketing | https://www.ft.dk | — | DA | DK | — | Parlamento danese |
| House of Representatives (Giappone) | https://www.shugiin.go.jp | — | JA/EN | JP | — | Camera bassa giapponese |
| IEBC Kenya | https://www.iebc.or.ke | — | EN | KE | — | Commissione elettorale keniota |
| IEC South Africa | https://www.elections.org.za | — | EN | ZA | — | Commissione elettorale sudafricana |
| IFES | https://www.ifes.org | — | EN | Globale | — | Fondazione internazionale sistemi elettorali |
| INE México | https://www.ine.mx | — | ES | MX | — | Instituto Nacional Electoral |
| INEC Nigeria | https://www.inecnigeria.org | — | EN | NG | — | Commissione elettorale nigeriana |
| International IDEA | https://www.idea.int | — | EN | Globale | — | Istituto democrazia e assistenza elettorale |
| IPU — Inter-Parliamentary Union (Parline) | https://www.ipu.org | — | EN/FR | Globale | — | Unione interparlamentare, database Parline |
| IRI — International Republican Institute | https://www.iri.org | — | EN | Globale | — | Sostegno processi democratici |
| Knesset | https://www.knesset.gov.il | — | HE/EN | IL | — | Parlamento israeliano |
| KPU Indonesia | https://www.kpu.go.id | — | ID | ID | — | Commissione elettorale indonesiana |
| NASS — National Assembly Nigeria | https://nass.gov.ng | — | EN | NG | — | Assemblea nazionale nigeriana |
| NDI — National Democratic Institute | https://www.ndi.org | — | EN | Globale | — | Sostegno processi democratici |
| New Zealand Parliament | https://www.parliament.nz | — | EN | NZ | — | Parlamento neozelandese |
| NPC — National People's Congress | https://www.npc.gov.cn | — | ZH/EN | CN | — | Assemblea nazionale del popolo cinese |
| Parliament of Australia | https://www.aph.gov.au | — | EN | AU | — | Parlamento australiano, Hansard |
| Parliament of Canada | https://www.parl.ca | — | EN/FR | CA | — | Parlamento canadese, LEGISinfo |
| Parliament of Kenya | https://www.parliament.go.ke | — | EN | KE | — | Parlamento keniota |
| Parliament of South Africa | https://www.parliament.gov.za | — | EN | ZA | — | Parlamento sudafricano |
| Registraduría Nacional (Colombia) | https://www.registraduria.gov.co | — | ES | CO | — | Organo elettorale colombiano |
| Riksdag | https://www.riksdagen.se | — | SV/EN | SE | — | Parlamento svedese |
| Sansad (Parlamento indiano) | https://sansad.in | — | EN/HI | IN | — | Portale digitale parlamento indiano |
| Sejm RP | https://www.sejm.gov.pl | — | PL/EN | PL | — | Camera bassa polacca |
| Senado Federal | https://www12.senado.leg.br | — | PT | BR | — | Senato brasiliano |
| Servel Chile | https://www.servel.cl | — | ES | CL | — | Servizio elettorale cileno |
| State Duma | https://www.duma.gov.ru | — | RU | RU | — | Camera bassa russa |
| Storting | https://www.stortinget.no | — | NO/EN | NO | — | Parlamento norvegese |
| Sénat (Francia) | https://www.senat.fr | — | FR | FR | — | Senato francese |
| The Carter Center | https://www.cartercenter.org | — | EN | Globale | — | Osservazione elettorale e democrazia |
| TSE Brasil | https://www.tse.jus.br | — | PT | BR | — | Tribunale superiore elettorale brasiliano |
| UK Parliament | https://www.parliament.uk | — | EN | GB | — | Parlamento britannico, Hansard |
| Venice Commission | https://venice.coe.int | — | EN/FR | Europa | — | Commissione di Venezia, diritto elettorale |
| Verkhovna Rada (portale) | https://www.rada.gov.ua | — | UK/EN | UA | — | Parlamento ucraino |

### 5.5 Open Data Subnazionale & Città (59)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AperTO — Torino | http://aperto.comune.torino.it | — | IT | IT | — | Open data Comune di Torino — HTTP (no HTTPS) |
| ARPAE Emilia-Romagna | https://dati.arpae.it | — | IT | IT | — | Open data ambiente/energia Emilia-Romagna — CKAN |
| California Open Data | https://data.ca.gov | — | EN | US | — | Open data Stato California |
| Chicago Data Portal | https://data.cityofchicago.org | — | EN | US | — | Open data Chicago |
| CM Napoli — Open Data | https://dati.cittametropolitana.na.it | — | IT | IT | — | Open data Città Metropolitana di Napoli — CKAN |
| Comune di Bari | https://opendata.comune.bari.it | — | IT | IT | — | Open data Comune di Bari — CKAN |
| Comune di Bologna | https://opendata.comune.bologna.it | — | IT | IT | — | Open data Comune di Bologna — OpenDataSoft |
| Comune di Cagliari | https://opendata.comune.cagliari.it | — | IT | IT | — | Open data Comune di Cagliari — CKAN |
| Comune di Catania | https://opendata.comune.catania.it | — | IT | IT | — | Open data Comune di Catania — CKAN |
| Comune di Ferrara | https://dati.comune.fe.it | — | IT | IT | — | Open data Comune di Ferrara — CKAN |
| Comune di Firenze | https://opendata.comune.fi.it | — | IT | IT | — | Open data Comune di Firenze — CC BY 4.0 |
| Comune di Genova | https://smart.comune.genova.it/opendata | — | IT | IT | — | Open data Comune di Genova |
| Comune di Livorno | https://opendata.comune.livorno.it | — | IT | IT | — | Open data Comune di Livorno — SIT — CC BY 4.0 |
| Comune di Messina | https://dati.comune.messina.it | — | IT | IT | — | Open data Comune di Messina — CKAN |
| Comune di Modena | https://opendata.comune.modena.it | — | IT | IT | — | Open data Comune di Modena — CKAN |
| Comune di Napoli | https://dati.comune.napoli.it | — | IT | IT | — | Open data Comune di Napoli — CKAN |
| Comune di Palermo | https://opendata.comune.palermo.it | — | IT | IT | — | Open data Comune di Palermo — CC BY 4.0 |
| Comune di Parma | https://opendata.comune.parma.it | — | IT | IT | — | Open data Comune di Parma — CC BY 4.0 |
| Comune di Reggio Emilia | https://opendata.comune.re.it | — | IT | IT | — | Open data Comune di Reggio Emilia — CKAN |
| Comune di Rimini | https://opendata.comune.rimini.it | — | IT | IT | — | Open data Comune di Rimini — CKAN |
| Data Amsterdam | https://data.amsterdam.nl | — | NL/EN | NL | — | Open data Amsterdam |
| Data LA | https://data.lacity.org | — | EN | US | — | Open data Los Angeles |
| Data NSW | https://data.nsw.gov.au | — | EN | AU | — | Open data New South Wales |
| DataSF | https://datasf.org | — | EN | US | — | Open data San Francisco |
| Daten Berlin | https://daten.berlin.de | — | DE | DE | — | Open data Berlino |
| Dati Emilia-Romagna | https://dati.emilia-romagna.it | — | IT | IT | — | Open data Regione Emilia-Romagna |
| Dati Piemonte | https://www.dati.piemonte.it | — | IT | IT | — | Open data Regione Piemonte |
| Dati Veneto | https://dati.veneto.it | — | IT | IT | — | Open data Regione Veneto |
| Datos Madrid | https://datos.madrid.es | — | ES | MX | — | Open data Madrid |
| Données Québec | https://www.donneesquebec.ca | — | FR | CA | — | Open data Québec |
| Eustat | https://www.eustat.eus | — | EU/ES/EN | ES | — | Istituto statistica Paesi Baschi |
| Idescat | https://www.idescat.cat | — | CA/ES/EN | ES | — | Istituto statistica Catalogna |
| Institut de la statistique du Québec | https://statistique.quebec.ca | — | FR/EN | CA | — | Statistica del Québec |
| London Datastore | https://data.london.gov.uk | — | EN | GB | — | Open data Greater London |
| Maggioli Cloud — Open Data EELL | https://www.opendata.maggioli.cloud | — | IT | IT | — | Open data enti locali — piattaforma Maggioli — CKAN |
| NISRA | https://www.nisra.gov.uk | — | EN | GB | — | Statistica Irlanda del Nord |
| NRS — National Records of Scotland | https://www.nrscotland.gov.uk | — | EN | GB | — | Statistiche e registri scozzesi |
| NY State Open Data | https://data.ny.gov | — | EN | US | — | Open data Stato New York |
| NYC Open Data | https://opendata.cityofnewyork.us | — | EN | US | — | Open data New York City |
| Ontario Data Catalogue | https://data.ontario.ca | — | EN/FR | CA | — | Open data Ontario |
| Open Data BCN | https://opendata-ajuntament.barcelona.cat | — | CA/ES/EN | ES | — | Open data Barcellona |
| Open Data Bolzano | https://data.civis.bz.it | — | IT/DE | IT | — | Open data Provincia Autonoma di Bolzano — CC0 / CC BY 4.0 |
| Open Toscana — Dati | https://dati.toscana.it | — | IT | IT | — | Open data Regione Toscana |
| Opendata Paris | https://opendata.paris.fr | — | FR | FR | — | Open data Ville de Paris |
| Regione Basilicata | https://dati.regione.basilicata.it | — | IT | IT | — | Open data Regione Basilicata — CKAN |
| Regione Calabria | https://dati.regione.calabria.it | — | IT | IT | — | Open data Regione Calabria — CKAN |
| Regione Campania | https://dati.regione.campania.it | — | IT | IT | — | Open data Regione Campania — CKAN |
| Regione Friuli Venezia Giulia | https://www.dati.friuliveneziagiulia.it | — | IT | IT | — | Open data Regione FVG — Socrata — IODL 2.0 |
| Regione Liguria | https://dati.regione.liguria.it | — | IT | IT | — | Open data Regione Liguria — CKAN |
| Regione Marche | https://dati.regione.marche.it | — | IT | IT | — | Open data Regione Marche — CC BY 4.0 |
| Regione Puglia | https://dati.puglia.it | — | IT | IT | — | Open data Regione Puglia — CC BY 4.0 |
| Regione Sicilia | https://dati.regione.sicilia.it | — | IT | IT | — | Open data Regione Sicilia — CKAN |
| Regione Umbria | https://dati.regione.umbria.it | — | IT | IT | — | Open data Regione Umbria — CKAN |
| Statistiek Vlaanderen | https://www.vlaanderen.be/statistiek-vlaanderen | — | NL | BE | — | Statistica fiamminga |
| Statistikportal (Länder) | https://www.statistikportal.de | — | DE | DE | — | Portale comune uffici statistici Länder |
| StatsWales | https://statswales.gov.wales | — | EN/CY | GB | — | Statistica gallese |
| Texas Open Data | https://data.texas.gov | — | EN | US | — | Open data Stato Texas |
| Tokyo Open Data | https://portal.data.metro.tokyo.lg.jp | — | JA | JP | — | Open data Metropoli di Tokyo |
| Trentino — Dati Aperti | https://dati.trentino.it | — | IT | IT | — | Open data Provincia Autonoma di Trento — CKAN — CC0 / CC BY 4.0 |

### 5.6 Esteri, Governi & Diplomazia (33)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Auswärtiges Amt | https://www.auswaertiges-amt.de | — | DE/EN | DE | — | Ministero esteri tedesco |
| BMEIA | https://www.bmeia.gv.at | — | DE/EN | AT | — | Esteri austriaco |
| Bundesregierung | https://www.bundesregierung.de | — | DE/EN | DE | — | Governo federale tedesco |
| Cancillería Argentina | https://www.cancilleria.gob.ar | — | ES | AR | — | Esteri argentino |
| Casa Rosada | https://www.casarosada.gob.ar | — | ES | AR | — | Presidenza argentina |
| DIRCO | https://www.dirco.gov.za | — | EN | ZA | — | Esteri sudafricano |
| Farnesina — Ministero degli Esteri | https://www.esteri.it | — | IT | IT | — | MAECI italiano |
| FDFA — Dipartimento federale affari esteri | https://www.eda.admin.ch | — | DE/FR/IT/EN | CH | — | Esteri svizzero |
| France Diplomatie | https://www.diplomatie.gouv.fr | — | FR/EN | FR | — | Quai d'Orsay |
| Kantei | https://www.kantei.go.jp | — | JA/EN | JP | — | Ufficio del primo ministro giapponese |
| Kemlu — MFA Indonesia | https://kemlu.go.id | — | ID/EN | ID | — | Esteri indonesiano |
| La Moncloa | https://www.lamoncloa.gob.es | — | ES | ES | — | Presidenza del governo spagnolo |
| MEA India | https://www.mea.gov.in | — | EN/HI | IN | — | Esteri indiano |
| MFA Greece | https://www.mfa.gr | — | EL/EN | GR | — | Esteri greco |
| MFA Kenya | https://mfa.go.ke | — | EN | KE | — | Esteri keniota |
| MFA Singapore | https://www.mfa.gov.sg | — | EN | SG | — | Esteri di Singapore |
| MFA Turkey | https://www.mfa.gov.tr | — | TR/EN | TR | — | Esteri turco |
| MFA Ukraine | https://mfa.gov.ua | — | UK/EN | UA | — | Esteri ucraino |
| MFAT New Zealand | https://www.mfat.govt.nz | — | EN | NZ | — | Esteri neozelandese |
| MID Russia | https://www.mid.ru | — | RU/EN | RU | — | Esteri russo |
| Ministerio de Asuntos Exteriores | https://www.exteriores.gob.es | — | ES | ES | — | Esteri spagnolo |
| MOFA China | https://www.fmprc.gov.cn | — | ZH/EN | CN | — | Esteri cinese, conferenze stampa |
| MOFA Japan | https://www.mofa.go.jp | — | JA/EN | JP | — | Esteri giapponese |
| MOFA Korea | https://www.mofa.go.kr | — | KO/EN | KR | — | Esteri sudcoreano |
| MOFA Saudi Arabia | https://www.mofa.gov.sa | — | AR/EN | SA | — | Esteri saudita |
| MOFA Taiwan | https://www.mofa.gov.tw | — | ZH/EN | TW | — | Esteri taiwanese |
| MoFA UAE | https://www.mofa.gov.ae | — | AR/EN | AE | — | Esteri emiratino |
| MOFA Vietnam | https://www.mofa.gov.vn | — | VI/EN | VN | — | Esteri vietnamita |
| PMO Australia | https://www.pm.gov.au | — | EN | AU | — | Primo ministro australiano |
| PMO Canada | https://www.pm.gc.ca | — | EN/FR | CA | — | Primo ministro canadese |
| PMO India | https://www.pmindia.gov.in | — | EN/HI | IN | — | Ufficio del primo ministro indiano |
| The Presidency (South Africa) | https://www.thepresidency.gov.za | — | EN | ZA | — | Presidenza sudafricana |
| Élysée | https://www.elysee.fr | — | FR | FR | — | Presidenza francese |

### 5.7 Corti dei Conti, Tesori & Vigilanza Pubblica (25)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Agence France Trésor | https://www.aft.gouv.fr | — | FR/EN | FR | — | Gestione debito francese |
| AGSA — Auditor-General South Africa | https://www.agsa.co.za | — | EN | ZA | — | Audit pubblico sudafricano |
| ANAO | https://www.anao.gov.au | — | EN | AU | — | Audit nazionale australiano |
| AOFM | https://www.aofm.gov.au | — | EN | AU | — | Gestione debito australiano |
| Belgian Debt Agency | https://www.debtagency.be | — | EN/FR/NL | BE | — | Gestione debito belga |
| Board of Audit of Japan | https://www.jbaudit.go.jp | — | JA/EN | JP | — | Corte dei conti giapponese |
| Bundesrechnungshof | https://www.bundesrechnungshof.de | — | DE | DE | — | Corte dei conti tedesca |
| CAG India | https://cag.gov.in | — | EN/HI | IN | — | Comptroller and Auditor General indiano |
| Cour des comptes | https://www.ccomptes.fr | — | FR | FR | — | Corte dei conti francese |
| Deutsche Finanzagentur | https://www.deutsche-finanzagentur.de | — | DE/EN | DE | — | Gestione debito tedesco |
| DSTA — Dutch State Treasury Agency | https://www.dsta.nl | — | NL/EN | NL | — | Gestione debito olandese |
| Défenseur des droits | https://www.defenseurdesdroits.fr | — | FR | FR | — | Difensore dei diritti francese |
| European Ombudsman | https://www.ombudsman.europa.eu | — | EN | EU | — | Mediatore europeo |
| INTOSAI | https://www.intosai.org | — | EN | Globale | — | Organizzazione istituzioni superiori di controllo |
| IOI — International Ombudsman Institute | https://www.theioi.org | — | EN | Globale | — | Rete difensori civici |
| ISSA — International Social Security Association | https://www.issa.int | — | EN | Globale | — | Sicurezza sociale comparata |
| MOF Japan | https://www.mof.go.jp | — | JA/EN | JP | — | Ministero finanze giapponese, JGB |
| NAIC | https://content.naic.org | — | EN | US | — | Associazione regolatori assicurativi statali |
| NAO — National Audit Office | https://www.nao.org.uk | — | EN | GB | — | Audit pubblico britannico |
| NTMA | https://www.ntma.ie | — | EN | IE | — | Gestione tesoro irlandese |
| OAG Canada | https://www.oag-bvg.gc.ca | — | EN/FR | CA | — | Auditor General canadese |
| Riksgälden | https://www.riksgalden.se | — | SV/EN | SE | — | Ufficio debito svedese |
| Tesoro Público | https://www.tesoro.es | — | ES | ES | — | Tesoro spagnolo, aste titoli |
| Tribunal de Cuentas | https://www.tcu.es | — | ES | ES | — | Corte dei conti spagnola |
| UK DMO — Debt Management Office | https://www.dmo.gov.uk | — | EN | GB | — | Gestione debito pubblico UK |

## 6. ✅ Fact-Checking & Disinformazione

### 6.1 Fact-Checking & Disinformazione (32)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AAP FactCheck | https://www.aap.com.au/factcheck | — | EN | — | — | Fact-checker — Australia (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Annie Lab | https://annielab.org | — | EN | — | — | Fact-checker — Hong Kong (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Check4Facts | https://check4facts.gr | — | EL | — | — | Fact-checker — Greece (rete IFCN/EFCSN/Duke) · verifica consigliata |
| China Fact Check | https://chinafactcheck.com | — | ZH | — | — | Fact-checker — China (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Demaskuok.lt | https://demaskuok.lt | — | LT | — | — | Fact-checker — Lithuania (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Dismislab | https://en.dismislab.com | — | BN | — | — | Fact-checker — Bangladesh (rete IFCN/EFCSN/Duke) · verifica consigliata |
| E-farsas | https://www.e-farsas.com | — | PT | — | — | Fact-checker — Brazil (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Ellinika Hoaxes | https://ellinikahoaxes.gr | — | EL | — | — | Fact-checker — Greece (rete IFCN/EFCSN/Duke) · verifica consigliata |
| EU DisinfoLab | https://www.disinfo.eu | — | EN | EU | — | Ricerca disinformazione e operazioni di influenza EU |
| Fact-Check Ghana (MFWA) | https://www.fact-checkghana.com | — | EN | — | — | Fact-checker — Ghana (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Factcheck Lab | https://www.factchecklab.org | — | ZH | — | — | Fact-checker — Hong Kong (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Factcheck.bg | https://factcheck.bg | — | BG | — | — | Fact-checker — Bulgaria (rete IFCN/EFCSN/Duke) · verifica consigliata |
| FactCheckHub (ICIR) | https://factcheckhub.com | — | EN | — | — | Fact-checker — Nigeria (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Factcrescendo | https://factcrescendo.com | — | EN | — | — | Fact-checker — India (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Factly | https://factly.in | — | EN | — | — | Fact-checker — India (rete IFCN/EFCSN/Duke) · verifica consigliata |
| FactSpace West Africa | https://factspace.org | — | EN | — | — | Fact-checker — Africa (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Factual.ro | https://www.factual.ro | — | RO | — | — | Fact-checker — Romania (rete IFCN/EFCSN/Duke) · verifica consigliata |
| FactWatch | https://www.fact-watch.org | — | BN | — | — | Fact-checker — Bangladesh (rete IFCN/EFCSN/Duke) · verifica consigliata |
| FakeNews.pl | https://fakenews.pl | — | PL | — | — | Fact-checker — Poland (rete IFCN/EFCSN/Duke) · verifica consigliata |
| GhanaFact | https://ghanafact.com | — | EN | — | — | Fact-checker — Ghana (rete IFCN/EFCSN/Duke) · verifica consigliata |
| HKBU Fact Check | https://factcheck.hkbu.edu.hk | — | ZH | — | — | Fact-checker — Hong Kong (rete IFCN/EFCSN/Duke) · verifica consigliata |
| IFCNdb — Poynter | https://ifcndatabase.poynter.org | — | EN | Globale | — | Database fact-checker accreditati IFCN — Poynter Institute |
| Jachai | https://www.jachai.org | — | BN | — | — | Fact-checker — Bangladesh (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Kompas Cek Fakta | https://cekfakta.kompas.com | — | ID | — | — | Fact-checker — Indonesia (rete IFCN) · verifica consigliata |
| News Verifier Africa | https://newsverifierafrica.com | — | EN | — | — | Fact-checker — Africa (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Observatorio de Datos UAI | https://observatoriodedatos.uai.cl | — | ES | — | — | Fact-checker — Chile (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Pravda.org.pl | https://pravda.org.pl | — | PL | — | — | Fact-checker — Poland (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Roundcheck | https://roundcheck.com.ng | — | EN | — | — | Fact-checker — Nigeria (rete IFCN/EFCSN/Duke) · verifica consigliata |
| Sawab (UNDP) | https://sawablb.com | — | AR | — | — | Fact-checker — Lebanon (rete IFCN/EFCSN/Duke) · verifica consigliata |
| THIP Media | https://thip.media | — | EN | — | — | Fact-checker — India (rete IFCN/EFCSN/Duke) · verifica consigliata |
| WaFact | https://www.wafact.sn | — | FR | — | — | Fact-checker — Senegal (rete IFCN) · verifica consigliata |
| YouTurn | https://youturn.in | — | TA | — | — | Fact-checker — India (rete IFCN/EFCSN/Duke) · verifica consigliata |

## 7. 🎓 Geopolitica & Intelligence

### 7.1 Geopolitica & Intelligence (154)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Access Now | https://www.accessnow.org | — | — | — | — | Diritti digitali — Globale — ONG |
| ACLU | https://www.aclu.org | — | — | — | — | Libertà civili USA — ONG |
| AEI — American Enterprise Institute | https://www.aei.org | — | EN | US | — | Think tank conservatore |
| Afrobarometer | https://www.afrobarometer.org | — | EN/FR | Africa | — | Sondaggi panafricani opinione pubblica |
| Al Jazeera Centre for Studies | https://studies.aljazeera.net | — | AR/EN | QA | — | Centro studi Al Jazeera |
| Amnesty International | https://www.amnesty.org | — | — | — | — | Diritti umani — Globale — ONG |
| Amnesty Italia | https://www.amnesty.it | — | — | — | — | Diritti umani |
| Article 19 | https://www.article19.org | — | UK | — | — | Libertà espressione — ONG |
| Asan Institute for Policy Studies | https://en.asaninst.org | — | KO/EN | KR | — | Think tank sudcoreano |
| Aspen Institute Italia | https://www.aspeninstitute.it | — | — | IT | — | Policy e leadership — Italia |
| ASPI — Australian Strategic Policy Institute | https://www.aspi.org.au | — | EN | AU | — | Strategia e difesa, Canberra |
| Atlantic Council | https://www.atlanticcouncil.org | — | EN | — | — | Geopolitica transatlantica — USA |
| BMJ | https://www.bmj.com | — | UK | — | — | Medica |
| Brookings Institution | https://www.brookings.edu | — | — | US | — | Policy e ricerca — USA |
| Bruegel | https://www.bruegel.org | — | — | BE | — | Economia europea — Belgio |
| Business & Human Rights | https://www.business-humanrights.org | — | — | — | Database | Corporate |
| CARI | https://cari.org.ar | — | ES | AR | — | Consejo Argentino para las Relaciones Internacionales |
| Carnegie Endowment | https://carnegieendowment.org | — | — | US | — | Policy internazionale — USA |
| Cato Institute | https://www.cato.org | — | — | US | — | Libertarismo — USA |
| CEBRI | https://cebri.org | — | PT/EN | BR | — | Centro Brasileiro de Relações Internacionais |
| Center for Human Rights Iran | https://iranhumanrights.org | — | HR | — | — | Iran |
| CEPR | https://cepr.org | — | UK | — | — | Economia e policy |
| CEPS | https://www.ceps.eu | — | EN | EU | — | Centre for European Policy Studies |
| CeSPI | https://www.cespi.it | — | — | IT | — | Cooperazione internazionale — Italia |
| CFR | https://www.cfr.org | — | EN | — | — | Relazioni internazionali — USA |
| Chatham House | https://www.chathamhouse.org | — | UK | — | — | Affari internazionali |
| CIDOB | https://www.cidob.org | — | ES/EN | ES | — | Barcelona Centre for International Affairs |
| Clingendael | https://www.clingendael.org | — | NL/EN | NL | — | Istituto olandese relazioni internazionali |
| CNAS | https://www.cnas.org | — | EN | US | — | Center for a New American Security |
| Committee to Protect Journalists | https://cpj.org | — | — | US | — | Sicurezza giornalisti — Globale |
| Conectas | https://www.conectas.org | — | — | — | — | Brasile — ONG |
| Corporate Accountability | https://www.corporateaccountability.org | — | — | — | — | USA — ONG |
| Crisis Group Alert | https://www.crisisgroup.org | https://www.crisisgroup.org/rss.xml | EN | — | — | Conflitti — Globale |
| CSIS | https://www.csis.org | — | — | US | — | Sicurezza e strategia — USA |
| CSIS Indonesia | https://www.csis.or.id | — | EN/ID | ID | — | Think tank indonesiano |
| DCAF — Geneva Centre | https://www.dcaf.ch | — | EN | CH | — | Governance settore sicurezza |
| Death Penalty Info | https://deathpenaltyinfo.org | — | — | US | — | Pena di morte — USA |
| Devex | https://www.devex.com | — | — | — | — | Aid/sviluppo — News |
| DGAP | https://dgap.org | — | DE/EN | DE | — | Consiglio tedesco relazioni estere |
| DIIS | https://www.diis.dk | — | DA/EN | DK | — | Istituto danese studi internazionali |
| Disability Rights International | https://www.driadvocacy.org | — | — | — | — | Disabilità — ONG |
| Earthrights International | https://earthrights.org | — | — | — | — | Ambiente-diritti — ONG |
| ECFR | https://ecfr.eu | — | — | EU | — | Politica estera europea |
| EFF | https://www.eff.org | — | — | — | — | Diritti digitali — USA — ONG |
| Egmont Institute | https://www.egmontinstitute.be | — | EN/FR | BE | — | Relazioni internazionali, Bruxelles |
| Equal Times | https://www.equaltimes.org | — | — | Globale | — | Lavoro e diritti |
| EUISS | https://www.iss.europa.eu | — | EN | EU | — | Istituto studi sicurezza UE |
| Eurobarometer | https://europa.eu/eurobarometer | — | — | EU | — | Dati opinione pubblica EU |
| FIDH | https://www.fidh.org | — | — | Globale | — | Federazione diritti umani |
| FIIA | https://www.fiia.fi | — | FI/EN | FI | — | Istituto finlandese affari internazionali |
| Freedom House | https://freedomhouse.org | — | — | US | — | Democrazia e libertà — USA |
| Freedom House Data | https://freedomhouse.org/reports/freedom-world | — | — | — | Pubblico | Democrazia — Database |
| Freedom of Press Foundation | https://freedom.press | — | — | — | — | SecureDrop — ONG |
| Friedrich Ebert Foundation | https://www.fes.de | — | — | DE | — | Socialdemocratico — Germania |
| Gallup | https://news.gallup.com | — | — | US | — | Sondaggi e ricerche — USA |
| GCSP | https://www.gcsp.ch | — | EN | CH | — | Geneva Centre for Security Policy |
| Geneva Solutions | https://genevasolutions.news | — | — | — | — | Genova umanitario — News |
| German Marshall Fund | https://www.gmfus.org | — | — | US/EU | — | Transatlantico — USA/EU |
| Global Corruption Barometer | https://www.transparency.org/en/gcb | — | — | — | Pubblico | Percezione corruzione — Database |
| Global Mental Health | https://www.globalmentalhealth.org | — | — | — | — | Accademia |
| Global Modern Slavery | https://www.globalmodernslavery.org | — | — | Globale | — | Schiavitù moderna |
| GLOBSEC | https://www.globsec.org | — | EN | SK | — | Sicurezza europea, Bratislava |
| Health Policy Watch | https://healthpolicy-watch.news | — | — | — | — | OMS — Policy |
| Heinrich Böll Foundation | https://www.boell.de | — | — | DE | — | Verde/progressista — Germania |
| Heritage Foundation | https://www.heritage.org | — | — | US | — | Policy conservatrice — USA |
| Hudson Institute | https://www.hudson.org | — | EN | US | — | Think tank conservatore |
| Human Rights Watch | https://www.hrw.org | — | — | — | — | Diritti umani — Globale — ONG |
| Human Rights Watch News | https://www.hrw.org/news | https://www.hrw.org/rss.xml | EN | — | — | Diritti |
| ifo Institute | https://www.ifo.de | — | DE/EN | DE | — | Ricerca economica, indice ifo |
| IFRI | https://www.ifri.org | — | — | FR | — | Relazioni internazionali — Francia |
| IISS | https://www.iiss.org | — | UK | — | — | Sicurezza internazionale |
| ILGA Europe | https://ilga-europe.org | — | — | — | — | LGBTQ+ UE — ONG |
| ILGA World | https://ilga.org | — | — | — | — | LGBTQ+ global — ONG |
| ILO | https://www.ilo.org | — | — | Globale | — | Lavoro — ONU |
| ILO News | https://www.ilo.org/news | — | — | Globale | — | Lavoro OIL |
| ILO – ILOSTAT | https://ilostat.ilo.org | — | — | — | — | Lavoro, occupazione, salari, condizioni lavorative — Gratuito — Portale ufficiale |
| Impunity Watch | https://www.impunitywatch.org | — | — | — | — | ONG |
| Index on Censorship | https://www.indexoncensorship.org | — | — | — | — | Censura — ONG |
| InfoMigrants | https://www.infomigrants.net | — | — | — | — | Multilingua — Servizio |
| INSS — Institute for National Security Studies | https://www.inss.org.il | — | HE/EN | IL | — | Studi sicurezza, Tel Aviv |
| Inter-American Dialogue | https://www.thedialogue.org | — | EN/ES | US | — | Think tank emisfero occidentale |
| IOM | https://www.iom.int | — | — | Globale | — | Migrazione |
| IPI Press Freedom | https://ipi.media | — | — | AT | — | Libertà stampa — Austria |
| IPSOS | https://www.ipsos.com/en | — | — | Globale | — | Sondaggi e insight |
| ISEAS — Yusof Ishak Institute | https://www.iseas.edu.sg | — | EN | SG | — | Studi Sud-Est asiatico |
| ISPI | https://www.ispi.it | — | — | IT | — | Geopolitica italiana — Italia |
| ISS Africa | https://issafrica.org | — | EN/FR | Africa | — | Institute for Security Studies |
| Istituto Affari Internazionali (IAI) | https://www.iai.it | — | — | IT | — | Relazioni internazionali IT — Italia |
| Iwacu Burundi | https://www.iwacu-burundi.org | https://www.iwacu-burundi.org/feed/ | — | BI | — | FR indip. — Burundi |
| JAMA | https://jamanetwork.com | — | — | — | — | USA — Medica |
| Jamestown Foundation | https://jamestown.org | — | — | US | — | Eurasia e sicurezza — USA |
| JIIA — Japan Institute of International Affairs | https://www.jiia.or.jp | — | JA/EN | JP | — | Think tank giapponese |
| Just Security | https://www.justsecurity.org | — | EN | — | — | Diritto sicurezza — USA |
| Kiel Institute (IfW) | https://www.ifw-kiel.de | — | DE/EN | DE | — | Economia mondiale; Ukraine Support Tracker |
| Konrad Adenauer Foundation | https://www.kas.de | — | — | DE | — | Cristiano-democratico — Germania |
| La Strada International | https://lastradainternational.org | — | — | Europa | — | Traffico umano |
| Lancet | https://www.thelancet.com | — | UK | — | — | Medica |
| Lawfare | https://www.lawfaremedia.org | — | EN | — | — | Diritto e sicurezza — USA |
| Lowy Institute | https://www.lowyinstitute.org | — | — | AU | — | Asia-Pacifico — Australia |
| MEI — Middle East Institute | https://www.mei.edu | — | EN | US | — | Studi mediorientali, Washington |
| Mental Health America | https://www.mhanational.org | — | — | — | — | USA salute mentale — ONG |
| Missing Migrants Project | https://missingmigrants.iom.int | — | — | — | Database | IOM |
| Mixed Migration Centre | https://mixedmigration.org | — | — | Globale | — | Migrazione mista |
| MP-IDSA | https://www.idsa.in | — | EN | IN | — | Studi difesa e sicurezza, Delhi |
| MSF | https://www.msf.org | — | — | — | — | Medici — ONG |
| NEJM | https://www.nejm.org | — | — | — | — | USA — Medica |
| Notre Europe | https://institutdelors.eu | — | — | FR | — | Integrazione europea — Francia/UE |
| NUPI | https://www.nupi.no | — | NO/EN | NO | — | Istituto norvegese affari internazionali |
| OHCHR | https://www.ohchr.org | — | — | — | — | ONU diritti umani — Globale — ONG/ONU |
| OHCHR LGBTI | https://www.ohchr.org/en/sexual-orientation-and-gender-identity | — | — | Globale | — | ONU |
| ORF — Observer Research Foundation | https://www.orfonline.org | — | EN | IN | — | Think tank indiano principale |
| OSW — Centre for Eastern Studies | https://www.osw.waw.pl | — | PL/EN | PL | — | Studi su Russia ed Est Europa |
| OutRight Action | https://outrightinternational.org | — | — | — | — | LGBTQ+ — ONG |
| Peterson Institute | https://www.piie.com | — | — | US | — | Economia internazionale — USA |
| Pew Research | https://www.pewresearch.org | — | — | US | — | Dati sociali — USA |
| Pew Research Journalism | https://www.pewresearch.org/journalism | — | — | — | — | Ricerca |
| PICUM | https://picum.org | — | — | — | — | UE migrazioni — ONG |
| PISM | https://www.pism.pl | — | PL/EN | PL | — | Istituto polacco affari internazionali |
| Privacy International | https://privacyinternational.org | — | UK | — | — | Privacy — ONG |
| Quincy Institute | https://quincyinst.org | — | EN | US | — | Realismo e moderazione strategica |
| RAND Australia | https://www.rand.org/australia | — | — | AU | — | Australia |
| RAND Corporation | https://www.rand.org | — | — | US | — | Ricerca e analisi — USA |
| RAND Europe | https://www.rand.org/randeurope | — | — | Europa | — |  |
| RAND Terrorism Incidents | https://www.rand.org/nsrd/projects/terrorism-incidents.html | — | — | — | Pubblico | Database |
| Razumkov Centre | https://razumkov.org.ua | — | UK/EN | UA | — | Think tank ucraino |
| Real Instituto Elcano | https://www.realinstitutoelcano.org | — | ES/EN | ES | — | Think tank spagnolo |
| Reporters Without Borders | https://rsf.org | — | — | Globale | — | Libertà di stampa |
| RSIS | https://www.rsis.edu.sg | — | EN | SG | — | Studi strategici NTU Singapore |
| RUSI | https://rusi.org | — | UK | — | — | Difesa e sicurezza |
| SAIIA | https://saiia.org.za | — | EN | ZA | — | Affari internazionali sudafricani |
| SIPRI | https://www.sipri.org | — | — | SE | — | Pace e armamenti — Svezia |
| SIPRI Military | https://www.sipri.org/databases | — | — | — | Pubblico | Spesa militare — Spese militari, armamenti, peacekeeping — Database |
| STAT News | https://www.statnews.com | — | — | — | — | USA — Salute |
| Statewatch | https://www.statewatch.org | — | — | — | — | UE securitizzazione — Monitor |
| Stockholm Intl. Peace (SIPRI DB) | https://www.sipri.org/databases/armstransfers | — | — | — | Pubblico | Trasferimenti armi — Database |
| Stratfor | https://worldview.stratfor.com | — | — | US | — | Intelligence geopolitica — USA |
| SWP Berlin | https://www.swp-berlin.org | — | — | DE | — | Policy tedesca ed EU — Germania |
| The Interpreter (Lowy) | https://www.lowyinstitute.org/the-interpreter | — | — | AU | — | Policy — Australia |
| The New Humanitarian | https://www.thenewhumanitarian.org | — | — | — | — | Umanitario — News |
| The Washington Institute | https://www.washingtoninstitute.org | — | EN | US | — | Politica USA in Medio Oriente |
| Transparency International | https://www.transparency.org | — | — | — | Pubblico | Anti-corruzione — Globale — Database |
| Trial International | https://trialinternational.org | — | — | — | — | ONG |
| UI — Swedish Institute of International Affairs | https://www.ui.se | — | SV/EN | SE | — | Istituto svedese affari internazionali |
| UN News Centre | https://news.un.org | https://news.un.org/feed/subscribe/en/news/all/rss.xml | EN | — | — | ONU |
| UNDP – Human Development Data | https://hdr.undp.org/data-center | — | — | — | — | Indice di Sviluppo Umano (HDI) — Gratuito — Portale ufficiale |
| UNICEF | https://www.unicef.org | — | — | Globale | — | Bambini — ONU |
| UNICEF Data | https://data.unicef.org | — | — | — | — | Infanzia: nutrizione, salute, istruzione, protezione — Gratuito — Portale ufficiale |
| Urban Institute | https://www.urban.org | — | — | US | — | Policy urbana e sociale — USA |
| V-Dem | https://www.v-dem.net | — | — | SE | — | Democrazia dati — Svezia |
| V-Dem Dataset | https://www.v-dem.net/data | — | — | — | Pubblico | Democrazia — Dataset |
| VoxEU | https://cepr.org/voxeu | — | UK | — | — | Economia ricerca — Europa |
| WHO | https://www.who.int | — | — | Globale | — | Salute — ONU |
| Wilson Center | https://www.wilsoncenter.org | — | — | US | — | Policy internazionale — USA |
| Witness | https://witness.org | — | — | — | — | Diritti umani video — USA — ONG |

## 8. 🕊️ Diritti Umani & Giudiziario

### 8.1 Diritti Umani & Giudiziario (35)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ACAPS | https://www.acaps.org | — | EN | Globale | — | Analisi crisi umanitarie |
| ACNUR España | https://www.acnur.org | — | ES | Globale | — | Portale spagnolo UNHCR — rifugiati e protezione |
| African Court on Human & Peoples' Rights | https://www.african-court.org | — | EN/FR | Africa | — | Corte africana diritti umani |
| Anti-Slavery International | https://www.antislavery.org | — | EN | Globale | — | Schiavitù moderna, la più antica NGO |
| CIPESA | https://cipesa.org | — | EN | Africa | — | Policy ICT e diritti digitali Africa |
| CIVICUS | https://www.civicus.org | — | EN | Globale | — | Monitor spazio civico mondiale |
| Counter Trafficking Data Collaborative | https://www.ctdatacollaborative.org | — | EN | Globale | — | Dataset globale tratta di esseri umani |
| ECCC — Cambodia Tribunal | https://www.eccc.gov.kh | — | EN/KH | KH | — | Camere straordinarie Cambogia |
| ECHR — HUDOC | https://hudoc.echr.coe.int | — | EN/FR | Europa | — | Giurisprudenza Corte EDU |
| ECHR — sito ufficiale | https://www.echr.coe.int | — | EN/FR | Europa | — | Corte europea diritti dell'uomo |
| EUAA — European Union Agency for Asylum | https://euaa.europa.eu | — | EN | EU | — | Agenzia UE per l'asilo — statistiche e report |
| Free Press Unlimited | https://www.freepressunlimited.org | — | EN/NL | Globale | — | Sostegno media indipendenti |
| Global Detention Project | https://www.globaldetentionproject.org | — | EN | Globale | — | Database detenzione migranti e richiedenti asilo |
| Harvard Humanitarian Initiative | https://hhi.harvard.edu | — | EN | Globale | — | Ricerca Harvard su crisi umanitarie e diritti |
| ICC — International Criminal Court | https://www.icc-cpi.int | — | EN/FR | Globale | — | Corte penale internazionale |
| ICC — Legal Tools Database | https://www.legal-tools.org | — | EN | Globale | — | Documenti diritto penale internazionale |
| ICJ — International Court of Justice | https://www.icj-cij.org | — | EN/FR | Globale | — | Corte internazionale di giustizia (ONU) |
| IJM — International Justice Mission | https://www.ijm.org | — | EN | Globale | — | Organizzazione giustizia contro schiavitù e traffico |
| Inter-American Commission HR (OAS) | https://www.oas.org/en/iachr | — | EN/ES | Americhe | — | Commissione interamericana |
| Inter-American Court of HR | https://www.corteidh.or.cr | — | ES/EN | Americhe | — | Corte interamericana diritti umani |
| Internews | https://internews.org | — | EN | Globale | — | Sviluppo media e informazione |
| IREX | https://www.irex.org | — | EN | Globale | — | Media sustainability, VIBE index |
| IRMCT — Residual Mechanism (ICTY/ICTR) | https://www.irmct.org | — | EN/FR | Globale | — | Meccanismo residuale tribunali ONU |
| IWGIA | https://www.iwgia.org | — | EN | Globale | — | Gruppo lavoro internazionale popoli indigeni |
| MFWA — Media Foundation for West Africa | https://www.mfwa.org | — | EN/FR | Africa Occ. | — | Libertà di stampa Africa occidentale |
| Minority Rights Group | https://minorityrights.org | — | EN | Globale | — | Minoranze e popoli indigeni, directory |
| OHCHR — Jurisprudence (Juris) | https://juris.ohchr.org | — | EN | Globale | — | Decisioni organi trattato ONU |
| Pew-Templeton Global Religious Futures | https://www.globalreligiousfutures.org | — | EN | Globale | — | Dati religione per Paese |
| Refugee Legal Aid Information | https://refugeelegalaidinformation.org | — | EN | Globale | — | Assistenza legale rifugiati per Paese |
| RSCSL — Sierra Leone | http://www.rscsl.org | — | EN | SL_C | — | Corte speciale residuale |
| Survival International | https://www.survivalinternational.org | — | EN/Multi | Globale | — | Popoli indigeni |
| Tactical Tech | https://tacticaltech.org | — | EN | Globale | — | Tecnologia e società civile |
| Walk Free | https://www.walkfree.org | — | EN | Globale | — | Global Slavery Index |
| WCC — World Council of Churches | https://www.oikoumene.org | — | EN | Globale | — | Consiglio ecumenico delle chiese |
| World Prison Brief | https://www.prisonstudies.org | — | EN | Globale | — | Database comparativo penitenziario globale (ICPR, Birkbeck) |

## 9. 🔐 Cybersecurity & Digital OSINT

### 9.1 Threat Intelligence & Cybersecurity (67)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AFRINIC | https://www.afrinic.net | — | EN/FR | Africa | — | Registro IP africano |
| APNIC | https://www.apnic.net | — | EN | Asia-Pacifico | — | Registro IP Asia-Pacifico, ricerca |
| ARIN | https://www.arin.net | — | EN | Nord America | — | Registro IP nordamericano |
| Ars Technica Security | https://arstechnica.com | — | EN | — | — | Tech generale — Security news |
| Avgi Greece | https://www.avgi.gr | — | — | GR | — | SYRIZA — Grecia |
| BleepingComputer | https://www.bleepingcomputer.com | — | — | — | — | Aggiornamenti rapidi — Malware, ransomware — News |
| CCCS Canada | https://cyber.gc.ca | — | — | — | — | Canada — CERT |
| CERT-AGID (IT) | https://www.cert-agid.gov.it | — | — | — | — | Alert ufficiali IT — CERT italiano |
| CERT-EU | https://cert.europa.eu | — | — | EU | — | Alert ufficiali UE — CERT europeo — CERT |
| Cloudflare Radar | https://radar.cloudflare.com | — | EN | Globale | — | Traffico internet, outage, attacchi |
| CrowdStrike Blog | https://www.crowdstrike.com/blog | — | — | — | — | CrowdStrike — Threat intel |
| Cybereason | https://www.cybereason.com/blog | — | — | — | — | EDR vendor — Threat research |
| CyberScoop | https://www.cyberscoop.com | — | — | — | — | Policy e news — Cybersecurity policy |
| Cybersecurity Dive | https://www.cybersecuritydive.com | — | — | — | — | Industry Dive — News |
| Cybersecurity360 | https://www.cybersecurity360.it | https://www.cybersecurity360.it/feed/ | — | — | Online | Cyber IT |
| Cyberwire | https://thecyberwire.com | — | — | — | — | Podcast/News |
| Dark Net Diaries (podcast) | https://darknetdiaries.com | — | — | — | — | Security podcast — Podcast |
| Dark Reading | https://www.darkreading.com | — | — | — | Enterprise | Professionale — Enterprise security |
| Defensive Security | https://defensivesecurity.org | — | — | — | — | Podcast |
| Digital Shadows | https://www.digitalshadows.com/blog-and-research | — | — | — | — | Threat intel |
| ESET Research | https://www.welivesecurity.com | — | — | — | — | ESET — Malware research |
| F-Secure Blog | https://blog.f-secure.com | — | — | — | — | WithSecure — Threat intel — Research |
| Google Project Zero | https://googleprojectzero.blogspot.com | — | — | — | — | Google — Zero-day research |
| Graham Cluley | https://grahamcluley.com | — | — | — | — | Blog personale — Security commentary |
| Help Net Security | https://www.helpnetsecurity.com | — | — | — | — | News e analisi — Security news |
| IANA | https://www.iana.org | — | EN | Globale | — | Registri tecnici internet |
| ICANN | https://www.icann.org | — | EN | Globale | — | Governance nomi a dominio |
| IGF — Internet Governance Forum | https://www.intgovforum.org | — | EN | Globale | — | Forum ONU governance internet |
| Infosecurity Magazine | https://www.infosecurity-magazine.com | — | — | — | — | Media professionale — Security news |
| Internet Society Pulse | https://pulse.internetsociety.org | — | EN | Globale | — | Shutdown, resilienza, centralizzazione |
| Kaspersky Securelist | https://securelist.com | — | — | — | — | Kaspersky — APT, malware — Research |
| Kela Cybersecurity | https://www.kelacyber.com/blog | — | — | — | — | Threat intel |
| Krebs on Security | https://krebsonsecurity.com | — | — | — | — | Brian Krebs — Cybercrime — Blog |
| Lacework Blog | https://www.lacework.com/blog | — | — | — | — | Cloud Sec. |
| LACNIC | https://www.lacnic.net | — | ES/EN | LatAm | — | Registro IP latinoamericano |
| Malwarebytes Blog | https://www.malwarebytes.com/blog | — | — | — | — | News |
| Mandiant Blog | https://www.mandiant.com/resources/blog | — | — | — | — | Google Cloud — Threat intelligence |
| Naked Security (Sophos) | https://nakedsecurity.sophos.com | — | — | — | — | Sophos blog — Threat news |
| OONI | https://ooni.org | — | EN | Globale | — | Misurazione censura internet |
| Qualys Blog | https://blog.qualys.com | — | — | — | — | Vulnerability |
| Rapid7 Blog | https://www.rapid7.com/blog | — | — | — | — | Research |
| RedHotCyber | https://www.redhotcyber.com | https://www.redhotcyber.com/feed/ | — | — | Online | Cyber IT — Cyber |
| RIPE NCC | https://www.ripe.net | — | EN | Europa | — | Registro IP Europa, RIPE Atlas |
| Risky Biz (podcast) | https://risky.biz | — | — | — | — | Security podcast — Podcast |
| SANS Internet Stormcast | https://isc.sans.edu | — | — | — | — | SANS Institute — Daily threat brief — Daily brief |
| SC Media | https://www.scmagazine.com | — | — | — | — | Media professionale — Security news |
| Schneier on Security | https://www.schneier.com | — | — | — | — | Bruce Schneier — Security analysis — Blog |
| Security Affairs | https://securityaffairs.com | https://securityaffairs.com/feed | — | — | Online | Cyber IT — Cyber |
| Security Intelligence (IBM) | https://securityintelligence.com | — | — | — | — | IBM — Blog |
| Security Now | https://www.grc.com/sn | — | — | — | — | Gibson — Podcast |
| SecurityWeek | https://www.securityweek.com | — | — | — | — | Copertura ampia — Security news |
| SentinelOne Blog | https://www.sentinelone.com/blog | — | — | — | — | SentinelOne — Threat intel |
| Smashing Security | https://www.smashingsecurity.com | — | — | — | — | Podcast |
| Symantec Threat Intel | https://symantec-enterprise-blogs.security.com | — | — | — | — | Broadcom — Threat intel — Research |
| Talos Intelligence Blog | https://blog.talosintelligence.com | — | — | — | — | Cisco Talos — Threat intel |
| TechCrunch Security | https://techcrunch.com | — | EN | — | — | Venture e security — Startup security |
| TechRepublic Security | https://www.techrepublic.com | — | — | — | — | News |
| Tenable Blog | https://www.tenable.com/blog | — | — | — | — | Vulnerability |
| The Hacker News | https://thehackernews.com | — | — | — | — | News quotidiane — Cybersecurity |
| Threatpost | https://threatpost.com | — | — | — | — | Kaspersky Lab — Security news |
| Trend Micro Blog | https://www.trendmicro.com/en_us/research.html | — | — | — | — | Research |
| Unit 42 (Palo Alto) | https://unit42.paloaltonetworks.com | — | — | — | — | Palo Alto — Threat intel |
| US-CERT / CISA | https://www.cisa.gov/cybersecurity-advisories | — | — | — | — | Alert ufficiali USA — CERT USA |
| Vectra AI Blog | https://www.vectra.ai/blog | — | — | — | — | AI Security |
| Virus Bulletin | https://www.virusbulletin.com | — | — | — | — | Ricerca tecnica — Malware research |
| Wired Security | https://www.wired.com/category/security | — | — | — | — | Copertura generale — Security news |
| ZDNet | https://www.zdnet.com | https://www.zdnet.com/rss/ | EN | — | — | Tech Enterprise — Enterprise security — Enterprise |

### 9.2 OSINT Tools & Intelligence (114)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Amass | https://github.com/owasp-amass/amass | — | — | — | Open Source | OWASP project — Subdomain Enum |
| AnyRun | https://app.any.run | — | — | — | Freemium | Malware sandbox |
| Archive.ph | https://archive.ph | — | — | — | Pubblico | Page archiving — Archive |
| BASE (Bielefeld) | https://www.base-search.net | — | — | — | — | Open access ricerca — Pubblico — Search |
| BeenVerified | https://www.beenverified.com | — | — | — | A pagamento | USA — People search |
| Bellingcat Toolkit | https://www.bellingcat.com/resources | — | — | — | Pubblico | Guide e tool OSINT — Risorse |
| Bing Visual Search | https://www.bing.com/visualsearch | — | — | — | Pubblico | Ricerca inversa Bing — Gratuito — Image Search |
| Buscador OSINT VM | https://inteltechniques.com/buscador | — | — | — | Pubblico | VM OSINT — VM |
| CachedPages | https://www.cachedpages.com | — | — | — | Pubblico | Archive |
| CachedView | https://cachedview.nl | — | — | — | Pubblico | Google cache — Archive |
| Censys | https://search.censys.io | — | — | — | Freemium | Infrastruttura internet — Motore di ricerca |
| Cuckoo Sandbox | https://cuckoosandbox.org | — | — | — | Open Source | Malware sandbox |
| Cylect.io | https://cylect.io | — | — | — | Pubblico | Search aggregator — OSINT |
| DataWrapper | https://www.datawrapper.de | — | — | — | Freemium | Visualizzazione dati — Tool |
| Datawrapper Blog | https://blog.datawrapper.de | — | — | Globale | — | Data journalism tools |
| DeHashed | https://www.dehashed.com | — | — | — | A pagamento | Credential leak — Database |
| DomainTools | https://www.domaintools.com | — | — | — | Commerciale | Domain intel |
| EmailRep | https://emailrep.io | — | — | — | Freemium | Email reputation |
| Exiftool | https://exiftool.org | — | — | — | Open Source | Metadata file — Metadata |
| Factiva (Dow Jones) | https://www.dowjones.com/professional/factiva | — | — | — | Database | News archive — A pagamento |
| FastPeopleSearch | https://www.fastpeoplesearch.com | — | — | — | Pubblico | USA — People search |
| Flashpoint | https://flashpoint.io/blog | — | — | — | — | Threat intel |
| Flourish | https://flourish.studio | — | — | — | Freemium | Visualizzazioni interattive — Tool |
| FotoForensics | https://fotoforensics.com | — | — | — | Pubblico | Analisi immagini — Image Analysis |
| GeoGuessr | https://www.geoguessr.com | — | — | — | Freemium | Geolocal. — Training |
| Geolocating | https://geolocating.com | — | — | — | — | Geolocalizzazione immagini — Pubblico — Geolocation |
| GeoSpy | https://geospy.ai | — | — | — | — | AI geolocalizzazione foto — Freemium — Geolocation AI |
| GeoTips | https://geotips.net | — | — | — | Pubblico | GeoGuessr tips — Geolocal. |
| Gephi | https://gephi.org | — | — | — | Open Source | Graph analysis — Network viz |
| Google Earth Pro | https://earth.google.com/web | — | — | — | Pubblico | Geolocalizzazione — Mappa |
| Google Images (reverse) | https://images.google.com | — | — | — | Pubblico | Ricerca inversa Google — Gratuito — Image Search |
| GreyNoise | https://www.greynoise.io | — | — | — | Freemium | IP noise — Database |
| Have I Been Pwned | https://haveibeenpwned.com | — | — | — | Pubblico | Troy Hunt — Data breach — Database |
| Hunchly | https://www.hunch.ly | — | — | — | A pagamento | OSINT browser — Web capture |
| Hunter.io | https://hunter.io | — | — | — | Freemium | Business — Email finder |
| Hybrid Analysis | https://www.hybrid-analysis.com | — | — | — | Freemium | CrowdStrike — Malware sandbox |
| i2 Analyst's Notebook | https://www.ibm.com/products/i2-analysts-notebook | — | — | — | Commerciale | IBM — Link analysis |
| Intelius | https://www.intelius.com | — | — | — | — | Ricerca persone USA — A pagamento — People Search |
| Intelligence X | https://intelx.io | — | — | — | Freemium | Dark web e leak — Motore di ricerca |
| IntelTechniques | https://inteltechniques.com/tools | — | — | — | Pubblico | Tool di Michael Bazzell — Risorse |
| Internet Archive | https://archive.org | — | — | — | Pubblico | Web, libri, media — Archivio |
| Investigative Dashboard | https://id.occrp.org | — | — | — | Database | Research OCCRP — Registrazione |
| Investigative Dashboard | https://investigativedashboard.org | — | — | — | Registrazione | OCCRP tools — Database |
| InVID / WeVerify | https://weverify.eu/verification-plugin | — | — | — | — | Verifica video — Gratuito — Image/Video |
| InVID WeVerify | https://weverify.eu | — | — | — | Pubblico | Video verification |
| Joe Sandbox | https://www.joesandbox.com | — | — | — | Commerciale | Malware sandbox |
| JSTOR | https://www.jstor.org | — | — | — | Database | Articoli accademici — Freemium |
| LibGen | https://libgen.is | — | — | — | — | Libri e paper — Pubblico — Archivio |
| Maltego CE | https://www.maltego.com | — | — | — | Freemium | Mappatura relazioni — Gratuito (CE) — Link Analysis |
| Maltego Transforms | https://www.maltego.com/transform-hub | — | — | — | Freemium | Hub — Transforms |
| Maxar Technologies | https://www.maxar.com | — | — | — | Commerciale | Immagini sat. HD — Satellite |
| MISP | https://www.misp-project.org | — | — | — | Open Source | Threat sharing |
| Mullvad VPN | https://mullvad.net | — | — | — | A pagamento | No-log — VPN |
| NodeXL | https://nodexl.com | — | — | — | Freemium | Social media — Network analysis |
| OpenCTI | https://www.opencti.io | — | — | — | Open Source | Threat intel |
| Oryon OSINT | https://oryon.net/osint | — | — | — | Pubblico | Directory |
| OSINT Curious | https://osintcurio.us | — | — | — | Pubblico | OSINT community — Blog |
| OSINT Dojo | https://www.osintdojo.com | — | — | — | Pubblico | Training |
| OSINT Framework | https://osintframework.com | — | — | — | Pubblico | Collection di tool — Risorse |
| OSINT Industries | https://www.osint.industries | — | — | — | — | Email/phone lookup — Freemium — Lookup Tool |
| Paliscope | https://www.paliscope.com | — | — | — | Commerciale | OSINT platform |
| PeakFinder | https://www.peakfinder.org | — | — | — | Freemium | Montagne — Geolocal. |
| PeakVisor | https://peakvisor.com | — | — | — | — | Identificazione montagne — Freemium — Tool |
| Phonebook.cz | https://phonebook.cz | — | — | — | Freemium | Email/domain |
| Pipl | https://pipl.com | — | — | — | Commerciale | Ricerca persone — A pagamento — People Search |
| Planet Labs | https://www.planet.com | — | — | — | Freemium | Immagini satellite giornaliere — A pagamento — Satellite |
| Power BI | https://powerbi.microsoft.com | — | — | — | Freemium | Microsoft — Data viz |
| ProQuest | https://www.proquest.com | — | — | — | Commerciale | Articoli e ricerca — A pagamento — Database |
| ProtonMail | https://proton.me | — | — | — | Freemium | Email sicura |
| ProtonVPN | https://protonvpn.com | — | — | — | Freemium | VPN |
| Qubes OS | https://www.qubes-os.org | — | — | — | Open Source | OS sicuro |
| Recon-ng | https://github.com/lanmaster53/recon-ng | — | — | — | Open Source | Python-based — Recon Framework |
| Recorded Future Blog | https://www.recordedfuture.com/blog | — | — | — | — | Intelligence commerciale — Threat intelligence |
| Reddit Search (Pushshift) | https://pushshift.io | — | — | — | — | Archivio Reddit — Pubblico — Search |
| RevEye | https://chrome.google.com/webstore/detail/reveye-reverse-image-sear | — | — | — | — | Ricerca inversa immagini — Gratuito — Browser Ext |
| Sci-Hub | https://sci-hub.se | — | — | — | — | Paper accademici — Pubblico — Archivio |
| Sentinel Hub | https://apps.sentinel-hub.com/eo-browser | — | — | — | Pubblico | Immagini satellitari — Satellite |
| Shodan | https://www.shodan.io | — | — | — | Freemium | Device connessi — Motore di ricerca |
| Signal | https://signal.org | — | — | — | Open Source | E2E — Messaging |
| Skopenow | https://www.skopenow.com | — | — | — | Commerciale | Social + deep — OSINT automation |
| Social Bearing | https://socialbearing.com | — | — | — | — | Analisi Twitter/X — Freemium — Social OSINT |
| Social Links | https://sociallinks.io | — | — | — | Commerciale | Maltego plugin — OSINT platform |
| SpiderFoot | https://www.spiderfoot.net | — | — | — | Open Source | Scansione automatica — OSINT Automation |
| Spokeo | https://www.spokeo.com | — | — | — | A pagamento | Ricerca persone USA — Freemium — People Search |
| Start.me | https://start.me | — | — | — | Freemium | OSINT dashboard — Bookmark |
| Start.me OSINT | https://start.me/p/4Q6v8D/osint | — | — | — | Pubblico | Collection condivisa — Bookmark Collection |
| SunCalc | https://suncalc.org | — | — | — | Pubblico | Calcolo ombre/sole — Tool |
| Syria Archive | https://syriaarchive.org | — | EN | — | — | Archivio diritti umani — Siria |
| Tableau Public | https://public.tableau.com | — | — | — | Gratuito | Dashboard dati — Pubblico — Tool |
| Tails OS | https://tails.boum.org | — | — | — | Open Source | OS anonimato |
| Telegram Analytics | https://tgstat.com | — | — | — | — | Statistiche Telegram — Freemium — Social OSINT |
| Telegram Search | https://lyzem.com | — | — | — | — | Ricerca Telegram — Pubblico — Search |
| That'sThem | https://thatsthem.com | — | — | — | Freemium | USA — People search |
| The Friday Times PK | https://thefridaytimes.com | — | — | PK | — | Long-form — Pakistan |
| The Record | https://therecord.media | — | — | — | — | Recorded Future — Cybercrime news |
| TheEE.ai | https://theee.ai | — | — | — | Pubblico | Directory AI — AI Tools |
| theOSINTionary | https://theosintionary.com | — | — | — | Pubblico | Terminologia OSINT — Glossary |
| TinEye | https://tineye.com | — | — | — | Freemium | Ricerca inversa immagini — Image Search |
| Toolify AI | https://www.toolify.ai | — | — | — | Pubblico | Catalogo tool AI — AI Directory |
| Tor Browser | https://www.torproject.org | — | — | — | Open Source | Dark web access — Anonimato |
| Twint | https://github.com/twintproject/twint | — | — | — | — | Scraping Twitter — Open Source — Social OSINT |
| Twitonomy | https://www.twitonomy.com | — | — | — | — | Analytics Twitter — Freemium — Social OSINT |
| Unpaywall | https://unpaywall.org | — | — | — | — | Articoli scientifici gratuiti — Pubblico — Tool |
| URLScan | https://urlscan.io | — | — | — | Freemium | URL analysis |
| VirusTotal | https://www.virustotal.com | — | — | — | Freemium | Google — File/URL analysis |
| VK Parser | https://vk.com | — | — | — | — | Social russo — Pubblico |
| Wayback CDX | https://web.archive.org/cdx/search | — | — | — | Pubblico | Archive API — API |
| Wayback Machine | https://archive.org/web | — | — | — | Pubblico | Pagine web storiche — Archivio |
| Whitepages | https://www.whitepages.com | — | — | — | Freemium | USA — People search |
| WHOIS | https://who.is | — | — | — | Pubblico | Domain lookup |
| World Monitor | https://worldmonitor.app | — | — | — | Freemium | Monitoraggio globale — Dashboard |
| Yandex Images | https://yandex.com/images | — | — | — | Pubblico | Ricerca inversa Yandex — Gratuito — Image Search |
| YouTube DataViewer | https://citizenevidence.amnestyusa.org | — | — | — | Pubblico | Amnesty — Video |
| ZabaSearch | https://www.zabasearch.com | — | — | — | Pubblico | Ricerca persone USA — People Search |

---

## 10. 📡 Social Media & Media Monitoring

### 10.1 Social Media & Media Monitoring (82)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| 99% Invisible | https://99percentinvisible.org | — | — | — | — | Design — Podcast |
| ACRIMED | https://www.acrimed.org | — | — | — | — | FR sinistra — Media critica |
| All-In Podcast | https://www.allinpodcast.co | — | — | — | — | Tech/VC — Podcast |
| Apple News | https://apple.news | — | — | — | — | Apple |
| Arts & Letters Daily | https://www.aldaily.com | — | — | — | — | Accademica — Curazione |
| Behind the Bastards | https://www.iheart.com/podcast/105-behind-the-bastards-29236323 | — | — | — | — | Storia nera — Podcast |
| Bluesky news | https://bsky.app | — | — | — | — | Social |
| Challenges | https://www.challenges.fr | https://www.challenges.fr/rss/ | FR | — | — | Business FR |
| Citation Needed | https://www.citationneeded.news | — | — | US | — | Tech accountability — USA |
| Columbia Journalism Review | https://www.cjr.org | — | — | US | — | Critica media — USA |
| Decoder (The Verge) | https://www.theverge.com/decoder-podcast | — | — | — | — | Tech — Podcast |
| Digiday | https://digiday.com | — | — | US | — | Media digitali — USA |
| Disconnect | https://disconnect.blog | — | — | US | — | Tech critica — USA |
| EJO | https://en.ejo.ch | — | — | — | — | Osservatorio — Accademia |
| European Journalism Centre | https://ejc.net | — | — | EU | — | Formazione |
| FAIR | https://fair.org | — | — | US | — | Critica media USA |
| Flipboard | https://flipboard.com | — | — | — | — | Aggregatore — App |
| Forum on Information & Democracy | https://informationdemocracy.org | — | — | — | — | Policy |
| Freakonomics | https://freakonomics.com | — | — | — | — | Economia — Podcast |
| Free Press | https://www.freepress.net | — | — | — | — | USA — Advocacy |
| Google News | https://news.google.com | — | — | — | — | Google — App |
| Ground News | https://ground.news | — | — | — | — | Bias comparazione — App |
| Hacker News | https://news.ycombinator.com | — | — | — | Community | Tech |
| Hard Fork (NYT) | https://www.nytimes.com/column/hard-fork | — | — | — | — | Tech — Podcast |
| Hardcore History | https://www.dancarlin.com | — | — | — | — | Storia — Podcast |
| How I Built This | https://www.npr.org/podcasts/510313/how-i-built-this | — | — | — | — | Imprenditoria — Podcast |
| ICFJ | https://www.icfj.org | — | — | — | — | Organizzazione |
| If Books Could Kill | https://www.ifbookscouldkill.com | — | — | — | — | Critica — Podcast |
| IJNet | https://ijnet.org | — | — | Globale | — | Risorse giornalisti |
| Intelligence Squared | https://www.intelligencesquared.com | — | — | — | — | Dibattito — Podcast |
| JournalismFund.eu | https://www.journalismfund.eu | — | — | EU | — | Funding |
| Knight Foundation | https://knightfoundation.org | — | — | — | — | USA — Funding |
| Kottke.org | https://kottke.org | — | — | — | — | Internet cultura — Blog |
| L'OJIM | https://ojim.fr | — | FR | — | — | Media critica |
| Lenfest Institute | https://www.lenfestinstitute.org | — | — | — | — | USA — Funding |
| Lex Fridman | https://lexfridman.com | — | — | — | — | Tech/AI — Podcast |
| Lobsters | https://lobste.rs | — | — | — | Community | Tech |
| Longreads | https://longreads.com | — | — | — | — | Long-form — Newsletter |
| Luca Sofri Newsletter | https://wittgenstein.it | — | — | — | — | Il Post — Newsletter IT |
| Luminate Group | https://www.luminategroup.com | — | — | — | — | Funding |
| Mastodon journalism | https://journa.host | — | — | — | — | Fediverse — Social |
| Media | https://www.404media.co | — | EN | — | — | Tech investigativo — USA |
| Media Freedom Rapid Response | https://www.mfrr.eu | — | — | EU | — | Monitor |
| Media Observatory | https://www.mediaobservatory.com | — | — | — | — | Monitor |
| MediaShift | https://mediashift.org | — | — | US | — | Innovazione media — USA |
| Medium Journalism | https://medium.com/topic/journalism | — | — | Globale | — | Articoli giornalismo |
| Meta Journalism Project | https://www.facebook.com/journalismproject | — | — | — | — | Meta — Funding |
| Metafilter | https://www.metafilter.com | — | — | — | Community | Link |
| Microsoft Start | https://www.msn.com | — | — | — | — | Microsoft — App |
| Morning Brew | https://www.morningbrew.com | — | — | — | — | Business — Newsletter |
| News Revenue Hub | https://newsrevenuehub.org | — | — | — | A pagamento | USA — Consulenza |
| Nieman Lab | https://www.niemanlab.org | — | — | US | — | Futuro del giornalismo — USA |
| Nieman Reports | https://niemanreports.org | — | — | US | — | Giornalismo qualità — USA |
| Open Society Media | https://www.opensocietyfoundations.org | — | — | — | — | Funding |
| Planet Money (NPR) | https://www.npr.org/podcasts/510289/planet-money | — | — | — | — | Economia — Podcast |
| Platformer | https://www.platformer.news | — | EN | — | — | Big Tech investigativo — USA |
| Pocket Worthy | https://getpocket.com/explore | — | — | — | — | Curazione |
| Politico Media | https://www.politico.com/media | — | — | US | — | Media e politica — USA |
| Protocol (Archivio) | https://www.protocol.com | — | EN | — | — | Tech policy (chiuso) — USA |
| Radiolab | https://radiolab.org | — | — | — | — | Scienza — Podcast |
| Reddit Journalism | https://www.reddit.com/r/journalism | — | — | — | Community |  |
| Reddit WorldNews | https://www.reddit.com/r/worldnews | — | — | — | Community |  |
| Reply All | https://gimletmedia.com/shows/reply-all | — | — | — | — | Internet — Podcast |
| Report for America | https://www.reportforamerica.org | — | — | — | — | USA locale — Fellowship |
| Search Engine | https://www.pjvogt.com | — | — | — | — | Internet cultura — Podcast |
| Shorenstein Center | https://shorensteincenter.org | — | — | — | — | Harvard — Accademia |
| Slow Boring | https://www.slowboring.com | — | — | — | — | Policy USA — Newsletter |
| SmartNews | https://www.smartnews.com | — | — | — | — | AI aggregatore — App |
| Splice Newsroom | https://www.splicenewsroom.com | — | — | SE Asia | — | Media innovation |
| Stratechery | https://stratechery.com | — | — | — | — | Tech analysis — Newsletter |
| Stratégies | https://www.strategies.fr | — | — | — | — | Media FR |
| Substack Journalism | https://journalism.substack.com | — | — | Globale | — | Newsletter indipendenti |
| Techdirt | https://www.techdirt.com | — | — | US | — | Policy tech — USA |
| The Browser | https://thebrowser.com | — | — | — | — | Cura — Newsletter |
| The Daily (NYT) | https://www.nytimes.com/column/the-daily | — | — | — | — | News — Podcast |
| The Fix Media | https://thefix.media | — | — | Europa | — | Innovazione redazioni |
| The Hustle | https://thehustle.co | — | — | — | — | Tech/Business — Newsletter |
| The Splice Newsroom | https://splice-newsroom.com | — | — | Asia | — | Media innovation |
| The Verge | https://www.theverge.com | — | EN | — | — | Tech media — USA |
| This Week in AI | https://www.cognilytica.com/twiai | — | — | — | — | Podcast — AI |
| Today Explained (Vox) | https://www.vox.com/today-explained | — | — | — | — | News — Podcast |
| Up First (NPR) | https://www.npr.org/podcasts/510318/up-first | — | — | — | — | News — Podcast |

---

## 11. 🌿 Sostenibilità & ESG

### 11.1 Sostenibilità & ESG (47)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AP Climate | https://apnews.com/hub/climate-and-environment | — | — | — | — | Wire — News |
| Carbon Brief | https://www.carbonbrief.org | — | EN | — | — | Clima e energia — UK/Globale |
| Circle of Blue | https://www.circleofblue.org | — | — | — | — | Acqua — News |
| ClientEarth | https://www.clientearth.org | — | — | — | — | Diritto ambiente — Legale |
| Climate Home News | https://www.climatechangenews.com | — | EN | — | — | Politica climatica — Globale |
| Climate Investigations Center | https://climateinvestigations.org | — | — | — | — | Denial — Investigativo |
| Desmog | https://www.desmog.com | — | — | — | — | Negazionismo climatico — Globale — Investigativo |
| Dialogue Earth | https://dialogue.earth | — | — | — | — | Globale — Analisi |
| Earth Journalism Network | https://earthjournalism.net | — | — | — | — | Risorse — Network |
| Earth.org | https://earth.org | — | — | — | — | Clima — News |
| Earthjustice | https://earthjustice.org | — | — | US | — | Diritto ambientale — USA |
| Eco-Business | https://www.eco-business.com | — | — | — | — | Asia sostenibilità — News |
| EcoWatch | https://www.ecowatch.com | — | — | — | — | USA — News |
| Env. Defense Fund | https://www.edf.org | — | — | — | — | Policy ambientale — USA — Advocacy |
| Environmental Health News | https://www.ehn.org | — | EN | — | — | Salute e ambiente — USA |
| Eos (AGU) | https://eos.org | — | — | — | — | Geoscienza — Scienza |
| Friends of the Earth | https://www.foe.org | — | — | — | — | ONG |
| Global Forest Watch | https://www.globalforestwatch.org | — | — | — | Pubblico | Deforestazione — Globale — Foreste — Database |
| Greenpeace Int. | https://www.greenpeace.org | — | — | — | — | ONG |
| Grist | https://grist.org | — | — | — | — | Ambiente e soluzioni — USA — News |
| Hakai Magazine | https://www.hakaimagazine.com | — | — | — | — | Costa oceano — Magazine |
| InfluenceMap | https://influencemap.org | — | — | — | Database | Corporate |
| Inside Climate News | https://insideclimatenews.org | — | EN | — | — | Clima investigativo — USA |
| IPCC | https://www.ipcc.ch | — | — | — | — | Scienza IPCC — Globale |
| Land Matrix | https://landmatrix.org | — | — | Globale | — | Land grabbing |
| Lifegate | https://www.lifegate.it | — | — | — | — | Sostenibilità e stile di vita — Ambiente |
| Mongabay | https://mongabay.com | — | EN | — | — | Foreste e biodiversità — Globale |
| Mongabay Africa | https://africa.mongabay.com | — | — | — | — | Africa — News |
| Mongabay India | https://india.mongabay.com | — | — | — | — | India — News |
| NASA Climate | https://climate.nasa.gov | — | — | — | — | Scienza NASA — USA |
| Natural Resources Defense Council | https://www.nrdc.org | — | — | — | — | USA — ONG |
| NOAA Climate | https://www.climate.gov | — | — | — | — | USA — Scienza |
| NYT Climate | https://www.nytimes.com/section/climate | — | — | — | — | USA — News |
| Plastic Soup Foundation | https://www.plasticsoupfoundation.org | — | — | — | — | Plastica — ONG |
| Pulitzer Center Environment | https://pulitzercenter.org | — | — | — | — | Funding |
| Seas At Risk | https://seas-at-risk.org | — | — | — | — | Oceani UE — ONG |
| Sierra Club | https://www.sierraclub.org | — | — | — | — | Conservazione USA — ONG |
| Terra Nuova | https://www.terranuova.it | — | — | — | — | Sostenibilità — Ambiente |
| The Ocean Cleanup | https://theoceancleanup.com | — | — | — | — | Oceani — ONG |
| The Revelator | https://therevelator.org | — | — | — | — | Center Biol. Div. — Opinion |
| Undark | https://undark.org | — | — | — | — | Giornalismo — Science |
| Unearthed (Greenpeace) | https://unearthed.greenpeace.org | — | UK | — | — | Investigativo ambiente |
| UNEP | https://www.unep.org | — | — | — | — | ONU ambiente — Org. |
| Waterkeeper Alliance | https://waterkeeper.org | — | — | — | — | Acqua — ONG |
| WMO (Portale Pubblico) | https://public.wmo.int | — | — | — | — | ONU meteo — Org. |
| WWF | https://www.worldwildlife.org | — | — | — | — | ONG |
| Yale Environment 360 | https://e360.yale.edu | — | — | — | — | Analisi accademia — USA |

---

## 12. 🧩 Settori Specifici

### 12.1 Finanza, Economia & Business (58)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| A. T. Kearney | https://www.kearney.com/insights | — | — | — | A pagamento | Consulenza |
| Alphaville FT | https://www.ft.com/alphaville | — | UK | — | — | Mercati e finanza |
| AP Business | https://apnews.com/hub/business | — | — | — | — | Wire |
| Arts Economics | https://www.artseconomics.com | — | — | Globale | — | Arte e mercato |
| Axios Pro Rata | https://www.axios.com/pro/pro-rata | — | — | — | — | VC/PE |
| Bain & Company | https://www.bain.com/insights | — | — | — | A pagamento | Consulenza |
| Banca d'Italia | https://www.bancaditalia.it | — | — | — | — | Banca centrale — Italia |
| Barron's | https://www.barrons.com | — | — | — | Premium | Finanza USA |
| BCG Insights | https://www.bcg.com/publications | — | — | — | A pagamento | Consulenza |
| BIS Working Papers | https://www.bis.org | — | — | — | — | Banca int. — Org. |
| Breakingviews | https://breakingviews.com | — | — | Globale | — | Opinion finanza |
| Bundesbank | https://www.bundesbank.de | — | — | — | — | Germania — Banca centrale |
| Business Insider | https://www.businessinsider.com | — | EN | — | — | Tech + business — USA |
| CNBC | https://www.cnbc.com | — | — | — | Online | TV/News finanza — USA |
| Corporate Europe Observatory | https://corporateeurope.org | — | — | — | — | Lobby UE — Advocacy |
| Crunchbase News | https://news.crunchbase.com | — | — | — | — | Startup — VC |
| Deloitte Insights | https://www2.deloitte.com/insights | — | — | — | A pagamento | Consulenza |
| ECB Research | https://www.ecb.europa.eu | — | — | EU | — | Banca centrale |
| EDGAR (SEC) | https://www.sec.gov/cgi-bin/browse-edgar | — | — | — | Database | Aziende USA quotate — Pubblico |
| European Securities (ESMA) | https://www.esma.europa.eu | — | — | EU | — | Regolatore |
| Fast Company | https://www.fastcompany.com | — | — | US | — | Innovazione business — USA |
| Fed Reserve | https://www.federalreserve.gov | — | — | — | — | USA — Banca centrale |
| Financial Crimes Enforcement | https://www.fincen.gov | — | — | — | — | USA — Gov |
| Financial Times | https://www.ft.com | — | EN | — | — | Economia globale |
| Fiscoetasse | https://www.fiscoetasse.com | — | — | — | — | Fiscale |
| Fitch Ratings | https://www.fitchratings.com | — | — | — | — | Ratings — Research |
| Forbes | https://www.forbes.com | — | — | US | — | Business — USA |
| Fox Business | https://www.foxbusiness.com | — | — | — | Online | USA — TV/Online |
| FT Climate Capital | https://www.ft.com/climate-capital | — | — | — | — | Economia — News |
| Global Financial Integrity | https://gfintegrity.org | — | — | — | — | Flussi illeciti — Research |
| Harvard Business Review | https://hbr.org | — | — | US | — | Management — USA |
| IMF Blog | https://www.imf.org/en/Blogs | — | — | — | — | Org. |
| Inc. Magazine | https://www.inc.com | — | — | US | — | Startup e business — USA |
| Investing.com | https://www.investing.com | — | — | Globale | — | Dati mercati |
| Investopedia | https://www.investopedia.com | — | — | — | — | Education |
| Korn Ferry Insights | https://www.kornferry.com/insights | — | HR | — | — | — |
| MarketWatch | https://www.marketwatch.com | — | — | — | — | Mercati USA — News |
| McKinsey Insights | https://www.mckinsey.com/insights | — | — | — | A pagamento | Consulting — Globale |
| Microsoft Security Blog | https://www.microsoft.com/en-us/security/blog | — | — | — | — | Microsoft — Microsoft threats — Threat intel |
| MIT Sloan Management Review | https://sloanreview.mit.edu | — | — | US | — | Management — USA |
| Morningstar | https://www.morningstar.com | — | — | — | — | Fund analysis — Research |
| Motley Fool | https://www.fool.com | — | — | — | Community |  |
| NBER | https://www.nber.org | — | — | US | — | Ricerca economica — USA |
| Nextdraft | https://nextdraft.com | — | — | — | — | Dave Pell cura — Newsletter |
| OECD Data | https://data.oecd.org | — | — | — | Pubblico | Paesi OCSE — Database |
| Pitchbook | https://pitchbook.com | — | — | — | — | Database — VC/PE |
| Project Syndicate | https://www.project-syndicate.org | — | — | Globale | — | Opinion economia |
| PwC Insights | https://www.pwc.com/gx/en/insights | — | — | — | A pagamento | Consulenza |
| Reuters Business | https://www.reuters.com/business | — | — | — | — | Wire |
| Seeking Alpha | https://seekingalpha.com | — | — | — | Community | Analisi investimenti — USA |
| Semafor Business | https://www.semafor.com | — | EN | — | — | News premium — Globale |
| Tax Justice Network | https://taxjustice.net | — | — | — | — | Evasione — Advocacy |
| Wall Street Journal | https://www.wsj.com | — | EN | — | — | Business USA |
| World Bank Blogs | https://blogs.worldbank.org | — | — | — | — | Org. |
| World Bank News | https://www.worldbank.org/en/news | https://www.worldbank.org/en/news/rss.xml | EN | — | — | Istituzionale |
| IMF Finances | https://finances.worldbank.org | — | — | — | Database | Dati finanziari storici dal 1984 — Gratuito |
| OCSE Data Explorer | https://data-explorer.oecd.org | — | — | — | — | Economie OCSE: lavoro, commercio, istruzione — Gratuito — Portale ufficiale |
| OECD Tax Stats | https://stats.oecd.org/index.aspx?DataSetCode=REV | — | — | — | — | Gratuito — Fiscalità |

### 12.2 Autorità di Vigilanza Finanziaria & Regolatori (66)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Argentina — CNV | https://www.argentina.gob.ar/cnv | — | ES | AR | — | Comisión Nacional de Valores |
| Australia — APRA | https://www.apra.gov.au | — | EN | AU | — | Vigilanza prudenziale bancaria/assicurativa |
| Austria — FMA | https://www.fma.gv.at | — | DE/EN | AT | — | Autorità mercati finanziari austriaca |
| Belgium — FSMA | https://www.fsma.be | — | FR/NL/EN | BE | — | Autorità servizi e mercati finanziari |
| Brazil — CVM | https://www.gov.br/cvm | — | PT | BR | — | Comissão de Valores Mobiliários |
| BVI — Financial Services Commission | https://www.bvifsc.vg | — | EN | VG | — | Vigilanza offshore BVI |
| Canada — CSA (Canadian Securities Administrators) | https://www.securities-administrators.ca | — | EN/FR | CA | — | Coordinamento regolatori provinciali |
| Canada — OSFI | https://www.osfi-bsif.gc.ca | — | EN/FR | CA | — | Vigilanza istituzioni finanziarie federali |
| Chile — CMF | https://www.cmfchile.cl | — | ES | CL | — | Comisión para el Mercado Financiero |
| China — CSRC | http://www.csrc.gov.cn | — | ZH/EN | CN | — | Regolatore mercati mobiliari cinese |
| China — NFRA | https://www.nfra.gov.cn | — | ZH | CN | — | Vigilanza bancaria/assicurativa (ex CBIRC) |
| Colombia — Superintendencia Financiera | https://www.superfinanciera.gov.co | — | ES | CO | — | Vigilanza finanziaria colombiana |
| Denmark — Finanstilsynet | https://www.finanstilsynet.dk | — | DA/EN | DK | — | Vigilanza finanziaria danese |
| EBA — European Banking Authority | https://www.eba.europa.eu | — | EN | EU | — | Autorità bancaria europea |
| ECB — Banking Supervision (SSM) | https://www.bankingsupervision.europa.eu | — | EN | EU | — | Vigilanza bancaria unica |
| Egmont Group of FIUs | https://egmontgroup.org | — | EN | Globale | — | Rete unità informazione finanziaria (AML) |
| Egypt — FRA | https://fra.gov.eg | — | AR/EN | EG | — | Financial Regulatory Authority egiziana |
| EIOPA | https://www.eiopa.europa.eu | — | EN | EU | — | Assicurazioni e fondi pensione |
| Finland — FIN-FSA | https://www.finanssivalvonta.fi | — | FI/EN | FI | — | Vigilanza finanziaria finlandese |
| France — AMF | https://www.amf-france.org | — | FR/EN | FR | — | Autorité des marchés financiers |
| FSB — Financial Stability Board | https://www.fsb.org | — | EN | Globale | — | Stabilità finanziaria globale, G-SIB list |
| Germany — BaFin | https://www.bafin.de | — | DE/EN | DE | — | Vigilanza finanziaria tedesca |
| Gibraltar — GFSC | https://www.fsc.gi | — | EN | GI | — | Vigilanza finanziaria di Gibilterra |
| Greece — Hellenic Capital Market Commission | https://www.hcmc.gr | — | EL/EN | GR | — | Vigilanza mercati mobiliari greca |
| Guernsey — GFSC | https://www.gfsc.gg | — | EN | GG | — | Guernsey Financial Services Commission |
| Hong Kong — SFC | https://www.sfc.hk | — | EN/ZH | HK | — | Securities and Futures Commission |
| IAIS — Insurance Supervisors | https://www.iaisweb.org | — | EN | Globale | — | Associazione internazionale vigilanza assicurativa |
| India — SEBI | https://www.sebi.gov.in | — | EN/HI | IN | — | Securities and Exchange Board of India |
| IOSCO | https://www.iosco.org | — | EN | Globale | — | Org. internazionale autorità mobiliari |
| Isle of Man — FSA | https://www.iomfsa.im | — | EN | IM | — | Vigilanza finanziaria Isola di Man |
| Israel — ISA | https://www.isa.gov.il | — | HE/EN | IL | — | Israel Securities Authority |
| Italy — IVASS | https://www.ivass.it | — | IT | IT | — | Vigilanza assicurazioni italiana |
| Japan — FSA | https://www.fsa.go.jp | — | JA/EN | JP | — | Financial Services Agency giapponese |
| Jersey — JFSC | https://www.jerseyfsc.org | — | EN | JE | — | Jersey Financial Services Commission (+ registro) |
| Kenya — Capital Markets Authority | https://www.cma.or.ke | — | EN | KE | — | Vigilanza mercati keniota |
| Liechtenstein — FMA | https://www.fma-li.li | — | DE/EN | LI | — | Vigilanza finanziaria del Liechtenstein |
| Luxembourg — CSSF | https://www.cssf.lu | — | FR/EN | LU | — | Vigilanza settore finanziario lussemburghese |
| Malta — MFSA | https://www.mfsa.mt | — | EN | MT | — | Malta Financial Services Authority |
| Mexico — CNBV | https://www.gob.mx/cnbv | — | ES | MX | — | Comisión Nacional Bancaria y de Valores |
| Netherlands — AFM | https://www.afm.nl | — | NL/EN | NL | — | Autorità mercati finanziari olandese |
| New Zealand — FMA | https://www.fma.govt.nz | — | EN | NZ | — | Financial Markets Authority |
| Nigeria — SEC Nigeria | https://sec.gov.ng | — | EN | NG | — | Securities and Exchange Commission nigeriana |
| Norway — Finanstilsynet | https://www.finanstilsynet.no | — | NO/EN | NO | — | Vigilanza finanziaria norvegese |
| Poland — KNF | https://www.knf.gov.pl | — | PL/EN | PL | — | Komisja Nadzoru Finansowego |
| Portugal — CMVM | https://www.cmvm.pt | — | PT/EN | PT | — | Vigilanza mercati mobiliari portoghese |
| Qatar — QFCRA | https://www.qfcra.com | — | EN/AR | QA | — | QFC Regulatory Authority |
| Saudi Arabia — CMA | https://cma.org.sa | — | AR/EN | SA | — | Capital Market Authority saudita |
| Singapore — MAS (Financial Institutions Directory) | https://eservices.mas.gov.sg/fid | — | EN | SG | — | Anagrafe istituzioni vigilate MAS |
| South Africa — FSCA | https://www.fsca.co.za | — | EN | ZA | — | Financial Sector Conduct Authority |
| South Korea — FSC | https://www.fsc.go.kr | — | KO/EN | KR | — | Financial Services Commission coreana |
| South Korea — FSS | https://www.fss.or.kr | — | KO/EN | KR | — | Financial Supervisory Service |
| Spain — CNMV | https://www.cnmv.es | — | ES/EN | ES | — | Mercati mobiliari |
| Sweden — Finansinspektionen | https://www.fi.se | — | SV/EN | SE | — | Vigilanza finanziaria svedese |
| Switzerland — FINMA | https://www.finma.ch | — | EN/DE | CH | — | Vigilanza finanziaria svizzera |
| Taiwan — FSC | https://www.fsc.gov.tw | — | ZH/EN | TW | — | Financial Supervisory Commission taiwanese |
| Turkey — BDDK | https://www.bddk.org.tr | — | TR/EN | TR | — | Vigilanza bancaria turca |
| Turkey — SPK (CMB) | https://www.spk.gov.tr | — | TR/EN | TR | — | Capital Markets Board turco |
| UAE — DFSA (DIFC) | https://www.dfsa.ae | — | EN | AE | — | Dubai Financial Services Authority |
| UAE — SCA | https://www.sca.gov.ae | — | AR/EN | AE | — | Securities & Commodities Authority |
| UK — Bank of England / PRA | https://www.bankofengland.co.uk/prudential-regulation | — | EN | GB | — | Vigilanza prudenziale UK |
| UK — FCA Register | https://register.fca.org.uk | — | EN | GB | — | Anagrafe soggetti vigilati |
| US — CFTC | https://www.cftc.gov | — | EN | US | — | Regolatore derivati/commodity |
| US — FDIC BankFind | https://banks.data.fdic.gov/bankfind-suite/bankfind | — | EN | US | — | Anagrafe banche assicurate |
| US — FINRA BrokerCheck | https://brokercheck.finra.org | — | EN | US | — | Verifica broker/consulenti |
| US — OCC | https://www.occ.gov | — | EN | US | — | Vigilanza banche nazionali |
| US — SEC | https://www.sec.gov | — | EN | US | — | Securities and Exchange Commission |

### 12.3 AI, LLM & Ricerca Scientifica (92)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Adobe Firefly | https://firefly.adobe.com | — | — | — | Freemium | Creative AI |
| AI21 Labs | https://www.ai21.com | — | — | — | Freemium | LLM API |
| Aider | https://aider.chat | — | — | — | Open Source | CLI — AI Code |
| Anthropic Console | https://console.anthropic.com | — | — | — | — | Dev platform — A pagamento — API |
| Anthropic API | https://www.anthropic.com/api | — | — | — | A pagamento | Claude — API |
| AnythingLLM | https://anythingllm.com | — | — | — | Open Source | RAG privato — RAG App |
| AssemblyAI | https://www.assemblyai.com | — | — | — | — | Trascrizione + analisi — Freemium — Audio AI |
| Beautiful.ai | https://www.beautiful.ai | — | — | — | Freemium | Presentazioni |
| Bing AI | https://www.bing.com/chat | — | — | — | Freemium | Microsoft — Search+LLM |
| ChatGPT | https://chatgpt.com | — | — | — | Freemium | OpenAI — LLM |
| Claude | https://claude.ai | — | — | — | Freemium | Anthropic — LLM |
| Claude Code | https://claude.ai/code | — | — | — | A pagamento | Anthropic — AI Code |
| Cohere | https://cohere.com | — | — | — | Freemium | NLP enterprise — API |
| ComfyUI | https://www.comfy.org | — | — | — | Open Source | Image AI |
| Common Crawl | https://commoncrawl.org | — | — | — | — | Gratuito — Pubblico — Web crawl grezzo (petabyte, base LLM) — Dataset — Repository |
| Connected Papers | https://www.connectedpapers.com | — | — | — | Freemium | Grafi paper — Research |
| Consensus | https://consensus.app | — | — | — | Freemium | Ricerca scientifica AI — Research AI |
| CSET ETO (Georgetown) | https://eto.tech/datasets | — | EN | — | Pubblico | Metriche AI per paese: pubblicazioni, brevetti, investimenti — CC BY-NC 4.0 — Database |
| Cursor | https://cursor.com | — | — | — | Freemium | Sviluppo con AI — AI Code Editor |
| DALL-E | https://openai.com/dall-e-3 | — | — | — | Freemium | OpenAI immagini — Image AI |
| Descript | https://www.descript.com | — | — | — | — | Editing AI — Freemium — Video/Audio |
| Dify | https://dify.ai | — | — | — | Freemium | LLM platform |
| EleutherAI Datasets | https://github.com/EleutherAI | — | — | — | — | Gratuito — Dataset testo per LLM open source — Repository |
| ElevenLabs | https://elevenlabs.io | — | — | — | Freemium | Sintesi vocale — Audio AI |
| Elicit | https://elicit.com | — | — | — | Freemium | Analisi paper scientifici — Research AI |
| Epoch AI | https://epoch.ai/data | — | EN | — | Pubblico | Trend modelli AI, compute, hardware, benchmark — CC BY 4.0 — Database |
| ERNIE Bot | https://ernie.baidu.com | — | — | — | Freemium | Baidu — LLM |
| Fal.ai | https://fal.ai | — | — | — | — | Immagini AI rapide — Freemium |
| Fireflies.ai | https://fireflies.ai | — | — | — | — | Note riunioni — Freemium — Trascrizione |
| Fireworks AI | https://fireworks.ai | — | — | — | Freemium | LLM API |
| Flowise | https://flowiseai.com | — | — | — | Open Source | LLM flow builder — No-code LLM |
| Flux | https://blackforestlabs.ai | — | — | — | Freemium | Image AI |
| Gemini | https://gemini.google.com | — | — | — | Freemium | Google — LLM |
| Google AI Studio | https://aistudio.google.com | — | — | — | Freemium | Google Gemini dev — API/Playground |
| Google Scholar | https://scholar.google.com | — | — | — | — | Ricerca accademica — Pubblico — Search |
| GPT4All | https://gpt4all.io | — | — | — | Gratuito | Privacy — Local LLM |
| Grok | https://grok.com | — | — | — | Premium | X/Twitter — LLM |
| Groq | https://groq.com | — | — | — | Freemium | Inferenza rapida — API/LLM |
| Hugging Face Datasets | https://huggingface.co/datasets | — | — | — | — | Freemium — 80.000+ dataset ML, NLP, CV — Hub |
| Ideogram | https://ideogram.ai | — | — | — | Freemium | Testo in immagini — Image AI |
| IEEE Spectrum | https://spectrum.ieee.org | — | — | US | — | Tecnologia ingegneria — USA |
| Jamba | https://www.ai21.com/jamba | — | — | — | Freemium | AI21 — LLM |
| Jenni AI | https://jenni.ai | — | — | — | Freemium | Accademico — Writing |
| Kimi | https://www.kimi.com | — | — | — | Freemium | Moonshot AI — LLM |
| Kling AI | https://klingai.com | — | — | — | Freemium | Kuaishou — Video AI |
| Langchain | https://www.langchain.com | — | — | — | Open Source | LLM apps framework — Framework |
| Litmaps | https://www.litmaps.com | — | — | — | Freemium | Papers — Research |
| LlamaIndex | https://www.llamaindex.ai | — | — | — | — | RAG framework — Open Source |
| LlamaIndex Cloud | https://cloud.llamaindex.ai | — | — | — | Freemium | Framework dati — RAG Platform |
| LM Studio | https://lmstudio.ai | — | — | — | Gratuito | LLM locale — Desktop |
| Luma Dream Machine | https://lumalabs.ai | — | — | — | Freemium | Video AI |
| Meta AI | https://www.meta.ai | — | — | — | Gratuito | Meta — Freemium — LLM |
| Midjourney | https://www.midjourney.com | — | — | — | A pagamento | Generazione immagini — Image AI |
| Mistral Chat | https://chat.mistral.ai | — | — | — | Freemium | Mistral AI — LLM |
| ModelScope | https://www.modelscope.ai | — | — | — | — | Alibaba — Open Source — ML Platform |
| ModelScope | https://www.modelscope.cn | — | — | — | Open Source | Alibaba — ML Platform |
| Murf AI | https://murf.ai | — | — | — | Freemium | TTS — Audio AI |
| Nature | https://www.nature.com | — | — | — | — | Scientifica |
| NotebookLM | https://notebooklm.google.com | — | — | — | Freemium | Google Research — Research AI |
| Ollama | https://ollama.ai | — | — | — | Gratuito | LLM locale — Open Source — CLI |
| OpenAI API | https://platform.openai.com | — | — | — | A pagamento | Dev platform — API |
| OpenRouter | https://openrouter.ai | — | — | — | Freemium | Multi-model — LLM API |
| OpenWebUI | https://openwebui.com | — | — | — | — | Frontend LLM locale — Open Source — UI |
| Otter.ai | https://otter.ai | — | — | — | — | Trascrizione riunioni — Freemium |
| Papers With Code | https://paperswithcode.com | — | — | — | — | ML papers + codice — Pubblico — Research |
| Papers With Code — Datasets | https://paperswithcode.com/datasets | — | — | — | — | Gratuito — Dataset ML con benchmark e codice — Lista — Dataset con benchmark riproducibili — Catalogo |
| Perplexity AI | https://www.perplexity.ai | — | — | — | Freemium | Ricerca con fonti — Search + LLM |
| Phind | https://www.phind.com | — | — | — | Freemium | Dev-focused — Search+LLM |
| Poe | https://poe.com | — | — | — | Freemium | Aggregatore AI — Multi-bot |
| Qwen Chat | https://chat.qwen.ai | — | — | — | Freemium | Alibaba — LLM |
| Replicate | https://replicate.com | — | — | — | Freemium | Modelli open source — A pagamento — API |
| ResearchRabbit | https://www.researchrabbit.ai | — | — | — | Gratuito | Papers — Research |
| Roboflow Universe | https://universe.roboflow.com | — | — | — | — | Dataset computer vision annotati — Freemium — Repository |
| RunwayML | https://runwayml.com | — | — | — | Freemium | Video AI |
| Scholarcy | https://www.scholarcy.com | — | — | — | Freemium | Summarizer — Research |
| Science | https://www.science.org | — | — | — | — | AAAS — Scientifica |
| SciSpace | https://typeset.io | — | — | — | Freemium | Papers chat — Research |
| Semantic Scholar | https://www.semanticscholar.org | — | — | — | Pubblico | Ricerca accademica AI — Research |
| Sora | https://sora.chatgpt.com | — | — | — | Freemium | OpenAI — Waitlist — Video AI |
| Stable Diffusion | https://stability.ai | — | — | — | Open Source | Immagini open — Image AI |
| Suno | https://suno.com | — | — | — | Freemium | Music AI |
| The Information | https://www.theinformation.com | — | EN | — | — | Tech premium |
| Together AI | https://www.together.ai | — | — | — | Freemium | Modelli open source — API |
| Tome | https://tome.app | — | — | — | Freemium | Presentazioni AI |
| Tray.io | https://tray.io | — | — | — | A pagamento | Enterprise — Automazione |
| UCI ML Repository | https://archive.ics.uci.edu/ml | — | — | — | — | Gratuito — Repository storico ML (Università UC Irvine) |
| Udio | https://www.udio.com | — | — | — | Freemium | Music AI |
| VentureBeat Security | https://venturebeat.com | — | EN | — | — | Innovazione — AI e security |
| Whisper (OpenAI) | https://openai.com/research/whisper | — | — | — | — | Trascrizione audio — Open Source — Audio AI |
| Windsurf | https://windsurf.ai | — | — | — | Freemium | AI Code |
| Yi Chat | https://www.yi.ai | — | — | — | Freemium | 01.AI — LLM |
| You.com | https://you.com | — | — | — | Freemium | Search+LLM |

### 12.4 Automazione, Dev & Produttività (149)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Activepieces | https://www.activepieces.com | — | — | — | Freemium | Alternativa Zapier — Open Source — Automazione |
| Airtable | https://airtable.com | — | — | — | Freemium | No-code database — Database/Spreadsheet |
| Apache Airflow | https://airflow.apache.org | — | — | — | Open Source | Workflow |
| Apify | https://apify.com | — | — | — | — | Scraping e automazione — Freemium — Web Scraping |
| Appwrite | https://appwrite.io | — | — | — | Open Source | Backend |
| Asana | https://asana.com | — | — | — | Freemium | Project mgmt |
| Asharq Al-Awsat | https://english.aawsat.com | — | EN/AR | — | — | Pan-Arab KSA |
| AWS Bedrock | https://aws.amazon.com/bedrock | — | — | — | A pagamento | Amazon — API |
| Azure OpenAI | https://azure.microsoft.com/ai-services/openai | — | — | — | A pagamento | Microsoft — API |
| Baserow | https://baserow.io | — | — | — | Open Source | No-code DB |
| BeautifulSoup4 | https://pypi.org/project/beautifulsoup4 | — | — | — | — | HTML parsing — Open Source — Python lib |
| Beehiiv | https://www.beehiiv.com | — | — | — | Freemium | Newsletter |
| Bitbucket | https://bitbucket.org | — | — | — | Freemium | Atlassian — Code hosting |
| Bloomberg | https://www.bloomberg.com | — | EN | — | — | Finanza e politica |
| Bloomberg Green | https://www.bloomberg.com/green | — | — | — | — | Sostenibilità Bloomberg — Globale — News |
| Bloomberg Markets | https://www.bloomberg.com/markets | — | — | Globale | — | Mercati finanziari |
| Bolt.new | https://bolt.new | — | — | — | Freemium | AI App Builder |
| Brevo | https://www.brevo.com | — | — | — | Freemium | Sendinblue — Email |
| Browserless | https://www.browserless.io | — | — | — | — | Browser automation — Freemium — Web Scraping |
| Bruno | https://www.usebruno.com | — | — | — | Open Source | API testing |
| Businessweek | https://www.bloomberg.com/businessweek | — | EN | — | — | Settimanale Bloomberg — USA |
| Calendly | https://calendly.com | — | — | — | Freemium | Scheduling |
| Camelot | https://camelot-py.readthedocs.io | — | — | — | Open Source | PDF tabelle Python — Data Extract |
| Canva AI | https://www.canva.com/ai-image-generator | — | — | — | Freemium | Creative AI |
| Censys Python | https://github.com/censys/censys-python | — | — | — | Freemium | Library |
| Cloudflare Pages | https://pages.cloudflare.com | — | — | — | Freemium | Deploy web — Hosting |
| Codeium | https://codeium.com | — | — | — | Freemium | AI Code |
| Copilot | https://copilot.microsoft.com | — | — | — | Freemium | Microsoft — LLM + Search |
| Creepy | https://github.com/ilektrojohn/creepy | — | — | — | — | Geoloc da social — Open Source — Geolocation |
| DataGrip | https://www.jetbrains.com/datagrip | — | — | — | A pagamento | JetBrains — DB client |
| DBeaver | https://dbeaver.io | — | — | — | Open Source | DB client |
| Deck.gl | https://deck.gl | — | — | — | Open Source | GIS viz |
| Discord | https://discord.com | — | — | — | Freemium | Team comm. |
| DocumentCloud | https://www.documentcloud.org | — | — | — | — | Analisi documenti giornalisti — Freemium — Doc Analysis |
| Dola | https://www.dola.com | — | — | — | Freemium | Assistant personale — AI Assistant |
| Dolt | https://www.dolthub.com | — | — | — | Open Source | Git+SQL — DB versionato |
| DuckDB | https://duckdb.org | — | — | — | Open Source | In-process SQL |
| ESLint | https://eslint.org | — | — | — | — | Open Source — Linter — JS |
| Excalidraw | https://excalidraw.com | — | — | — | Open Source | Whiteboard — Sketch |
| Feedbin | https://feedbin.com | — | — | — | — | RSS premium — A pagamento — RSS Reader |
| Feedly | https://feedly.com | — | — | — | Freemium | Aggregatore RSS — RSS Reader |
| FigJam | https://www.figma.com/figjam | — | — | — | Freemium | Whiteboard |
| Figma | https://www.figma.com | — | — | — | Freemium | Design |
| Fly.io | https://fly.io | — | — | — | Freemium | Hosting |
| Framer | https://www.framer.com | — | — | — | Freemium | No-code web |
| FreshRSS | https://freshrss.org | — | — | — | Open Source | RSS self-hosted — RSS Reader |
| Gamma | https://gamma.app | — | — | — | Freemium | Slides con AI — Presentazioni AI |
| GDAL | https://gdal.org | — | — | — | Open Source | GIS |
| Ghost | https://ghost.org | — | — | — | Open Source | Newsletter — CMS |
| GitHub Copilot | https://github.com/features/copilot | — | — | — | A pagamento | Microsoft — AI Coding |
| GitLab | https://gitlab.com | — | — | — | Freemium | Alternativa a GitHub — Code Hosting |
| Google Looker Studio | https://lookerstudio.google.com | — | — | — | Gratuito | Dashboard e report — Data Viz |
| Gradio | https://www.gradio.app | — | — | — | Open Source | Python AI — Data app |
| Holehe | https://github.com/megadose/holehe | — | — | — | Open Source | Email OSINT |
| HTTPie | https://httpie.io | — | — | — | Freemium | API testing |
| Huginn | https://github.com/huginn/huginn | — | — | — | — | Agent autonomi — Open Source — Automazione |
| IFTTT | https://ifttt.com | — | — | — | Freemium | Applet semplici — Automazione |
| Inoreader | https://www.inoreader.com | — | — | — | Freemium | RSS avanzato — RSS Reader |
| Insomnia | https://insomnia.rest | — | — | — | Open Source | API testing |
| Instapaper | https://www.instapaper.com | — | — | — | Freemium | Read later |
| Intel Owl | https://github.com/intelowlproject/IntelOwl | — | — | — | Open Source | Threat analysis — Platform |
| Jira | https://www.atlassian.com/software/jira | — | — | — | Freemium | Project mgmt |
| Kashmir Observer | https://kashmirobserver.net | — | EN | — | — | Kashmir |
| Kepler.gl | https://kepler.gl | — | — | — | Open Source | GIS viz |
| Linear | https://linear.app | — | — | — | Freemium | Project mgmt |
| Logseq | https://logseq.com | — | — | — | Open Source | Note grafo — Knowledge |
| Loom | https://www.loom.com | — | — | — | Freemium | Screen rec. — Video async |
| Lovable | https://lovable.dev | — | — | — | Freemium | Creazione app con AI — AI App Builder |
| Maigret | https://github.com/soxoj/maigret | — | — | — | Open Source | Username hunt |
| Mailchimp | https://mailchimp.com | — | — | — | Freemium | Email |
| Make | https://www.make.com | — | — | — | Freemium | Ex-Integromat — Automazione |
| Manus | https://manus.im | — | — | — | Waitlist | Agent autonomi — AI Agent |
| Matter | https://hq.getmatter.com | — | — | — | — | Reader e highlights — Freemium — Reading |
| Mattermost | https://mattermost.com | — | — | — | Open Source | Team comm. |
| Mendeley | https://www.mendeley.com | — | — | — | Freemium | Elsevier — Reference |
| Metabase | https://www.metabase.com | — | — | — | Open Source | Data viz |
| Miro | https://miro.com | — | — | — | Freemium | Whiteboard |
| Monday.com | https://monday.com | — | — | — | Freemium | Project mgmt |
| Money Stuff (Levine) | https://www.bloomberg.com/opinion/authors/ARbTQlRLRjE/matthew-s-levine | — | — | US | — | Newsletter Bloomberg — USA |
| n8n | https://n8n.io | — | — | — | Self-hosted | Workflow automation — Automazione |
| Netlify | https://www.netlify.com | — | — | — | Freemium | Deploy web — Hosting |
| NetNewsWire | https://netnewswire.com | — | — | — | Gratuito | Mac/iOS — RSS Reader |
| NewsBlur | https://www.newsblur.com | — | — | — | — | RSS social — Freemium — RSS Reader |
| NocoDB | https://nocodb.com | — | — | — | Open Source | No-code DB |
| Notion | https://www.notion.so | — | — | — | Freemium | Documenti e database — Workspace |
| Observable | https://observablehq.com | — | — | — | Freemium | D3/JS — Data viz |
| Obsidian | https://obsidian.md | — | — | — | Freemium | Note e connessioni — Knowledge |
| Omnivore | https://omnivore.app | — | — | — | Open Source | Read later |
| OpenRefine | https://openrefine.org | — | — | — | Open Source | Pulizia dati — Data Cleaning |
| Overview | https://www.overviewdocs.com | — | — | — | — | Cluster documenti — Gratuito — Doc Analysis |
| pandas | https://pandas.pydata.org | — | — | — | Open Source | Analisi dati Python — Python lib |
| Panel | https://panel.holoviz.org | — | — | — | Open Source | Python — Data app |
| pdfplumber | https://github.com/jsvine/pdfplumber | — | — | — | — | PDF Python — Open Source — Data Extract |
| Penpot | https://penpot.app | — | — | — | Open Source | Design |
| Pinpoint | https://journaliststudio.google.com/pinpoint | — | — | — | — | Google giornalisti — Gratuito — Doc Analysis |
| Pipedream | https://pipedream.com | — | — | — | Freemium | API integrations — Automazione |
| PlanetScale | https://planetscale.com | — | — | — | Database | MySQL serverless — Freemium |
| Playwright | https://playwright.dev | — | — | — | — | Browser automation — Open Source — Testing/Scraping |
| Plotly Dash | https://dash.plotly.com | — | — | — | Open Source | Python — Data viz |
| Pocket | https://getpocket.com | — | — | — | Freemium | Mozilla — Read later |
| PocketBase | https://pocketbase.io | — | — | — | Open Source | Backend |
| Polars | https://www.pola.rs | — | — | — | Open Source | Python — Data library |
| Postman | https://www.postman.com | — | — | — | Freemium | API testing |
| Prefect | https://www.prefect.io | — | — | — | Freemium | Data — Workflow |
| Prettier | https://prettier.io | — | — | — | Open Source | Formatter |
| Puppeteer | https://pptr.dev | — | — | — | — | Chrome automation — Open Source — Scraping |
| QGIS | https://qgis.org | — | — | — | Open Source | Mappe — GIS |
| R/RStudio | https://posit.co | — | — | — | — | Analisi statistica — Open Source — Statistiche |
| Railway | https://railway.app | — | — | — | Freemium | Backend deploy — Cloud Deploy |
| Readwise | https://readwise.io | — | — | — | — | Evidenziazioni e review — A pagamento — Reading |
| Readwise Reader | https://readwise.io/read | — | — | — | Freemium | RSS+Read |
| Reclaim AI | https://reclaim.ai | — | — | — | Freemium | Scheduling |
| Redash | https://redash.io | — | — | — | Open Source | Data viz |
| Reeder | https://reederapp.com | — | — | — | — | Client RSS Apple — A pagamento — RSS Reader |
| Render | https://render.com | — | — | — | Freemium | Web services — Cloud Deploy |
| Replit AI | https://replit.com | — | — | — | Freemium | AI Dev |
| Roam Research | https://roamresearch.com | — | — | — | A pagamento | Note bidirezionali — Knowledge |
| RSSBridge | https://rss-bridge.org | — | — | — | Open Source | Crea RSS da siti — RSS Generator |
| Scrapy | https://scrapy.org | — | — | — | — | Web scraping — Open Source — Framework |
| Sherlock | https://github.com/sherlock-project/sherlock | — | — | — | Open Source | Social media — Username hunt |
| Shodan CLI | https://github.com/achillean/shodan-python | — | — | — | Freemium | Shodan da terminale — CLI Tool |
| Slack | https://slack.com | — | — | — | Freemium | Team comm. |
| SQLite | https://www.sqlite.org | — | — | — | Open Source | DB |
| STIX/TAXII | https://oasis-open.github.io/cti-documentation | — | — | — | Pubblico | Threat intel formato — Standard |
| Subfinder | https://github.com/projectdiscovery/subfinder | — | — | — | Open Source | Subdomain |
| Substack | https://substack.com | — | — | — | Freemium | Newsletter |
| Supabase | https://supabase.com | — | — | — | Freemium | Database open source — Database |
| Superset | https://superset.apache.org | — | — | — | Open Source | Apache — Data viz |
| TablePlus | https://tableplus.com | — | — | — | Freemium | DB client |
| Tabnine | https://www.tabnine.com | — | — | — | Freemium | AI Code |
| Tabula | https://tabula.technology | — | — | — | Open Source | PDF tabelle — Data Extract |
| Tally | https://tally.so | — | — | — | Freemium | Survey |
| Tella | https://tella.tv | — | — | — | Freemium | Video async |
| Temporal | https://temporal.io | — | — | — | Open Source | Workflow |
| The Old Reader | https://theoldreader.com | — | — | — | Freemium | RSS Reader |
| theHarvester | https://github.com/laramies/theHarvester | — | — | — | Open Source | Raccolta email — Email Harvester |
| Tldraw | https://www.tldraw.com | — | — | — | Open Source | Sketch |
| Trello | https://trello.com | — | — | — | Freemium | Kanban — Project mgmt |
| Typeform | https://www.typeform.com | — | — | — | Freemium | Survey |
| v0 (Vercel) | https://v0.dev | — | — | — | — | Freemium — AI App Builder |
| Vega-Altair | https://altair-viz.github.io | — | — | — | Open Source | Python — Data viz |
| Vercel | https://vercel.com | — | — | — | Freemium | Serverless functions — Hosting/Deploy |
| Vercel AI SDK | https://sdk.vercel.ai | — | — | — | Open Source | Framework |
| Vijesti Montenegro | https://en.vijesti.me | — | — | ME | — | Quality — Montenegro |
| Webflow | https://webflow.com | — | — | — | Freemium | No-code web |
| Windmill | https://www.windmill.dev | — | — | — | Open Source | Script e workflow — Dev Platform |
| Zapier | https://zapier.com | — | — | — | Freemium | Workflow no-code — Automazione |
| Zotero | https://www.zotero.org | — | — | — | Open Source | Ricerca — Reference |
| Awesome Public Datasets | https://github.com/awesomedata/awesome-public-datasets | — | — | — | — | Lista curata di dataset pubblici per tema — Gratuito — Lista GitHub |

---

### 12.5 Borse Valori & Mercati (67)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ADX — Abu Dhabi Securities Exchange | https://www.adx.ae | — | AR/EN | AE | — | Borsa di Abu Dhabi |
| ASE — Amman Stock Exchange | https://www.ase.com.jo | — | AR/EN | JO | — | Borsa giordana |
| ASX — Australian Securities Exchange | https://www.asx.com.au | — | EN | AU | — | Borsa australiana |
| ATHEX — Athens Exchange Group | https://www.athexgroup.gr | — | EL/EN | GR | — | Borsa di Atene |
| B3 — Brasil Bolsa Balcão | https://www.b3.com.br | — | PT/EN | BR | — | Borsa brasiliana |
| Bahrain Bourse | https://www.bahrainbourse.com | — | AR/EN | BH | — | Borsa del Bahrein |
| BELEX — Belgrade Stock Exchange | https://www.belex.rs | — | SR/EN | RS | — | Borsa di Belgrado |
| BME — Bolsas y Mercados Españoles | https://www.bolsasymercados.es | — | ES/EN | ES | — | Borse spagnole |
| BMV — Bolsa Mexicana de Valores | https://www.bmv.com.mx | — | ES/EN | MX | — | Borsa messicana |
| Bolsa de Santiago | https://www.bolsadesantiago.com | — | ES | CL | — | Borsa cilena |
| Borsa Istanbul | https://www.borsaistanbul.com | — | TR/EN | TR | — | Borsa turca |
| Boursa Kuwait | https://www.boursakuwait.com.kw | — | AR/EN | KW | — | Borsa kuwaitiana |
| Bourse de Casablanca | https://www.casablanca-bourse.com | — | FR/AR/EN | MA | — | Borsa marocchina |
| BRVM | https://www.brvm.org | — | FR | Africa Occ. | — | Borsa regionale UEMOA (8 Paesi) |
| BSE India | https://www.bseindia.com | — | EN | IN | — | Bombay Stock Exchange |
| BSE — Budapest Stock Exchange | https://www.bse.hu | — | HU/EN | HU | — | Borsa di Budapest |
| Bursa Malaysia | https://www.bursamalaysia.com | — | EN/MS | MY | — | Borsa malese |
| BVB — Bucharest Stock Exchange | https://www.bvb.ro | — | RO/EN | RO | — | Borsa di Bucarest |
| BVC — Bolsa de Valores de Colombia | https://www.bvc.com.co | — | ES | CO | — | Borsa colombiana |
| BVL — Bolsa de Valores de Lima | https://www.bvl.com.pe | — | ES/EN | PE | — | Borsa peruviana |
| BYMA — Bolsas y Mercados Argentinos | https://www.byma.com.ar | — | ES | AR | — | Borsa argentina |
| Cboe Global Markets | https://www.cboe.com | — | EN | US | — | Borsa opzioni e azioni |
| CME Group | https://www.cmegroup.com | — | EN | US | — | Derivati e futures |
| CSE — Colombo Stock Exchange | https://www.cse.lk | — | EN | LK | — | Borsa dello Sri Lanka |
| Deutsche Börse | https://www.deutsche-boerse.com | — | DE/EN | DE | — | Borsa di Francoforte / Xetra |
| DFM — Dubai Financial Market | https://www.dfm.ae | — | AR/EN | AE | — | Borsa di Dubai |
| DSE — Dhaka Stock Exchange | https://www.dsebd.org | — | EN/BN | BD | — | Borsa del Bangladesh |
| EGX — Egyptian Exchange | https://www.egx.com.eg | — | AR/EN | EG | — | Borsa egiziana |
| Euronext | https://www.euronext.com | — | EN | EU | — | Borse Parigi, Amsterdam, Bruxelles, Milano, Lisbona, Dublino, Oslo |
| Finnhub | https://finnhub.io | — | EN | Globale | Freemium | Market data API — azioni, FX, crypto, fondamentali |
| GPW — Warsaw Stock Exchange | https://www.gpw.pl | — | PL/EN | PL | — | Borsa di Varsavia |
| GSE — Ghana Stock Exchange | https://gse.com.gh | — | EN | GH | — | Borsa ghanese |
| HKEX — Hong Kong Exchanges | https://www.hkex.com.hk | — | EN/ZH | HK | — | Borsa di Hong Kong |
| HOSE — Ho Chi Minh Stock Exchange | https://www.hsx.vn | — | VI/EN | VN | — | Borsa vietnamita |
| ICE — Intercontinental Exchange | https://www.theice.com | — | EN | US | — | Gruppo borsistico (NYSE, futures) |
| IDX — Indonesia Stock Exchange | https://www.idx.co.id | — | ID/EN | ID | — | Borsa indonesiana |
| Jamaica Stock Exchange | https://www.jamstockex.com | — | EN | JM | — | Borsa giamaicana |
| JPX — Japan Exchange Group | https://www.jpx.co.jp | — | JA/EN | JP | — | Borsa di Tokyo/Osaka |
| JSE — Johannesburg Stock Exchange | https://www.jse.co.za | — | EN | ZA | — | Borsa sudafricana |
| KASE — Kazakhstan Stock Exchange | https://kase.kz | — | KK/RU/EN | KZ | — | Borsa kazaka |
| KRX — Korea Exchange | https://www.krx.co.kr | — | KO/EN | KR | — | Borsa coreana |
| LJSE — Ljubljana Stock Exchange | https://ljse.si | — | SL/EN | SI | — | Borsa di Lubiana |
| LSE — London Stock Exchange | https://www.londonstockexchange.com | — | EN | GB | — | Borsa di Londra |
| MOEX — Moscow Exchange | https://www.moex.com | — | RU/EN | RU | — | Borsa di Mosca |
| MSX — Muscat Stock Exchange | https://www.msx.om | — | AR/EN | OM | — | Borsa omanita |
| Nasdaq Nordic | https://www.nasdaqomxnordic.com | — | EN | Nordics | — | Borse Stoccolma, Helsinki, Copenaghen, Islanda, Baltici |
| NGX — Nigerian Exchange | https://ngxgroup.com | — | EN | NG | — | Borsa nigeriana |
| NSE Kenya — Nairobi Securities Exchange | https://www.nse.co.ke | — | EN | KE | — | Borsa keniota |
| NSE — National Stock Exchange of India | https://www.nseindia.com | — | EN | IN | — | Borsa indiana principale |
| NYSE | https://www.nyse.com | — | EN | US | — | New York Stock Exchange |
| NZX — New Zealand's Exchange | https://www.nzx.com | — | EN | NZ | — | Borsa neozelandese |
| PSE — Philippine Stock Exchange | https://www.pse.com.ph | — | EN | PH | — | Borsa filippina |
| PSE — Prague Stock Exchange | https://www.pse.cz | — | CS/EN | CZ | — | Borsa di Praga |
| PSX — Pakistan Stock Exchange | https://www.psx.com.pk | — | EN | PK | — | Borsa pakistana |
| QSE — Qatar Stock Exchange | https://www.qe.com.qa | — | AR/EN | QA | — | Borsa del Qatar |
| Saudi Exchange (Tadawul) | https://www.saudiexchange.sa | — | AR/EN | SA | — | Borsa saudita |
| SET — Stock Exchange of Thailand | https://www.set.or.th | — | TH/EN | TH | — | Borsa thailandese |
| SGX — Singapore Exchange | https://www.sgx.com | — | EN | SG | — | Borsa di Singapore |
| SIX Swiss Exchange | https://www.six-group.com | — | DE/EN | CH | — | Borsa svizzera |
| SSE — Shanghai Stock Exchange | https://www.sse.com.cn | — | ZH/EN | CN | — | Borsa di Shanghai |
| SZSE — Shenzhen Stock Exchange | https://www.szse.cn | — | ZH/EN | CN | — | Borsa di Shenzhen |
| TASE — Tel Aviv Stock Exchange | https://www.tase.co.il | — | HE/EN | IL | — | Borsa israeliana |
| TSX — Toronto Stock Exchange | https://www.tsx.com | — | EN/FR | CA | — | Borsa di Toronto |
| TWSE — Taiwan Stock Exchange | https://www.twse.com.tw | — | ZH/EN | TW | — | Borsa di Taiwan |
| WFE — World Federation of Exchanges | https://www.world-exchanges.org | — | EN | Globale | — | Federazione mondiale delle borse |
| Wiener Börse | https://www.wienerborse.at | — | DE/EN | AT | — | Borsa di Vienna |
| ZSE — Zagreb Stock Exchange | https://zse.hr | — | HR/EN | HR | — | Borsa di Zagabria |

### 12.6 Autorità Data Protection & Privacy (46)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AAIP Argentina | https://www.argentina.gob.ar/aaip | — | ES | AR | — | Agenzia accesso informazione pubblica/privacy |
| AEPD | https://www.aepd.es | — | ES | ES | — | Autorità privacy spagnola |
| AKI — Andmekaitse Inspektsioon | https://www.aki.ee | — | ET/EN | EE | — | Autorità privacy estone |
| ANPD Brasil | https://www.gov.br/anpd | — | PT | BR | — | Autorità privacy brasiliana (LGPD) |
| ANSPDCP | https://www.dataprotection.ro | — | RO | RO | — | Autorità privacy rumena |
| AP — Autoriteit Persoonsgegevens | https://www.autoriteitpersoonsgegevens.nl | — | NL | NL | — | Autorità privacy olandese |
| APD/GBA — Autorité de protection des données | https://www.autoriteprotectiondonnees.be | — | FR/NL | BE | — | Autorità privacy belga |
| AZOP | https://azop.hr | — | HR/EN | HR | — | Autorità privacy croata |
| BfDI | https://www.bfdi.bund.de | — | DE/EN | DE | — | Garante federale tedesco |
| CNIL | https://www.cnil.fr | — | FR | FR | — | Autorità privacy francese |
| CNPD Luxembourg | https://cnpd.public.lu | — | FR/EN | LU | — | Autorità privacy lussemburghese |
| CNPD Portugal | https://www.cnpd.pt | — | PT | PT | — | Autorità privacy portoghese |
| Commissioner for Personal Data Protection (Cipro) | https://www.dataprotection.gov.cy | — | EL/EN | CY | — | Autorità privacy cipriota |
| CPDP | https://www.cpdp.bg | — | BG/EN | BG | — | Autorità privacy bulgara |
| Datatilsynet (Danimarca) | https://www.datatilsynet.dk | — | DA | DK | — | Autorità privacy danese |
| Datatilsynet (Norvegia) | https://www.datatilsynet.no | — | NO/EN | NO | — | Autorità privacy norvegese |
| DPC — Data Protection Commission | https://www.dataprotection.ie | — | EN | IE | — | Autorità privacy irlandese (lead per Big Tech) |
| DSB — Datenschutzbehörde | https://www.dsb.gv.at | — | DE | AT | — | Autorità privacy austriaca |
| DVI — Datu valsts inspekcija | https://www.dvi.gov.lv | — | LV/EN | LV | — | Autorità privacy lettone |
| EDPB — European Data Protection Board | https://www.edpb.europa.eu | — | EN | EU | — | Comitato europeo protezione dati |
| EDPS — European Data Protection Supervisor | https://www.edps.europa.eu | — | EN | EU | — | Garante UE per le istituzioni |
| FDPIC / IFPDT | https://www.edoeb.admin.ch | — | DE/FR/IT/EN | CH | — | Garante privacy svizzero |
| GPA — Global Privacy Assembly | https://globalprivacyassembly.org | — | EN | Globale | — | Rete mondiale autorità privacy |
| HDPA — Hellenic DPA | https://www.dpa.gr | — | EL/EN | GR | — | Autorità privacy greca |
| ICO — Information Commissioner's Office | https://ico.org.uk | — | EN | GB | — | Autorità privacy britannica |
| IDPC Malta | https://idpc.org.mt | — | EN/MT | MT | — | Autorità privacy maltese |
| IMY — Integritetsskyddsmyndigheten | https://www.imy.se | — | SV/EN | SE | — | Autorità privacy svedese |
| Information Regulator (South Africa) | https://inforegulator.org.za | — | EN | ZA | — | Autorità privacy sudafricana (POPIA) |
| IP — Informacijski pooblaščenec | https://www.ip-rs.si | — | SL/EN | SI | — | Autorità privacy slovena |
| KVKK | https://www.kvkk.gov.tr | — | TR/EN | TR | — | Autorità privacy turca |
| NAIH | https://naih.hu | — | HU/EN | HU | — | Autorità privacy ungherese |
| NDPC Nigeria | https://ndpc.gov.ng | — | EN | NG | — | Commissione protezione dati nigeriana |
| OAIC | https://www.oaic.gov.au | — | EN | AU | — | Autorità privacy australiana |
| ODPC Kenya | https://www.odpc.go.ke | — | EN | KE | — | Ufficio protezione dati keniota |
| OPC Canada | https://www.priv.gc.ca | — | EN/FR | CA | — | Garante privacy federale canadese |
| OPC New Zealand | https://www.privacy.org.nz | — | EN | NZ | — | Autorità privacy neozelandese |
| PCPD Hong Kong | https://www.pcpd.org.hk | — | EN/ZH | HK | — | Autorità privacy di Hong Kong |
| PDPC Singapore | https://www.pdpc.gov.sg | — | EN | SG | — | Autorità privacy di Singapore |
| Persónuvernd | https://www.personuvernd.is | — | IS/EN | IS | — | Autorità privacy islandese |
| PIPC Korea | https://www.pipc.go.kr | — | KO/EN | KR | — | Autorità privacy sudcoreana |
| PPC — Personal Information Protection Commission | https://www.ppc.go.jp | — | JA/EN | JP | — | Autorità privacy giapponese |
| Tietosuojavaltuutettu | https://tietosuoja.fi | — | FI/EN | FI | — | Autorità privacy finlandese |
| UODO | https://uodo.gov.pl | — | PL | PL | — | Autorità privacy polacca |
| VDAI | https://vdai.lrv.lt | — | LT/EN | LT | — | Autorità privacy lituana |
| ÚOOÚ | https://uoou.gov.cz | — | CS/EN | CZ | — | Autorità privacy ceca |
| Úrad na ochranu osobných údajov SR | https://dataprotection.gov.sk | — | SK/EN | SK | — | Autorità privacy slovacca |

### 12.7 Dogane, Trade & Export Control (28)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Agenzia Dogane e Monopoli | https://www.adm.gov.it | — | IT | IT | — | Dogane italiane |
| Australia Group | https://www.dfat.gov.au/publications/minisite/theaustraliagroupnet/site/en/index.html | — | EN | Globale | — | Regime controllo chimico/biologico |
| Brazil Comex Stat | https://comexstat.mdic.gov.br | — | PT/EN | BR | — | Statistiche commercio estero brasiliane |
| Canada CBSA | https://www.cbsa-asfc.gc.ca | — | EN/FR | CA | — | Dogane canadesi |
| China Customs (GACC) | https://english.customs.gov.cn | — | ZH/EN | CN | — | Dogane cinesi, statistiche import/export |
| CITES Trade Database | https://trade.cites.org | — | EN | Globale | — | Database commercio specie CITES — traffico fauna selvatica |
| EU Access2Markets | https://trade.ec.europa.eu/access-to-markets | — | Multi | EU | — | Tariffe, regole origine, barriere UE |
| Export.gov / Trade.gov | https://www.trade.gov | — | EN | US | — | Portale commercio internazionale USA — market intelligence |
| GTA — Global Trade Alert | https://www.globaltradealert.org | — | EN | Globale | — | Monitor misure commerciali discriminatorie per Paese |
| HMRC UK Trade Tariff | https://www.trade-tariff.service.gov.uk | — | EN | GB | — | Tariffa doganale UK post-Brexit — classificazione merci |
| ImportGenius | https://www.importgenius.com | — | EN | Globale | — | Bill of lading USA e LatAm (commerciale) |
| India CBIC | https://www.cbic.gov.in | — | EN/HI | IN | — | Dogane e imposte indirette indiane |
| ITC Market Access Map | https://www.macmap.org | — | EN | Globale | — | Tariffe e misure non tariffarie |
| ITC Trade Map | https://www.trademap.org | — | EN | Globale | — | Statistiche commercio per prodotto/Paese |
| Japan Customs | https://www.customs.go.jp | — | JA/EN | JP | — | Dogane giapponesi |
| MTCR — Missile Technology Control Regime | https://www.mtcr.info | — | EN | Globale | — | Regime controllo tecnologia missilistica |
| NSG — Nuclear Suppliers Group | https://www.nuclearsuppliersgroup.org | — | EN | Globale | — | Regime controllo nucleare |
| OEC — Observatory of Economic Complexity | https://oec.world | — | EN | Globale | — | Visualizzazione flussi commerciali |
| Panjiva (S&P Global) | https://panjiva.com | — | EN | Globale | — | Dati spedizioni import/export (commerciale) |
| Trade Data Monitor | https://tradedatamonitor.com | — | EN | Globale | — | Dati commercio globale granulari (Freemium) |
| US BIS — Bureau of Industry and Security | https://www.bis.doc.gov | — | EN | US | — | Export control, Entity List, EAR |
| US CBP — Customs and Border Protection | https://www.cbp.gov | — | EN | US | — | Dogane statunitensi |
| US DDTC — Directorate of Defense Trade Controls | https://www.pmddtc.state.gov | — | EN | US | — | ITAR, esportazioni difesa |
| USTR — US Trade Representative | https://ustr.gov | — | EN | US | — | Politica commerciale USA, Section 301 |
| Volza | https://www.volza.com | — | EN | Globale | — | Dati EXIM globali (commerciale) |
| Wassenaar Arrangement | https://www.wassenaar.org | — | EN | Globale | — | Regime export control dual-use e armi convenzionali |
| WCO — World Customs Organization | https://www.wcoomd.org | — | EN/FR | Globale | — | Organizzazione mondiale dogane, HS nomenclature |
| WITS — World Integrated Trade Solution | https://wits.worldbank.org | — | EN | Globale | — | Dati commercio Banca Mondiale |

### 12.8 Marittimo, Aviazione & Trasporti (51)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ABS — American Bureau of Shipping | https://www.eagle.org | — | EN | Globale | — | Società di classificazione |
| AISStream | https://aisstream.io | — | EN | Globale | Gratuito | AIS navi real-time via WebSocket (API key gratuita) — complemento marittimo a OpenSky |
| Aviation Safety Network | https://asn.flightsafety.org | — | EN | Globale | — | Database incidenti aerei |
| ch-aviation | https://www.ch-aviation.com | — | EN | Globale | — | Database flotte e compagnie (commerciale) |
| ClassNK | https://www.classnk.or.jp | — | EN/JA | Globale | — | Società di classificazione giapponese |
| DNV | https://www.dnv.com | — | EN | Globale | — | Società di classificazione e registro navi |
| DP World | https://www.dpworld.com | — | EN | AE | — | Operatore portuale globale (Dubai) |
| EASA | https://www.easa.europa.eu | — | EN | EU | — | Agenzia UE sicurezza aerea, AD e certificazioni |
| ENAC | https://www.enac.gov.it | — | IT | IT | — | Ente nazionale aviazione civile |
| Equasis | https://www.equasis.org | — | EN | Globale | — | Profili navi, PSC, gestori — gratuito |
| ESPO | https://www.espo.be | — | EN | EU | — | Organizzazione porti europei |
| FAA | https://www.faa.gov | — | EN | US | — | Aviazione civile USA, registro N-number |
| gCaptain | https://gcaptain.com | — | EN | Globale | — | News marittime |
| Hafen Hamburg | https://www.hafen-hamburg.de | — | DE/EN | DE | — | Porto di Amburgo |
| HAROPA Port | https://www.haropaport.com | — | FR/EN | FR | — | Le Havre-Rouen-Parigi |
| Hellenic Shipping News | https://www.hellenicshippingnews.com | — | EN | Globale | — | Aggregatore news shipping |
| IACS | https://iacs.org.uk | — | EN | Globale | — | Associazione società di classificazione |
| IAPH | https://www.iaphworldports.org | — | EN | Globale | — | Associazione mondiale porti |
| IATA | https://www.iata.org | — | EN | Globale | — | Associazione compagnie aeree |
| ICAO | https://www.icao.int | — | EN/Multi | Globale | — | Organizzazione aviazione civile internazionale |
| IMO GISIS | https://gisis.imo.org | — | EN | Globale | — | Database navi, incidenti, port facilities IMO |
| IMO — International Maritime Organization | https://www.imo.int | — | EN | Globale | — | Organizzazione marittima internazionale |
| KPA — Kenya Ports Authority | https://www.kpa.co.ke | — | EN | KE | — | Porto di Mombasa |
| Liberian Registry (LISCR) | https://www.liscr.com | — | EN | LR | — | Registro navale liberiano |
| Lloyd's List | https://www.lloydslist.com | — | EN | Globale | — | Testata shipping storica (commerciale) |
| Lloyd's Register | https://www.lr.org | — | EN | Globale | — | Società di classificazione |
| Marine Department HK | https://www.mardep.gov.hk | — | EN/ZH | HK | — | Dipartimento marittimo HK |
| Marshall Islands Registry (IRI) | https://www.register-iri.com | — | EN | MH | — | Registro navale Isole Marshall |
| MPA Singapore | https://www.mpa.gov.sg | — | EN | SG | — | Autorità marittima e portuale |
| Nigerian Ports Authority | https://nigerianports.gov.ng | — | EN | NG | — | Autorità portuale nigeriana |
| OpenSky Network | https://opensky-network.org | — | EN | Globale | — | Dati ADS-B open per ricerca |
| Panama Maritime Authority (AMP) | https://amp.gob.pa | — | ES/EN | PA | — | Registro navale panamense |
| Paris MoU | https://parismou.org | — | EN | Europa | — | Port State Control, liste bianche/nere bandiere |
| Piraeus Port Authority | https://www.olp.gr | — | EL/EN | GR | — | Porto del Pireo (COSCO) |
| Planespotters | https://www.planespotters.net | — | EN | Globale | — | Database flotte e storia aeromobili |
| Port Authority NY & NJ | https://www.panynj.gov | — | EN | US | — | Autorità portuale NY/NJ |
| Port of Antwerp-Bruges | https://www.portofantwerpbruges.com | — | NL/EN | BE | — | Porto di Anversa-Bruges |
| Port of Long Beach | https://polb.com | — | EN | US | — | Porto di Long Beach |
| Port of Los Angeles | https://www.portoflosangeles.org | — | EN | US | — | Primo porto container USA |
| Port of Rotterdam | https://www.portofrotterdam.com | — | NL/EN | NL | — | Primo porto europeo |
| Ports of Genoa | https://www.portsofgenoa.com | — | IT/EN | IT | — | AdSP Mar Ligure Occidentale |
| Splash247 | https://splash247.com | — | EN | Globale | — | News shipping indipendente |
| Tanger Med | https://www.tangermed.ma | — | FR/EN | MA | — | Primo porto africano |
| The Aviation Herald | https://avherald.com | — | EN | Globale | — | Incidenti e occorrenze aviazione |
| The Maritime Executive | https://maritime-executive.com | — | EN | Globale | — | News e analisi marittime |
| Tokyo MoU | https://www.tokyo-mou.org | — | EN | Asia-Pacifico | — | Port State Control Asia-Pacifico |
| TradeWinds | https://www.tradewindsnews.com | — | EN | Globale | — | News shipping |
| Transnet | https://www.transnet.net | — | EN | ZA | — | Porti e ferrovie sudafricani |
| UK CAA | https://www.caa.co.uk | — | EN | GB | — | Aviazione civile britannica, registro G-INFO |
| USCG PSIX | https://cgmix.uscg.mil | — | EN | US | — | Database ispezioni navi US Coast Guard |
| Valenciaport | https://www.valenciaport.com | — | ES/EN | ES | — | Porto di Valencia |

### 12.9 Energia & Materie Prime (50)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ACER | https://www.acer.europa.eu | — | EN | EU | — | Agenzia UE cooperazione regolatori energia |
| AEMO | https://aemo.com.au | — | EN | AU | — | Operatore mercato energia australiano |
| ANP — Agência Nacional do Petróleo | https://www.gov.br/anp | — | PT | BR | — | Regolatore petrolio e gas brasiliano |
| ARERA | https://www.arera.it | — | IT | IT | — | Autorità energia, reti e ambiente italiana |
| Argus Media | https://www.argusmedia.com | — | EN | Globale | — | Price reporting agency (commerciale) |
| Bundesnetzagentur | https://www.bundesnetzagentur.de | — | DE/EN | DE | — | Regolatore reti tedesco |
| CER — Canada Energy Regulator | https://www.cer-rec.gc.ca | — | EN/FR | CA | — | Regolatore energia canadese |
| CNMC | https://www.cnmc.es | — | ES | ES | — | Regolatore mercati e concorrenza spagnolo |
| CRE — Commission de régulation de l'énergie | https://www.cre.fr | — | FR | FR | — | Regolatore energia francese |
| EITI | https://eiti.org | — | EN | Globale | — | Trasparenza industrie estrattive |
| Ember | https://ember-energy.org | — | EN | Globale | — | Dati elettricità e transizione |
| Energy Intelligence | https://www.energyintel.com | — | EN | Globale | — | Analisi settore energia (commerciale) |
| ENTSO-E | https://www.entsoe.eu | — | EN | EU | — | Rete elettrica europea, transparency platform |
| ENTSOG | https://www.entsog.eu | — | EN | EU | — | Rete gas europea |
| EUROFER | https://www.eurofer.eu | — | EN | EU | — | Acciaio europeo |
| Federacciai | https://federacciai.it | — | IT | IT | — | Acciaio italiano |
| FERC | https://www.ferc.gov | — | EN | US | — | Regolatore federale energia USA |
| GIE — Gas Infrastructure Europe | https://www.gie.eu | — | EN | EU | — | Stoccaggi gas (AGSI) e terminali GNL (ALSI) |
| GIIGNL | https://giignl.org | — | EN | Globale | — | Importatori GNL, report annuale |
| Global Energy Monitor | https://globalenergymonitor.org | — | EN | Globale | — | Tracker centrali, gasdotti, carbone |
| IAEA | https://www.iaea.org | — | EN | Globale | — | Agenzia internazionale energia atomica |
| ICCO — International Cocoa Organization | https://www.icco.org | — | EN | Globale | — | Cacao, statistiche |
| ICMM | https://www.icmm.com | — | EN | Globale | — | Consiglio internazionale miniere e metalli |
| ICO — International Coffee Organization | https://ico.org | — | EN | Globale | — | Caffè, statistiche |
| ICSG — International Copper Study Group | https://icsg.org | — | EN | Globale | — | Rame, dati mondiali |
| IGU — International Gas Union | https://www.igu.org | — | EN | Globale | — | Unione internazionale gas, World LNG Report |
| International Aluminium Institute | https://international-aluminium.org | — | EN | Globale | — | Alluminio, statistiche |
| IRENA | https://www.irena.org | — | EN | Globale | — | Agenzia internazionale rinnovabili |
| ISO — International Sugar Organization | https://www.isosugar.org | — | EN | Globale | — | Zucchero, dati mondiali |
| JODI — Joint Organisations Data Initiative | https://www.jodidata.org | — | EN | Globale | — | Database mondiale petrolio e gas |
| Kpler | https://www.kpler.com | — | EN | Globale | — | Tracking cargo e flussi commodity (commerciale) |
| LME — London Metal Exchange | https://www.lme.com | — | EN | GB | — | Borsa metalli, prezzi di riferimento |
| Mining Weekly | https://www.miningweekly.com | — | EN | Globale | — | News minerario (Creamer Media) |
| Mining.com | https://www.mining.com | — | EN | Globale | — | News settore minerario |
| NERC | https://www.nerc.com | — | EN | US | — | Affidabilità rete elettrica nordamericana |
| NERSA | https://www.nersa.org.za | — | EN | ZA | — | Regolatore energia sudafricano |
| NRGI — Natural Resource Governance Institute | https://resourcegovernance.org | — | EN | Globale | — | Governance risorse naturali |
| NUPRC | https://www.nuprc.gov.ng | — | EN | NG | — | Regolatore upstream nigeriano |
| Ofgem | https://www.ofgem.gov.uk | — | EN | GB | — | Regolatore energia britannico |
| OilPrice.com | https://oilprice.com | — | EN | Globale | — | News e prezzi energia |
| OPEC | https://www.opec.org | — | EN | Globale | — | Organizzazione Paesi esportatori petrolio, MOMR |
| pv magazine | https://www.pv-magazine.com | — | EN | Globale | — | News fotovoltaico |
| Recharge | https://www.rechargenews.com | — | EN | Globale | — | News rinnovabili |
| Rystad Energy | https://www.rystadenergy.com | — | EN | Globale | — | Ricerca energia (commerciale) |
| Upstream | https://www.upstreamonline.com | — | EN | Globale | — | News oil & gas |
| USGS Mineral Resources | https://www.usgs.gov/programs/mineral-resources-program | — | EN | US | — | Commodity summaries minerali |
| WNA — World Nuclear Association | https://world-nuclear.org | — | EN | Globale | — | Database reattori e ciclo combustibile |
| Wood Mackenzie | https://www.woodmac.com | — | EN | Globale | — | Ricerca energia e materie prime (commerciale) |
| World Nuclear News | https://www.world-nuclear-news.org | — | EN | Globale | — | News nucleare |
| worldsteel | https://worldsteel.org | — | EN | Globale | — | Associazione mondiale acciaio, dati produzione |

### 12.10 Salute & Regolatori Farmaceutici (28)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AEMPS | https://www.aemps.gob.es | — | ES | ES | — | Regolatore farmaci spagnolo |
| Africa CDC | https://africacdc.org | — | EN/FR | Africa | — | Centro africano controllo malattie |
| AIFA | https://www.aifa.gov.it | — | IT | IT | — | Agenzia italiana del farmaco |
| ANSM | https://ansm.sante.fr | — | FR | FR | — | Regolatore farmaci francese |
| ANVISA | https://www.gov.br/anvisa | — | PT | BR | — | Regolatore sanitario brasiliano |
| BfArM | https://www.bfarm.de | — | DE/EN | DE | — | Regolatore farmaci tedesco |
| CDC — Centers for Disease Control | https://www.cdc.gov | — | EN | US | — | Centro controllo malattie USA — sorveglianza epidemie |
| CDSCO | https://cdsco.gov.in | — | EN | IN | — | Regolatore farmaci indiano |
| CEPI — Coalition for Epidemic Preparedness | https://cepi.net | — | EN | Globale | — | Coalizione preparazione epidemie — vaccini innovativi |
| ECDC | https://www.ecdc.europa.eu | — | EN | EU | — | Centro europeo controllo malattie |
| EMA — European Medicines Agency | https://www.ema.europa.eu | — | EN | EU | — | Agenzia europea farmaci |
| FDA — Food and Drug Administration | https://www.fda.gov | — | EN | US | — | Regolatore farmaci e alimenti USA |
| Gavi | https://www.gavi.org | — | EN | Globale | — | Alleanza vaccini |
| Global Fund | https://www.theglobalfund.org | — | EN | Globale | — | Fondo globale AIDS/TB/malaria |
| HPRA | https://www.hpra.ie | — | EN | IE | — | Regolatore farmaci irlandese |
| INVIMA | https://www.invima.gov.co | — | ES | CO | — | Regolatore sanitario colombiano |
| IQVIA Institute | https://www.iqvia.com/insights/the-iqvia-institute | — | EN | Globale | — | Dati mercato farmaceutico e healthcare globale |
| Medsafe | https://www.medsafe.govt.nz | — | EN | NZ | — | Regolatore farmaci neozelandese |
| MFDS | https://www.mfds.go.kr | — | KO/EN | KR | — | Regolatore farmaci e alimenti coreano |
| MSF Access Campaign | https://msfaccess.org | — | EN | Globale | — | Accesso ai farmaci nei Paesi in via di sviluppo |
| NAFDAC | https://www.nafdac.gov.ng | — | EN | NG | — | Regolatore farmaci e alimenti nigeriano |
| NMPA | https://www.nmpa.gov.cn | — | ZH | CN | — | Regolatore farmaci cinese |
| PAHO | https://www.paho.org | — | EN/ES | Americhe | — | Organizzazione panamericana sanità |
| PMDA | https://www.pmda.go.jp | — | JA/EN | JP | — | Regolatore farmaci giapponese |
| SAHPRA | https://www.sahpra.org.za | — | EN | ZA | — | Regolatore farmaci sudafricano |
| Swissmedic | https://www.swissmedic.ch | — | DE/FR/IT/EN | CH | — | Regolatore farmaci svizzero |
| TGA — Therapeutic Goods Administration | https://www.tga.gov.au | — | EN | AU | — | Regolatore farmaci australiano |
| WHO EMRO | https://www.emro.who.int | — | EN/AR | MENA | — | Ufficio OMS per il Mediterraneo orientale — dati regionali |

### 12.11 Proprietà Intellettuale & Brevetti (27)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ARIPO | https://www.aripo.org | — | EN | Africa | — | Organizzazione PI africana anglofona |
| CIPO — Canadian IP Office | https://www.ic.gc.ca/eic/site/cipointernet-internetopic.nsf/eng/home | — | EN/FR | CA | — | Ufficio PI Canada — brevetti, marchi, copyright |
| CNIPA | https://www.cnipa.gov.cn | — | ZH/EN | CN | — | Ufficio proprietà intellettuale cinese |
| DPMA | https://www.dpma.de | — | DE/EN | DE | — | Ufficio brevetti tedesco |
| EPO — European Patent Office | https://www.epo.org | — | EN/DE/FR | Europa | — | Ufficio brevetti europeo |
| Espacenet | https://worldwide.espacenet.com | — | EN | Globale | — | Ricerca brevetti mondiale (EPO) |
| EUIPO | https://www.euipo.europa.eu | — | EN/Multi | EU | — | Marchi e design UE |
| Google Patents | https://patents.google.com | — | EN | Globale | — | Ricerca brevetti gratuita |
| HKIPO — Hong Kong IP Department | https://www.ipd.gov.hk | — | EN/ZH | HK | — | Dipartimento PI Hong Kong |
| INAPI — Chile | https://www.inapi.cl | — | ES | CL | — | Istituto nazionale PI Cile |
| INPI Brasil | https://www.gov.br/inpi | — | PT | BR | — | Istituto brasiliano proprietà industriale |
| INPI France | https://www.inpi.fr | — | FR | FR | — | Istituto francese proprietà industriale |
| IP Australia | https://www.ipaustralia.gov.au | — | EN | AU | — | Ufficio PI australiano |
| IP India | https://ipindia.gov.in | — | EN | IN | — | Ufficio brevetti indiano |
| IPOS — Singapore IP Office | https://www.ipos.gov.sg | — | EN | SG | — | Ufficio PI Singapore |
| JPO — Japan Patent Office | https://www.jpo.go.jp | — | JA/EN | JP | — | Ufficio brevetti giapponese |
| KIPO | https://www.kipo.go.kr | — | KO/EN | KR | — | Ufficio brevetti coreano |
| OAPI | https://oapi.int | — | FR | Africa | — | Organizzazione PI africana francofona |
| OEPM | https://www.oepm.es | — | ES | ES | — | Ufficio brevetti spagnolo |
| PatSnap | https://www.patsnap.com | — | EN | Globale | — | Piattaforma analisi brevetti e innovazione (Freemium) |
| Rospatent | https://rospatent.gov.ru | — | RU | RU | — | Ufficio brevetti russo |
| SAIP — Saudi IP Authority | https://www.saip.gov.sa | — | AR/EN | SA | — | Autorità PI Arabia Saudita |
| The Lens | https://www.lens.org | — | EN | Globale | — | Brevetti e letteratura scientifica open |
| TMview — EUIPO Trademark Search | https://www.tmview.org | — | Multi | Globale | — | Database marchi internazionale — EUIPO |
| UIBM | https://uibm.mise.gov.it | — | IT | IT | — | Ufficio italiano brevetti e marchi |
| USPTO | https://www.uspto.gov | — | EN | US | — | Ufficio brevetti e marchi USA |
| WIPO GOLD — IP Statistics | https://www.wipo.int/ipstats | — | EN | Globale | — | Statistiche PI globali per Paese — WIPO |

### 12.12 Standard & Normazione Tecnica (26)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AENOR — Spain Standards | https://www.aenor.com | — | ES | ES | — | Ente normazione spagnolo — standard UNE |
| AFNOR | https://www.afnor.org | — | FR | FR | — | Ente normazione francese |
| ANSI | https://www.ansi.org | — | EN | US | — | Istituto standard americano |
| ASTM International | https://www.astm.org | — | EN | Globale | — | Standard tecnici internazionali |
| BSI Group | https://www.bsigroup.com | — | EN | GB | — | Ente normazione britannico |
| Bureau of Indian Standards (BIS) | https://www.bis.gov.in | — | EN/HI | IN | — | Ente normazione India — standard BIS |
| CEN-CENELEC | https://www.cencenelec.eu | — | EN | EU | — | Normazione europea |
| DIN | https://www.din.de | — | DE/EN | DE | — | Ente normazione tedesco |
| ETSI | https://www.etsi.org | — | EN | EU | — | Standard telecomunicazioni europei |
| GOST — Russia Standards | https://www.gost.ru | — | RU | RU | — | Sistema normativo russo — standard GOST |
| IEC | https://www.iec.ch | — | EN | Globale | — | Commissione elettrotecnica internazionale |
| IEEE Standards Association | https://standards.ieee.org | — | EN | Globale | — | Standard IEEE (802.x, etc.) |
| IETF | https://www.ietf.org | — | EN | Globale | — | Standard protocolli internet (RFC) |
| INMETRO Brazil | https://www.inmetro.gov.br | — | PT | BR | — | Ente metrologico e normazione Brasile |
| ISO | https://www.iso.org | — | EN/FR | Globale | — | Organizzazione internazionale normazione |
| JIS — Japanese Industrial Standards | https://www.jisc.go.jp/eng | — | EN/JA | JP | — | Ente normazione industriale giapponese |
| KATS — Korean Agency Technology Standards | https://www.kats.go.kr | — | KO/EN | KR | — | Agenzia standard tecnologici Corea del Sud |
| NEN — Netherlands Standardization | https://www.nen.nl | — | NL/EN | NL | — | Ente normazione olandese — standard NEN |
| NIST — National Institute of Standards | https://www.nist.gov | — | EN | US | — | Standard tecnici e metrologia USA |
| OASIS Open | https://www.oasis-open.org | — | EN | Globale | — | Standard aperti per cloud, IoT, sicurezza |
| SABS — South African Bureau of Standards | https://www.sabs.co.za | — | EN | ZA | — | Ufficio standard sudafricano — normazione e certificazione |
| SAC — Standardization Administration China | https://www.sac.gov.cn | — | ZH | CN | — | Ente normazione nazionale cinese |
| SIS — Swedish Institute for Standards | https://www.sis.se | — | SV/EN | SE | — | Istituto svedese per gli standard tecnici |
| SNV — Swiss Standards | https://www.snv.ch | — | DE/FR/EN | CH | — | Associazione svizzera normazione |
| UNI | https://www.uni.com | — | IT | IT | — | Ente italiano di normazione |
| W3C | https://www.w3c.org | — | EN | Globale | — | Consorzio standard web globali |

### 12.13 Antitrust & Concorrenza (29)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ACCC | https://www.accc.gov.au | — | EN | AU | — | Antitrust e consumatori australiano |
| ACM — Autoriteit Consument & Markt | https://www.acm.nl | — | NL/EN | NL | — | Antitrust e consumatori olandese |
| Autorité de la concurrence | https://www.autoritedelaconcurrence.fr | — | FR/EN | FR | — | Antitrust francese |
| Bundeskartellamt | https://www.bundeskartellamt.de | — | DE/EN | DE | — | Antitrust tedesco |
| CADE | https://www.gov.br/cade | — | PT | BR | — | Antitrust brasiliano |
| CCCS Singapore | https://www.cccs.gov.sg | — | EN | SG | — | Concorrenza e consumatori Singapore |
| CCI — Competition Commission of India | https://www.cci.gov.in | — | EN | IN | — | Antitrust indiano |
| CMA — Competition & Markets Authority | https://www.gov.uk/government/organisations/competition-and-markets-authority | — | EN | GB | — | Autorità concorrenza UK — decisioni e indagini |
| COFECE | https://www.cofece.mx | — | ES | MX | — | Antitrust messicano |
| Commerce Commission NZ | https://comcom.govt.nz | — | EN | NZ | — | Antitrust neozelandese |
| Competition Bureau Canada | https://competition-bureau.canada.ca | — | EN/FR | CA | — | Antitrust canadese |
| Competition Commission HK | https://www.compcomm.hk | — | EN/ZH | HK | — | Antitrust di Hong Kong |
| Competition Commission SA | https://www.compcom.co.za | — | EN | ZA | — | Antitrust sudafricano |
| DG COMP — Commissione Europea | https://competition-policy.ec.europa.eu | — | EN | EU | — | Direzione concorrenza UE, casi e decisioni |
| DOJ Antitrust Division | https://www.justice.gov/atr | — | EN | US | — | Divisione antitrust DOJ USA — casi e procedimenti |
| FAS Russia | https://fas.gov.ru | — | RU | RU | — | Servizio federale antimonopolio |
| FNE — Fiscalía Nacional Económica | https://www.fne.gob.cl | — | ES | CL | — | Antitrust cileno |
| FTC — Federal Trade Commission | https://www.ftc.gov | — | EN | US | — | Commissione federale commercio USA — antitrust e consumer |
| GVH — Hungarian Competition Authority | https://www.gvh.hu | — | HU/EN | HU | — | Autorità concorrenza ungherese |
| ICN — International Competition Network | https://www.internationalcompetitionnetwork.org | — | EN | Globale | — | Rete autorità concorrenza |
| Indecopi | https://www.indecopi.gob.pe | — | ES | PE | — | Concorrenza e PI peruviana |
| JFTC — Japan Fair Trade Commission | https://www.jftc.go.jp | — | JA/EN | JP | — | Antitrust giapponese |
| KFTC — Korea Fair Trade Commission | https://www.ftc.go.kr | — | KO/EN | KR | — | Antitrust coreano |
| KPPU Indonesia | https://kppu.go.id | — | ID | ID | — | Antitrust indonesiano |
| OECD Competition | https://www.oecd.org/competition | — | EN | Globale | — | Policy e analisi concorrenza OCSE — database decisioni |
| Rekabet Kurumu | https://www.rekabet.gov.tr | — | TR/EN | TR | — | Antitrust turco |
| SAMR | https://www.samr.gov.cn | — | ZH | CN | — | Regolazione mercato cinese (antitrust) |
| SIC Colombia | https://www.sic.gov.co | — | ES | CO | — | Superintendencia Industria y Comercio |
| TFTC Taiwan | https://www.ftc.gov.tw | — | ZH/EN | TW | — | Fair Trade Commission taiwanese |

### 12.14 Agenzie Fiscali & Entrate (33)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AEAT — Agencia Tributaria | https://www.agenciatributaria.es | — | ES | ES | — | Fisco spagnolo |
| Agenzia delle Entrate | https://www.agenziaentrate.gov.it | — | IT | IT | — | Agenzia fiscale italiana (e catasto) |
| ARCA (ex AFIP) | https://www.arca.gob.ar | — | ES | AR | — | Fisco argentino |
| ATO — Australian Taxation Office | https://www.ato.gov.au | — | EN | AU | — | Fisco australiano |
| Belastingdienst | https://www.belastingdienst.nl | — | NL | NL | — | Fisco olandese |
| BZSt | https://www.bzst.de | — | DE/EN | DE | — | Ufficio federale tributi tedesco |
| CIAT | https://www.ciat.org | — | ES/EN | Americhe | — | Centro interamericano amministrazioni tributarie |
| DGFiP — Impots.gouv.fr | https://www.impots.gouv.fr | — | FR | FR | — | Fisco francese |
| DIAN Colombia | https://www.dian.gov.co | — | ES | CO | — | Fisco e dogane colombiano |
| FIRS Nigeria | https://www.firs.gov.ng | — | EN | NG | — | Fisco nigeriano |
| FTA UAE | https://tax.gov.ae | — | AR/EN | AE | — | Fisco emiratino |
| FTS — Nalog.gov.ru | https://www.nalog.gov.ru | — | RU | RU | — | Fisco russo (anche EGRUL) |
| GIB Turkey | https://www.gib.gov.tr | — | TR | TR | — | Fisco turco |
| Income Tax Department (India) | https://www.incometax.gov.in | — | EN/HI | IN | — | Fisco indiano |
| Inland Revenue NZ | https://www.ird.govt.nz | — | EN | NZ | — | Fisco neozelandese |
| IOTA | https://www.iota-tax.org | — | EN | Europa | — | Organizzazione amministrazioni fiscali europee |
| IRAS Singapore | https://www.iras.gov.sg | — | EN | SG | — | Fisco di Singapore |
| IRS | https://www.irs.gov | — | EN | US | — | Internal Revenue Service |
| KRA — Kenya Revenue Authority | https://www.kra.go.ke | — | EN | KE | — | Fisco keniota |
| LHDN — Hasil Malaysia | https://www.hasil.gov.my | — | MS/EN | MY | — | Fisco malese |
| NTA — National Tax Agency | https://www.nta.go.jp | — | JA/EN | JP | — | Fisco giapponese |
| NTS Korea | https://www.nts.go.kr | — | KO/EN | KR | — | Fisco coreano |
| Receita Federal | https://www.gov.br/receitafederal | — | PT | BR | — | Fisco brasiliano (CNPJ/CPF) |
| SARS | https://www.sars.gov.za | — | EN | ZA | — | Fisco sudafricano |
| SAT México | https://www.sat.gob.mx | — | ES | MX | — | Fisco messicano |
| SII Chile | https://www.sii.cl | — | ES | CL | — | Fisco cileno |
| Skatteetaten | https://www.skatteetaten.no | — | NO/EN | NO | — | Fisco norvegese |
| Skattestyrelsen | https://skat.dk | — | DA | DK | — | Fisco danese |
| Skatteverket | https://www.skatteverket.se | — | SV/EN | SE | — | Fisco svedese |
| STA — State Taxation Administration | https://www.chinatax.gov.cn | — | ZH/EN | CN | — | Fisco cinese |
| SUNAT | https://www.sunat.gob.pe | — | ES | PE | — | Fisco e dogane peruviano, consulta RUC |
| Vero — Verohallinto | https://www.vero.fi | — | FI/EN | FI | — | Fisco finlandese |
| ZATCA | https://zatca.gov.sa | — | AR/EN | SA | — | Fisco e dogane saudita |

### 12.15 Law Enforcement & Giustizia (27)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AFP — Australian Federal Police | https://www.afp.gov.au | — | EN | AU | — | Polizia federale australiana |
| AustLII | https://www.austlii.edu.au | — | EN | AU | — | Giurisprudenza australasiatica open |
| BAILII | https://www.bailii.org | — | EN | GB/IE | — | Giurisprudenza britannica e irlandese open |
| BKA — Bundeskriminalamt | https://www.bka.de | — | DE/EN | DE | — | Polizia criminale federale tedesca |
| Bundesverfassungsgericht | https://www.bundesverfassungsgericht.de | — | DE/EN | DE | — | Corte costituzionale tedesca |
| CanLII | https://www.canlii.org | — | EN/FR | CA | — | Giurisprudenza canadese open |
| CEPOL — EU Law Enforcement Training | https://www.cepol.europa.eu | — | EN | EU | — | Agenzia formazione polizia UE |
| Conseil constitutionnel | https://www.conseil-constitutionnel.fr | — | FR | FR | — | Corte costituzionale francese |
| Corte di Cassazione | https://www.cortedicassazione.it | — | IT | IT | — | Cassazione italiana, sentenze |
| CourtListener | https://www.courtlistener.com | — | EN | US | — | Giurisprudenza USA open (Free Law Project) |
| DEA | https://www.dea.gov | — | EN | US | — | Drug Enforcement Administration |
| EJTN — European Judicial Training Network | https://www.ejtn.eu | — | EN | EU | — | Rete formazione giudiziaria europea |
| FBI | https://www.fbi.gov | — | EN | US | — | Federal Bureau of Investigation, wanted e crime data |
| Frontex | https://www.frontex.europa.eu | — | EN | EU | — | Agenzia frontiere UE, dati flussi |
| Global Impunity Index (CPJ) | https://www.globalimpunityindex.org | — | EN | Globale | — | Indice impunità globale per giornalisti — CPJ |
| Indian Kanoon | https://indiankanoon.org | — | EN | IN | — | Giurisprudenza indiana open |
| Leiden Law Repository | https://scholarlypublications.universiteitleiden.nl | — | EN/NL | NL | — | Repository diritto internazionale Università di Leiden |
| NCA — National Crime Agency | https://www.nationalcrimeagency.gov.uk | — | EN | GB | — | Crimine organizzato UK, SARs |
| NPA Japan | https://www.npa.go.jp | — | JA/EN | JP | — | Agenzia nazionale polizia giapponese |
| PACER | https://pacer.uscourts.gov | — | EN | US | — | Atti giudiziari federali USA |
| Polizia di Stato | https://www.poliziadistato.it | — | IT | IT | — | Polizia italiana |
| RCMP | https://www.rcmp-grc.gc.ca | — | EN/FR | CA | — | Polizia federale canadese |
| SAFLII | https://www.saflii.org | — | EN | Africa | — | Giurisprudenza Africa australe open |
| Supreme Court of India | https://www.sci.gov.in | — | EN/HI | IN | — | Corte suprema indiana |
| UK Supreme Court | https://www.supremecourt.uk | — | EN | GB | — | Corte suprema britannica |
| UNODC Criminal Justice | https://www.unodc.org/unodc/en/justice-and-prison-reform/index.html | — | EN | Globale | — | Riforma giustizia e sistema penitenziario UNODC |
| US Supreme Court | https://www.supremecourt.gov | — | EN | US | — | Corte suprema USA |

### 12.16 Spazio, Geoscienze & Meteo (31)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AEMET | https://www.aemet.es | — | ES | ES | — | Servizio meteo spagnolo |
| ASI — Agenzia Spaziale Italiana | https://www.asi.it | — | IT/EN | IT | — | Agenzia spaziale italiana |
| CNES | https://cnes.fr | — | FR/EN | FR | — | Agenzia spaziale francese |
| CNSA | https://www.cnsa.gov.cn | — | ZH/EN | CN | — | Agenzia spaziale cinese |
| Copernicus Emergency Management Service | https://emergency.copernicus.eu | — | EN | EU | — | Monitoraggio emergenze e disastri naturali da satellite |
| DLR | https://www.dlr.de | — | DE/EN | DE | — | Agenzia aerospaziale tedesca |
| DWD — Deutscher Wetterdienst | https://www.dwd.de | — | DE/EN | DE | — | Servizio meteo tedesco |
| ECMWF | https://www.ecmwf.int | — | EN | Europa | — | Centro europeo previsioni medio termine |
| EMSC | https://www.emsc-csem.org | — | EN | Europa | — | Centro sismologico euro-mediterraneo |
| ESA — Earth Observation | https://www.esa.int/Applications/Observing_the_Earth | — | EN | Globale | — | Osservazione della Terra ESA — missioni e dati |
| EUMETSAT | https://www.eumetsat.int | — | EN | Europa | — | Satelliti meteo europei |
| EUSPA | https://www.euspa.europa.eu | — | EN | EU | — | Agenzia UE programma spaziale (Galileo) |
| GDACS | https://www.gdacs.org | — | EN | Globale | — | Sistema globale allerta disastri (ONU/UE) |
| GFZ — German Research Centre Geosciences | https://www.gfz-potsdam.de | — | EN/DE | DE | — | Centro ricerca geoscienze Germania — sismologia e geodesia |
| Global Volcano Monitor (Smithsonian GVM) | https://volcano.si.edu | — | EN | Globale | — | Database vulcani attivi mondiali — Smithsonian |
| IRIS — Seismology Data | https://www.iris.edu | — | EN | US | — | Dati sismologici globali — waveform e stazioni |
| ISRO | https://www.isro.gov.in | — | EN/HI | IN | — | Agenzia spaziale indiana |
| JAXA | https://global.jaxa.jp | — | JA/EN | JP | — | Agenzia spaziale giapponese |
| JMA — Japan Meteorological Agency | https://www.jma.go.jp | — | JA/EN | JP | — | Meteo e sismi Giappone |
| Met Office | https://www.metoffice.gov.uk | — | EN | GB | — | Servizio meteo britannico |
| Météo-France | https://meteofrance.com | — | FR | FR | — | Servizio meteo francese |
| NASA — Earthdata | https://earthdata.nasa.gov | — | EN | US | — | Portale dati osservazione Terra NASA — open access |
| NOAA NCEI — Climate Data | https://www.ncei.noaa.gov | — | EN | US | — | Dati climatici e ambientali storici NOAA |
| Open-Meteo | https://open-meteo.com | — | EN | Globale | — | API meteorologica open source — dati orari globali |
| Roscosmos | https://www.roscosmos.ru | — | RU | RU | — | Agenzia spaziale russa |
| Servizio Meteo AM | https://www.meteoam.it | — | IT | IT | — | Servizio meteorologico Aeronautica Militare |
| SpaceX — Launch Manifests | https://www.spacex.com/launches | — | EN | US | — | Schedula missioni e manifesti lanci SpaceX |
| UNOOSA | https://www.unoosa.org | — | EN | Globale | — | Ufficio ONU affari spaziali, registro oggetti |
| USGS Earthquakes | https://earthquake.usgs.gov | — | EN | Globale | — | Monitoraggio sismico mondiale USGS |
| USGS — National Map | https://www.usgs.gov/programs/national-geospatial-program/national-map | — | EN | US | — | Mappa nazionale USA — dati topografici e geospaziali USGS |
| WMO | https://wmo.int | — | EN | Globale | — | Organizzazione meteorologica mondiale |

### 12.17 Archivi, Biblioteche & Patrimonio Documentale (25)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Arquivo.pt | https://arquivo.pt | — | PT | PT | — | Archivio web portoghese — patrimonio digitale nazionale |
| BNC — Biblioteca Nacional de Colombia | https://www.bibliotecanacional.gov.co | — | ES | CO | — | Biblioteca nazionale Colombia |
| BNE — Biblioteca Nacional de España | https://www.bne.es | — | ES | ES | — | Biblioteca nazionale spagnola |
| BnF — Bibliothèque nationale de France | https://www.bnf.fr | — | FR | FR | — | Biblioteca nazionale francese |
| BNL — Bibliothèque nationale du Luxembourg | https://www.bnl.public.lu | — | FR | LU | — | Biblioteca nazionale Lussemburgo |
| British Library | https://www.bl.uk | — | EN | GB | — | Biblioteca nazionale britannica |
| Bundesarchiv | https://www.bundesarchiv.de | — | DE | DE | — | Archivio federale tedesco |
| DART-Europe E-theses | https://www.dart-europe.org | — | EN/Multi | EU | — | Database tesi dottorali europee open access |
| DigiVatLib | https://digi.vatlib.it | — | Multi | VA | — | Biblioteca Vaticana digitale |
| DNB — Deutsche Nationalbibliothek | https://www.dnb.de | — | DE/EN | DE | — | Biblioteca nazionale tedesca |
| Gallica | https://gallica.bnf.fr | — | FR | FR | — | Biblioteca digitale BnF |
| HathiTrust | https://www.hathitrust.org | — | EN | Globale | — | Biblioteca digitale accademica |
| ICA — International Council on Archives | https://www.ica.org | — | EN/FR | Globale | — | Consiglio internazionale archivi |
| KB — Koninklijke Bibliotheek | https://www.kb.nl | — | NL/EN | NL | — | Biblioteca nazionale olandese (e Delpher) |
| Library and Archives Canada | https://library-archives.canada.ca | — | EN/FR | CA | — | Biblioteca e archivi canadesi |
| Library of Congress | https://www.loc.gov | — | EN | US | — | Biblioteca del Congresso |
| NDL — National Diet Library | https://www.ndl.go.jp | — | JA/EN | JP | — | Biblioteca della Dieta giapponese |
| NLM — National Library of Medicine | https://www.nlm.nih.gov | — | EN | US | — | Biblioteca nazionale di medicina USA |
| OPAC SBN | https://opac.sbn.it | — | IT | IT | — | Catalogo collettivo biblioteche italiane |
| RISM — International Sources of Music | https://rism.info | — | EN/DE | Globale | — | Database fonti musicali storiche internazionale |
| SAN — Sistema Archivistico Nazionale | https://san.beniculturali.it | — | IT | IT | — | Portale archivi di Stato italiani |
| Trove (NLA) | https://trove.nla.gov.au | — | EN | AU | — | Archivio digitale australiano, giornali storici |
| UK National Archives | https://www.nationalarchives.gov.uk | — | EN | GB | — | Archivi nazionali britannici |
| US National Archives (NARA) | https://www.archives.gov | — | EN | US | — | Archivi nazionali USA |
| WorldCat | https://search.worldcat.org | — | EN | Globale | — | Catalogo bibliotecario mondiale (OCLC) |

### 12.18 Ricerca Economica & Policy (39)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| CBO — Congressional Budget Office | https://www.cbo.gov | — | EN | US | — | Analisi bilancio Congresso USA |
| CEIBS | https://www.ceibs.edu | — | EN/ZH | CN | — | China Europe International Business School |
| CGD — Center for Global Development | https://www.cgdev.org | — | EN | US | — | Sviluppo globale, policy |
| CPB Netherlands | https://www.cpb.nl | — | NL/EN | NL | — | Ufficio analisi politica economica olandese |
| Crossref | https://www.crossref.org | — | EN | Globale | — | Metadati DOI pubblicazioni |
| CRS Reports | https://crsreports.congress.gov | — | EN | US | — | Rapporti Congressional Research Service |
| DIW Berlin | https://www.diw.de | — | DE/EN | DE | — | Istituto tedesco ricerca economica |
| ESADE | https://www.esade.edu | — | ES/EN | ES | — | Business school spagnola |
| ETLA | https://www.etla.fi | — | FI/EN | FI | — | Istituto ricerca economia finlandese |
| Europe PMC | https://europepmc.org | — | EN | Globale | — | Letteratura biomedica open |
| GAO — Government Accountability Office | https://www.gao.gov | — | EN | US | — | Audit federale USA |
| HEC Paris | https://www.hec.edu | — | FR/EN | FR | — | Business school francese |
| IE University | https://www.ie.edu | — | ES/EN | ES | — | Business school spagnola |
| IFPRI | https://www.ifpri.org | — | EN | Globale | — | Ricerca politiche alimentari |
| IFS — Institute for Fiscal Studies | https://ifs.org.uk | — | EN | GB | — | Politica fiscale britannica |
| IMD | https://www.imd.org | — | EN | CH | — | World Competitiveness Ranking |
| IMF eLibrary | https://www.elibrary.imf.org | — | EN | Globale | — | Pubblicazioni e dati FMI |
| INSEAD | https://www.insead.edu | — | EN | FR/SG | — | Business school, ricerca e indici |
| ISB — Indian School of Business | https://www.isb.edu | — | EN | IN | — | Business school indiana |
| IZA — Institute of Labor Economics | https://www.iza.org | — | EN | DE | — | Economia del lavoro, discussion papers |
| Konjunkturinstitutet (NIER) | https://www.konj.se | — | SV/EN | SE | — | Istituto congiunturale svedese |
| NIESR | https://www.niesr.ac.uk | — | EN | GB | — | Istituto nazionale ricerca economica e sociale |
| OBR — Office for Budget Responsibility | https://obr.uk | — | EN | GB | — | Previsioni fiscali indipendenti UK |
| ODI | https://odi.org | — | EN | GB | — | Sviluppo internazionale e politiche |
| OFCE | https://www.ofce.sciences-po.fr | — | FR | FR | — | Osservatorio congiunture economiche Sciences Po |
| ORCID | https://orcid.org | — | EN | Globale | — | Identificativi ricercatori |
| Project MUSE | https://muse.jhu.edu | — | EN | Globale | — | Riviste accademiche umanistiche |
| Prometeia | https://www.prometeia.com | — | IT/EN | IT | — | Ricerca economica e consulenza |
| QS Top Universities | https://www.topuniversities.com | — | EN | Globale | — | Ranking QS |
| RePEc | https://repec.org | — | EN | Globale | — | Archivio working paper economia |
| Resolution Foundation | https://www.resolutionfoundation.org | — | EN | GB | — | Living standards e lavoro |
| Scimago | https://www.scimagojr.com | — | EN | Globale | — | Ranking riviste e istituzioni |
| SDA Bocconi | https://www.sdabocconi.it | — | IT/EN | IT | — | Business school italiana |
| ShanghaiRanking (ARWU) | https://www.shanghairanking.com | — | EN | Globale | — | Academic Ranking of World Universities |
| Times Higher Education | https://www.timeshighereducation.com | — | EN | Globale | — | Ranking e news università |
| UNU-WIDER | https://www.wider.unu.edu | — | EN | Globale | — | Ricerca economia dello sviluppo ONU |
| wiiw | https://wiiw.ac.at | — | EN | AT | — | Studi economici comparati internazionali (Est Europa) |
| World Bank Open Knowledge | https://openknowledge.worldbank.org | — | EN | Globale | — | Repository pubblicazioni Banca Mondiale |
| ZEW | https://www.zew.de | — | DE/EN | DE | — | Ricerca economica europea, Mannheim |

### 12.19 Telecomunicazioni & Regolatori Media (27)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ACMA | https://www.acma.gov.au | — | EN | AU | — | Regolatore comunicazioni australiano |
| ANACOM Portugal | https://www.anacom.pt | — | PT | PT | — | Autorità nazionale comunicazioni Portogallo |
| Anatel | https://www.gov.br/anatel | — | PT | BR | — | Regolatore TLC brasiliano |
| ARCEP | https://www.arcep.fr | — | FR/EN | FR | — | Regolatore TLC francese |
| ARCOM | https://www.arcom.fr | — | FR | FR | — | Regolatore audiovisivo francese |
| BEREC | https://www.berec.europa.eu | — | EN | EU | — | Organismo regolatori TLC europei |
| BTK Turkey | https://www.btk.gov.tr | — | TR | TR | — | Regolatore TLC turco |
| CA Kenya | https://www.ca.go.ke | — | EN | KE | — | Communications Authority keniota |
| CRC Colombia | https://www.crcom.gov.co | — | ES | CO | — | Regolatore comunicazioni colombiano |
| CRTC | https://crtc.gc.ca | — | EN/FR | CA | — | Regolatore radiotelevisione e TLC canadese |
| CST Saudi Arabia | https://www.cst.gov.sa | — | AR/EN | SA | — | Regolatore TLC e spazio saudita |
| ERC — European Radio Regulations DB | https://www.erodocdb.dk | — | EN | EU | — | Database decisioni frequenze regolatori europei |
| FCC | https://www.fcc.gov | — | EN | US | — | Federal Communications Commission |
| GSMA Intelligence | https://www.gsma.com/intelligence | — | EN | Globale | — | Dati mercato mobile globale — GSMA |
| ICASA | https://www.icasa.org.za | — | EN | ZA | — | Regolatore comunicazioni sudafricano |
| IFT México | https://www.ift.org.mx | — | ES | MX | — | Regolatore TLC messicano |
| IMDA Singapore | https://www.imda.gov.sg | — | EN | SG | — | Regolatore media e TLC Singapore |
| ITU Datahub | https://datahub.itu.int | — | EN | Globale | — | Statistiche ICT per Paese — ITU |
| KCC Korea | https://www.kcc.go.kr | — | KO/EN | KR | — | Korea Communications Commission |
| MIC Japan (Soumu) | https://www.soumu.go.jp | — | JA/EN | JP | — | Ministero comunicazioni giapponese |
| NCC Nigeria | https://www.ncc.gov.ng | — | EN | NG | — | Regolatore TLC nigeriano |
| OFCA Hong Kong | https://www.ofca.gov.hk | — | EN/ZH | HK | — | Regolatore comunicazioni HK |
| Ofcom | https://www.ofcom.org.uk | — | EN | GB | — | Regolatore comunicazioni britannico |
| RTR | https://www.rtr.at | — | DE/EN | AT | — | Regolatore TLC e media austriaco |
| Speedtest Global Index (Ookla) | https://www.speedtest.net/global-index | — | EN | Globale | — | Indice velocità internet per Paese — Ookla |
| TDRA UAE | https://tdra.gov.ae | — | AR/EN | AE | — | Regolatore TLC emiratino |
| TRAI | https://www.trai.gov.in | — | EN/HI | IN | — | Regolatore TLC indiano |

### 12.20 Agricoltura & Sicurezza Alimentare (25)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AMIS — Agricultural Market Information System | https://www.amis-outlook.org | — | EN | Globale | — | Mercati agricoli G20 |
| CGIAR | https://www.cgiar.org | — | EN | Globale | — | Rete ricerca agricola internazionale |
| Codex Alimentarius | https://www.fao.org/fao-who-codexalimentarius | — | EN | Globale | — | Standard internazionali sicurezza alimentare FAO/WHO |
| EFSA | https://www.efsa.europa.eu | — | EN | EU | — | Autorità europea sicurezza alimentare |
| Embrapa | https://www.embrapa.br | — | PT | BR | — | Ricerca agricola brasiliana |
| EudraSurveillance | https://www.eurosurveillance.org | — | EN | EU | — | Rivista sorveglianza epidemiologica europea |
| FAO — Food Price Index | https://www.fao.org/world-food-situation/foodpricesindex | — | EN | Globale | — | Indice prezzi alimenti FAO — aggiornamento mensile |
| FEWS NET | https://fews.net | — | EN | Globale | — | Allerta precoce carestie (USAID) |
| FSA — Food Standards Agency | https://www.food.gov.uk | — | EN | GB | — | Sicurezza alimentare britannica |
| FSANZ | https://www.foodstandards.gov.au | — | EN | AU/NZ | — | Standard alimentari Australia/NZ |
| GFSI — Global Food Safety Initiative | https://www.mygfsi.com | — | EN | Globale | — | Iniziativa globale sicurezza alimentare — standard |
| GODAN — Global Open Data for Agriculture | https://www.godan.info | — | EN | Globale | — | Dati aperti per agricoltura e nutrizione globale |
| ICRISAT | https://www.icrisat.org | — | EN | Globale | — | Ricerca internazionale colture semiaride tropicali |
| IFA — International Fertilizer Association | https://www.fertilizer.org | — | EN | Globale | — | Dati mercato fertilizzanti globale |
| IGC — International Grains Council | https://www.igc.int | — | EN | Globale | — | Consiglio internazionale cereali |
| IIASA — Biodiversity & Natural Resources | https://iiasa.ac.at/programs/biodiversity-natural-resources | — | EN | Globale | — | Ricerca sistemi agricoli e risorse naturali IIASA |
| INRAE | https://www.inrae.fr | — | FR/EN | FR | — | Ricerca agronomica francese |
| IPPC | https://www.ippc.int | — | EN | Globale | — | Convenzione protezione piante |
| IRRI — International Rice Research Institute | https://www.irri.org | — | EN | Globale | — | Ricerca riso globale — sicurezza alimentare Asia |
| MASAF | https://www.masaf.gov.it | — | IT | IT | — | Ministero agricoltura italiano |
| USDA ERS — Economic Research Service | https://www.ers.usda.gov | — | EN | US | — | Ricerca economica settore agricolo USA |
| USDA | https://www.usda.gov | — | EN | US | — | Dipartimento agricoltura USA, WASDE |
| Wageningen UR | https://www.wur.nl | — | NL/EN | NL | — | Università e ricerca agroalimentare |
| WAHIS — WOAH Animal Disease Data | https://wahis.woah.org | — | EN | Globale | — | Database sorveglianza malattie animali WOAH |
| WOAH — Organizzazione mondiale sanità animale | https://www.woah.org | — | EN/FR | Globale | — | Ex OIE, epidemie animali |

### 12.21 Lavoro & Welfare (25)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| AIAS — Formatori Sicurezza Lavoro | https://www.aias.it | — | IT | IT | — | Formazione sicurezza lavoro Italia |
| Bollettino ADAPT | https://www.bollettinoadapt.it | — | IT/EN | IT | — | Ricerca e documentazione diritto del lavoro |
| CEDEFOP | https://www.cedefop.europa.eu | — | EN | EU | — | Centro europeo sviluppo formazione professionale |
| Child Labour Platform (ILO) | https://www.ilo.org/ipec/Informationresources/WCMS_206038/lang--en/index.htm | — | EN | Globale | — | Piattaforma lavoro minorile ILO — dati per settore e Paese |
| DOL — US Department of Labor | https://www.dol.gov | — | EN | US | — | Dipartimento lavoro USA |
| EEOC | https://www.eeoc.gov | — | EN | US | — | Pari opportunità lavoro USA |
| ETUC — European Trade Union Confederation | https://www.etuc.org | — | EN/FR | EU | — | Confederazione sindacati europei |
| ETUI | https://www.etui.org | — | EN | EU | — | Istituto sindacale europeo, ricerca |
| EU-OSHA | https://osha.europa.eu | — | EN | EU | — | Salute e sicurezza sul lavoro UE |
| Eurofound | https://www.eurofound.europa.eu | — | EN | EU | — | Condizioni di vita e lavoro UE |
| Global Deal — Social Dialogue | https://www.theglobaldeal.com | — | EN | Globale | — | Partenariato globale dialogo sociale e lavoro dignitoso |
| Global Wages Database (ILO) | https://www.ilo.org/global/statistics-and-databases/WCMS_142568/lang--en/index.htm | — | EN | Globale | — | Database salari globali ILO |
| ILO NORMLEX | https://normlex.ilo.org | — | EN | Globale | — | Convenzioni e raccomandazioni ILO — database |
| ILO — Social Protection Platform | https://www.social-protection.org | — | EN | Globale | — | Piattaforma dati protezione sociale globale ILO |
| ILO — World Employment & Social Outlook | https://www.ilo.org/global/research/global-reports/weso | — | EN | Globale | — | Rapporto annuale ILO su occupazione e protezione sociale |
| INAIL | https://www.inail.it | — | IT | IT | — | Assicurazione infortuni, dati incidenti |
| ITUC | https://www.ituc-csi.org | — | EN/Multi | Globale | — | Confederazione sindacale internazionale, Global Rights Index |
| Korea Employment Information Service (KEIS) | https://www.keis.or.kr | — | KO/EN | KR | — | Servizio informazioni lavoro Corea del Sud |
| Lavoro.gov.it — ANPAL | https://www.anpal.gov.it | — | IT | IT | — | Agenzia nazionale politiche attive del lavoro IT |
| Ministero del Lavoro | https://www.lavoro.gov.it | — | IT | IT | — | Politiche del lavoro italiane |
| OECD Better Life Index | https://www.oecdbetterlifeindex.org | — | EN | Globale | — | Indice OCSE benessere e qualità della vita per Paese |
| OECD Employment | https://www.oecd.org/employment | — | EN | Globale | — | Dati occupazione e lavoro OCSE |
| OSHA — Occupational Safety and Health Admin. | https://www.osha.gov | — | EN | US | — | Sicurezza lavoro USA, ispezioni |
| Social Protection Global Database (WB) | https://www.worldbank.org/en/topic/socialprotection | — | EN | Globale | — | Banca Mondiale — protezione sociale globale |
| WageIndicator | https://wageindicator.org | — | EN/Multi | Globale | — | Salari e diritto del lavoro comparato |

### 12.22 Difesa & Procurement Pubblico (25)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Acquisti in Rete PA (Consip) | https://www.acquistinretepa.it | — | IT | IT | — | Procurement PA italiana |
| Airforce Technology | https://www.airforce-technology.com | — | EN | Globale | — | Sistemi e appalti aeronautica militare |
| Armada International | https://www.armadaint.com | — | EN | Globale | — | Rivista internazionale sistemi navali e difesa marina |
| ASD — AeroSpace and Defence Industries EU | https://www.asd-europe.org | — | EN | EU | — | Associazione industrie aerospazio e difesa europee |
| BSDI — Baltic Security Defence Index (ICDS) | https://icds.ee | — | EN | EE | — | Istituto studi difesa e sicurezza baltica |
| C4ISRNET | https://www.c4isrnet.com | — | EN | US | — | News C4ISR — comando, controllo, comunicazioni, intelligence |
| DARPA | https://www.darpa.mil | — | EN | US | — | Ricerca avanzata difesa |
| Defence24 | https://defence24.com | — | EN/PL | PL | — | Difesa Europa centro-orientale |
| Defense Acquisition University | https://www.dau.edu | — | EN | US | — | Università appalti difesa USA — policy e formazione |
| DSCA | https://www.dsca.mil | — | EN | US | — | Vendite militari estere (FMS) |
| EDA — European Defence Agency | https://eda.europa.eu | — | EN | EU | — | Agenzia europea per la difesa |
| Ministero della Difesa | https://www.difesa.it | — | IT | IT | — | Difesa italiana |
| NATO Support and Procurement Agency (NSPA) | https://www.nspa.nato.int | — | EN | NATO | — | Agenzia supporto e approvvigionamento NATO |
| NATO — Contracts & Procurement | https://www.nato.int/cps/en/natohq/topics_141644.htm | — | EN | NATO | — | Appalti NATO e procurement alleanza |
| Naval News | https://www.navalnews.com | — | EN | Globale | — | News navali e cantieristica |
| OCDS — Open Contracting Data Standard | https://standard.open-contracting.org | — | EN | Globale | — | Standard dati appalti aperti — schema globale |
| Opentender | https://opentender.eu | — | EN | EU | — | Dati appalti 33 Paesi europei |
| PESCO — Permanent Structured Cooperation EU | https://www.pesco.europa.eu | — | EN | EU | — | Cooperazione strutturata permanente difesa UE |
| SAM.gov | https://sam.gov | — | EN | US | — | Appalti federali USA e registro contractor |
| Shephard Media | https://www.shephardmedia.com | — | EN | Globale | — | Media difesa specializzati |
| Spend Network | https://spendnetwork.com | — | EN | GB | — | Analisi spesa pubblica e contratti governativi |
| Tenders.gov.au | https://www.tenders.gov.au | — | EN | AU | — | Bandi gara governo australiano |
| The War Zone | https://www.twz.com | — | EN | Globale | — | OSINT militare e aviazione |
| UNGM — UN Global Marketplace | https://www.ungm.org | — | EN | Globale | — | Appalti sistema ONU |
| US Department of Defense | https://www.defense.gov | — | EN | US | — | Pentagono, contratti e comunicati |

### 12.23 Cultura, Arte & Patrimonio (25)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| Art Loss Register | https://www.artloss.com | — | EN | Globale | — | Database opere rubate |
| Artnet News | https://news.artnet.com | — | EN | Globale | — | Mercato dell'arte e aste |
| Artsy | https://www.artsy.net | — | EN | Globale | — | Mercato e database arte contemporanea online |
| British Museum | https://www.britishmuseum.org | — | EN | GB | — | Museo, collezione digitale |
| Centre Pompidou | https://www.centrepompidou.fr | — | FR/EN | FR | — | Museo arte moderna e contemporanea Parigi |
| Europeana Pro | https://pro.europeana.eu | — | EN/Multi | EU | — | Portale professionale patrimonio digitale europeo |
| Gallerie degli Uffizi | https://www.uffizi.it | — | IT/EN | IT | — | Museo, collezioni digitali |
| Getty Research Institute | https://www.getty.edu/research | — | EN | US | — | Risorse ricerca storia dell'arte e patrimonio |
| ICCROM | https://www.iccrom.org | — | EN | Globale | — | Conservazione patrimonio culturale |
| ICOM | https://icom.museum | — | EN/FR | Globale | — | Consiglio internazionale musei, Red Lists |
| ICOMOS | https://www.icomos.org | — | EN/FR | Globale | — | Monumenti e siti, patrimonio |
| INTERPOL — Cultural Heritage Crime | https://www.interpol.int/en/Crimes/Cultural-heritage-crime | — | EN | Globale | — | INTERPOL furti opere d'arte e crimine culturale |
| Louvre | https://www.louvre.fr | — | FR/EN | FR | — | Museo, collezioni online |
| Ministero della Cultura | https://cultura.gov.it | — | IT | IT | — | MiC italiano |
| MoMA | https://www.moma.org | — | EN | US | — | Museum of Modern Art — collezione e archivio online |
| Musei Vaticani | https://www.museivaticani.va | — | IT/EN | VA | — | Musei Vaticani |
| Museo del Prado | https://www.museodelprado.es | — | ES/EN | ES | — | Museo, collezione online |
| Rijksmuseum | https://www.rijksmuseum.nl | — | NL/EN | NL | — | Museo, Rijksstudio open data |
| Smithsonian Open Access | https://www.si.edu/openaccess | — | EN | US | — | Collezioni Smithsonian in open access — 4.5M oggetti digitali |
| Smithsonian | https://www.si.edu | — | EN | US | — | Rete musei e open access |
| Tate | https://www.tate.org.uk | — | EN | GB | — | Galleria nazionale arte britannica — archivio |
| The Art Newspaper | https://www.theartnewspaper.com | — | EN | Globale | — | News mondo dell'arte |
| The Met | https://www.metmuseum.org | — | EN | US | — | Metropolitan Museum, open access |
| UNESCO World Heritage | https://whc.unesco.org | — | EN/FR | Globale | — | Lista patrimonio mondiale UNESCO |
| V&A — Victoria and Albert Museum | https://www.vam.ac.uk | — | EN | GB | — | Museo arti decorative — collezione online |

### 12.24 Sport & Governance Sportiva (26)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| FIBA — Basketball | https://www.fiba.basketball | — | EN | Globale | — | Federazione internazionale pallacanestro |
| FIDE — Chess | https://www.fide.com | — | EN | Globale | — | Federazione internazionale scacchi — governance e rating |
| FIFA | https://www.fifa.com | — | EN/Multi | Globale | — | Federazione calcio mondiale |
| FISA — World Rowing | https://worldrowing.com | — | EN | Globale | — | Federazione internazionale canottaggio |
| Football Leaks / EIC | https://www.eic.network | — | EN | Globale | — | Rete investigativa europea — Football Leaks e oltre |
| Front Office Sports | https://frontofficesports.com | — | EN | US | — | Business dello sport |
| GAISF — Federazioni Sportive INT | https://www.gaisf.sport | — | EN | Globale | — | Federazione ombrello federazioni sportive internazionali |
| IBA — Boxing | https://www.iba.sport | — | EN | Globale | — | Associazione internazionale boxe — governance |
| ICAS — Council of Arbitration for Sport | https://www.icas.sport | — | EN | Globale | — | Consiglio arbitrale sportivo internazionale |
| ICSS — International Centre for Sport Security | https://www.theicss.org | — | EN | Globale | — | Centro internazionale sicurezza nello sport |
| Inside the Games | https://www.insidethegames.biz | — | EN | Globale | — | Politica sportiva e olimpica |
| IOC — Olympics | https://olympics.com | — | EN/Multi | Globale | — | Comitato olimpico internazionale |
| ITTF — Table Tennis | https://www.ittf.com | — | EN | Globale | — | Federazione internazionale tennis tavolo |
| Play the Game | https://www.playthegame.org | — | EN | Globale | — | Governance e integrità sportiva |
| SIGA — Sport Integrity Global Alliance | https://siga-sport.com | — | EN | Globale | — | Alleanza globale integrità sportiva |
| SportBusiness | https://www.sportbusiness.com | — | EN | Globale | — | Industria sportiva (commerciale) |
| Sportico | https://www.sportico.com | — | EN | US | — | Business e valutazioni sportive |
| SportRadar Integrity Services | https://www.sportradar.com/services/integrity-services | — | EN | Globale | — | Integrità sport e match-fixing monitoring |
| Sportradar UFED | https://fraud-detection.sportradar.com | — | EN | Globale | — | Sistema rilevamento frodi scommesse sportive |
| TAS-CAS | https://www.tas-cas.org | — | EN/FR | Globale | — | Tribunale arbitrale dello sport |
| TAS-CAS — Jurisprudence | https://jurisprudence.tas-cas.org | — | EN/FR | Globale | — | Decisioni Tribunale arbitrale dello sport |
| UCI — Cycling | https://www.uci.org | — | EN/FR | Globale | — | Unione ciclistica internazionale |
| UEFA | https://www.uefa.com | — | EN/Multi | Europa | — | Calcio europeo |
| WA — World Athletics | https://worldathletics.org | — | EN | Globale | — | Federazione mondiale atletica leggera |
| WADA | https://www.wada-ama.org | — | EN/FR | Globale | — | Agenzia mondiale antidoping |
| World Rugby | https://www.world.rugby | — | EN | Globale | — | Federazione mondiale rugby — governance e regole |

### 12.25 Ordini & Associazioni Professionali (29)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ABA — American Bar Association | https://www.americanbar.org | — | EN | US | — | Ordine avvocati USA |
| ACCA | https://www.accaglobal.com | — | EN | Globale | — | Association of Chartered Certified Accountants |
| AICPA & CIMA | https://www.aicpa-cima.com | — | EN | US | — | Commercialisti USA |
| AMA — American Medical Association | https://www.ama-assn.org | — | EN | US | — | Associazione medica USA |
| BMA — British Medical Association | https://www.bma.org.uk | — | EN | GB | — | Associazione medica britannica |
| Bundesärztekammer | https://www.bundesaerztekammer.de | — | DE | DE | — | Ordine medici federale tedesco |
| CA ANZ | https://www.charteredaccountantsanz.com | — | EN | AU/NZ | — | Chartered accountants Australia/NZ |
| CCBE | https://www.ccbe.eu | — | EN/FR | EU | — | Consiglio ordini forensi europei |
| CNDCEC | https://commercialisti.it | — | IT | IT | — | Consiglio nazionale commercialisti |
| CNF — Consiglio Nazionale Forense | https://www.consiglionazionaleforense.it | — | IT | IT | — | Ordine forense italiano |
| Consiglio Nazionale del Notariato | https://www.notariato.it | — | IT | IT | — | Notariato italiano |
| CPA Canada | https://www.cpacanada.ca | — | EN/FR | CA | — | Commercialisti canadesi |
| EFJ — European Federation of Journalists | https://europeanjournalists.org | — | EN | EU | — | Federazione europea giornalisti |
| Engineers Australia | https://www.engineersaustralia.org.au | — | EN | AU | — | Ordine ingegneri australiano |
| FNOMCeO | https://portale.fnomceo.it | — | IT | IT | — | Federazione ordini medici italiani |
| IBA — International Bar Association | https://www.ibanet.org | — | EN | Globale | — | Associazione internazionale avvocati |
| ICAEW | https://www.icaew.com | — | EN | GB | — | Chartered accountants Inghilterra/Galles |
| ICAI | https://www.icai.org | — | EN | IN | — | Institute of Chartered Accountants of India |
| ICE — Institution of Civil Engineers | https://www.ice.org.uk | — | EN | GB | — | Ingegneri civili britannici |
| IFAC | https://www.ifac.org | — | EN | Globale | — | Federazione internazionale commercialisti |
| NSPE | https://www.nspe.org | — | EN | US | — | Professional engineers USA |
| NUJ | https://www.nuj.org.uk | — | EN | GB | — | Sindacato giornalisti UK/IE |
| RIBA | https://www.architecture.com | — | EN | GB | — | Royal Institute of British Architects |
| The Law Society | https://www.lawsociety.org.uk | — | EN | GB | — | Ordine solicitor Inghilterra/Galles |
| UIA — Union Internationale des Architectes | https://www.uia-architectes.org | — | EN/FR | Globale | — | Unione internazionale architetti |
| UINL | https://www.uinl.org | — | ES/FR/EN | Globale | — | Unione internazionale notariato |
| VDI | https://www.vdi.de | — | DE/EN | DE | — | Associazione ingegneri tedeschi |
| WFEO | https://www.wfeo.org | — | EN | Globale | — | Federazione mondiale organizzazioni ingegneri |
| WMA — World Medical Association | https://www.wma.net | — | EN | Globale | — | Associazione medica mondiale |

### 12.26 Fondazioni, Filantropia & Nonprofit (26)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ACNC | https://www.acnc.gov.au | — | EN | AU | — | Registro charity australiano |
| Aga Khan Development Network (AKDN) | https://www.akdn.org | — | EN | Globale | — | Rete sviluppo Aga Khan — filantropia Paesi in via di sviluppo |
| Bloomberg Philanthropies | https://www.bloomberg.org | — | EN | Globale | — | Filantropie Bloomberg — salute, ambiente, arte, governance |
| CAF — Charities Aid Foundation | https://www.cafonline.org | — | EN | GB | — | Fondazione supporto filantropia globale |
| Calouste Gulbenkian Foundation | https://gulbenkian.pt | — | PT/EN | PT | — | Fondazione Gulbenkian — arte, scienza, sviluppo |
| Candid | https://candid.org | — | EN | US | — | Database fondazioni e nonprofit (990) |
| Charities Services NZ | https://www.charities.govt.nz | — | EN | NZ | — | Registro charity neozelandese |
| Charity Commission Register | https://register-of-charities.charitycommission.gov.uk | — | EN | GB | — | Registro charity Inghilterra/Galles |
| Charity Navigator | https://www.charitynavigator.org | — | EN | US | — | Rating nonprofit USA |
| CIVICUS Monitor | https://monitor.civicus.org | — | EN | Globale | — | Monitor spazio civico per Paese |
| Compagnia di San Paolo | https://www.compagniadisanpaolo.it | — | IT | IT | — | Fondazione bancaria torinese |
| CONCORD — European NGO Confederation | https://concord.eu | — | EN | EU | — | Confederazione europea ONG sviluppo e cooperazione |
| Fondazione Cariplo | https://www.fondazionecariplo.it | — | IT | IT | — | Fondazione bancaria, grant |
| Fondazione con il Sud | https://www.fondazioneconilsud.it | — | IT | IT | — | Filantropia e coesione sociale Sud Italia |
| Ford Foundation | https://www.fordfoundation.org | — | EN | Globale | — | Giustizia sociale, grant database |
| Gates Foundation | https://www.gatesfoundation.org | — | EN | Globale | — | Filantropia salute/sviluppo, Goalkeepers |
| GuideStar USA | https://www.guidestar.org | — | EN | US | — | Database nonprofit USA con trasparenza finanziaria |
| Hewlett Foundation | https://hewlett.org | — | EN | US | — | Filantropia, trasparenza grant |
| King Baudouin Foundation | https://www.kbs-frb.be | — | FR/NL/EN | BE | — | Fondazione belga, filantropia europea |
| MacArthur Foundation | https://www.macfound.org | — | EN | US | — | Grant, giustizia, clima |
| OSCR | https://www.oscr.org.uk | — | EN | GB | — | Registro charity scozzese |
| Philea — Philanthropy Europe | https://philea.eu | — | EN | EU | — | Associazione europea fondazioni e filantropia |
| Robert Bosch Stiftung | https://www.bosch-stiftung.de | — | DE/EN | DE | — | Fondazione tedesca |
| Rockefeller Foundation | https://www.rockefellerfoundation.org | — | EN | Globale | — | Filantropia, resilienza |
| Voluntaris | https://www.voluntaris.de | — | EN/DE | DE | — | Rivista scientifica internazionale volontariato corporate |
| Wellcome | https://wellcome.org | — | EN | GB | — | Ricerca sanitaria, grant |

### 12.27 Promozione Investimenti & Fondi Sovrani (34)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ADIA | https://www.adia.ae | — | EN/AR | AE | — | Abu Dhabi Investment Authority |
| ApexBrasil | https://apexbrasil.com.br | — | PT/EN | BR | — | Promozione export brasiliana |
| Austrade | https://www.austrade.gov.au | — | EN | AU | — | Promozione commercio australiana |
| BKPM — Kementerian Investasi | https://www.bkpm.go.id | — | ID/EN | ID | — | Ministero investimenti indonesiano |
| BOI Philippines | https://boi.gov.ph | — | EN | PH | — | Board of Investments filippino |
| BOI Thailand | https://www.boi.go.th | — | TH/EN | TH | — | Board of Investment thailandese |
| Business France | https://www.businessfrance.fr | — | FR/EN | FR | — | Promozione investimenti francese |
| CIC — China Investment Corporation | http://www.china-inv.cn | — | ZH/EN | CN | — | Fondo sovrano cinese |
| CzechInvest | https://www.czechinvest.org | — | CS/EN | CZ | — | Promozione investimenti ceca |
| Enterprise Singapore | https://www.enterprisesg.gov.sg | — | EN | SG | — | Agenzia imprese di Singapore |
| GIC | https://www.gic.com.sg | — | EN | SG | — | Fondo sovrano di Singapore |
| GIPC Ghana | https://www.gipc.gov.gh | — | EN | GH | — | Centro promozione investimenti ghanese |
| GTAI — Germany Trade & Invest | https://www.gtai.de | — | DE/EN | DE | — | Promozione investimenti tedesca |
| HIPA | https://hipa.hu | — | HU/EN | HU | — | Agenzia investimenti ungherese |
| ICEX | https://www.icex.es | — | ES/EN | ES | — | Promozione export/investimenti spagnola |
| IDA Ireland | https://www.idaireland.com | — | EN | IE | — | Promozione IDE irlandese |
| Invest in Canada | https://www.investcanada.ca | — | EN/FR | CA | — | Promozione investimenti canadese |
| Invest India | https://www.investindia.gov.in | — | EN | IN | — | Promozione investimenti indiana |
| Invest Lithuania | https://investlithuania.com | — | EN | LT | — | Promozione investimenti lituana |
| Invest Qatar | https://www.invest.qa | — | EN/AR | QA | — | Promozione investimenti qatariota |
| InvestChile | https://investchile.gob.cl | — | ES/EN | CL | — | Promozione investimenti cilena |
| InvestHK | https://www.investhk.gov.hk | — | EN/ZH | HK | — | Promozione investimenti HK |
| Invitalia | https://www.invitalia.it | — | IT | IT | — | Agenzia nazionale investimenti e sviluppo |
| KenInvest | https://www.invest.go.ke | — | EN | KE | — | Autorità investimenti keniota |
| KOTRA | https://www.kotra.or.kr | — | KO/EN | KR | — | Promozione commercio coreana |
| MIDA | https://www.mida.gov.my | — | EN | MY | — | Autorità sviluppo industriale malese |
| Mubadala | https://www.mubadala.com | — | EN/AR | AE | — | Fondo sovrano di Abu Dhabi |
| NBIM — Norges Bank Investment Management | https://www.nbim.no | — | EN | NO | — | Fondo sovrano norvegese, holdings pubbliche |
| NIPC Nigeria | https://www.nipc.gov.ng | — | EN | NG | — | Commissione promozione investimenti nigeriana |
| PAIH | https://www.paih.gov.pl | — | PL/EN | PL | — | Agenzia investimenti polacca |
| PIF — Public Investment Fund | https://www.pif.gov.sa | — | AR/EN | SA | — | Fondo sovrano saudita |
| ProColombia | https://procolombia.co | — | ES/EN | CO | — | Promozione investimenti colombiana |
| QIA — Qatar Investment Authority | https://www.qia.qa | — | EN/AR | QA | — | Fondo sovrano qatariota |
| Temasek | https://www.temasek.com.sg | — | EN | SG | — | Holding statale di Singapore |

### 12.28 Ambiente & Vigilanza Ambientale (25)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ADEME | https://www.ademe.fr | — | FR | FR | — | Agenzia transizione ecologica francese |
| CARB — California Air Resources Board | https://ww2.arb.ca.gov | — | EN | US | — | Regolatore emissioni California — standard riferimento globale |
| Climate Action Tracker | https://climateactiontracker.org | — | EN | Globale | — | Monitoraggio impegni climatici per Paese vs. Accordo di Parigi |
| CREA — Centre for Research on Energy and Clean Air | https://energyandcleanair.org | — | EN | Globale | — | Ricerca indipendente su inquinamento aria e politiche energetiche |
| DCCEEW | https://www.dcceew.gov.au | — | EN | AU | — | Clima, energia e ambiente australiano |
| DFFE South Africa | https://www.dffe.gov.za | — | EN | ZA | — | Foreste, pesca e ambiente sudafricano |
| EPA Ireland | https://www.epa.ie | — | EN | IE | — | Agenzia ambiente irlandese |
| EPA USA | https://www.epa.gov | — | EN | US | — | Agenzia protezione ambiente USA |
| IPBES — Biodiversity & Ecosystem Services | https://www.ipbes.net | — | EN | Globale | — | Piattaforma intergovernativa biodiversità ed ecosistemi |
| IRDAI | https://irdai.gov.in | — | EN | IN | — | Vigilanza assicurativa indiana |
| IUCN Red List | https://www.iucnredlist.org | — | EN | Globale | — | Lista rossa specie minacciate IUCN |
| MEE China | https://www.mee.gov.cn | — | ZH/EN | CN | — | Ministero ecologia e ambiente cinese |
| Miljødirektoratet | https://www.miljodirektoratet.no | — | NO/EN | NO | — | Agenzia ambiente norvegese |
| MITECO | https://www.miteco.gob.es | — | ES | ES | — | Ministero transizione ecologica spagnolo |
| MOE Japan | https://www.env.go.jp | — | JA/EN | JP | — | Ministero ambiente giapponese |
| Naturvårdsverket | https://www.naturvardsverket.se | — | SV/EN | SE | — | Agenzia ambiente svedese |
| NEMA Kenya | https://www.nema.go.ke | — | EN | KE | — | Autorità ambiente keniota |
| NESREA | https://www.nesrea.gov.ng | — | EN | NG | — | Enforcement ambientale nigeriano |
| Plastic Pollution Coalition | https://www.plasticpollutioncoalition.org | — | EN | Globale | — | Monitoraggio e advocacy inquinamento da plastica |
| RIVM | https://www.rivm.nl | — | NL/EN | NL | — | Sanità pubblica e ambiente olandese |
| SEPA — Scottish EPA | https://www.sepa.org.uk | — | EN | GB | — | Agenzia ambiente scozzese |
| SYKE | https://www.syke.fi | — | FI/EN | FI | — | Istituto ambiente finlandese |
| UBA — Umweltbundesamt | https://www.umweltbundesamt.de | — | DE/EN | DE | — | Agenzia ambiente tedesca |
| UNEP GRID-Arendal | https://www.grida.no | — | EN | Globale | — | Dati ambientali e visualizzazioni UNEP |
| UNEP-WCMC | https://www.unep-wcmc.org | — | EN | Globale | — | Centro monitoraggio conservazione UNEP |

### 12.29 Associazioni Bancarie & Infrastrutture di Mercato (34)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ABA — American Bankers Association | https://www.aba.com | — | EN | US | — | Banche statunitensi |
| ABA — Australian Banking Association | https://www.ausbanking.org.au | — | EN | AU | — | Banche australiane |
| ABI — Association of British Insurers | https://www.abi.org.uk | — | EN | GB | — | Assicuratori britannici |
| ABI — Associazione Bancaria Italiana | https://www.abi.it | — | IT | IT | — | Associazione banche italiane |
| ABM — Asociación de Bancos de México | https://www.abm.org.mx | — | ES | MX | — | Banche messicane |
| AEB — Asociación Española de Banca | https://www.aebanca.es | — | ES | ES | — | Banche spagnole |
| AFME | https://www.afme.eu | — | EN | EU | — | Mercati finanziari europei |
| ANIA | https://www.ania.it | — | IT | IT | — | Assicuratori italiani |
| Asobancaria | https://www.asobancaria.com | — | ES | CO | — | Banche colombiane |
| Bankenverband (BdB) | https://bankenverband.de | — | DE/EN | DE | — | Banche private tedesche |
| BASA — Banking Association South Africa | https://www.banking.org.za | — | EN | ZA | — | Banche sudafricane |
| CBA — Canadian Bankers Association | https://cba.ca | — | EN/FR | CA | — | Banche canadesi |
| Clearstream | https://www.clearstream.com | — | EN | EU | — | Depositario centrale (Deutsche Börse) |
| CLS Group | https://www.cls-group.com | — | EN | Globale | — | Settlement valutario globale |
| DTCC | https://www.dtcc.com | — | EN | US | — | Clearing e settlement USA |
| EBF — European Banking Federation | https://www.ebf.eu | — | EN | EU | — | Federazione bancaria europea |
| Euroclear | https://www.euroclear.com | — | EN | EU | — | Depositario centrale europeo |
| FBF — Fédération Bancaire Française | https://www.fbf.fr | — | FR | FR | — | Federazione bancaria francese |
| Febelfin | https://www.febelfin.be | — | FR/NL | BE | — | Settore finanziario belga |
| Febraban | https://portal.febraban.org.br | — | PT | BR | — | Federazione banche brasiliane |
| GDV | https://www.gdv.de | — | DE/EN | DE | — | Assicuratori tedeschi |
| IBA — Indian Banks' Association | https://www.iba.org.in | — | EN | IN | — | Banche indiane |
| ICMA | https://www.icmagroup.org | — | EN | Globale | — | Mercati capitali internazionali |
| III — Insurance Information Institute | https://www.iii.org | — | EN | US | — | Dati assicurativi USA |
| Insurance Europe | https://www.insuranceeurope.eu | — | EN | EU | — | Federazione assicuratori europei |
| ISDA | https://www.isda.org | — | EN | Globale | — | Derivati OTC, documentazione standard |
| KFB — Korea Federation of Banks | https://www.kfb.or.kr | — | KO/EN | KR | — | Banche coreane |
| LCH | https://www.lch.com | — | EN | GB | — | Clearing house (LSEG) |
| NVB | https://www.nvb.nl | — | NL | NL | — | Banche olandesi |
| SIFMA | https://www.sifma.org | — | EN | US | — | Industria titoli USA |
| Swiss Bankers Association | https://www.swissbanking.ch | — | DE/EN | CH | — | Banche svizzere |
| The Geneva Association | https://www.genevaassociation.org | — | EN | Globale | — | Think tank assicurativo |
| UK Finance | https://www.ukfinance.org.uk | — | EN | GB | — | Settore finanziario britannico |
| Zenginkyo — Japanese Bankers Association | https://www.zenginkyo.or.jp | — | JA/EN | JP | — | Banche giapponesi |

### 12.30 Associazioni Industriali, di Categoria & Turismo (70)

| Fonte | URL | RSS Feed | Lingua | Paese / Area | Accesso | Note |
|-------|-----|----------|--------|--------------|---------|------|
| ACEA | https://www.acea.auto | — | EN | EU | — | Costruttori auto europei, dati immatricolazioni |
| ACI — Airports Council International | https://aci.aero | — | EN | Globale | — | Aeroporti mondiali, traffico |
| American Chemistry Council | https://www.americanchemistry.com | — | EN | US | — | Chimica USA |
| American Farm Bureau | https://www.fb.org | — | EN | US | — | Agricoltori USA |
| ANCE | https://ance.it | — | IT | IT | — | Costruttori edili italiani |
| ANFIA | https://www.anfia.it | — | IT | IT | — | Filiera automotive italiana |
| Atout France | https://www.atout-france.fr | — | FR | FR | — | Ente turismo francese |
| Austria Info | https://www.austria.info | — | Multi | AT | — | Ente turismo austriaco |
| BDI | https://bdi.eu | — | DE/EN | DE | — | Industria tedesca |
| Bitkom | https://www.bitkom.org | — | DE/EN | DE | — | Digitale tedesco |
| BUSA — Business Unity South Africa | https://busa.org.za | — | EN | ZA | — | Imprese sudafricane |
| Business Roundtable | https://www.businessroundtable.org | — | EN | US | — | CEO grandi imprese USA |
| BusinessEurope | https://www.businesseurope.eu | — | EN | EU | — | Confederazione imprese europee |
| CBI — Confederation of British Industry | https://www.cbi.org.uk | — | EN | GB | — | Industria britannica |
| CCE — Consejo Coordinador Empresarial | https://cce.org.mx | — | ES | MX | — | Imprese messicane |
| Cefic | https://cefic.org | — | EN | EU | — | Industria chimica europea |
| CEOE | https://www.ceoe.es | — | ES | ES | — | Imprese spagnole |
| Confagricoltura | https://www.confagricoltura.it | — | IT | IT | — | Imprese agricole italiane |
| Confesercenti | https://www.confesercenti.it | — | IT | IT | — | PMI commercio italiane |
| Confindustria | https://www.confindustria.it | — | IT | IT | — | Industria italiana |
| Copa-Cogeca | https://copa-cogeca.eu | — | EN | EU | — | Agricoltori e cooperative europee |
| DigitalEurope | https://www.digitaleurope.org | — | EN | EU | — | Industria digitale europea |
| EFPIA | https://www.efpia.eu | — | EN | EU | — | Industria farmaceutica europea |
| Embratur | https://embratur.com.br | — | PT | BR | — | Ente turismo brasiliano |
| ENIT | https://www.enit.it | — | IT | IT | — | Agenzia nazionale turismo italiana |
| EuroCommerce | https://www.eurocommerce.eu | — | EN | EU | — | Commercio e retail europei |
| Farmindustria | https://www.farmindustria.it | — | IT | IT | — | Farmaceutica italiana |
| Federalimentare | https://www.federalimentare.it | — | IT | IT | — | Alimentare italiano |
| Federchimica | https://www.federchimica.it | — | IT | IT | — | Chimica italiana |
| FIATA | https://fiata.org | — | EN | Globale | — | Spedizionieri internazionali |
| FIEC | https://www.fiec.eu | — | EN | EU | — | Costruzioni europee |
| FIESP | https://www.fiesp.com.br | — | PT | BR | — | Industria di San Paolo |
| FoodDrinkEurope | https://www.fooddrinkeurope.eu | — | EN | EU | — | Industria alimentare europea |
| German National Tourist Board | https://www.germany.travel | — | Multi | DE | — | Ente turismo tedesco |
| HOTREC | https://www.hotrec.eu | — | EN | EU | — | Ospitalità europea |
| IFPMA | https://www.ifpma.org | — | EN | Globale | — | Farmaceutica mondiale |
| IRU | https://www.iru.org | — | EN | Globale | — | Trasporto stradale mondiale |
| ITI — Information Technology Industry Council | https://www.itic.org | — | EN | US | — | Big Tech policy |
| JAMA | https://www.jama.or.jp | — | JA/EN | JP | — | Costruttori auto giapponesi |
| JNTO | https://www.japan.travel | — | Multi | JP | — | Ente turismo giapponese |
| Keidanren | https://www.keidanren.or.jp | — | JA/EN | JP | — | Federazione imprese giapponesi |
| MEDEF | https://www.medef.com | — | FR | FR | — | Imprese francesi |
| NAHB | https://www.nahb.org | — | EN | US | — | Home builders USA |
| NAM — National Association of Manufacturers | https://nam.org | — | EN | US | — | Manifattura USA |
| NAR — National Association of Realtors | https://www.nar.realtor | — | EN | US | — | Agenti immobiliari USA, dati mercato |
| NFU | https://www.nfuonline.com | — | EN | GB | — | Agricoltori britannici |
| NRF — National Retail Federation | https://nrf.com | — | EN | US | — | Retail USA |
| OICA | https://www.oica.net | — | EN | Globale | — | Costruttori auto mondiali, statistiche produzione |
| PhRMA | https://phrma.org | — | EN | US | — | Farmaceutica USA |
| RICS | https://www.rics.org | — | EN | Globale | — | Chartered surveyors, standard immobiliari |
| SEMI | https://www.semi.org | — | EN | Globale | — | Industria semiconduttori, dati fab |
| SIA — Semiconductor Industry Association | https://www.semiconductors.org | — | EN | US | — | Semiconduttori USA |
| SMMT | https://www.smmt.co.uk | — | EN | GB | — | Automotive britannico |
| South African Tourism | https://www.southafrica.net | — | EN | ZA | — | Ente turismo sudafricano |
| STB — Singapore Tourism Board | https://www.stb.gov.sg | — | EN | SG | — | Ente turismo di Singapore |
| Switzerland Tourism | https://www.myswitzerland.com | — | Multi | CH | — | Ente turismo svizzero |
| TAT Newsroom | https://www.tatnews.org | — | EN | TH | — | Ente turismo thailandese, newsroom |
| techUK | https://www.techuk.org | — | EN | GB | — | Settore tech britannico |
| Tourism Australia | https://www.tourism.australia.com | — | EN | AU | — | Ente turismo australiano |
| Turespaña | https://www.tourspain.es | — | ES | ES | — | Ente turismo spagnolo |
| TÜSİAD | https://tusiad.org | — | TR/EN | TR | — | Industria e business turchi |
| UIA — Unión Industrial Argentina | https://uia.org.ar | — | ES | AR | — | Industria argentina |
| UIC — International Union of Railways | https://uic.org | — | EN/FR | Globale | — | Ferrovie mondiali |
| UITP | https://www.uitp.org | — | EN | Globale | — | Trasporto pubblico internazionale |
| ULI — Urban Land Institute | https://uli.org | — | EN | Globale | — | Real estate e uso del suolo |
| VCI | https://www.vci.de | — | DE | DE | — | Chimica tedesca |
| VDA | https://www.vda.de | — | DE/EN | DE | — | Industria automobilistica tedesca |
| VisitBritain | https://www.visitbritain.org | — | EN | GB | — | Ente turismo britannico, dati |
| VNO-NCW | https://www.vno-ncw.nl | — | NL | NL | — | Imprese olandesi |
| WTTC | https://wttc.org | — | EN | Globale | — | Consiglio mondiale viaggi e turismo |
