import json

import pytest

from cats.calibration.dataset import LabeledSample
from cats.calibration.evaluate import (
    BAND_ORDER,
    EvalReport,
    _class_metrics,
    evaluate_dataset,
    is_unreliable,
    load_weights_file,
    main,
    static_weights_for,
)


def _samples():
    # Reliability rises with coherence and falls with gaming; a sensible weight
    # set should rank these in roughly label order.
    rows = [
        ("news", 90, 15, 8, 5, 92),
        ("news", 70, 25, 12, 18, 74),
        ("news", 50, 40, 30, 35, 48),
        ("news", 30, 55, 45, 60, 30),
        ("social", 80, 30, 15, 20, 78),
        ("social", 40, 70, 35, 65, 28),
    ]
    return [
        LabeledSample(
            source_type=st,
            signals={"coherence": coh, "volatility": vol, "silence": sil, "gaming": gam},
            label=lbl,
        )
        for st, coh, vol, sil, gam, lbl in rows
    ]


def test_static_weights_for_restricts_to_groups():
    w = static_weights_for(["news"])
    assert set(w) == {"news"}
    assert abs(sum(w["news"].values()) - 1.0) < 1e-9


def test_evaluate_report_shape_and_ranges():
    report = evaluate_dataset(_samples(), static_weights_for(["news", "social"]))
    assert isinstance(report, EvalReport)
    assert report.n == 6
    assert -1.0 <= report.spearman <= 1.0
    assert 0.0 <= report.concordance <= 1.0
    assert 0.0 <= report.band_agreement_exact <= report.band_agreement_adjacent <= 1.0
    # Band rows only list non-empty bands, in canonical order, counts summing to n.
    assert [r.band for r in report.bands] == [b for b in BAND_ORDER if b in {r.band for r in report.bands}]
    assert sum(r.count for r in report.bands) == 6


def test_evaluate_ranks_monotone_data_positively():
    # Controlled case: only coherence varies (others held constant), so any
    # non-negative weighting yields predictions monotone in coherence == label.
    # This pins harness correctness independently of the weight values.
    samples = [
        LabeledSample(
            source_type="news",
            signals={"coherence": coh, "volatility": 50, "silence": 50, "gaming": 50},
            label=coh,
        )
        for coh in (20, 40, 60, 80, 95)
    ]
    report = evaluate_dataset(samples, static_weights_for(["news"]))
    assert report.spearman == pytest.approx(1.0)
    assert report.concordance == pytest.approx(1.0)


def test_per_source_type_marks_small_groups_na():
    # 2 social samples (< 3) -> metrics reported as None; 4 news -> numeric.
    report = evaluate_dataset(_samples(), static_weights_for(["news", "social"]))
    by_st = {g.source_type: g for g in report.per_source_type}
    assert by_st["social"].count == 2
    assert by_st["social"].spearman is None
    assert by_st["news"].count == 4
    assert by_st["news"].spearman is not None


def test_evaluate_empty_raises():
    with pytest.raises(ValueError):
        evaluate_dataset([], {})


def test_load_weights_file_falls_back_for_missing_group(tmp_path):
    p = tmp_path / "w.json"
    p.write_text(
        json.dumps({"weights": {"news": {"coherence": 0.5, "volatility": 0.2, "silence": 0.2, "gaming": 0.1}}}),
        encoding="utf-8",
    )
    weights = load_weights_file(p, ["news", "social"])
    assert weights["news"]["coherence"] == 0.5
    # social was absent from the file -> static fallback, still sums to 1.
    assert abs(sum(weights["social"].values()) - 1.0) < 1e-9


@pytest.mark.parametrize(
    "payload",
    [
        [1, 2],  # top level is not a mapping (already handled)
        {"weights": [1]},  # weights table is not a mapping
        {"weights": "news"},  # weights table is a string
        {"weights": {"news": None}},  # group is not a mapping (already handled)
    ],
)
def test_load_weights_file_wrong_shape_falls_back_to_static(tmp_path, payload):
    # A structurally wrong file is treated like a file without the groups: every
    # group gets the static WP 4.1 estimates instead of an AttributeError.
    p = tmp_path / "w.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    assert load_weights_file(p, ["news", "social"]) == static_weights_for(["news", "social"])


