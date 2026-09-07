"""Domain-provenance signal: structural red-flags in a source's *domain*.

The four behavioural signals (coherence, volatility, silence, gaming) all read a
source's *messages*. They are structurally blind to infrastructure-based
impersonation — Doppelganger-style clones (`spiegel.ltd`, `bild.pics`,
`ansa.ltd`) whose *content* is plausible but whose *domain* is the deception. The
06-Jul-2026 future-snapshot validation showed CATS's discrimination rests almost
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

**Popularity corroboration, not a standalone flag.** A domain absent from the
Tranco top-1M (`data/tranco_top1m.csv`, refreshed offline — see
`domain_popularity_path`) adds a small bonus, but only ON TOP of an existing
structural flag (free-host/suspicious-TLD/typosquat); it never fires alone.
Empirically, 24% of legitimate sources in `data/Fonti_OSINT.csv` (government
subdomains, regional open-data portals, niche outlets — a 25-source sample,
2026-08-28) have no Tranco rank at all, so "unranked" alone is not a reliable
red flag — it would mislabel real institutional sources. Used only as
corroboration, it cannot introduce a new false positive on a domain that was
otherwise clean; it can only sharpen confidence on a domain already flagged.
The same unranked check also gates `AMBIGUOUS_CCTLDS` below.

**Status: wired in as an asymmetric penalty (ENGINE 1.4), not a weighted
signal.** `cats.scoring.engine.apply_domain_penalty` subtracts
`DOMAIN_PENALTY_WEIGHT × value` from the aggregated behavioural score — it is
deliberately NOT in `SIGNAL_NAMES` and NOT GA-calibrated (see `CLAUDE.md`,
`docs/signal_research_2026-07.md`), so a list/coefficient change here needs
`research/validate_domain_penalty.py` re-validation on the future holdout, not
a full GA recalibration cycle. The scoring logic is kept identical to
`research/domain_provenance_spike.py` so the originally-validated numbers still
hold; periodic maintenance updates (TLD/free-host/brand lists, the 0.6
coefficient) are logged in dated `docs/domain_provenance_*` findings docs.

`value` is a 0-100 red-flag score, **higher = more suspicious** — a
higher-is-worse signal, to be inverted at aggregation like volatility/silence/
gaming when it is wired in.
"""

from __future__ import annotations

from urllib.parse import urlparse

import structlog

from cats.signals.types import DomainProvenanceResult

logger = structlog.get_logger()

_popularity_table = None  # type: dict | None
_popularity_load_attempted = False

# Cheap/rare TLDs favoured by clone networks — the exact set Doppelganger used
# (data/disinfo_sources.csv), MINUS four real ccTLDs moved to AMBIGUOUS_CCTLDS
# below (2026-09 maintenance — see docs/domain_provenance_maintenance_2026-09.md).
SUSPICIOUS_TLDS = {
    "pics", "ltd", "cfd", "live", "work", "fun", "today", "asia", "vip",
    "llc", "agency", "cab", "online", "cc", "life", "pro",
    "xyz", "top", "click",
}  # fmt: skip

# ccTLDs that Doppelganger-style campaigns HAVE used (data/disinfo_sources.csv:
# co x4, ws x2, in x1, me x1) but that are also real national top-level domains
# with substantial legitimate use: Colombia, Samoa, India, Montenegro. Flagging
# them unconditionally would mislabel real national outlets — 0.85% of
# data/Fonti_OSINT.csv's 5 275-source catalogue uses "in" alone (thewire.in,
# scroll.in), 0.53% uses "co" (tempo.co, portafolio.co). Checked against the
# real Tranco top-1M (2026-09-07): every one of those legitimate examples IS
# ranked, while the one confirmed clone in the holdout that uses this group
# (empiresports.co) is NOT — so, mirroring the existing popularity-corroboration
# design, these four fire only when the domain is ALSO Tranco-unranked, never on
# TLD alone. Deliberately NOT combined with the separate corroboration bonus
# below (see `already_flagged`) — that would double-count the same "unranked"
# evidence for one domain.
AMBIGUOUS_CCTLDS = {"co", "in", "me", "ws"}

# Free-hosting parents whose subdomains anyone can register.
FREE_HOSTS = ("altervista.org", "blogspot.com", "wordpress.com", "weebly.com", "wixsite.com", "blogspot.it")

# Fixed brand list for typo-squat detection — independent of the labelled set,
# so detection generalises rather than memorising known-bad domains. Sourced
# from the `authentic_domain` column of the Doppelganger threat-intel corpus
# (data/disinfo_sources.csv) — every entry here is a real outlet that corpus
# documents as impersonated. 2026-09 maintenance: added 7 domains present in
# that same corpus but missed by the original extraction (nd-aktuell.de,
# rbc.ua, obozrevatel.com, delfi.lt/.lv/.ee, lsm.lv) — see
# docs/domain_provenance_maintenance_2026-09.md.
MAJOR_BRANDS = [
    "repubblica.it", "corriere.it", "ilfattoquotidiano.it", "ilgiornale.it",
    "panorama.it", "ilsole24ore.it", "ansa.it", "spiegel.de", "bild.de",
    "welt.de", "faz.net", "sueddeutsche.de", "tagesspiegel.de", "t-online.de",
    "theguardian.com", "dailymail.co.uk", "reuters.com", "foxnews.com",
    "libero.it", "sky.it", "20minutes.fr",
    "nd-aktuell.de", "rbc.ua", "obozrevatel.com", "delfi.lt", "delfi.lv",
    "delfi.ee", "lsm.lv",
]  # fmt: skip

