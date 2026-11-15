# NewsGuard's criteria compared with CATS — 2026-11-15

A desk study. It reads NewsGuard's published methodology and asks which parts
CATS could measure automatically. It decides no legal question and changes
no score.

> **What this is, and is not.**
> - **No NewsGuard data.** No NewsGuard score, label or list is used, stored
>   or redistributed in this repository. The criteria below are paraphrased
>   from NewsGuard's public pages.
> - **No scoring change.** `SIGNAL_NAMES`, the weight table and the band cutoffs
>   (80/60/40/20) are unchanged (ENGINE 1.4). Scores stay **ordinal**, not
>   calibrated probabilities (WP 4.1/4.3).
> - **No new signal before mid-December 2026** (roadmap constraint). The only
>   code change is in collection (*Phase A* below).

## 1. Summary

- **Different method.** NewsGuard's journalists rate a site by hand on nine
  pass/fail criteria. NewsGuard states that AI plays no role in those
  judgements. CATS scores a source automatically from its publishing
  behaviour. The two are complements, not substitutes.
- **Half of NewsGuard's points need human judgement.**
  - **The criteria:** false content (22), responsible gathering (18) and
    misleading headlines (10).
  - **What CATS has tried:** the August 2026 content-credibility spike tested
    lexicon proxies for the last two and rejected them
    ([`content_credibility_spike_2026-08.md`](content_credibility_spike_2026-08.md)).
  - **In CATS today:** these remain the analyst's job, flagged by
    `requires_human_review`.
- **The transparency criteria are the automatable part.** These are author
  bylines, ownership and the responsible editor, and in part corrections,
  opinion labelling and advertising labelling.
  - **Limit:** a machine can detect that an element is *absent*, not that it
    is true.
  - **Form:** the right shape is a **one-sided penalty**, like
    `apply_domain_penalty`, not a weighted signal (see `CLAUDE.md`).
- **NewsGuard's data is licensed, not open.** Its Terms of Service restrict
  reuse, derivative works and use "in algorithms", including research use
  without a licence. Whether and how CATS could use NewsGuard scores is a
  question for counsel (§5), not for this note.

## 2. NewsGuard's criteria and how CATS could approach them

Source: the rating criteria page (last updated 14 April 2026),
<https://www.newsguardtech.com/it/valutazioni/processo-e-criteri-di-valutazione/>
and <https://www.newsguardtech.com/ratings/rating-process-criteria/>.

**How NewsGuard scores:**
- **Scale:** 0–100, the sum of nine pass/fail criteria.
- **N/A rule:** a criterion that does not apply to a site gives its full
  points. For example, the advertising criterion for a site with no ads.
- **Tiers:** 100, 75–99, 60–74, 40–59 and 0–39.
- **Not scored:** satire sites and user-content platforms get a description,
  not a score.

| # | Criterion (paraphrased) | Points | CATS feasibility | How, and what blocks it |
|---|---|---:|---|---|
| C1 | Does not repeatedly publish false content | 22 | Human judgement | Matching texts against a catalogue of known false claims would need NewsGuard's licensed *False Claim Fingerprints* feed. Using it would make NewsGuard labels unusable for validation (leakage). |
| C2 | Gathers and presents information responsibly | 18 | Human judgement | The attribution lexicon failed in the August spike. A real test needs full articles, which raises the open TDM question (`DATA_LICENSE` §3). |
| C3 | Regularly corrects errors | 12.5 | Partial, new collection | Possible checks: a corrections page on the site, and "Rettifica" or "Aggiornamento:" markers in titles. A site under a year old is not failed for lacking corrections. |
| C4 | Separates news and opinion | 12.5 | Partial | Possible checks: an "Opinioni" or "Editoriale" category or URL path. Opinion language inside news reports needs a model. N/A for transparent advocacy sites. |
| C5 | Avoids misleading headlines | 10 | Not with lexicons | Needs a title-versus-body model. `title_len` (below) keeps the split for later. |
| C6 | Discloses ownership and financing | 7.5 | Presence only, new collection | On the "Chi siamo" page or footer: publisher name, VAT number (P.IVA), ROC or court registration. Whether a disclosure is adequate needs a human. |
| C7 | Clearly labels advertising | 7.5 | Partial, low priority | Possible checks: "Contenuto sponsorizzato" or "Pubbliredazionale" markers, `rel="sponsored"`. Unlabelled native advertising cannot be detected. N/A for sites without ads. |
| C8 | Names those in charge, discloses conflicts | 5 | Presence only, new collection | A "Direttore responsabile" line. Conflicts of interest need a human. |
| C9 | Names content authors with bio or contact | 5 | Yes, from feeds (Phase A) | Measures: share of signed items, and author concentration. A staff page with areas of expertise passes the criterion even without bylines. |

## 3. Measured coverage (2026-11-15)

**Scope:** one fetch of the 125 feeds of `data/labels.jsonl` with the
collector's own code. 99 parsed; the rest were blocked or failed on this
egress. Aggregates only: no text and no author ID was stored.

