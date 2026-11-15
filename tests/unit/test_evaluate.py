import json

import pytest

from cats.calibration.dataset import LabeledSample
from cats.calibration.evaluate import (
    BAND_ORDER,
    EvalReport,
    _bootstrap_indices,
    _class_metrics,
    _concordance_or_none,
    bootstrap_metrics,
    evaluate_dataset,
    is_unreliable,
    load_weights_file,
    main,
    paired_bootstrap_comparison,
    static_weights_for,
)
from cats.calibration.objective import predict_scores


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


# --------------------------------------------------------------------------- #
# Uncertainty (bootstrap) and paired comparison.
# Replicate counts and levels below are test fixtures, not recommendations.
# --------------------------------------------------------------------------- #


def _monotone_samples(labels):
    # Only coherence varies and equals the label, so predictions are strictly
    # monotone in the label under any non-negative weighting.
    return [
        LabeledSample(
            source_type="news",
            signals={"coherence": lbl, "volatility": 50, "silence": 50, "gaming": 50},
            label=lbl,
        )
        for lbl in labels
    ]


def _by_metric(rows):
    return {r.metric: r for r in rows}


def test_bootstrap_same_seed_same_interval():
    w = static_weights_for(["news", "social"])
    a = bootstrap_metrics(_samples(), w, replicates=50, level=0.8, seed=3)
    b = bootstrap_metrics(_samples(), w, replicates=50, level=0.8, seed=3)
    assert a == b


def test_bootstrap_lower_not_above_upper():
    rows = bootstrap_metrics(_samples(), static_weights_for(["news", "social"]), replicates=40, level=0.8, seed=1)
    assert [r.metric for r in rows] == ["concordance", "spearman", "recall_unreliable"]
    for r in rows:
        assert r.defined + r.excluded == 40
        if r.defined:
            assert r.lower is not None and r.upper is not None
            assert r.lower <= r.upper


def test_bootstrap_perfectly_ordered_concordance_is_one_in_every_defined_replicate():
    samples = _monotone_samples([10, 25, 45, 60, 75, 90])
    w = static_weights_for(["news"])
    preds = predict_scores(samples, w)
    labels = [s.label for s in samples]
    defined = 0
    for idx in _bootstrap_indices(len(samples), 60, seed=5):
        v = _concordance_or_none([preds[i] for i in idx], [labels[i] for i in idx])
        if v is not None:
            defined += 1
            assert v == pytest.approx(1.0)
    rows = _by_metric(bootstrap_metrics(samples, w, replicates=60, level=0.8, seed=5))
    assert rows["concordance"].defined == defined
    assert rows["concordance"].lower == rows["concordance"].upper == pytest.approx(1.0)


def test_concordance_undefined_replicate_is_excluded_not_zero():
    # A replicate with a single distinct label has no comparable pair.
    assert _concordance_or_none([1.0, 2.0], [50.0, 50.0]) is None
    samples = _monotone_samples([30, 70])
    rows = _by_metric(bootstrap_metrics(samples, static_weights_for(["news"]), replicates=40, level=0.8, seed=2))
    conc = rows["concordance"]
    # With 2 rows, about half the replicates draw the same row twice.
    assert conc.excluded > 0
    assert conc.defined + conc.excluded == 40
    assert conc.lower == pytest.approx(1.0)  # never pulled down by a fake 0


def test_paired_comparison_with_itself_is_exactly_zero():
    w = static_weights_for(["news", "social"])
    pc = paired_bootstrap_comparison(_samples(), w, w, replicates=30, level=0.8, seed=4)
    for d in pc.metrics:
        if d.point_difference is not None:
            assert d.point_difference == 0.0
        if d.defined:
            assert d.lower == 0.0 and d.upper == 0.0


def test_recall_without_unreliable_labels_is_excluded_in_every_replicate():
    samples = _monotone_samples([45, 55, 70, 85, 95])  # no label below 40
    rows = _by_metric(bootstrap_metrics(samples, static_weights_for(["news"]), replicates=25, level=0.8, seed=0))
    rec = rows["recall_unreliable"]
    assert rec.point is None
    assert rec.defined == 0 and rec.excluded == 25
    assert rec.lower is None and rec.upper is None


@pytest.mark.parametrize(
    "kwargs",
    [{"replicates": 0, "level": 0.9}, {"replicates": 10, "level": 0.0}, {"replicates": 10, "level": 1.0}],
)
def test_bootstrap_rejects_bad_parameters(kwargs):
    with pytest.raises(ValueError):
        bootstrap_metrics(_samples(), static_weights_for(["news", "social"]), seed=0, **kwargs)


_UNC_ARGS = ["--bootstrap-replicates", "30", "--bootstrap-level", "0.8", "--bootstrap-seed", "7"]


def test_main_with_uncertainty_prints_section(capsys):
    argv = ["--dataset", "examples/calibration_sample.jsonl", *_UNC_ARGS, "--compare-weights", "static"]
    assert main(argv) == 0
    out = capsys.readouterr().out
    assert "Uncertainty:" in out and "percentile bootstrap" in out
    assert "replicates      : 30" in out and "seed            : 7" in out and "level           : 0.8" in out
    assert "excluded" in out and "Paired comparison" in out
    # Same seed -> identical output on a second run.
    assert main(argv) == 0
    assert capsys.readouterr().out == out


def test_main_with_uncertainty_json_key(capsys):
    argv = ["--dataset", "examples/calibration_sample.jsonl", *_UNC_ARGS, "--compare-weights", "static", "--json"]
    assert main(argv) == 0
    payload = json.loads(capsys.readouterr().out)
    unc = payload["uncertainty"]
    assert unc["replicates"] == 30 and unc["seed"] == 7 and unc["level"] == 0.8
    assert "percentile" in unc["method"]
    assert [m["metric"] for m in unc["metrics"]] == ["concordance", "spearman", "recall_unreliable"]
    assert all("excluded" in m for m in unc["metrics"])
    # Static compared against static: every defined difference is exactly 0.
    for d in unc["paired_comparison"]["metrics"]:
        assert d["point_difference"] in (0.0, None)


def test_main_without_uncertainty_has_no_key(capsys):
    assert main(["--dataset", "examples/calibration_sample.jsonl", "--json"]) == 0
    assert "uncertainty" not in json.loads(capsys.readouterr().out)
    assert main(["--dataset", "examples/calibration_sample.jsonl"]) == 0
    assert "Uncertainty" not in capsys.readouterr().out


@pytest.mark.parametrize(
    "extra",
    [
        ["--bootstrap-replicates", "10"],
        ["--bootstrap-level", "0.9"],
        ["--bootstrap-seed", "1"],
        ["--compare-weights", "static"],
        ["--bootstrap-replicates", "10", "--bootstrap-level", "90"],
        ["--bootstrap-replicates", "0", "--bootstrap-level", "0.9"],
    ],
)
def test_main_uncertainty_requires_replicates_and_level(extra):
    with pytest.raises(SystemExit) as exc:
        main(["--dataset", "examples/calibration_sample.jsonl", *extra])
    assert exc.value.code == 2
