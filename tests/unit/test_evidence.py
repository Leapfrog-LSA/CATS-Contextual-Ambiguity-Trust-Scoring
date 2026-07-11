from cats.scoring.engine import evidence_summary, requires_human_review
from cats.signals.types import SignalResult


def _signals(*confidences, with_domain=False):
    names = ("coherence", "volatility", "silence", "gaming")
    sigs = [SignalResult(name=n, value=50.0, confidence=c) for n, c in zip(names, confidences)]
    if with_domain:
        sigs.append(SignalResult(name="domain_provenance", value=45.0, confidence=1.0))
    return sigs


class TestEvidenceSummary:
    def test_below_minimum_is_insufficient(self):
        e = evidence_summary(_signals(0.0, 0.0, 0.0, 0.0), n_messages=1, min_messages=3)
        assert e["sufficient"] is False
        assert e["messages"] == 1
        assert e["min_messages"] == 3
        assert e["mean_signal_confidence"] == 0.0

    def test_at_minimum_is_sufficient(self):
        e = evidence_summary(_signals(0.3, 0.15, 0.1, 0.06), n_messages=3, min_messages=3)
        assert e["sufficient"] is True
        assert e["mean_signal_confidence"] == round((0.3 + 0.15 + 0.1 + 0.06) / 4, 3)

    def test_domain_signal_excluded_from_mean(self):
        # domain-provenance is a penalty, not evidence about the message
        # history: its (always 1.0) confidence must not inflate the mean.
        with_domain = evidence_summary(_signals(0.2, 0.2, 0.2, 0.2, with_domain=True), 5, 3)
        without = evidence_summary(_signals(0.2, 0.2, 0.2, 0.2), 5, 3)
        assert with_domain["mean_signal_confidence"] == without["mean_signal_confidence"] == 0.2


class TestReviewOnInsufficientEvidence:
    def test_insufficient_evidence_forces_review_even_on_high_band(self):
        sigs = _signals(0.0, 0.0, 0.0, 0.0)
        assert requires_human_review(85.0, "high", sigs, sufficient_evidence=False) is True

    def test_sufficient_evidence_keeps_existing_rules(self):
        confident = _signals(0.9, 0.9, 0.9, 0.9)
        assert requires_human_review(85.0, "high", confident, sufficient_evidence=True) is False
        assert requires_human_review(25.0, "low", confident, sufficient_evidence=True) is True

    def test_lite_honours_min_evidence_setting(self, monkeypatch):
        from cats.core.config import settings
        from cats.lite import score

        msgs = [
            {"timestamp": f"2026-01-0{i + 1}T08:00:00Z", "text": "Il governo annuncia il piano economico oggi."}
            for i in range(3)
        ]
        monkeypatch.setattr(settings, "min_evidence_messages", 3)
        ok = score(msgs, load_nlp=False, explain=False)
        assert ok["evidence"]["sufficient"] is True
        monkeypatch.setattr(settings, "min_evidence_messages", 5)
        poor = score(msgs, load_nlp=False, explain=False)
        assert poor["evidence"]["sufficient"] is False
        assert poor["requires_human_review"] is True
        assert poor["trust_score"] == ok["trust_score"]  # flag-only: the score never changes
