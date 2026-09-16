"""Zero-infrastructure scoring: the CATS signal pipeline as a library call.

The full CATS deployment (FastAPI + PostgreSQL + Redis) exists for audited,
GDPR-compliant production use. For research, notebooks and quick evaluation
none of that is needed — the four signals and the aggregation are pure
computation. This module exposes them directly:

    from cats.lite import score

    result = score(
        [
            {"timestamp": "2026-01-01T08:00:00Z", "text": "Il governo annuncia un piano."},
            {"timestamp": "2026-01-01T09:00:00Z", "text": "I sindacati commentano il piano."},
            {"timestamp": "2026-01-02T10:00:00Z", "text": "Il parlamento discute il piano."},
        ],
        source_type="news",
    )
    print(result["trust_score"], result["band"])

No database, no Redis, no API keys. The runtime settings that normally come
from the environment (``COHERENCE_BACKEND``, ``CATS_WEIGHTS_FILE``, …) are
still honoured when set; the infrastructure-only settings (database, Redis,
audit encryption) are defaulted to inert placeholders because nothing in this
path touches them.

Same caveats as the API: scores are ordinal (WP 4.3), the default NLP is
Italian-optimised (WP 4.1) and, without ``init_nlp``/the spaCy model,
NER coherence degrades to a neutral zero-confidence value.

For a source you only have a URL for, ``score_feed(url)`` fetches its
RSS/Atom feed (with autodiscovery) and calls ``score`` for you.
"""

from __future__ import annotations

import os
from html.parser import HTMLParser
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

# The signal/scoring modules read ``cats.core.config.settings`` at import time,
# which fails fast when the deployment-only variables are missing — correct for
# the API, pointless for pure scoring. Default them (only if unset) to inert
# placeholders *before* those imports. Real values from the environment always
# win because setdefault never overrides.
_LITE_ENV_DEFAULTS = {
    "CATS_API_KEY": "lite-mode-unused",
    "DATABASE_URL": "postgresql+asyncpg://lite:lite@localhost:1/unused",
    "REDIS_URL": "redis://localhost:1/0",
    "AUDIT_ENCRYPTION_KEY": "bGl0ZS1tb2RlLXBsYWNlaG9sZGVyLW5vdC1hLWtleT0=",
}
for _k, _v in _LITE_ENV_DEFAULTS.items():
    os.environ.setdefault(_k, _v)

import httpx  # noqa: E402
import structlog  # noqa: E402

from cats.calibration.collect_rss import DEFAULT_USER_AGENT, fetch_feed, parse_feed  # noqa: E402
from cats.pipeline.language import detect_language  # noqa: E402
from cats.pipeline.normalizer import normalize_messages  # noqa: E402
from cats.scoring.engine import (  # noqa: E402
    aggregate_score,
    apply_domain_penalty,
    determine_band,
    evidence_summary,
    requires_human_review,
)
from cats.scoring.explainer import generate_explanation  # noqa: E402
from cats.scoring.weights import get_dynamic_weights  # noqa: E402
from cats.signals import coherence  # noqa: E402
from cats.signals.coherence import compute_coherence  # noqa: E402
from cats.signals.domain_provenance import compute_domain_provenance  # noqa: E402
from cats.signals.gaming import compute_gaming  # noqa: E402
from cats.signals.silence import compute_silence  # noqa: E402
from cats.signals.types import SignalResult  # noqa: E402
from cats.signals.volatility import compute_volatility  # noqa: E402

logger = structlog.get_logger()

_nlp_attempted = False

_WELL_KNOWN_FEED_PATHS = ("/feed", "/rss", "/feed.xml", "/rss.xml", "/atom.xml", "/index.xml")


class FeedNotFoundError(ValueError):
    """Raised by :func:`score_feed` when no RSS/Atom feed could be discovered for a URL."""


class FeedFetchError(ValueError):
    """Raised by :func:`score_feed` when the source (and every candidate feed path) was unreachable."""


