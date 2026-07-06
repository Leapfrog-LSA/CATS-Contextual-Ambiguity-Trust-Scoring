from cats.signals.silence import compute_silence
from cats.signals.types import Message
from cats.signals.volatility import compute_volatility


class TestCoherence:
    _MSGS = [
        Message(timestamp="2026-01-01T08:00:00+00:00", text="Primo messaggio sul governo."),
        Message(timestamp="2026-01-01T09:00:00+00:00", text="Secondo messaggio sul parlamento."),
    ]

    def test_degrades_without_model(self, monkeypatch):
        from cats.core.config import settings
        from cats.signals import coherence

        # Default (ner) backend, spaCy model not loaded -> graceful degradation.
        monkeypatch.setattr(settings, "coherence_backend", "ner")
        monkeypatch.setattr(coherence, "nlp", None)
        r = coherence.compute_coherence(self._MSGS)
        assert r.value == 50.0
        assert r.confidence == 0.0
        assert r.metadata.get("reason") == "nlp_unavailable"

    def test_sbert_backend_falls_back_when_unavailable(self, monkeypatch):
        from cats.core.config import settings
        from cats.signals import coherence

        # sentence-transformers is not installed in the test env, so the sbert
        # backend must fall back to NER (which then degrades gracefully because
        # the spaCy model is also absent) instead of crashing.
        monkeypatch.setattr(settings, "coherence_backend", "sbert")
        monkeypatch.setattr(coherence, "_sbert_model", None)
        monkeypatch.setattr(coherence, "_sbert_failed", False)
        monkeypatch.setattr(coherence, "nlp", None)
        r = coherence.compute_coherence(self._MSGS)
        assert r.value == 50.0
        assert r.metadata.get("reason") == "nlp_unavailable"
        assert coherence._sbert_failed is True


class TestVolatility:
    def test_insufficient_messages(self, single_message):
        r = compute_volatility(single_message)
        assert r.value == 0.0
        assert r.confidence == 0.0

    def test_stable_sentiment(self, sample_messages):
        r = compute_volatility(sample_messages)
        assert 0 <= r.value <= 100
        assert r.sentiment_spikes >= 0

    def test_high_volatility(self):
        msgs = [
            Message(timestamp="2026-01-01T08:00:00+00:00", text="Tutto è meraviglioso, fantastico, bellissimo!"),
            Message(timestamp="2026-01-01T09:00:00+00:00", text="Terribile, orribile, disastroso, pessimo!"),
            Message(timestamp="2026-01-01T10:00:00+00:00", text="Incredibile successo, vittoria magnifica!"),
        ]
        r = compute_volatility(msgs)
        assert r.value >= 0


class TestSilence:
    def test_insufficient_messages(self, single_message):
        r = compute_silence(single_message)
        assert r.value == 0.0
        assert r.confidence == 0.0

    def test_no_anomalous_gaps(self, sample_messages):
        r = compute_silence(sample_messages)
        assert r.value == 0.0
        assert r.anomalous_gaps == 0

    def test_anomalous_gap_detected(self):
        msgs = [
            Message(timestamp="2026-01-01T08:00:00+00:00", text="First message"),
            Message(timestamp="2026-01-10T08:00:00+00:00", text="Message after long gap"),
        ]
        r = compute_silence(msgs, anomaly_threshold_hours=72.0)
        assert r.value > 0
        assert r.anomalous_gaps == 1
        assert r.max_gap_hours > 72.0

    def test_custom_threshold(self, sample_messages):
        r = compute_silence(sample_messages, anomaly_threshold_hours=0.5)
        assert r.value > 0


class TestGaming:
    def test_insufficient_tokens(self):
        from cats.signals.gaming import compute_gaming

        msgs = [Message(timestamp="2026-01-01T08:00:00+00:00", text="Corto")]
        r = compute_gaming(msgs)
        assert r.value == 0.0
        assert r.metadata.get("reason") == "insufficient_tokens"

    def test_normal_text(self):
        from cats.signals.gaming import compute_gaming

        msgs = [
            Message(
                timestamp=f"2026-01-{i+1:02d}T08:00:00+00:00",
                text=(
                    "Il governo italiano ha discusso il nuovo piano economico "
                    "con i sindacati delle principali industrie."
                ),
            )
            for i in range(5)
        ]
        r = compute_gaming(msgs)
        assert 0 <= r.value <= 100

    def test_repetitive_text_scores_higher(self):
        from cats.signals.gaming import compute_gaming

        msgs = [
            Message(
                timestamp=f"2026-01-{i+1:02d}T08:00:00+00:00",
                text="compra compra compra adesso adesso adesso offerta offerta offerta gratis gratis gratis",
            )
            for i in range(10)
        ]
        r = compute_gaming(msgs)
        assert r.repetition_score > 0


class TestGamingVocabFloor:
    def test_short_corpus_vocab_subscore_is_neutral(self):
        from cats.signals.gaming import _vocab_diversity

        # 10-49 tokens: no evidence of vocabulary collapse -> neutral 0.0,
        # not the maximum 1.0 (which inflated gaming by +25 points).
        assert _vocab_diversity(["parola"] * 20) == 0.0

    def test_long_corpus_vocab_subscore_measures_uniformity(self):
        from cats.signals.gaming import _vocab_diversity

        assert _vocab_diversity(["stessa"] * 100) > 0.9
        varied = [f"parola{i}" for i in range(100)]
        assert _vocab_diversity(varied) == 0.0


class TestSilenceThresholds:
    def test_threshold_table_covers_all_source_types(self):
        from cats.signals.silence import SOURCE_TYPE_THRESHOLDS, threshold_for

        assert set(SOURCE_TYPE_THRESHOLDS) == {"social", "news", "default"}
        assert threshold_for("blog") == SOURCE_TYPE_THRESHOLDS["default"]

    def test_explicit_threshold_overrides_table(self):
        msgs = [
            Message(timestamp="2026-01-01T00:00:00+00:00", text="a"),
            Message(timestamp="2026-01-02T00:00:00+00:00", text="b"),  # 24h gap
        ]
        strict = compute_silence(msgs, "news", anomaly_threshold_hours=1.0)
        lax = compute_silence(msgs, "news", anomaly_threshold_hours=100.0)
        assert strict.value == 100.0
        assert lax.value == 0.0
        assert strict.metadata["threshold_h"] == 1.0