# Point contributions (identical to the research spike).
_FREE_HOST_POINTS = 45.0
_SUSPICIOUS_TLD_POINTS = 40.0
_TYPOSQUAT_POINTS = 50.0
_BRAND_ON_BAD_TLD_POINTS = 25.0

# Corroboration only — see module docstring for why this never fires alone.
_LOW_POPULARITY_CORROBORATION_POINTS = 15.0


def _load_popularity_table() -> "dict | None":
    """Lazily load the local Tranco-format popularity table once; cache the result.

    Missing/unreadable file degrades to ``None`` (corroboration never fires),
    the same graceful-degradation pattern as the optional SBERT coherence
    backend — never raises.
    """
    global _popularity_table, _popularity_load_attempted
    if _popularity_table is not None or _popularity_load_attempted:
        return _popularity_table
    _popularity_load_attempted = True
    try:
        from cats.core.config import settings

        table: dict = {}
        with open(settings.domain_popularity_path, encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                rank_str, domain = line.split(",", 1)
                table[domain.strip().lower()] = int(rank_str)
        _popularity_table = table
        logger.info("domain_popularity_loaded", entries=len(table))
    except Exception as exc:
        logger.warning("domain_popularity_unavailable", error=str(exc))
        _popularity_table = None
    return _popularity_table


def _is_unranked(host: str) -> bool:
    """True when ``host`` has no Tranco rank AND the table loaded successfully.

    Returns False (never corroborates) when the table itself is unavailable —
    absence of data must not look like absence of popularity.
    """
    table = _load_popularity_table()
    if table is None:
        return False
    return host not in table


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
    nearest_brand, best = min(((b, _levenshtein(host, b)) for b in MAJOR_BRANDS), key=lambda t: t[1], default=("", 9))
    # A fixed distance<=2 window over-triggers on short brands (an audit of
    # data/Fonti_OSINT.csv's 5 275-source catalogue, 2026-09-07, found "ansa.it"
    # alone false-flagging 6 unrelated short Italian acronym domains at
    # distance 2 -- fnsi.it, asi.it, ania.it, ance.it, anfia.it, dna.it -- with
    # no corresponding real catch lost, since every real distance-2 typosquat on
    # a <=7-char brand in data/disinfo_sources.csv is independently caught by
    # brand_on_bad_tld or ambiguous_cctld_unranked). Requiring distance==1 for
    # short brands removes that false-positive class; longer brands keep the
    # wider distance<=2 window, which the real corpus still needs (e.g.
    # "ilfattoquotidaino.it" vs "ilfattoquotidiano.it", distance 2).
    _max_typosquat_distance = 1 if len(nearest_brand) <= 7 else 2
    typosquat = 1 <= best <= _max_typosquat_distance and host not in MAJOR_BRANDS

    brand_on_bad_tld = False
    if suspicious_tld:
        for b in MAJOR_BRANDS:
            bname = b.rsplit(".", 1)[0]
            if len(bname) >= 4 and bname in host and not host.endswith(b):
                brand_on_bad_tld = True
                break

    # See AMBIGUOUS_CCTLDS: a real national ccTLD fires only when the domain is
    # also Tranco-unranked, never on TLD alone.
    ambiguous_cctld_unranked = tld in AMBIGUOUS_CCTLDS and _is_unranked(host)

    score = 0.0
    if free_host:
        score += _FREE_HOST_POINTS
    if suspicious_tld:
        score += _SUSPICIOUS_TLD_POINTS
    if typosquat:
        score += _TYPOSQUAT_POINTS
    if brand_on_bad_tld:
        score += _BRAND_ON_BAD_TLD_POINTS
    if ambiguous_cctld_unranked:
        score += _SUSPICIOUS_TLD_POINTS

    # Corroboration only: never a standalone trigger (see module docstring —
    # 24% of legitimate catalogue sources are unranked; only ever amplifies an
    # existing structural flag, so a previously-clean domain cannot newly fire).
    # Deliberately excludes ambiguous_cctld_unranked, which already required
    # unranked-ness to fire — double-counting it here would penalise the same
    # evidence twice for one domain.
    already_flagged = free_host or suspicious_tld or typosquat or brand_on_bad_tld
    low_popularity_corroboration = already_flagged and _is_unranked(host)
    if low_popularity_corroboration:
        score += _LOW_POPULARITY_CORROBORATION_POINTS
    score = min(score, 100.0)

    reasons = [
        r
        for r, fired in (
            ("free_host", free_host),
            ("suspicious_tld", suspicious_tld),
            ("typosquat", typosquat),
            ("brand_on_bad_tld", brand_on_bad_tld),
            ("ambiguous_cctld_unranked", ambiguous_cctld_unranked),
            ("low_popularity_corroboration", low_popularity_corroboration),
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
        ambiguous_cctld_unranked=ambiguous_cctld_unranked,
        low_popularity_corroboration=low_popularity_corroboration,
        host=host,
    )
