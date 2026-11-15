# Related work and positioning — DRAFT

> **DRAFT — do not cite or republish.** Every external reference on this page
> is marked *to be verified on the primary source*: none has yet been opened
> and confirmed by a person. Do not quote this page, or copy its references
> elsewhere, until that check is done.
>
> - **Authoritative source:** §1.4 *Stato dell'Arte e Posizionamento* of the
>   technical whitepaper v1.1
>   ([`CATS_WhitePaper_Tecnico_v1.1.docx`](CATS_WhitePaper_Tecnico_v1.1.docx),
>   in Italian). This page is an English rendering of that section; where the
>   two differ, the whitepaper wins.
> - **Scores are ordinal**, not calibrated probabilities. Nothing on this page
>   changes a score, band, weight or signal.

## 1. What is being measured: four distinct objects

In the literature, "reliability" covers four different objects, which
operational systems tend to conflate. CATS estimates the first one, and only
that one.

| Object | Question | Research line |
|---|---|---|
| **Source** | How often has this source told the truth? | Truth discovery, source factuality |
| Claim | Is this single fact true? | Automated fact-checking |
| Support | Does the cited source actually support the sentence? | Attribution, NLI |
| Dependence | Are the sources that agree independent? | Copy detection, source dependence |

CATS does not verify claims, does not check that a citation supports a
sentence, and does not correct for dependence between sources. This is not an
implicit limitation: it is the definition of the scope. Two distinctions shape
the design. *Reliability is not trust*: the first is a statistical property
estimable from history, the second is an analyst's decision that depends on
context and stakes. *Source is not information*: a reliable source can report
wrong information, and vice versa.

## 2. The method is not new

CATS does not claim a novel method: it claims to apply published methods to a
domain that research does not cover. As summarised in whitepaper §1.4.2:

- **Truth discovery** (Li et al., SIGKDD Explorations 2016) estimates claim
  truth and source reliability jointly, updating each from the other.
- **Knowledge-Based Trust** (Dong et al., PVLDB 2015) estimates reliability
  from the correct facts a page contains rather than from links.
- **The Beta Reputation System** (Jøsang and Ismail, 2002) models reputation as
  a Beta distribution over feedback, with a forgetting factor. Two properties
  follow that CATS shares by design: a new source starts neutral with high
  uncertainty, and the score worsens if behaviour worsens.
- **News outlets:** Baly et al. (EMNLP 2018) rate the whole outlet rather than
  the single article; Burdisso et al. (NAACL 2024) estimate a continuous degree
  from the link graph over about 17,000 sources, with a Spearman correlation
  of 0.80 against NewsGuard scores.

## 3. Relation to the Admiralty Code

The de facto standard in intelligence and OSINT is the Admiralty Code (NATO
STANAG 2511, now AJP-2.1): two separate scales, source reliability from A to F
and information credibility from 1 to 6. **CATS sits entirely on the A–F
axis.** The continuity is that the standard judges reliability only on sources
used in the past, assigning F to a new source; it is the same behavioural
logic by which CATS, without enough history, does not produce a judgement but
an insufficient-evidence flag.

Recent research documents three weaknesses that an explicit rule avoids by
construction (whitepaper §1.4.3): analysts collapse onto the A1/B2/C3 diagonal,
using source reliability to infer information credibility (Mandel et al.,
2025); with conflicting cues the same analyst is poorly repeatable over time
(Mandel et al., 2023); and criteria such as "authenticity" and "competence" are
not operationalised (Irwin and Mandel, 2019).

**Not a feature.** CATS does not map its output onto the A–F grid. An optional
A–F view of the output is an open long-term item in the
[roadmap](piano_sviluppo_roadmap_2026-09.md) (Phase 3), with no date; it is not
an existing function.

## 4. Why no LLM produces the score

Studies from 2025–2026 advise against using a language model as the judge of a
source's reliability. Ratings produced by nine LLMs agree strongly with each
other (Spearman 0.79) but only moderately with human experts (0.50) (Yang and
Menczer, ACM WebSci 2025), and the prior tied to the outlet's brand can
outweigh the article's content. **No CATS component calls an LLM to produce
the score:** the four signals are deterministic functions of the message
history.

## 5. The gap CATS fills

The individual components of a behavioural trust score are established prior
art. The little-covered space is their application to heterogeneous Italian
sources — chamber-of-commerce registers, court records, local press — with an
output that is verifiable and readable by a lawyer. The literature validates
almost exclusively on ratings of English-language outlets (MBFC, NewsGuard,
Wikipedia): labelled datasets for CATS's target domain are missing, and that is
also its main validation vulnerability (whitepaper §5.4).

## 6. References

Every row is *to be verified on the primary source*. Entries (a) are
transcribed as they appear in the whitepaper, without correction or
completion; the whitepaper's own note on references 12–23 says they come from
a September 2026 literature review and must be checked against the primary
sources before any academic citation, and the same check is an open item of the
[Zenodo deposit checklist](zenodo_deposit_checklist.md). This list does not
claim that no comparable tools or more recent work exist.

