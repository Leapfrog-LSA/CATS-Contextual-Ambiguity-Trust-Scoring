"""Domain-provenance signal: structural red-flags in a source's *domain*.

The four behavioural signals (coherence, volatility, silence, gaming) all read a
source's *messages*. They are structurally blind to infrastructure-based
impersonation — Doppelganger-style clones (`spiegel.ltd`, `bild.pics`,
`ansa.ltd`) whose *content* is plausible but whose *domain* is the deception. The
28-Jul-2026 future-snapshot validation showed CATS's discrimination rests almost
entirely on `silence`, so a clone that simply publishes on a regular cadence
defeats the only informative behavioural signal. A signal computed from the
domain is orthogonal to the behavioural four and closes exactly that gap
(`docs/signal_research_2026-07.md`).

**Leakage discipline.** The score is built from GENERAL domain structure only
(rare/cheap TLDs, free-hosting subdomains, edit distance to a fixed major-brand
list) — never from membership in `data/disinfo_sources.csv`. It therefore fires
on unseen domains with the same structure, not just the labelled ones.

**High precision, low recall.** It catches infrastructure clones with near-zero
false positives, but misses fake-news content on ordinary domains — so a *low*
score is weak evidence of reliability. That asymmetry is for the aggregation /
calibration layer to weigh.

**Status: standalone, not wired into scoring.** Adding a fifth signal changes
band semantics and requires recalibration + future-holdout re-validation (see
`CLAUDE.md`, `docs/signal_research_2026-07.md`). This module is the reusable,
tested implementation that a future promotion builds on; the scoring logic is
kept identical to `research/domain_provenance_spike.py` so the validated numbers
still hold.

`value` is a 0-100 red-flag score, **higher = more suspicious** — a
higher-is-worse signal, to be inverted at aggregation like volatility/silence/
gaming when it is wired in.
"""

from __future__ import annotations

from urllib.parse import urlparse

import structlog

from cats.signals.types import DomainProvenanceResult

logger = structlog.get_logger()

# Cheap/rare TLDs favoured by clone networks — the exact set Doppelganger used.
SUSPICIOUS_TLDS = {
    "pics", "ltd", "cfd", "live", "work", "fun", "today", "asia", "vip", "ws",
    "llc", "agency", "cab", "me", "online", "cc", "co", "life", "pro", "in",
    "xyz", "top", "click",
}  # fmt: skip

# Free-hosting parents whose subdomains anyone can register.
FREE_HOSTS = ("altervista.org", "blogspot.com", "wordpress.com", "weebly.com", "wixsite.com", "blogspot.it")

# Fixed brand list for typo-squat detection — independent of the labelled set,
# so detection generalises rather than memorising known-bad domains.
MAJOR_BRANDS = [
    "repubblica.it", "corriere.it", "ilfattoquotidiano.it", "ilgiornale.it",
    "panorama.it", "ilsole24ore.it", "ansa.it", "spiegel.de", "bild.de",
    "welt.de", "faz.net", "sueddeutsche.de", "tagesspiegel.de", "t-online.de",
    "theguardian.com", "dailymail.co.uk", "reuters.com", "foxnews.com",
    "libero.it", "sky.it", "20minutes.fr",
]  # fmt: skip

# Point contributions (identical to the research spike).
_FREE_HOST_POINTS = 45.0
_SUSPICIOUS_TLD_POINTS = 40.0
_TYPOSQUAT_POINTS = 50.0
_BRAND_ON_BAD_TLD_POINTS = 25.0


def _levenshtein(a: str, b: str) -> int:
    """Edit distance, short-circuited when lengths differ by more than 3."""
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


def extract_host(url: str) -> str:
    """Lower-cased registrable host from a URL or bare domain.

    Tolerates a missing scheme (``bild.pics`` as well as ``https://bild.pics``),
    strips a leading ``www.`` and any port. Returns ``""`` when no host is found.
    """
    u = (url or "").strip()
    if not u:
        return ""
    parsed = urlparse(u if "//" in u else "//" + u)
    host = (parsed.netloc or "").lower()
    host = host.split("@")[-1].split(":")[0]  # drop userinfo and port
    if host.startswith("www."):
        host = host[4:]
    return host


def compute_domain_provenance(url: str) -> DomainProvenanceResult:
    """Score a source domain's impersonation/clone red-flags (0-100, higher worse).

    ``confidence`` is 1.0 when a host can be parsed (the check is deterministic)
    and 0.0 when the URL yields no host — mirroring how the other signals report
    a neutral, zero-confidence result when they cannot be computed.
    """
    host = extract_host(url)
    if not host:
        return DomainProvenanceResult(
            name="domain_provenance",
            value=0.0,
            confidence=0.0,
            metadata={"reason": "no_domain"},
        )

    tld = host.rsplit(".", 1)[-1]
    free_host = any(host == h or host.endswith("." + h) for h in FREE_HOSTS)
    suspicious_tld = tld in SUSPICIOUS_TLDS
    best = min((_levenshtein(host, b) for b in MAJOR_BRANDS), default=9)
    typosquat = 1 <= best <= 2 and host not in MAJOR_BRANDS

    brand_on_bad_tld = False
    if suspicious_tld:
        for b in MAJOR_BRANDS:
            bname = b.rsplit(".", 1)[0]
            if len(bname) >= 4 and bname in host and not host.endswith(b):
                brand_on_bad_tld = True
                break

    score = 0.0
    if free_host:
        score += _FREE_HOST_POINTS
    if suspicious_tld:
        score += _SUSPICIOUS_TLD_POINTS
    if typosquat:
        score += _TYPOSQUAT_POINTS
    if brand_on_bad_tld:
        score += _BRAND_ON_BAD_TLD_POINTS
    score = min(score, 100.0)

    reasons = [
        r
        for r, fired in (
            ("free_host", free_host),
            ("suspicious_tld", suspicious_tld),
            ("typosquat", typosquat),
            ("brand_on_bad_tld", brand_on_bad_tld),
        )
        if fired
    ]
    return DomainProvenanceResult(
        name="domain_provenance",
        value=score,
        confidence=1.0,
        metadata={"host": host, "tld": tld, "reasons": reasons},
        suspicious_tld=suspicious_tld,
        free_host=free_host,
        typosquat=typosquat,
        brand_on_bad_tld=brand_on_bad_tld,
        host=host,
    )
