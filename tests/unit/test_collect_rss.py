import json

import pytest

from cats.calibration.collect_rss import (
    attach_messages,
    main,
    parse_feed,
    parse_timestamp,
    strip_html,
)

RSS2 = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>Example News</title>
  <item>
    <title>Prima notizia</title>
    <description>&lt;p&gt;Dettagli   della &lt;b&gt;prima&lt;/b&gt; notizia.&lt;/p&gt;</description>
    <link>https://example.com/1</link>
    <pubDate>Mon, 01 Jun 2026 08:00:00 GMT</pubDate>
  </item>
  <item>
    <title>Seconda notizia</title>
    <pubDate>Tue, 02 Jun 2026 09:30:00 +0200</pubDate>
  </item>
  <item>
    <title>Senza data: scartata</title>
  </item>
</channel></rss>"""

ATOM = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Example Atom</title>
  <entry>
    <title>Post uno</title>
    <summary>Riassunto del post uno.</summary>
    <link href="https://example.com/a1"/>
    <published>2026-06-01T10:00:00Z</published>
  </entry>
  <entry>
    <title>Post due</title>
    <updated>2026-06-02T11:00:00+02:00</updated>
  </entry>
</feed>"""

RDF = """<?xml version="1.0"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns="http://purl.org/rss/1.0/"
         xmlns:dc="http://purl.org/dc/elements/1.1/">
  <item><title>Voce RDF</title><dc:date>2026-06-03T12:00:00Z</dc:date></item>
</rdf:RDF>"""


# ── Helpers ────────────────────────────────────────────────────────────────
def test_strip_html_unescapes_and_collapses_whitespace():
    assert strip_html("&lt;p&gt;ciao&lt;/p&gt;") == "ciao"
    assert strip_html("<p>a\n  <b>b</b></p>") == "a b"
    assert strip_html("") == ""


def test_parse_timestamp_rfc822_and_iso_normalise_to_utc():
    assert parse_timestamp("Mon, 01 Jun 2026 08:00:00 GMT") == "2026-06-01T08:00:00Z"
    assert parse_timestamp("2026-06-02T11:00:00+02:00") == "2026-06-02T09:00:00Z"
    assert parse_timestamp("2026-06-02T11:00:00Z") == "2026-06-02T11:00:00Z"
    assert parse_timestamp("not a date") is None
    assert parse_timestamp("") is None


def test_parse_timestamp_naive_dates_assume_utc():
    assert parse_timestamp("2026-06-02T11:00:00") == "2026-06-02T11:00:00Z"


# ── Feed parsing ───────────────────────────────────────────────────────────
def test_parse_feed_rss2():
    msgs = parse_feed(RSS2)
    assert len(msgs) == 2  # the dateless item is dropped
    assert msgs[0]["timestamp"] == "2026-06-01T08:00:00Z"
    assert msgs[0]["text"] == "Prima notizia. Dettagli della prima notizia."
    assert msgs[0]["metadata"] == {"link": "https://example.com/1"}
    assert msgs[1]["timestamp"] == "2026-06-02T07:30:00Z"
    assert msgs[1]["text"] == "Seconda notizia"


def test_parse_feed_atom():
    msgs = parse_feed(ATOM)
    assert len(msgs) == 2
    assert msgs[0]["text"] == "Post uno. Riassunto del post uno."
    assert msgs[0]["metadata"] == {"link": "https://example.com/a1"}
    assert msgs[1]["timestamp"] == "2026-06-02T09:00:00Z"


def test_parse_feed_rdf_dc_date():
    msgs = parse_feed(RDF)
    assert msgs == [{"timestamp": "2026-06-03T12:00:00Z", "text": "Voce RDF"}]


def test_parse_feed_description_repeating_title_is_not_duplicated():
    xml = RSS2.replace(
        "&lt;p&gt;Dettagli   della &lt;b&gt;prima&lt;/b&gt; notizia.&lt;/p&gt;",
        "Prima notizia con altri dettagli.",
    )
    assert parse_feed(xml)[0]["text"] == "Prima notizia con altri dettagli."


def test_parse_feed_rejects_dtd_bad_xml_and_empty_feeds():
    with pytest.raises(ValueError, match="DTD"):
        parse_feed('<?xml version="1.0"?><!DOCTYPE rss []><rss/>')
    with pytest.raises(ValueError, match="not well-formed"):
        parse_feed("<rss><channel>")
    with pytest.raises(ValueError, match="no <item>"):
        parse_feed("<rss><channel><title>vuoto</title></channel></rss>")