| # | Reference | Provenance | Verification status |
|---|---|---|---|
| 12 | Li, Y. et al. (2016). A Survey on Truth Discovery. SIGKDD Explorations 17(2). | (a) Whitepaper v1.1, Appendix D | To be verified on the primary source |
| 13 | Dong, X. L., Berti-Equille, L., Srivastava, D. (2009). Integrating Conflicting Data: The Role of Source Dependence. PVLDB 2(1). | (a) Whitepaper v1.1, Appendix D | To be verified on the primary source |
| 14 | Dong, X. L. et al. (2015). Knowledge-Based Trust: Estimating the Trustworthiness of Web Sources. PVLDB 8(9). | (a) Whitepaper v1.1, Appendix D | To be verified on the primary source |
| 15 | Jøsang, A., Ismail, R. (2002). The Beta Reputation System. Bled eCommerce Conference. | (a) Whitepaper v1.1, Appendix D | To be verified on the primary source |
| 16 | Baly, R. et al. (2018). Predicting Factuality of Reporting and Bias of News Media Sources. EMNLP. | (a) Whitepaper v1.1, Appendix D | To be verified on the primary source |
| 17 | Burdisso, S. et al. (2024). Reliability Estimation of News Media Sources: Birds of a Feather Flock Together. NAACL. | (a) Whitepaper v1.1, Appendix D | To be verified on the primary source |
| 18 | Thorne, J. et al. (2018). FEVER: a Large-scale Dataset for Fact Extraction and VERification. NAACL. | (a) Whitepaper v1.1, Appendix D | To be verified on the primary source |
| 19 | Irwin, D., Mandel, D. R. (2019). Improving Information Evaluation for Intelligence Production. | (a) Whitepaper v1.1, Appendix D | To be verified on the primary source |
| 20 | Mandel, D. R. et al. (2023). Meta-informational cue inconsistency and judgment of information accuracy. Journal of Behavioral Decision Making. | (a) Whitepaper v1.1, Appendix D | To be verified on the primary source |
| 21 | Mandel, D. R. et al. (2025). The effect of source reliability and information credibility on judgments of information quality. Judgment and Decision Making. | (a) Whitepaper v1.1, Appendix D | To be verified on the primary source |
| 22 | Yang, K.-C., Menczer, F. (2025). Accuracy and Political Bias of News Source Credibility Ratings by Large Language Models. ACM WebSci. | (a) Whitepaper v1.1, Appendix D | To be verified on the primary source |
| 23 | NATO. AJP-2.1 / STANAG 2511 — Allied Joint Doctrine for Intelligence Procedures (Admiralty Code). | (a) Whitepaper v1.1, Appendix D | To be verified on the primary source |
| — | NewsGuard's published criteria, compared with CATS in a desk study. No NewsGuard score, label or list is used, and no score changes. | (b) [`newsguard_criteria_comparison_2026-11.md`](newsguard_criteria_comparison_2026-11.md) | To be verified on the primary source |
| — | CRED-1 (external reference dataset, 2 674 domains). Only 14 of 114 CATS-known domains (12%) appear in it, and 0 of the 50 clone domains. Evaluated and rejected as a calibration source; not used in any pipeline. | (b) [`data/README.md`](../data/README.md) → `cred1_current.csv` | To be verified on the primary source |
| — | Media Bias/Fact Check (MBFC) *Factual Reporting* ratings, used as reference labels (distant supervision) with attribution; terms not yet verified — see the open legal TODO in [`NOTICE.md`](../NOTICE.md) §2. | (b) [`data/README.md`](../data/README.md) → `ratings.csv` | To be verified on the primary source |

## 7. What CATS does not see

The general limits are listed in the README under
[Honest limits](../README.md#honest-limits) and in the warning under
[Trust score bands](../README.md#trust-score-bands); they are not repeated
here. Two further points matter when placing CATS next to the work above:

1. **Low recall on unreliable sources.** On the 06-Jul-2026 future holdout,
   with the shipped calibrated weights, CATS calls unreliable 5 of the 15
   unreliable sources: recall 0.333, precision 1.000 measured over only 5
   predictions, 53 sources in all. Read it as a small-sample figure
   ([calibration.md](calibration.md)).
2. **Fake news on ordinary domains is invisible.** False content published on
   an ordinary domain remains invisible to every signal CATS currently has
   ([content-credibility spike](content_credibility_spike_2026-08.md)).

For the record, not as a proposal: the roadmap holds no spike on new signals
until mid-December 2026. Model-based content credibility and cross-source
corroboration are long-term items, conditional on a validation set able to
separate them from noise and on a user who asks for them
([roadmap](piano_sviluppo_roadmap_2026-09.md)).
