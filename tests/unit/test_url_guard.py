import httpx
import pytest

from cats.calibration.collect_rss import MAX_REDIRECTS, fetch_feed
from cats.core import url_guard
from cats.core.url_guard import UnsafeURLError, check_url
from cats.lite import FeedNotFoundError, score_feed

_RSS = (
    "<rss><channel>"
    "<item><title>Uno</title><pubDate>Mon, 01 Sep 2026 08:00:00 GMT</pubDate></item>"
    "<item><title>Due</title><pubDate>Mon, 01 Sep 2026 12:00:00 GMT</pubDate></item>"
    "<item><title>Tre</title><pubDate>Tue, 02 Sep 2026 09:00:00 GMT</pubDate></item>"
    "</channel></rss>"
)

# Host name -> addresses it resolves to in these tests.
_DNS = {
    "news.example": ["93.184.216.34"],
    "internal.example": ["10.0.0.5"],
    "mixed.example": ["93.184.216.34", "127.0.0.1"],
}


@pytest.fixture
def fake_dns(monkeypatch):
    def resolve(host):
        if host in _DNS:
            return _DNS[host]
        # IP literals resolve to themselves, as getaddrinfo does
        return [host.strip("[]")]

    monkeypatch.setattr(url_guard, "_resolve_host", resolve)


@pytest.mark.parametrize(
    "url",
    [
        "http://127.0.0.1/feed",
        "http://localhost.example@10.1.2.3/",
        "http://169.254.169.254/latest/meta-data/",  # cloud metadata
        "http://192.168.1.10/rss",
        "http://100.64.0.1/rss",  # carrier-grade NAT
        "http://[::1]/rss",
        "http://[::ffff:127.0.0.1]/rss",  # IPv4-mapped loopback
        "http://0.0.0.0/",
        "https://internal.example/feed",
        "https://mixed.example/feed",  # one bad address is enough
    ],
)
def test_non_public_targets_are_refused(fake_dns, url):
    with pytest.raises(UnsafeURLError):
        check_url(url)


@pytest.mark.parametrize("url", ["file:///etc/passwd", "ftp://news.example/feed", "gopher://news.example/"])
def test_non_http_schemes_are_refused(fake_dns, url):
    with pytest.raises(UnsafeURLError):
        check_url(url)


def test_public_host_is_allowed(fake_dns):
    check_url("https://news.example/feed")


def test_allow_private_skips_only_the_address_check(fake_dns):
    check_url("http://10.0.0.5/feed", allow_private=True)
    with pytest.raises(UnsafeURLError):
        check_url("file:///etc/passwd", allow_private=True)


def test_unresolvable_host_is_left_to_the_fetch(monkeypatch):
    def fail(host):
        raise url_guard.socket.gaierror("no such host")

    monkeypatch.setattr(url_guard, "_resolve_host", fail)
    check_url("https://does-not-exist.example/feed")


def test_redirect_to_internal_address_is_refused_before_it_is_requested(fake_dns):
    requested = []

    def handler(request):
        requested.append(str(request.url))
        if request.url.host == "news.example":
            return httpx.Response(302, headers={"location": "http://169.254.169.254/latest/meta-data/"})
        return httpx.Response(200, text=_RSS)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(UnsafeURLError):
            fetch_feed("https://news.example/feed", client)
    assert requested == ["https://news.example/feed"]


def test_public_redirects_are_followed(fake_dns):
    def handler(request):
        if request.url.path == "/old":
            return httpx.Response(301, headers={"location": "/feed"})
        return httpx.Response(200, text=_RSS)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        assert "<rss>" in fetch_feed("https://news.example/old", client)


def test_redirect_loop_stops(fake_dns):
    calls = []

    def handler(request):
        calls.append(1)
        return httpx.Response(302, headers={"location": "/again"})

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(ValueError, match="redirects"):
            fetch_feed("https://news.example/feed", client)
    assert len(calls) == MAX_REDIRECTS + 1


def test_oversize_body_stops_while_streaming(fake_dns):
    served = []

    def endless():
        for _ in range(1000):
            served.append(1)
            yield b"x" * 1024

    def handler(request):
        return httpx.Response(200, content=endless())

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(ValueError, match="exceeds"):
            fetch_feed("https://news.example/feed", client, max_bytes=10 * 1024)
    assert len(served) < 1000  # stopped early, not after reading everything


def test_score_feed_refuses_internal_url(fake_dns):
    with httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(200, text=_RSS))) as client:
        with pytest.raises(UnsafeURLError):
            score_feed("http://127.0.0.1:8000/metrics", client=client, load_nlp=False)


def test_score_feed_skips_an_internal_feed_link_on_a_public_page(fake_dns):
    page = '<html><head><link rel="alternate" type="application/rss+xml" href="http://10.0.0.5/rss"></head></html>'
    requested = []

    def handler(request):
        requested.append(request.url.host)
        if request.url.path == "/":
            return httpx.Response(200, text=page)
        return httpx.Response(404)

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(FeedNotFoundError):
            score_feed("https://news.example/", client=client, load_nlp=False)
    assert "10.0.0.5" not in requested


def test_score_feed_allow_private_reaches_a_local_feed(fake_dns):
    with httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(200, text=_RSS))) as client:
        result = score_feed("http://10.0.0.5/rss", client=client, load_nlp=False, allow_private=True)
    assert result["source"]["messages"] == 3


class _Proc:
    def __init__(self, stdout=b"", stderr=b"200 ", returncode=0):
        self.stdout, self.stderr, self.returncode = stdout, stderr, returncode


def _waf_client():
    # httpx gets a 403 everywhere, which is what triggers the curl fallback
    return httpx.Client(transport=httpx.MockTransport(lambda r: httpx.Response(403)))


def test_curl_fallback_follows_public_redirects_hop_by_hop(fake_dns, monkeypatch):
    calls = []

    def run(cmd, **kwargs):
        calls.append(cmd)
        if cmd[-1] == "https://news.example/rss.xml":
            return _Proc(stdout=b"<html>moved</html>", stderr=b"301 https://news.example/feed.xml")
        return _Proc(stdout=_RSS.encode(), stderr=b"200 ")

    monkeypatch.setattr("cats.calibration.collect_rss.shutil.which", lambda name: "/usr/bin/curl")
    monkeypatch.setattr("cats.calibration.collect_rss.subprocess.run", run)
    with _waf_client() as client:
        body = fetch_feed("https://news.example/rss.xml", client)
    assert "<rss>" in body
    assert [c[-1] for c in calls] == ["https://news.example/rss.xml", "https://news.example/feed.xml"]
    assert all("-L" not in c and "-sL" not in c for c in calls)


def test_curl_fallback_refuses_redirect_to_internal_address(fake_dns, monkeypatch):
    calls = []

    def run(cmd, **kwargs):
        calls.append(cmd)
        return _Proc(stdout=b"", stderr=b"302 http://169.254.169.254/latest/meta-data/")

    monkeypatch.setattr("cats.calibration.collect_rss.shutil.which", lambda name: "/usr/bin/curl")
    monkeypatch.setattr("cats.calibration.collect_rss.subprocess.run", run)
    with _waf_client() as client:
        with pytest.raises(ValueError, match="403"):
            fetch_feed("https://news.example/rss.xml", client)
    assert len(calls) == 1  # the metadata URL was never requested