class _FeedLinkParser(HTMLParser):
    """Collects ``<link rel="alternate" type="application/{rss,atom}+xml" href=...>`` targets."""

    def __init__(self) -> None:
        super().__init__()
        self.feed_links: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag.lower() != "link":
            return
        attrs_d = {k.lower(): (v or "") for k, v in attrs}
        rel = attrs_d.get("rel", "").lower().split()
        type_ = attrs_d.get("type", "").lower()
        href = attrs_d.get("href", "")
        if "alternate" in rel and type_ in ("application/rss+xml", "application/atom+xml") and href:
            self.feed_links.append(href)


def _discover_feed_links(html_text: str) -> List[str]:
    parser = _FeedLinkParser()
    try:
        parser.feed(html_text)
    except Exception:  # malformed HTML must degrade, not crash discovery
        return []
    return parser.feed_links


def _reachable(exc: ValueError) -> bool:
    """Whether ``exc`` (from :func:`fetch_feed`) still means the host answered.

    An HTTP status error (404, 500, …) or an oversize-body rejection means we
    got a real response; only a transport-level failure (DNS, connect,
    timeout) means the host itself was unreachable.
    """
    cause = exc.__cause__
    if cause is None or isinstance(cause, httpx.HTTPStatusError):
        return True
    return not isinstance(cause, httpx.HTTPError)


def _resolve_feed(url: str, client: httpx.Client) -> Tuple[str, List[dict], str]:
    """Find a scorable feed for ``url``: direct fetch, then HTML autodiscovery, then well-known paths."""
    saw_reachable = False
    html_body: Optional[str] = None

    def _attempt(candidate: str, *, keep_html: bool) -> Optional[List[dict]]:
        nonlocal saw_reachable, html_body
        try:
            body = fetch_feed(candidate, client)
        except ValueError as exc:
            if _reachable(exc):
                saw_reachable = True
            return None
        saw_reachable = True
        try:
            messages = parse_feed(body)
        except ValueError:
            if keep_html:
                html_body = body
            return None
        return messages or None

    messages = _attempt(url, keep_html=True)
    if messages:
        return url, messages, "direct"

    if html_body:
        for link in _discover_feed_links(html_body):
            candidate = urljoin(url, link)
            messages = _attempt(candidate, keep_html=False)
            if messages:
                return candidate, messages, "html_link"

    parsed = urlparse(url)
    root = f"{parsed.scheme}://{parsed.netloc}"
    for path in _WELL_KNOWN_FEED_PATHS:
        candidate = root + path
        messages = _attempt(candidate, keep_html=False)
        if messages:
            return candidate, messages, "well_known_path"

    if not saw_reachable:
        raise FeedFetchError(f"could not reach {url} or any candidate feed path")
    raise FeedNotFoundError(f"no RSS/Atom feed found for {url}")


def score_feed(
    url: str,
    source_type: str = "default",
    *,
    max_messages: int = 200,
    timeout: float = 20.0,
    client: Optional[httpx.Client] = None,
    **score_kwargs,
) -> Dict:
    """Score a source straight from its RSS/Atom feed: fetch, discover, then :func:`score`.

    ``url`` may omit its scheme (``https://`` is assumed). If it is not itself
    a feed, autodiscovery tries the page's ``<link rel="alternate">`` tags,
    then well-known paths (``/feed``, ``/rss``, …). ``client`` is an
    injectable ``httpx.Client`` (e.g. with a ``MockTransport``) for tests;
    when omitted, a client is created and closed internally.

    Raises :class:`FeedNotFoundError` if the host answers but no feed is
    found, or :class:`FeedFetchError` if the host (and every candidate path)
    is unreachable. :func:`score` still raises ``ValueError`` if the feed
    yields zero usable messages after normalisation.

    The result adds a ``source`` block (``url``, ``feed_url``, ``messages``,
    ``first_timestamp``, ``last_timestamp``, ``discovery``) to ``score()``'s
    normal output. The domain-provenance penalty is applied against the
    original ``url``, not the feed URL, so it scores the source rather than
    its feed host.
    """
    if "://" not in url:
        url = f"https://{url}"

    owns_client = client is None
    active_client = client or httpx.Client(
        timeout=timeout, follow_redirects=True, headers={"User-Agent": DEFAULT_USER_AGENT}
    )
    try:
        feed_url, messages, discovery = _resolve_feed(url, active_client)
    finally:
        if owns_client:
            active_client.close()

    messages.sort(key=lambda m: m["timestamp"])
    messages = messages[-max_messages:]

    result = score(messages, source_type=source_type, url=url, **score_kwargs)
    result["source"] = {
        "url": url,
        "feed_url": feed_url,
        "messages": len(messages),
        "first_timestamp": messages[0]["timestamp"],
        "last_timestamp": messages[-1]["timestamp"],
        "discovery": discovery,
    }
    logger.info(
        "score_feed_completed",
        url=url,
        feed_url=feed_url,
        discovery=discovery,
        messages=len(messages),
        trust_score=result["trust_score"],
    )
    return result


