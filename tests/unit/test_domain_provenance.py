from cats.signals.domain_provenance import compute_domain_provenance, extract_host


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

    def test_free_hosting_subdomain_flagged(self):
        # e.g. "Il Corrispondente" — a blogspot disinformation site that
        # publishes on a regular cadence, so silence misses it but the domain
        # signal catches it.
        r = compute_domain_provenance("https://ilcorrispondente.blogspot.com")
        assert r.free_host is True
        assert r.value == 45.0
        assert r.metadata["reasons"] == ["free_host"]

    def test_typosquat_on_ordinary_tld(self):
        r = compute_domain_provenance("https://repubblika.it")
        assert r.typosquat is True
        assert r.value == 50.0


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
