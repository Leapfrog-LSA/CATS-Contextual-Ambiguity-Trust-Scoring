# Domain-provenance maintenance — October 2026

A first-run test of 1.7.0 against an Italian NewsGuard list found **Open**
(`open.online`) scored 40.2, the lowest of the sample. The cause was the
domain-provenance penalty: `.online` is in `SUSPICIOUS_TLDS`, so the domain
got a 40-point red flag, which is a 24-point penalty at
`DOMAIN_PENALTY_WEIGHT = 0.6`. Open is a legitimate national outlet, and
`data/labels.jsonl` itself labels it 85.

## The change

A domain on a suspicious TLD is now exempt from the `suspicious_tld` flag when
the popularity table is loaded **and** ranks the domain, unless the domain
also imitates a brand (`typosquat` or `brand_on_bad_tld`).

This mirrors the September rule for `AMBIGUOUS_CCTLDS`, which fire only when
the domain is unranked. The rule never fires on missing data:

- With no table (`data/tranco_top1m.csv` absent), the flag behaves exactly as
  before.
- A ranked brand imitation keeps both flags.
- `brand_on_bad_tld` is still computed from the raw TLD, so popularity cannot
  hide an impersonation.

New helper: `_is_ranked(host)`, the mirror of `_is_unranked`. Both return
False when the table is unavailable.

## Evidence

All numbers use the Tranco top-1M list downloaded on 2026-10-02
(`make tranco-download`).

| Set | Hosts on a suspicious TLD | Tranco-ranked |
|---|---|---|
| `data/disinfo_sources.csv` (clones) | 35 | **0** |
| `data/Fonti_OSINT.csv` (legitimate catalogue) | 4 | 3: `open.online` #40 089, `fergana.agency` #140 712, `lindipendente.online` #285 088 |

The fourth catalogue host, `africauncensored.online`, is unranked and stays
flagged, at 55 with the corroboration bonus.

Measured through `compute_domain_provenance`, before and after:

| Measure | Before | After |
|---|---|---|
| Catalogue domains flagged (false positives) | 26 / 5 053 (0.51%) | **23 / 5 053 (0.46%)** |
| Clone domains flagged (`disinfo_sources.csv`) | 60 / 113 | **60 / 113** |
| Future holdout (n=53), `research/validate_domain_penalty.py` | concordance 0.762, Spearman 0.578 | **identical** |

The holdout contains no suspicious-TLD source, so it cannot move. The
catalogue and clone audits are the relevant checks. The clone set is used
only to *measure* recall, never as a scoring input (leakage discipline).

## Limits

- **The exemption needs the Tranco table.** A default `pip install` has no
  table, so Open is still penalised there. Shipping the table, or a small
  derived list of ranked suspicious-TLD domains, depends on the Tranco
  licence. That check is already an open roadmap item for a human.
- **Rank is not reliability.** A clone that gathers enough traffic to enter
  the top 1M would be exempt from `suspicious_tld`, though not from the brand
  flags. None of the 35 known clones is ranked today. Re-run this audit when
  the clone corpus or the list changes.
- `DOMAIN_PENALTY_WEIGHT` (0.6) is unchanged.

## Test fragility fixed in passing

`tests/unit/test_adversarial.py::test_domain_penalty_is_clamped_and_asymmetric`
assumed the Tranco file was absent: with the file present, `bild.pics`
scores 80, not 65. It now pins the table to "unavailable", like the tests
fixed in September.
