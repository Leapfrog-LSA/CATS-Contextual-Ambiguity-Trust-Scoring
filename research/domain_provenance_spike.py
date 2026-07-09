"""Research spike (task #8): does a domain-provenance signal add discriminative
power beyond the four behavioural signals?

Motivation: the 6-Jul future-snapshot validation showed CATS's discrimination
rests almost entirely on `silence` (holdout rho -0.43); coherence/volatility/
gaming are near zero even on four weeks of history. A source that publishes on
a regular cadence therefore defeats the only informative signal. This spike
tests the highest-leverage candidate from the findings: a signal computed from
the source *domain* rather than its messages — the class of feature to which
impersonation clones (Doppelganger) are visible and the behavioural signals are
blind.

Leakage discipline: the score is built from GENERAL domain structure (rare/cheap
TLDs, free-hosting subdomains, edit distance to a fixed brand list) — never from
membership in `data/disinfo_sources.csv`. It would therefore fire on unseen
domains with the same structure, not just the labelled ones.

Run from the repo root:  python research/domain_provenance_spike.py
Reads only committed data (data/labels.jsonl, data/holdout_future.jsonl,
data/snapshots/labelled_sources_2026-07-06.jsonl, data/calibrated_weights.json).
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent

# Cheap/rare TLDs favoured by clone networks — the exact set Doppelganger used.
SUSPICIOUS_TLDS = {
    "pics",
    "ltd",
    "cfd",
    "live",
    "work",
    "fun",
    "today",
    "asia",
    "vip",
    "ws",
    "llc",
    "agency",
    "cab",
    "me",
    "online",
    "cc",
    "co",
    "life",
    "pro",
    "in",
    "xyz",
    "top",
    "click",
}
FREE_HOSTS = ("altervista.org", "blogspot.com", "wordpress.com", "weebly.com", "wixsite.com", "blogspot.it")
# Fixed brand list for typo-squat detection (independent of the labelled set).
MAJOR_BRANDS = [
    "repubblica.it",
    "corriere.it",
    "ilfattoquotidiano.it",
    "ilgiornale.it",
    "panorama.it",
    "ilsole24ore.it",
    "ansa.it",
    "spiegel.de",
    "bild.de",
    "welt.de",
    "faz.net",
    "sueddeutsche.de",
    "tagesspiegel.de",
    "t-online.de",
    "theguardian.com",
    "dailymail.co.uk",
    "reuters.com",
    "foxnews.com",
    "libero.it",
    "sky.it",
    "20minutes.fr",
]


def _lev(a: str, b: str) -> int:
    if abs(len(a) - len(b)) > 3:
        return 9
    dp = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        prev = dp[0]
        dp[0] = i
        for j, cb in enumerate(b, 1):
            cur = dp[j]
            dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + (ca != cb))
            prev = cur
    return dp[-1]


def domain_provenance_score(url: str) -> float:
    """0-100 domain red-flag score; higher = more impersonation/clone signals."""
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    if not host:
        return 0.0
    score = 0.0
    if any(host.endswith(h) or ("." + h) in host for h in FREE_HOSTS):
        score += 45
    tld = host.rsplit(".", 1)[-1]
    if tld in SUSPICIOUS_TLDS:
        score += 40
    best = min((_lev(host, b) for b in MAJOR_BRANDS), default=9)
    if 1 <= best <= 2 and host not in MAJOR_BRANDS:
        score += 50
    for b in MAJOR_BRANDS:
        bname = b.rsplit(".", 1)[0]
        if len(bname) >= 4 and bname in host and not host.endswith(b) and tld in SUSPICIOUS_TLDS:
            score += 25
            break
    return min(score, 100.0)


def _rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
            j += 1
        for k in range(i, j + 1):
            r[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(xs, ys) -> float:
    rx, ry = _rank(xs), _rank(ys)
    n = len(xs)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def concordance(preds, labels) -> float:
    n = len(preds)
    num = den = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            if labels[i] == labels[j]:
                continue
            den += 1
            hi, lo = (i, j) if labels[i] > labels[j] else (j, i)
            if preds[hi] > preds[lo]:
                num += 1
            elif preds[hi] == preds[lo]:
                num += 0.5
    return num / den if den else 0.0


_NEG = {"volatility", "silence", "gaming"}


def _behavioural(rec, weights):
    g = rec["source_type"] if rec["source_type"] in ("social", "news") else "default"
    wt = weights[g]
    num = den = 0.0
    for k, v in rec["signals"].items():
        rv = 100 - v if k in _NEG else v
        num += rv * wt[k]
        den += wt[k]
    return num / den


def main() -> None:
    labels_rows = [json.loads(line) for line in open(ROOT / "data/labels.jsonl")]
    dp = [domain_provenance_score(r["url"]) for r in labels_rows]
    labels = [r["label"] for r in labels_rows]
    print(f"Registry (n={len(labels_rows)}): rho(domain_redflag, label) = {spearman(dp, labels):+.3f}")

    hold = [json.loads(line) for line in open(ROOT / "data/holdout_future.jsonl")]
    snap = [json.loads(line) for line in open(ROOT / "data/snapshots/labelled_sources_2026-07-06.jsonl")]
    weights = json.load(open(ROOT / "data/calibrated_weights.json"))["weights"]
    assert len(hold) == len(snap), (len(hold), len(snap))

    hl = [r["label"] for r in hold]
    beh = [_behavioural(r, weights) for r in hold]
    dom = [domain_provenance_score(s.get("url", "")) for s in snap]
    comb = [max(0.0, b - 0.6 * d) for b, d in zip(beh, dom)]

    print(f"\nFuture holdout (n={len(hold)}) — pairwise concordance vs label:")
    print(f"  behavioural (calibrated, silence-driven) : {concordance(beh, hl):.3f}")
    print(f"  domain-provenance alone                  : {concordance([100 - d for d in dom], hl):.3f}")
    print(f"  combined (behavioural + domain penalty)  : {concordance(comb, hl):.3f}")
    print(f"  Spearman behavioural={spearman(beh, hl):+.3f}  combined={spearman(comb, hl):+.3f}")


if __name__ == "__main__":
    main()
