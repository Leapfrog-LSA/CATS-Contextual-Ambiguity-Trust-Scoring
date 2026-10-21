from datetime import datetime, timedelta, timezone
from email.utils import format_datetime

import httpx
import pytest

from cats.lite import FeedFetchError, FeedNotFoundError, score, score_feed
from cats.signals import coherence
from cats.signals.types import CoherenceResult

_MESSAGES = [
    {"timestamp": "2026-01-01T08:00:00Z", "text": "Il governo annuncia un piano economico."},
    {"timestamp": "2026-01-01T12:00:00Z", "text": "I sindacati commentano il piano del governo."},
    {"timestamp": "2026-01-02T09:00:00Z", "text": "Il parlamento discute la legge di bilancio."},
]


def test_score_returns_full_result():
    result = score(_MESSAGES, source_type="news", load_nlp=False)
    assert 0.0 <= result["trust_score"] <= 100.0
    assert result["band"] in {"very_low", "low", "medium", "medium_high", "high"}
    assert isinstance(result["requires_human_review"], bool)
    assert set(result["signals"]) == {"coherence", "volatility", "silence", "gaming"}
    assert result["explanation"]["trust_score"] == result["trust_score"]
    assert "disclaimer" in result["explanation"]


def test_score_without_explanation():
    result = score(_MESSAGES, source_type="social", load_nlp=False, explain=False)
    assert "explanation" not in result


def test_score_with_weight_override():
    weights = {"coherence": 0.7, "volatility": 0.1, "silence": 0.1, "gaming": 0.1}
    result = score(_MESSAGES, weights=weights, load_nlp=False)
    assert result["explanation"]["signals"][0]["weight"] in {0.7, 0.1}


def test_score_rejects_empty_messages():
    with pytest.raises(ValueError):
        score([], load_nlp=False)
    with pytest.raises(ValueError):
        score([{"timestamp": "", "text": ""}], load_nlp=False)


def test_clone_url_penalises_and_reports_domain(monkeypatch):
    # Popularity table mocked as "ranked" so this stays deterministic whether
    # or not the real Tranco table (not committed -- see .gitignore) happens
    # to be present in this environment -- 2026-09-07 maintenance: an earlier
    # version of this test relied on ambient file absence and broke the
    # moment `make tranco-download` was run locally, the same environment-
    # dependent-test class as the SBERT/BERT backend-availability tests.
    import cats.signals.domain_provenance as dp

    monkeypatch.setattr(dp, "_popularity_table", {"spiegel.ltd": 392949})
    monkeypatch.setattr(dp, "_popularity_load_attempted", True)
    base = score(_MESSAGES, source_type="news", load_nlp=False, explain=False)
    clone = score(_MESSAGES, source_type="news", load_nlp=False, url="https://spiegel.ltd")
    assert clone["trust_score"] < base["trust_score"]
    assert "domain_provenance" in clone["signals"]
    assert "domain_penalty" in clone["explanation"]
    # 40.0 suspicious_tld + 25.0 brand_on_bad_tld; no corroboration bonus since
    # the domain is (mocked) ranked -- see
    # tests/unit/test_domain_provenance.py::TestPopularityCorroboration for
    # the unranked/corroboration path itself.
    assert clone["explanation"]["domain_penalty"]["domain_red_flag_score"] == 65.0


def test_clean_url_does_not_change_score():
    base = score(_MESSAGES, source_type="news", load_nlp=False, explain=False)
    clean = score(_MESSAGES, source_type="news", load_nlp=False, explain=False, url="https://www.corriere.it")
    assert clean["trust_score"] == base["trust_score"]


def test_no_url_keeps_four_signals():
    result = score(_MESSAGES, source_type="news", load_nlp=False, explain=False)
    assert set(result["signals"]) == {"coherence", "volatility", "silence", "gaming"}


# ── score_feed ────────────────────────────────────────────────────────────


def _rss(items):
    """Build a minimal RSS 2.0 document from ``[(title, rfc822_pubdate), ...]``."""
    entries = "\n".join(
        f"  <item>\n    <title>{title}</title>\n    <pubDate>{pub}</pubDate>\n  </item>" for title, pub in items
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">'
        f"<channel>\n  <title>Test feed</title>\n{entries}\n</channel></rss>"
    )


_FIVE_ITEMS = _rss(
    [
        ("Prima notizia", "Mon, 01 Jun 2026 08:00:00 GMT"),
        ("Seconda notizia", "Tue, 02 Jun 2026 08:00:00 GMT"),
        ("Terza notizia", "Wed, 03 Jun 2026 08:00:00 GMT"),
        ("Quarta notizia", "Thu, 04 Jun 2026 08:00:00 GMT"),
        ("Quinta notizia", "Fri, 05 Jun 2026 08:00:00 GMT"),
    ]
)

_PLAIN_HTML = "<html><head><title>Example</title></head><body><p>Not a feed.</p></body></html>"

_HTML_WITH_LINK = (
    "<html><head><title>Example</title>"
    '<link rel="alternate" type="application/rss+xml" title="RSS" href="/blog/feed.xml"/>'
    "</head><body><p>Blog homepage.</p></body></html>"
)


