"""Risk-register-driven adversarial tests (docs/eu_ai_act/risk_management_art9.md §7).

Each class exercises one register entry — R3 (non-Italian input), R4
(adversarial evasion of the behavioural signals), R5 (minimal-sample
instability) — against the CURRENT engine and pins today's measured behaviour,
including the known weaknesses. The point is regression detection in both
directions: hardening work (roadmap phase C) that changes one of these outcomes
must do so deliberately and update the pin; a refactor that accidentally weakens
a mitigation fails here. Pinning a weakness documents it, it does not endorse
it (WP 4.1).
"""

from datetime import datetime, timedelta

import pytest

from cats.lite import score
from cats.scoring.engine import apply_domain_penalty
from cats.signals.domain_provenance import compute_domain_provenance
from cats.signals.gaming import compute_gaming
from cats.signals.silence import compute_silence
from cats.signals.types import Message
from cats.signals.volatility import compute_volatility

_T0 = datetime(2026, 1, 1, 8, 0, 0)

# Explicit static tables (cats.scoring.weights._STATIC_WEIGHTS) so every number
# here is deterministic regardless of any CATS_WEIGHTS_FILE in the environment.
_NEWS_WEIGHTS = {"coherence": 0.35, "volatility": 0.20, "silence": 0.25, "gaming": 0.20}
_DEFAULT_WEIGHTS = {"coherence": 0.30, "volatility": 0.25, "silence": 0.25, "gaming": 0.20}

_BAND_ORDER = ["very_low", "low", "medium", "medium_high", "high"]


@pytest.fixture(autouse=True)
def _degraded_ner(monkeypatch):
    """Pin coherence to the degraded NER path (model absent), exactly as in CI.

    Keeps this module deterministic whether or not the spaCy model happens to
    be installed locally: coherence is always the neutral 50 / confidence 0.
    """
    from cats.core.config import settings
    from cats.signals import coherence

    monkeypatch.setattr(settings, "coherence_backend", "ner")
    monkeypatch.setattr(coherence, "nlp", None)


def _daily_dicts(n=30):
    """One message per day at 08:00 — the cadence that defeats `silence`."""
    subjects = ["Il governo", "La regione", "Il ministero", "Il comune", "La commissione", "Il sindacato"]
    verbs = ["annuncia", "discute", "approva", "rinvia", "presenta"]
    objects = [
        "il piano economico",
        "la riforma fiscale",
        "il bilancio annuale",
        "la nuova misura",
        "il decreto attuativo",
        "lo stanziamento previsto",
        "il programma sociale",
    ]
    return [
        {
            "timestamp": (_T0 + timedelta(days=i)).isoformat() + "Z",
            "text": f"{subjects[i % 6]} {verbs[i % 5]} {objects[i % 7]}.",
        }
        for i in range(n)
    ]


def _daily_messages(n=30):
    return [Message(timestamp=m["timestamp"], text=m["text"]) for m in _daily_dicts(n)]


class TestR4AdversarialEvasion:
    """R4 — an adversary who manages the publishing cadence evades `silence`,
    the one behavioural signal carrying rank information on the July 2026
    holdout (docs/calibration_findings_2026-07-28.md)."""

    def test_regular_cadence_neutralises_silence(self):
        r = compute_silence(_daily_messages(), "news")
        assert r.value == 0.0
        assert r.anomalous_gaps == 0
        assert r.confidence == 1.0  # full confidence: the signal is genuinely evaded, not undecided

    def test_regular_cadence_clone_not_flagged_behaviourally(self):
        # KNOWN GAP: without a URL, a regular-cadence clone is NOT banded low —
        # the behavioural signals cannot see infrastructure impersonation.
        result = score(_daily_dicts(), source_type="news", weights=_NEWS_WEIGHTS, load_nlp=False, explain=False)
        assert result["band"] not in {"low", "very_low"}

    def test_domain_penalty_catches_regular_cadence_clone(self):
        # The ENGINE 1.4 counter-measure: the same source WITH its clone URL
        # (free-hosting subdomain, red-flag 45) drops by exactly 0.6 * 45 = 27
        # and lands in a strictly lower band.
        base = score(_daily_dicts(), source_type="news", weights=_NEWS_WEIGHTS, load_nlp=False, explain=False)
        clone = score(
            _daily_dicts(),
            source_type="news",
            weights=_NEWS_WEIGHTS,
            load_nlp=False,
            url="https://ilcorrispondente.blogspot.com",
        )
        assert clone["trust_score"] == pytest.approx(max(0.0, base["trust_score"] - 27.0), abs=0.01)
        assert clone["signals"]["domain_provenance"] == 45.0
        assert clone["explanation"]["domain_penalty"]["penalty_applied"] == 27.0
        assert _BAND_ORDER.index(clone["band"]) < _BAND_ORDER.index(base["band"])

    def test_domain_penalty_is_clamped_and_asymmetric(self):
        flagged = compute_domain_provenance("bild.pics")  # suspicious TLD (+40) + brand on foreign TLD (+25)
        assert flagged.value == 65.0
        assert apply_domain_penalty(10.0, flagged) == 0.0  # clamped at zero, never negative
        assert apply_domain_penalty(80.0, None) == 80.0  # no URL supplied: no-op
        clean = compute_domain_provenance("https://www.repubblica.it")
        assert clean.value == 0.0
        assert apply_domain_penalty(42.0, clean) == 42.0  # clean domain is never rewarded

    def test_spam_burst_scores_far_above_editorial_baseline(self):
        # Bot-like corpus: identical repetitive text, 9 posts within seconds,
        # then silence — repetition, TTR, burst and vocab sub-scores all fire.
        spam_text = "compra ora offerta imperdibile sconto esclusivo " * 3
        spam = [
            Message(timestamp=(_T0 + timedelta(seconds=i)).isoformat() + "+00:00", text=spam_text.strip())
            for i in range(9)
        ]
        spam.append(Message(timestamp=(_T0 + timedelta(days=30)).isoformat() + "+00:00", text=spam_text.strip()))
        g_spam = compute_gaming(spam)
        g_editorial = compute_gaming(_daily_messages(10))
        assert g_spam.repetition_score > 0.5
        assert g_spam.burst_score > 0.5
        assert g_spam.vocab_score > 0.5
        assert g_spam.value > g_editorial.value + 30