def init_nlp(model_name: Optional[str] = None) -> bool:
    """Load the spaCy NER model once (idempotent); returns True on success.

    Without it the NER coherence backend degrades to a neutral,
    zero-confidence value — exactly as the API does when the model is missing.
    """
    global _nlp_attempted
    if coherence.nlp is not None:
        return True
    if _nlp_attempted:
        return False
    _nlp_attempted = True
    try:
        from cats.core.config import settings

        coherence.init_nlp(model_name or settings.spacy_model)
        return True
    except Exception:  # model not downloaded — degrade, don't crash
        return False


def score(
    messages: List[dict],
    source_type: str = "default",
    weights: Optional[Dict[str, float]] = None,
    explain: bool = True,
    load_nlp: bool = True,
    url: Optional[str] = None,
) -> Dict:
    """Score one source's message history with the CATS signal pipeline.

    ``messages``: list of ``{"timestamp": ISO-8601, "text": str}`` dicts.
    ``weights``: optional signal-name -> weight override; defaults to the
    static/calibrated table for ``source_type`` (``CATS_WEIGHTS_FILE`` honoured).
    ``url``: optional source URL/domain. When given, the domain-provenance
    penalty is applied (impersonation/clone red-flags only lower the score).

    Returns ``{trust_score, band, requires_human_review, signals, language,
    evidence, explanation}``. ``language`` flags non-Italian input (the NLP
    stack is Italian-optimised — risk R3); ``evidence`` reports the message
    count vs ``CATS_MIN_EVIDENCE_MESSAGES`` (risk R5) — an insufficient
    history forces ``requires_human_review`` but never changes the score.
    """
    if load_nlp:
        init_nlp()
    msgs = normalize_messages(messages)
    if not msgs:
        raise ValueError("no valid messages after normalisation (need timestamp + text)")

    behavioural: List[SignalResult] = [
        compute_coherence(msgs),
        compute_volatility(msgs),
        compute_silence(msgs, source_type),
        compute_gaming(msgs),
    ]
    w = weights or get_dynamic_weights({"source_type": source_type})
    value = aggregate_score(behavioural, w)

    domain = compute_domain_provenance(url or "")
    value = apply_domain_penalty(value, domain)
    signals: List[SignalResult] = behavioural + ([domain] if domain.confidence > 0 else [])
    band = determine_band(value)

    from cats.core.config import settings

    language = detect_language(msgs)
    evidence = evidence_summary(behavioural, len(msgs), settings.min_evidence_messages)
    result = {
        "trust_score": round(value, 2),
        "band": band,
        "requires_human_review": requires_human_review(
            value, band, signals, sufficient_evidence=bool(evidence["sufficient"])
        ),
        "signals": {s.name: round(s.value, 2) for s in signals},
        "language": language.as_dict(),
        "evidence": evidence,
    }
    if explain:
        explanation = generate_explanation(value, band, signals, w)
        if language.detected == "other":
            explanation["language_warning"] = (
                "Input does not look Italian: the default NLP stack is "
                "Italian-optimised, so signal quality is degraded (WP 4.1 / risk R3)."
            )
        result["explanation"] = explanation
    return result
