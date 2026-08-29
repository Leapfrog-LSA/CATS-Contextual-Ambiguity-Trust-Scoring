"""
Coverage/agreement check: CRED-1's "satire" domains against
data/disinfo_sources.csv's satire_recognizable entries.

Read-only, one-off analysis script (same category as the other research/
spikes) -- writes nothing, feeds no pipeline. Run it again after either data
file is updated to get a fresh count; the numbers below are a snapshot.

Usage:
    python research/compare_satire.py
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CRED1 = ROOT / "data" / "cred1_current.csv"
CATS_DISINFO = ROOT / "data" / "disinfo_sources.csv"


def norm(d):
    d = (d or "").strip().lower()
    for p in ("https://", "http://"):
        if d.startswith(p):
            d = d[len(p) :]
    if d.startswith("www."):
        d = d[4:]
    return d.split("/")[0]


def main():
    with CRED1.open(encoding="utf-8") as f:
        cred1_rows = list(csv.DictReader(f))
    cred1_satire = {norm(r["domain"]): r for r in cred1_rows if r["category"] == "satire"}

    with CATS_DISINFO.open(encoding="utf-8") as f:
        cats_rows = list(csv.DictReader(f))
    cats_by_domain = {norm(r["domain"]): r for r in cats_rows}

    print(f"CRED-1 domains labelled 'satire': {len(cred1_satire)}")
    print(f"Domains in disinfo_sources.csv (CATS): {len(cats_by_domain)}")

    overlap = sorted(set(cred1_satire) & set(cats_by_domain))
    print(f"Overlap (CRED-1 'satire' domains also in CATS): {len(overlap)}\n")

    agree, disagree = [], []
    for d in overlap:
        cats_flag = cats_by_domain[d]["cats_flag"]
        if cats_flag == "satire_recognizable":
            agree.append((d, cats_flag))
        else:
            disagree.append((d, cats_flag))

    print(f"=== AGREE ({len(agree)}) -- CRED-1 'satire' == CATS 'satire_recognizable' ===")
    for d, flag in agree:
        print(f"  {d}  (CATS: {flag})")

    print(f"\n=== DISAGREE ({len(disagree)}) -- CRED-1 says 'satire', CATS says something else ===")
    for d, flag in disagree:
        score = cred1_satire[d]["credibility_score"]
        print(f"  {d}  ->  CRED-1: satire (score {score})  |  CATS: {flag}")

    if overlap:
        pct = 100 * len(disagree) / len(overlap)
        print(f"\nDisagreement rate on the checkable subset: {len(disagree)}/{len(overlap)} ({pct:.0f}%)")
    print(
        f"\nCoverage caveat: only {len(overlap)} of {len(cred1_satire)} CRED-1 'satire' domains "
        f"are also in CATS -- the other {len(cred1_satire) - len(overlap)} have no second source to "
        f"check against, so this disagreement rate applies only to the checkable subset, not to "
        f"CRED-1's full 'satire' list."
    )


if __name__ == "__main__":
    main()
