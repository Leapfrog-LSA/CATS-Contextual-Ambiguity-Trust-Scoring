"""
Full coverage/agreement check: every cats_flag in data/disinfo_sources.csv
against CRED-1's category, not just satire (see research/compare_satire.py
for that narrower first pass).

The two taxonomies are not equivalent, so this does not force a 1:1 mapping
where none makes conceptual sense:
  - suspect_source: people/organisations with no domain of their own (e.g.
    "Avvocato Giacinto Canzona") -- not checkable against CRED-1, which is a
    domain registry.
  - disinformation_clone: infrastructure/typosquat impersonation -- CRED-1
    does not track this concept at all, so absence is coverage information,
    not a judgement.
  - fake_news_site / fake_news_portal: comparable to CRED-1. Its
    fake/conspiracy/unreliable/mixed/rumor labels are treated as "consistent"
    (both sources say the source is bad, with different granularity);
    satire or reliable is a genuine conflict.

Read-only, one-off analysis script -- writes nothing, feeds no pipeline.

Usage:
    python research/compare_all_flags.py
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CRED1 = ROOT / "data" / "cred1_current.csv"
CATS_DISINFO = ROOT / "data" / "disinfo_sources.csv"

UNRELIABLE_LIKE = {"fake", "conspiracy", "unreliable", "mixed", "rumor"}


def norm(d):
    d = (d or "").strip().lower()
    for p in ("https://", "http://"):
        if d.startswith(p):
            d = d[len(p) :]
    if d.startswith("www."):
        d = d[4:]
    return d.split("/")[0]


def has_domain(cats_row):
    d = cats_row["domain"].strip()
    return "." in d and " " not in d and "/" not in d.replace("://", "")


def main():
    with CRED1.open(encoding="utf-8") as f:
        cred1_by_domain = {norm(r["domain"]): r for r in csv.DictReader(f)}

    with CATS_DISINFO.open(encoding="utf-8") as f:
        cats_rows = list(csv.DictReader(f))

    by_flag = {}
    for row in cats_rows:
        by_flag.setdefault(row["cats_flag"], []).append(row)

    print(f"Domains in disinfo_sources.csv (CATS): {len(cats_rows)}")
    print(f"Distribution by cats_flag: {[(k, len(v)) for k, v in sorted(by_flag.items())]}\n")
    print("=" * 78)

    grand_covered = grand_consistent = grand_conflict = 0

    for flag, rows in sorted(by_flag.items()):
        print(f"\n--- cats_flag = {flag} ({len(rows)} domains) ---")
        not_applicable = [r for r in rows if not has_domain(r)]
        checkable = [r for r in rows if has_domain(r)]
        if not_applicable:
            print(f"  {len(not_applicable)} with no checkable domain (people/organisations, not URLs)")

        covered = consistent = conflict = 0
        details = []
        for r in checkable:
            d = norm(r["domain"])
            c1 = cred1_by_domain.get(d)
            if c1 is None:
                continue
            covered += 1
            cred1_cat = c1["category"]
            if flag == "satire_recognizable":
                ok = cred1_cat == "satire"
            elif flag in ("fake_news_site", "fake_news_portal"):
                ok = cred1_cat in UNRELIABLE_LIKE
            else:
                ok = None
            if ok is True:
                consistent += 1
            elif ok is False:
                conflict += 1
                details.append((d, cred1_cat, c1["credibility_score"]))
            else:
                details.append((d, cred1_cat, c1["credibility_score"], "coverage only, not comparable"))

        print(f"  covered by CRED-1: {covered}/{len(checkable)} checkable domains")
        if flag in ("satire_recognizable", "fake_news_site", "fake_news_portal"):
            print(f"  consistent: {consistent}  |  conflicting: {conflict}")
            grand_consistent += consistent
            grand_conflict += conflict
        grand_covered += covered

        for item in details:
            if len(item) == 4:
                d, cat, score, note = item
                print(f"    {d}: CRED-1={cat} (score {score}) -- {note}")
            else:
                d, cat, score = item
                print(f"    CONFLICT  {d}: CATS={flag}  vs  CRED-1={cat} (score {score})")

    print("\n" + "=" * 78)
    print(f"TOTAL CATS domains covered by CRED-1 (any category): {grand_covered}")
    print(f"TOTAL genuinely comparable checks (satire + fake_news_*): {grand_consistent + grand_conflict}")
    print(f"  consistent: {grand_consistent}  |  conflicting: {grand_conflict}")
    if (grand_consistent + grand_conflict) > 0:
        pct = 100 * grand_conflict / (grand_consistent + grand_conflict)
        print(f"  overall conflict rate: {pct:.0f}%")


if __name__ == "__main__":
    main()
