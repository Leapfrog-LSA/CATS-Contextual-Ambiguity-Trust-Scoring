"""
Manual cross-check against CRED-1 (aloth/cred-1, CC BY 4.0) -- a reference
tool, not a pipeline. Given a domain encountered during OSINT work, prints
what CRED-1 knows about it, if anything.

Deliberately NOT wired into any CATS pipeline (calibration, scoring, or
domain_provenance): see docs/calibration.md and the coverage/agreement
analysis below for why. cats_flag / evidence_level in data/disinfo_sources.csv
use a different taxonomy than CRED-1's category field (fake/conspiracy/
unreliable/satire/mixed/reliable/rumor); this tool does not attempt to map
between them, it just reports CRED-1's own label for a human to weigh.

Attribution: CRED-1 is (c) Alexander Loth, CC BY 4.0
(https://github.com/aloth/cred-1). It aggregates OpenSources.co (CC BY 4.0,
Melissa Zimdars et al.) and the Iffy.news Index (MIT, Reynolds Journalism
Institute) -- see data/cred1_current.csv.

Coverage and agreement, checked against data/disinfo_sources.csv
(2026-08-29, see research/compare_all_flags.py for the full breakdown):
only 14 of 114 CATS-known domains (12%) are also in CRED-1, and of those 14,
5 (36%) disagree on category -- in both directions (CRED-1 calling something
"satire" that CATS's debunker sources call a fake-news factory, and once the
reverse). CRED-1 has zero coverage of the 50 Doppelganger-style clone
domains in data/disinfo_sources.csv -- it tracks editorial credibility, not
domain/infrastructure impersonation. Treat any single CRED-1 label as a
starting point for a human to check, never as a verdict on its own.

Usage:
    python research/cred1_lookup.py example.com [another-domain.it ...]
"""

import csv
import sys
from pathlib import Path

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "cred1_current.csv"


def normalize(domain: str) -> str:
    d = domain.strip().lower()
    for prefix in ("https://", "http://"):
        if d.startswith(prefix):
            d = d[len(prefix) :]
    if d.startswith("www."):
        d = d[4:]
    return d.split("/")[0]


def load_index():
    with CSV_PATH.open(encoding="utf-8") as f:
        return {row["domain"].strip().lower(): row for row in csv.DictReader(f)}


def report(domain: str, row: "dict | None") -> str:
    if row is None:
        return (
            f"{domain}: not in CRED-1. Not evidence of reliability either way -- "
            f"CRED-1 skews English-language; an absent Italian/regional domain is "
            f"simply outside its coverage."
        )
    lines = [f"{domain}: found in CRED-1"]
    lines.append(f"  CRED-1 category: {row['category']}  (credibility_score {row['credibility_score']})")
    if row.get("iffy_factual") or row.get("iffy_bias"):
        lines.append(f"  Iffy/MBFC: factual={row.get('iffy_factual') or '-'}  bias={row.get('iffy_bias') or '-'}")
    if row.get("tranco_rank"):
        lines.append(f"  Tranco rank: {row['tranco_rank']}")
    if row.get("domain_age_years"):
        lines.append(f"  domain age: {row['domain_age_years']} years (registered {row.get('domain_registered', '?')})")
    if row.get("factcheck_claims"):
        lines.append(f"  linked fact-checked claims: {row['factcheck_claims']}")
    if row.get("safe_browsing_flagged") in ("True", "true", "1"):
        lines.append("  WARNING: flagged by Google Safe Browsing")
    lines.append(f"  CRED-1 upstream sources: {row.get('sources', '?')}")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python research/cred1_lookup.py domain1 [domain2 ...]")
        raise SystemExit(1)
    index = load_index()
    for raw in sys.argv[1:]:
        d = normalize(raw)
        print(report(d, index.get(d)))
        print()


if __name__ == "__main__":
    main()
