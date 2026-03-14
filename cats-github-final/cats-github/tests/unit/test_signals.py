"""Unit tests — signal computations (no DB, no spaCy model required)."""
import pytest
from cats.signals.types import Message
from cats.signals.volatility import compute_volatility
from cats.signals.silence import compute_silence
from cats.signals.gaming import compute_gaming


# ── Volatility ─────────────────────────────────────────────────────────────────

def test_volatility_insufficient_messages():
    msgs = [Message("2026-01-01T10:00:00Z", "x"), Message("2026-01-01T11:00:00Z", "y")]
    r = compute_volatility(msgs)
    assert r.value == 0.0
    assert r.confidence == 0.0
    assert r.metadata.get("reason") == "insufficient_messages"


def test_volatility_computes_in_range():
    msgs = [
        Message("2026-01-01T10:00:00Z", "Grande gioia felicità meravigliosa"),
        Message("2026-01-01T11:00:00Z", "Tragedia disastro catastrofe orribile"),
        Message("2026-01-01T12:00:00Z", "Ottima notizia successo straordinario"),
    ]
    r = compute_volatility(msgs)
    assert r.name == "volatility"
    assert 0.0 <= r.value <= 100.0
    assert 0.0 <= r.confidence <= 1.0


def test_volatility_zero_for_uniform_text():
    msgs = [Message(f"2026-01-01T{h:02d}:00:00Z", "Messaggio neutro") for h in range(5)]
    r = compute_volatility(msgs)
    assert r.sentiment_spikes == 0


# ── Silence ────────────────────────────────────────────────────────────────────

def test_silence_detects_anomaly():
    msgs = [
        Message("2026-01-01T10:00:00Z", "prima"),
        Message("2026-01-10T10:00:00Z", "seconda"),  # 216 h gap
    ]
    r = compute_silence(msgs, anomaly_threshold_hours=48.0)
    assert r.anomalous_gaps == 1
    assert r.max_gap_hours > 200


def test_silence_no_anomaly():
    msgs = [
        Message("2026-01-01T10:00:00Z", "prima"),
        Message("2026-01-01T12:00:00Z", "seconda"),  # 2 h gap
    ]
    r = compute_silence(msgs, anomaly_threshold_hours=48.0)
    assert r.anomalous_gaps == 0


def test_silence_single_message():
    msgs = [Message("2026-01-01T10:00:00Z", "sola")]
    r = compute_silence(msgs)
    assert r.value == 0.0 and r.confidence == 0.0


def test_silence_confidence_scales_with_volume():
    msgs_small = [Message(f"2026-01-{d:02d}T10:00:00Z", "x") for d in range(1, 4)]
    msgs_large = [Message(f"2026-01-{d:02d}T10:00:00Z", "x") for d in range(1, 32)]
    r_small = compute_silence(msgs_small)
    r_large = compute_silence(msgs_large)
    assert r_large.confidence >= r_small.confidence


# ── Gaming ─────────────────────────────────────────────────────────────────────

def test_gaming_below_min_tokens():
    msgs = [Message("2026-01-01T10:00:00Z", "corto")]
    r = compute_gaming(msgs)
    assert r.value == 0.0
    assert r.confidence == 0.0
    assert r.metadata.get("reason") == "insufficient_tokens"


def test_gaming_detects_repetition():
    spam = "compra adesso compra adesso compra adesso "
    msgs = [Message(f"2026-01-01T{i:02d}:00:00Z", spam * 3) for i in range(15)]
    r = compute_gaming(msgs)
    assert r.name == "gaming"
    assert r.repetition_score > 0.0


def test_gaming_score_in_range():
    msgs = [Message(f"2026-01-01T{i:02d}:00:00Z", f"Contenuto {i} articolo interessante notizia recente") for i in range(20)]
    r = compute_gaming(msgs)
    assert 0.0 <= r.value <= 100.0


def test_gaming_legitimate_content_lower_score():
    diverse_texts = [
        "Il Parlamento approva la nuova legge sul lavoro dopo lungo dibattito.",
        "La Banca Centrale annuncia variazioni ai tassi di interesse.",
        "Il presidente incontra i leader europei a Bruxelles per il vertice.",
        "Nuove scoperte scientifiche cambiano la comprensione del clima.",
        "Il tribunale emette sentenza storica nel processo per corruzione.",
        "Il ministro presenta il piano quinquennale per le infrastrutture.",
        "I dati economici mostrano crescita del PIL nel terzo trimestre.",
        "La conferenza internazionale affronta il tema della sicurezza.",
        "Il comune approva il piano regolatore per la nuova zona industriale.",
        "Gli esperti discutono le implicazioni della riforma pensionistica.",
        "La ricerca universitaria porta a scoperte nel campo medico.",
        "Il governo presenta il bilancio preventivo per il prossimo anno.",
    ]
    msgs = [Message(f"2026-01-{i+1:02d}T10:00:00Z", t) for i, t in enumerate(diverse_texts)]
    r = compute_gaming(msgs)
    assert r.value < 70.0  # diverse content → lower gaming signal