def _client_for(handler) -> httpx.Client:
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_score_feed_direct_rss():
    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "https://example.com/rss"
        return httpx.Response(200, text=_FIVE_ITEMS)

    with _client_for(handler) as client:
        result = score_feed("https://example.com/rss", client=client, load_nlp=False)

    assert result["source"]["discovery"] == "direct"
    assert result["source"]["feed_url"] == "https://example.com/rss"
    assert result["source"]["messages"] == 5
    assert 0.0 <= result["trust_score"] <= 100.0
    assert set(result["signals"]) >= {"coherence", "volatility", "silence", "gaming"}


def test_score_feed_autodiscovery_html_link():
    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url == "https://example.com/":
            return httpx.Response(200, text=_HTML_WITH_LINK)
        if url == "https://example.com/blog/feed.xml":
            return httpx.Response(200, text=_FIVE_ITEMS)
        return httpx.Response(404, text="not found")

    with _client_for(handler) as client:
        result = score_feed("https://example.com/", client=client, load_nlp=False)

    assert result["source"]["discovery"] == "html_link"
    assert result["source"]["feed_url"] == "https://example.com/blog/feed.xml"
    assert result["source"]["messages"] == 5


def test_score_feed_well_known_path():
    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url == "https://example.com/":
            return httpx.Response(200, text=_PLAIN_HTML)
        if url == "https://example.com/feed":
            return httpx.Response(200, text=_FIVE_ITEMS)
        return httpx.Response(404, text="not found")

    with _client_for(handler) as client:
        result = score_feed("example.com", client=client, load_nlp=False)

    assert result["source"]["discovery"] == "well_known_path"
    assert result["source"]["feed_url"] == "https://example.com/feed"
    assert result["source"]["url"] == "https://example.com"


def test_score_feed_not_found():
    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url == "https://example.com/":
            return httpx.Response(200, text=_PLAIN_HTML)
        return httpx.Response(404, text="not found")

    with _client_for(handler) as client:
        with pytest.raises(FeedNotFoundError):
            score_feed("https://example.com/", client=client, load_nlp=False)


def test_score_feed_unreachable_host_raises_fetch_error():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused", request=request)

    with _client_for(handler) as client:
        with pytest.raises(FeedFetchError):
            score_feed("https://example.com/", client=client, load_nlp=False)


def test_score_feed_max_messages_keeps_latest():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=_FIVE_ITEMS)

    with _client_for(handler) as client:
        result = score_feed("https://example.com/rss", client=client, load_nlp=False, max_messages=2)

    assert result["source"]["messages"] == 2
    assert result["source"]["first_timestamp"] < result["source"]["last_timestamp"]
    assert result["source"]["last_timestamp"].startswith("2026-06-05")


def _recent_rss(days_ago: int = 0):
    """Five items ending ``days_ago`` days before now, so freshness does not depend on the test date."""
    newest = datetime.now(timezone.utc) - timedelta(days=days_ago)
    return _rss(
        [(f"Notizia {i}", format_datetime(newest - timedelta(hours=6 * (4 - i)), usegmt=True)) for i in range(5)]
    )


_STALE_ITEMS = _rss(
    [
        ("Vecchia notizia uno", "Tue, 26 Mar 2024 08:00:00 GMT"),
        ("Vecchia notizia due", "Mon, 06 May 2024 08:00:00 GMT"),
        ("Vecchia notizia tre", "Mon, 13 May 2024 06:07:52 GMT"),
    ]
)

_FEED_INDEX_PAGE = (
    "<html><head><title>RSS</title></head><body>"
    '<a href="/news/2026/an-article.html">Un articolo</a>'
    '<a href="//feeds.example.net/home.xml">Home - tutte le notizie</a>'
    '<a href="/rss/section/Cronache.xml">Cronache</a>'
    "</body></html>"
)


def test_discover_index_links_keeps_feed_looking_anchors_in_order():
    from cats.lite import _discover_index_links

    html = _FEED_INDEX_PAGE + '<a href="/feed/">Feed</a><a href="/rss/section/Cronache.xml">dup</a>'
    assert _discover_index_links(html) == ["//feeds.example.net/home.xml", "/rss/section/Cronache.xml", "/feed/"]


def test_score_feed_feed_index_page():
    # corriere.it: no <link rel="alternate">, no feed at the usual paths, but
    # /rss/ is an HTML page listing the section feeds, main feed first.
    fresh = _recent_rss()

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url == "https://example.com/":
            return httpx.Response(200, text=_PLAIN_HTML)
        if url == "https://example.com/rss/":
            return httpx.Response(200, text=_FEED_INDEX_PAGE)
        if url == "https://feeds.example.net/home.xml":
            return httpx.Response(200, text=fresh)
        return httpx.Response(404, text="not found")

    with _client_for(handler) as client:
        result = score_feed("https://example.com/", client=client, load_nlp=False)

    assert result["source"]["discovery"] == "feed_index"
    assert result["source"]["feed_url"] == "https://feeds.example.net/home.xml"
    assert result["source"]["stale"] is False