| Measure | Value |
|---|---:|
| Feeds with at least one signed item | 72 of 99 |
| Feeds with ≥ 80% of items signed | 67 of 99 |
| Feeds with at least one `<category>` | 65 of 99 |
| Feeds with ≥ 80% of items categorised | 62 of 99 |
| Items signed / categorised | 2,475 / 2,394 of 3,842 |
| Signed feeds with a single distinct author | 13 of 72 |

**What the numbers show:**
- **Missing data is the common case.** About a quarter of feeds carry no
  byline at all. A C9-style measure must therefore not treat a missing byline
  as evidence by itself. The staff-page rule and the N/A cases above apply.
- **A single author is not a red flag by itself.** In NewsGuard's 2023 report
  on Italian AI content farms, every site attributed all articles to one
  author. But 13 signed registry feeds also show one author. Whether these are
  generic newsroom bylines was not checked (only hashes were computed). The
  signal needs care before any use.

## 4. Phased plan

**Phase A — now, no scoring change (this change)**
1. This note.
2. **Collection change** in `cats/calibration/collect_rss.py`. Feed fields that
   no signal reads today are kept in each message's `metadata`. A feed only
   exposes its recent window, so this history cannot be rebuilt later.
   - **`title_len`:** the title is always the first `title_len` characters of
     `text`, so it is not stored twice.
   - **`authors`:** pseudonymous IDs, never names. Each ID is the first 16 hex
     digits of SHA-256 over the normalised byline.
     - The hash is unsalted, so generic bylines ("Redazione") can still be
       recognised later by hashing them.
     - Pseudonymised data is still personal data under the GDPR. See the
       question added to `DATA_LICENSE` §3 (e).
   - **`categories`:** `<category>` labels, deduplicated and capped.
   - **`Message.text` is unchanged** (title + summary), so every signal sees
     the same input. A unit test checks that scores are identical with and
     without the new metadata.
   - **Cost:** it adds roughly 80 bytes per message, about +12% on a daily
     snapshot of about 5,500 messages.

**Phase B — after mid-December 2026, toward the January 2027 recalibration**
- **Transparency penalty:** a one-sided penalty for C6, C8, C9 and possibly
  C3, outside `SIGNAL_NAMES`.
  - **Lexicons:** fixed and versioned before any correlation is computed.
  - **Rules:** N/A cases respected.
  - **Validation:** on the **future holdout**.
- **Domain registration data:** domain age and registration bursts from
  WHOIS/RDAP, as an extension of domain provenance. This needs future-holdout
  re-validation, plus a GDPR check on registrant data.
- **AI content-farm signal:** author concentration or chatbot error phrases.
  It would be a new weighted signal, so it needs the full recalibration
  cycle. NewsGuard's AI-farm lists must not be used to build the lexicon if
  they are later used as labels.

**Phase C — only with a licence and legal advice**
- **NewsGuard scores as validation labels:**
  - kept privately, outside the repository;
  - reported only as rank metrics on the 0–100 scale, separately from MBFC.
  - Validating a penalty built on NewsGuard's own criteria against NewsGuard
    scores would be close to circular, and must be reported as such.
- **False Claim Fingerprints:** a feature built on this feed is incompatible
  with using NewsGuard as labels.

## 5. Open questions for the maintainer and counsel

These are open questions, not determinations.

1. **Licence scope:** does a NewsGuard research licence allow using ratings as
   calibration targets, or only for validation? Does calibration count as use
   "in algorithms" (ToS §5)?
2. **Publishing:** could anything derived from NewsGuard ratings be published
   in an MIT-licensed repository or on PyPI? The options are per-domain
   scores, binary labels, aggregate metrics only, or weights calibrated
   against the ratings. ToS §8 forbids sublicensing.
3. **Terms:** who would hold the licence, at what cost, and what must be
   deleted when it ends?
4. **GDPR basis:** what is the lawful basis for storing pseudonymous author
   IDs and, in Phase B, registrant data from WHOIS/RDAP? See `DATA_LICENSE`
   §3 (e).

## 6. Independent evaluations (for context)

- **Agreement with other lists.** Lin et al. 2023, *PNAS Nexus* 2(9),
  doi:10.1093/pnasnexus/pgad286, compare six expert lists, including
  NewsGuard and MBFC. The lists correlate strongly with one another, and the
  first principal component explains about 68% of the variance.
- **Stability and bias.** Lühring et al. 2025, *Journal of Quantitative
  Description: Digital Media* 5, doi:10.51685/jqd.2025.003, find NewsGuard
  ratings stable since 2022 across nine countries, Italy included. They warn
  against relying only on the binary reliable/unreliable split.
- **Gaps in the literature.** No published inter-rater reliability study was
  found. No study was found that compares NewsGuard scores with
  message-history signals like CATS's.

Pages read for this note, among others:
- <https://www.newsguardtech.com/how-newsguard-uses-and-doesnt-use-ai/>
- <https://www.newsguardtech.com/it/termini-di-servizio/>
- <https://www.newsguardtech.com/special-reports/ai-tracking-center>
- <https://www.newsguardtech.com/ratings/false-claim-fingerprints-process/>

Quotes and figures from the Terms of Service must be re-checked on the live
page before anyone relies on them.
