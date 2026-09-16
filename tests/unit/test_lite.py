import httpx
import pytest

from cats.lite import FeedFetchError, FeedNotFoundError, score, score_feed

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


def test_score_feed_applies_domain_penalty_to_source_url(monkeypatch):
    import cats.signals.domain_provenance as dp

    monkeypatch.setattr(dp, "_popularity_table", {"spiegel.ltd": 392949})
    monkeypatch.setattr(dp, "_popularity_load_attempted", True)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=_FIVE_ITEMS)

    with _client_for(handler) as client:
        result = score_feed("https://spiegel.ltd/rss", client=client, load_nlp=False, source_type="news")

    assert "domain_provenance" in result["signals"]