def test_score_feed_skips_stale_advertised_feed_for_live_one():
    html = (
        '<html><head><link rel="alternate" type="application/rss+xml" href="/old.xml"/></head>' "<body></body></html>"
    )
    fresh = _recent_rss(days_ago=1)

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url == "https://example.com/":
            return httpx.Response(200, text=html)
        if url == "https://example.com/old.xml":
            return httpx.Response(200, text=_STALE_ITEMS)
        if url == "https://example.com/feed":
            return httpx.Response(200, text=fresh)
        return httpx.Response(404, text="not found")

    with _client_for(handler) as client:
        result = score_feed("https://example.com/", client=client, load_nlp=False)

    assert result["source"]["feed_url"] == "https://example.com/feed"
    assert result["source"]["stale"] is False


def test_score_feed_falls_back_to_stale_feed_and_flags_it():
    from cats.lite import review_reason

    def handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if url == "https://example.com/":
            return httpx.Response(200, text=_PLAIN_HTML)
        if url == "https://example.com/rss.xml":
            return httpx.Response(200, text=_STALE_ITEMS)
        return httpx.Response(404, text="not found")

    with _client_for(handler) as client:
        result = score_feed("https://example.com/", client=client, load_nlp=False, stale_after_days=30)

    assert result["source"]["feed_url"] == "https://example.com/rss.xml"
    assert result["source"]["discovery"] == "well_known_path"
    assert result["source"]["stale"] is True
    assert result["requires_human_review"] is True
    assert review_reason(result) == "stale feed (newest item 2024-05-13)"


def test_score_feed_direct_stale_feed_is_kept_and_flagged():
    requested = []

    def handler(request: httpx.Request) -> httpx.Response:
        requested.append(str(request.url))
        return httpx.Response(200, text=_STALE_ITEMS)

    with _client_for(handler) as client:
        result = score_feed("https://example.com/rss/homepage.xml", client=client, load_nlp=False)

    assert requested == ["https://example.com/rss/homepage.xml"]
    assert result["source"]["discovery"] == "direct"
    assert result["source"]["stale"] is True


def test_score_feed_stale_check_can_be_disabled():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=_STALE_ITEMS)

    with _client_for(handler) as client:
        result = score_feed("https://example.com/rss", client=client, load_nlp=False, stale_after_days=0)

    assert result["source"]["stale"] is False


def test_score_feed_applies_domain_penalty_to_source_url(monkeypatch):
    import cats.signals.domain_provenance as dp

    monkeypatch.setattr(dp, "_popularity_table", {"spiegel.ltd": 392949})
    monkeypatch.setattr(dp, "_popularity_load_attempted", True)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=_FIVE_ITEMS)

    with _client_for(handler) as client:
        result = score_feed("https://spiegel.ltd/rss", client=client, load_nlp=False, source_type="news")

    assert "domain_provenance" in result["signals"]


def test_missing_nlp_model_is_reported_and_forces_review(monkeypatch):
    monkeypatch.setattr(coherence, "nlp", None)
    result = score(_MESSAGES, source_type="news", load_nlp=False)
    assert result["degraded_signals"] == ["coherence"]
    assert result["signals"]["coherence"] == 50.0
    assert result["requires_human_review"] is True
    assert "it_core_news_lg" in result["explanation"]["degraded_warning"]


def test_measured_coherence_is_not_degraded(monkeypatch):
    measured = CoherenceResult(name="coherence", value=40.0, confidence=1.0, metadata={"backend": "ner"})
    monkeypatch.setattr("cats.lite.compute_coherence", lambda msgs: measured)
    result = score(_MESSAGES, source_type="news", load_nlp=False)
    assert result["degraded_signals"] == []
    assert "degraded_warning" not in result["explanation"]


def test_compare_feeds_ranks_and_collects_errors(monkeypatch):
    from cats.lite import COMPARE_NOTE, FeedNotFoundError, compare_feeds

    def fake_score_feed(url, **kwargs):
        if url == "https://gone.example":
            raise FeedNotFoundError("no RSS/Atom feed found for https://gone.example")
        value = {"https://a.example": 40.0, "https://b.example": 70.0}[url]
        return {
            "trust_score": value,
            "band": "medium",
            "requires_human_review": False,
            "signals": {"coherence": 10.0, "domain_provenance": 0.0},
            "degraded_signals": [],
            "evidence": {"messages": 5, "min_messages": 3, "sufficient": True},
            "explanation": {"primary_driver": "silence"},
            "source": {"messages": 5},
        }

    monkeypatch.setattr("cats.lite.score_feed", fake_score_feed)
    out = compare_feeds(["https://a.example", "https://gone.example", "https://b.example", "https://a.example"])

    assert [(r["rank"], r["url"]) for r in out["ranked"]] == [(1, "https://b.example"), (2, "https://a.example")]
    assert out["ranked"][0]["review_reason"] is None
    assert out["errors"] == [
        {"url": "https://gone.example", "error": "no RSS/Atom feed found for https://gone.example"}
    ]
    assert out["note"] == COMPARE_NOTE
