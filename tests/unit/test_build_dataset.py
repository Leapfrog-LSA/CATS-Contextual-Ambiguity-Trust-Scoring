import json

import pytest

from cats.calibration.build_dataset import build_dataset, build_record, compute_signals, main
from cats.calibration.dataset import SIGNAL_NAMES, load_dataset

# Coherence needs spaCy loaded for non-degraded output, but all four signals
# return valid values without it, so these tests run NLP-free. We assert on
# structure/shape, not on the (model-dependent) coherence magnitude.

_MESSAGES = [
    {"timestamp": "2026-01-01T08:00:00Z", "text": "Il governo annuncia un piano economico."},
    {"timestamp": "2026-01-01T09:00:00Z", "text": "I lavoratori protestano in piazza."},
    {"timestamp": "2026-01-01T10:00:00Z", "text": "Il parlamento discute la legge di bilancio."},
]


def test_compute_signals_returns_all_four():
    signals = compute_signals(_MESSAGES, "news")
    assert set(signals) == set(SIGNAL_NAMES)
    assert all(0.0 <= v <= 100.0 for v in signals.values())


def test_compute_signals_empty_messages_raises():
    with pytest.raises(ValueError):
        compute_signals([], "social")


def test_build_record_uses_label_and_source_type():
    record = build_record(
        {"source_type": "news", "label": 85, "messages": _MESSAGES},
        default_source_type="social",
    )
    assert record["source_type"] == "news"
    assert record["label"] == 85.0
    assert set(record["signals"]) == set(SIGNAL_NAMES)


def test_build_record_falls_back_to_default_source_type():
    record = build_record({"label": 50, "messages": _MESSAGES}, default_source_type="blog")
    assert record["source_type"] == "blog"


def test_build_record_missing_label_raises():
    with pytest.raises(ValueError):
        build_record({"messages": _MESSAGES}, default_source_type="social")


def test_build_record_empty_messages_raises():
    with pytest.raises(ValueError):
        build_record({"label": 50, "messages": []}, default_source_type="social")


def test_build_dataset_skips_bad_records_and_counts():
    sources = [
        {"source_id": "good1", "source_type": "news", "label": 80, "messages": _MESSAGES},
        {"source_id": "bad", "messages": _MESSAGES},  # no label -> skipped
        {"source_id": "good2", "source_type": "social", "label": 40, "messages": _MESSAGES},
    ]
    records, stats = build_dataset(sources, default_source_type="social")
    assert stats.written == 2
    assert stats.skipped == 1
    assert stats.per_source_type == {"news": 1, "social": 1}


def test_main_produces_loadable_dataset(tmp_path):
    src = tmp_path / "sources.jsonl"
    src.write_text(
        "\n".join(
            json.dumps({"source_type": st, "label": lbl, "messages": _MESSAGES})
            for st, lbl in [("news", 80), ("social", 35)]
        ),
        encoding="utf-8",
    )
    out = tmp_path / "train.jsonl"
    rc = main(["--input", str(src), "--out", str(out), "--no-init-nlp"])
    assert rc == 0
    # The output must round-trip through the calibrator's own loader.
    samples = load_dataset(out)
    assert len(samples) == 2
    assert {s.source_type for s in samples} == {"news", "social"}


def test_main_errors_on_missing_input(tmp_path, capsys):
    with pytest.raises(SystemExit):
        main(["--input", str(tmp_path / "nope.jsonl"), "--out", str(tmp_path / "o.jsonl")])
