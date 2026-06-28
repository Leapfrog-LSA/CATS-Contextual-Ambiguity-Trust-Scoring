from cats.signals.silence import compute_silence
from cats.signals.types import Message
from cats.signals.volatility import compute_volatility


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