def test_main_runs_on_sample_dataset(capsys):
    rc = main(["--dataset", "examples/calibration_sample.jsonl"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Spearman" in out and "Band agreement" in out


def test_main_json_output_is_valid(capsys):
    rc = main(["--dataset", "examples/calibration_sample.jsonl", "--json"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["n"] > 0
    assert "spearman" in payload and "bands" in payload


def _by_class(rows):
    return {r.label: r for r in rows}


def test_is_unreliable_follows_band_cutoff():
    # The split is the shipped `low` band cutoff (40), not a second threshold.
    assert is_unreliable(0) and is_unreliable(19.9) and is_unreliable(39.9)
    assert not is_unreliable(40) and not is_unreliable(85)


def test_class_metrics_perfect_agreement():
    rows = _by_class(_class_metrics([10, 30, 50, 90], [10, 30, 50, 90]))
    for name in ("unreliable", "reliable"):
        assert rows[name].support == 2
        assert rows[name].predicted == 2
        assert rows[name].precision == rows[name].recall == rows[name].f1 == 1.0


def test_low_tail_f1_zero_while_rank_agreement_is_perfect():
    # The case the metric exists for: predictions ordered exactly like the
    # labels (Spearman 1.0) but the whole low tail pushed above the cutoff, so
    # not one unreliable source is called unreliable.
    labels = [10, 30, 50, 90]
    preds = [45, 50, 55, 90]
    rows = _by_class(_class_metrics(preds, labels))

    assert rows["unreliable"].support == 2
    assert rows["unreliable"].predicted == 0
    assert rows["unreliable"].precision is None  # nothing was predicted unreliable
    assert rows["unreliable"].recall == 0.0
    assert rows["unreliable"].f1 == 0.0
    # The reliable class still looks respectable — which is why it is reported
    # separately rather than averaged into one number.
    assert rows["reliable"].recall == 1.0
    assert rows["reliable"].f1 == pytest.approx(0.6667, abs=1e-4)


def test_class_absent_from_data_reports_none_not_zero():
    rows = _by_class(_class_metrics([55, 75, 95], [50, 70, 90]))
    assert rows["unreliable"].support == 0
    assert rows["unreliable"].predicted == 0
    assert rows["unreliable"].precision is None
    assert rows["unreliable"].recall is None
    assert rows["unreliable"].f1 is None
    assert rows["reliable"].f1 == 1.0


def test_macro_f1_averages_only_defined_classes():
    # unreliable undefined (absent both sides) -> macro-F1 is the reliable F1.
    samples = [
        LabeledSample(
            source_type="news",
            signals={"coherence": coh, "volatility": 50, "silence": 50, "gaming": 50},
            label=coh,
        )
        for coh in (60, 80, 95)
    ]
    report = evaluate_dataset(samples, static_weights_for(["news"]))
    rows = _by_class(report.per_class)
    assert rows["unreliable"].f1 is None
    assert report.macro_f1 == rows["reliable"].f1


def test_report_carries_per_class_rows():
    report = evaluate_dataset(_samples(), static_weights_for(["news", "social"]))
    assert [r.label for r in report.per_class] == ["unreliable", "reliable"]
    # Every sample lands on exactly one side of the split, per axis.
    assert sum(r.support for r in report.per_class) == report.n
    assert sum(r.predicted for r in report.per_class) == report.n
    assert report.macro_f1 is None or 0.0 <= report.macro_f1 <= 1.0


def test_main_reports_macro_f1_in_both_formats(capsys):
    assert main(["--dataset", "examples/calibration_sample.jsonl"]) == 0
    out = capsys.readouterr().out
    assert "Macro-F1" in out and "Per class" in out

    assert main(["--dataset", "examples/calibration_sample.jsonl", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert "macro_f1" in payload
    assert [r["label"] for r in payload["per_class"]] == ["unreliable", "reliable"]
