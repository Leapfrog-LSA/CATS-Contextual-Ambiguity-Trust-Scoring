import cats.signals.domain_provenance as dp
from cats.signals.domain_provenance import compute_domain_provenance, extract_host


def _mock_popularity_table(monkeypatch, table):
    """Deterministic stand-in for the (not committed, see .gitignore) real
    Tranco download — a domain absent from ``table`` behaves as unranked."""
    monkeypatch.setattr(dp, "_popularity_table", table)
    monkeypatch.setattr(dp, "_popularity_load_attempted", True)


class TestExtractHost:
    def test_strips_scheme_www_and_port(self):
        assert extract_host("https://www.repubblica.it:443/politica") == "repubblica.it"

    def test_bare_domain_without_scheme(self):
        assert extract_host("bild.pics") == "bild.pics"

    def test_empty_returns_blank(self):
        assert extract_host("") == ""
        assert extract_host("   ") == ""


class TestCloneDomains:
    def test_brand_on_suspicious_tld_flagged(self):
        # Doppelganger-style clone: legit brand on a cheap TLD.
        r = compute_domain_provenance("https://spiegel.ltd/artikel")
        assert r.name == "domain_provenance"
        assert r.value >= 40  # high-precision flag threshold used in the research
        assert r.suspicious_tld is True
        assert r.brand_on_bad_tld is True
        assert r.confidence == 1.0
        assert "suspicious_tld" in r.metadata["reasons"]

    def test_free_hosting_subdomain_flagged(self, monkeypatch):
        # e.g. "Il Corrispondente" — a blogspot disinformation site that
        # publishes on a regular cadence, so silence misses it but the domain
        # signal catches it. Confirmed unranked in the real Tranco top-1M
        # (verified 2026-08-28, not committed -- `make tranco-download`); a
        # deterministic empty table reproduces that here.
        _mock_popularity_table(monkeypatch, {})
        r = compute_domain_provenance("https://ilcorrispondente.blogspot.com")
        assert r.free_host is True
        assert r.low_popularity_corroboration is True
        assert r.value == 60.0  # 45.0 free_host + 15.0 corroboration
        assert r.metadata["reasons"] == ["free_host", "low_popularity_corroboration"]

    def test_typosquat_on_ordinary_tld(self, monkeypatch):
        # Also confirmed unranked in the real Tranco top-1M (2026-08-28).
        _mock_popularity_table(monkeypatch, {})
        r = compute_domain_provenance("https://repubblika.it")
        assert r.typosquat is True
        assert r.low_popularity_corroboration is True
        assert r.value == 65.0  # 50.0 typosquat + 15.0 corroboration


class TestLegitimateDomains:
    def test_major_brand_scores_zero(self):
        r = compute_domain_provenance("https://www.corriere.it/cronaca")
        assert r.value == 0.0
        assert r.confidence == 1.0
        assert (r.suspicious_tld, r.free_host, r.typosquat, r.brand_on_bad_tld) == (False, False, False, False)
        assert r.metadata["reasons"] == []

    def test_low_recall_fake_news_on_ordinary_domain(self):
        # Documented limitation: content fakery on an ordinary domain is
        # invisible to a structural domain signal.
        r = compute_domain_provenance("https://worldnewsdailyreport.com/story")
        assert r.value == 0.0


class TestPopularityCorroboration:
    """The Tranco-rank corroboration bonus (2026-08-28): never a standalone
    trigger, only amplifies an already-fired structural flag.

    Design note (not re-derived by CI): a one-off check against a 25-source
    sample of `data/Fonti_OSINT.csv` on 2026-08-28 found 24% of legitimate
    catalogue sources (government subdomains, regional open-data portals,
    niche outlets) have no Tranco rank at all, so "unranked" alone would
    mislabel real institutional sources — hence corroboration-only.
    """

    def test_unranked_alone_never_fires_on_clean_domain(self, monkeypatch):
        # A domain with no structural flag must stay at 0.0 even when
        # genuinely unranked (empty table = everything is "unranked") — this
        # is the safety property the corroboration-only design guarantees.
        _mock_popularity_table(monkeypatch, {})
        r = compute_domain_provenance("https://an-ordinary-outlet.example")
        assert r.low_popularity_corroboration is False
        assert r.value == 0.0

    def test_ranked_clone_gets_no_corroboration_bonus(self, monkeypatch):
        # A structurally-flagged domain that DOES have a rank (an established,
        # high-traffic site despite the suspicious TLD) must not get the
        # extra penalty — corroboration only fires on genuine absence.
        _mock_popularity_table(monkeypatch, {"spiegel.ltd": 392949})
        r = compute_domain_provenance("https://spiegel.ltd")
        assert r.suspicious_tld is True  # structural flag still fires
        assert r.low_popularity_corroboration is False
        assert r.value == 65.0  # unchanged: 40.0 suspicious_tld + 25.0 brand_on_bad_tld

    def test_missing_popularity_table_degrades_to_no_corroboration(self, monkeypatch):
        # No `data/tranco_top1m.csv` present (not committed -- see
        # .gitignore / `make tranco-download`) must degrade cleanly, same
        # pattern as every other optional-dependency signal in this codebase.
        _mock_popularity_table(monkeypatch, None)
        r = compute_domain_provenance("https://ilcorrispondente.blogspot.com")
        assert r.free_host is True
        assert r.low_popularity_corroboration is False
        assert r.value == 45.0  # unchanged from the pre-corroboration behaviour

    def test_real_load_failure_is_graceful(self, monkeypatch):
        # End-to-end through _load_popularity_table (not pre-mocked): pointing
        # at a nonexistent path must not raise, and must resolve to "no
        # corroboration" rather than crash the whole signal computation.
        monkeypatch.setattr(dp, "_popularity_table", None)
        monkeypatch.setattr(dp, "_popularity_load_attempted", False)
        from cats.core.config import settings

        monkeypatch.setattr(settings, "domain_popularity_path", "data/does_not_exist.csv")
        r = compute_domain_provenance("https://ilcorrispondente.blogspot.com")
        assert r.low_popularity_corroboration is False
        assert r.value == 45.0


class TestDegradation:
    def test_no_domain_is_neutral_zero_confidence(self):
        r = compute_domain_provenance("")
        assert r.value == 0.0
        assert r.confidence == 0.0
        assert r.metadata.get("reason") == "no_domain"

    def test_score_is_bounded(self):
        for url in [
            "",
            "bild.pics",
            "https://spiegel.ltd",
            "https://x.blogspot.com",
            "https://repubblica.it",
            "https://repubblika.cfd",
        ]:
            r = compute_domain_provenance(url)
            assert 0.0 <= r.value <= 100.0