class TestR5MinimalEvidence:
    """R5 — few messages yield near-zero-confidence signals, and the aggregate
    still reports a HIGH band: negative-polarity signals return 0 when they
    cannot be computed, which inverts to a perfect reliability contribution.
    Since the minimum-evidence guardrail (roadmap item 9) landed, that poverty
    is *flagged*: `evidence.sufficient=false` forces human review. The score
    itself stays unpenalised — changing it needs the recalibration cycle."""

    def test_single_message_high_score_is_flagged_for_review(self):
        result = score(
            [{"timestamp": "2026-01-01T08:00:00Z", "text": "Unico messaggio senza storia."}],
            weights=_DEFAULT_WEIGHTS,
            load_nlp=False,
        )
        # 0.30*50 (neutral coherence) + (0.25+0.25+0.20)*100 (uncomputable
        # negative signals inverted) = 85.0 — still "high" from one message...
        assert result["trust_score"] == 85.0
        assert result["band"] == "high"
        assert all(s["confidence"] == 0.0 for s in result["explanation"]["signals"])
        # ...but the evidence guardrail now surfaces it and forces review.
        assert result["evidence"]["sufficient"] is False
        assert result["evidence"]["messages"] == 1
        assert result["requires_human_review"] is True

    def test_every_signal_reports_zero_confidence_below_its_floor(self):
        # The evidence poverty IS visible per signal — it is just not acted on.
        from cats.signals.coherence import compute_coherence

        single = [Message(timestamp="2026-01-01T08:00:00+00:00", text="Solo.")]
        assert compute_coherence(single).confidence == 0.0
        assert compute_volatility(single).confidence == 0.0
        assert compute_silence(single).confidence == 0.0
        assert compute_gaming(single).confidence == 0.0

    def test_api_schema_floor_is_one_message(self):
        # The schema floor stays at ONE message (backwards compatible): the R5
        # mitigation is the evidence flag above, not request rejection.
        from cats.api.schemas import EvaluateRequest

        req = EvaluateRequest(
            source_id="src",
            messages=[{"timestamp": "2026-01-01T08:00:00Z", "text": "ciao"}],
        )
        assert len(req.messages) == 1


class TestR3NonItalianInput:
    """R3 — the NLP stack is Italian-optimised; non-Italian input used to
    degrade silently. Since the language guardrail (roadmap item 8) landed,
    the mismatch is detected and flagged (`language.detected`, plus an
    explanation warning); scores are still computed and never altered by the
    flag."""

    @staticmethod
    def _msgs(texts):
        return [{"timestamp": (_T0 + timedelta(days=i)).isoformat() + "Z", "text": t} for i, t in enumerate(texts)]

    _ENGLISH = [
        "The government announced a new economic plan this morning.",
        "Trade unions replied with a general strike threat over the plan.",
        "Parliament will debate the proposed budget law next week.",
    ]

    def test_english_input_is_flagged(self):
        result = score(self._msgs(self._ENGLISH), source_type="news", weights=_NEWS_WEIGHTS, load_nlp=False)
        assert 0.0 <= result["trust_score"] <= 100.0
        assert result["band"] in set(_BAND_ORDER)
        assert result["language"]["detected"] == "other"
        assert "language_warning" in result["explanation"]

    def test_italian_input_is_not_flagged(self):
        result = score(_daily_dicts(5), source_type="news", weights=_NEWS_WEIGHTS, load_nlp=False)
        assert result["language"]["detected"] == "italian"
        assert "language_warning" not in result["explanation"]

    def test_non_latin_scripts_flagged_and_do_not_crash(self):
        result = score(
            self._msgs(
                [
                    "Правительство объявило новый экономический план сегодня утром.",
                    "Профсоюзы ответили угрозой всеобщей забастовки.",
                    "Парламент обсудит проект бюджета на следующей неделе.",
                ]
            ),
            source_type="news",
            weights=_NEWS_WEIGHTS,
            load_nlp=False,
            explain=False,
        )
        assert 0.0 <= result["trust_score"] <= 100.0
        assert result["band"] in set(_BAND_ORDER)
        assert result["language"]["detected"] == "other"
        assert result["language"]["reason"] == "non_latin_script"