# ── attach_messages ────────────────────────────────────────────────────────
def _registry():
    return [
        {"source_id": "a", "source_type": "news", "label": 85.0, "rss": "https://a/feed"},
        {"source_id": "b", "source_type": "news", "label": 50.0, "rss": "https://b/feed"},
        {"source_id": "c", "source_type": "social", "label": 30.0, "rss": None},
    ]


def _msgs(n, day0=1):
    return [{"timestamp": f"2026-06-{day0 + i:02d}T08:00:00Z", "text": f"msg {i}"} for i in range(n)]


def test_attach_messages_keeps_labels_and_counts():
    def fetch(url):
        return _msgs(5) if url == "https://a/feed" else _msgs(1)

    records, stats = attach_messages(_registry(), fetch, min_messages=3)
    assert [r["source_id"] for r in records] == ["a"]
    assert records[0]["label"] == 85.0 and len(records[0]["messages"]) == 5
    assert stats.no_feed == 1  # c has no rss
    assert stats.too_few_messages == 1  # b
    assert stats.collected == 1 and stats.total_messages == 5
    assert stats.by_source_type == {"news": 1}


def test_attach_messages_feed_errors_are_skipped():
    def fetch(url):
        raise ValueError("boom")

    records, stats = attach_messages(_registry(), fetch, min_messages=1)
    assert records == []
    assert stats.feed_error == 2


def test_attach_messages_since_and_max_messages():
    def fetch(url):
        return list(reversed(_msgs(10)))  # unsorted input

    records, _ = attach_messages(
        [{"source_id": "a", "rss": "https://a/feed"}],
        fetch,
        min_messages=1,
        max_messages=3,
        since="2026-06-05T00:00:00Z",
    )
    ts = [m["timestamp"] for m in records[0]["messages"]]
    assert ts == sorted(ts)
    assert len(ts) == 3 and ts[0] >= "2026-06-05T00:00:00Z"
    assert ts[-1] == "2026-06-10T08:00:00Z"  # keeps the most recent


# ── CLI ────────────────────────────────────────────────────────────────────
def test_main_end_to_end_with_mocked_transport(tmp_path, monkeypatch, capsys):
    import httpx

    import cats.calibration.collect_rss as mod

    def handler(request):
        return httpx.Response(200, text=RSS2 if "a" in request.url.host else ATOM)

    real_client = httpx.Client

    def patched_client(**kwargs):
        kwargs.pop("timeout", None)
        return real_client(transport=httpx.MockTransport(handler), **kwargs)

    monkeypatch.setattr(mod.httpx, "Client", patched_client)

    labels = tmp_path / "labels.jsonl"
    labels.write_text(
        "\n".join(
            json.dumps(r)
            for r in [
                {"source_id": "a", "source_type": "news", "label": 85.0, "rss": "https://a.example/feed"},
                {"source_id": "b", "source_type": "news", "label": 50.0, "rss": "https://b.example/feed"},
            ]
        ),
        encoding="utf-8",
    )
    out = tmp_path / "labelled_sources.jsonl"
    assert main(["--labels", str(labels), "--out", str(out), "--min-messages", "2"]) == 0

    records = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
    assert {r["source_id"] for r in records} == {"a", "b"}
    assert all("messages" in r and "label" in r for r in records)
    assert "Wrote 2 labelled source(s)" in capsys.readouterr().out


def test_main_errors_on_missing_or_empty_labels(tmp_path):
    with pytest.raises(SystemExit):
        main(["--labels", str(tmp_path / "nope.jsonl"), "--out", str(tmp_path / "o.jsonl")])
    empty = tmp_path / "empty.jsonl"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(SystemExit):
        main(["--labels", str(empty), "--out", str(tmp_path / "o.jsonl")])


def test_main_bad_since_errors(tmp_path):
    labels = tmp_path / "labels.jsonl"
    labels.write_text(json.dumps({"source_id": "a", "rss": "https://a/f"}), encoding="utf-8")
    with pytest.raises(SystemExit):
        main(["--labels", str(labels), "--out", str(tmp_path / "o.jsonl"), "--since", "garbage"])
