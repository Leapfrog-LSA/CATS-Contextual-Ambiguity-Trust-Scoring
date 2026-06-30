import json

from cats.calibration.dataset import LabeledSample
from cats.calibration.evaluate import evaluate_dataset, static_weights_for
from cats.calibration.report import main, render_declaration


def _report():
    samples = [
        LabeledSample(
            source_type="news",
            signals={"coherence": coh, "volatility": 30, "silence": 20, "gaming": 25},
            label=coh,
        )
        for coh in (20, 40, 60, 80, 95)
    ]
    return evaluate_dataset(samples, static_weights_for(["news"]), weights_source="static")


def test_render_declaration_contains_metrics_and_headings():
    md = render_declaration(_report(), dataset="holdout.jsonl", generated="2026-06-30 00:00:00Z")
    assert "Annex IV §6 / Art. 15" in md
    assert "Spearman rank correlation" in md
    assert "Per source type" in md
    assert "holdout.jsonl" in md
    # TODO provenance/sign-off must be preserved (not fabricated).
    assert "TODO (human / legal)" in md


def test_main_writes_markdown_file(tmp_path, capsys):
    ds = tmp_path / "holdout.jsonl"
    ds.write_text(
        "\n".join(
            json.dumps(
                {
                    "source_type": "news",
                    "signals": {"coherence": c, "volatility": 30, "silence": 20, "gaming": 25},
                    "label": c,
                }
            )
            for c in (20, 50, 90)
        ),
        encoding="utf-8",
    )
    out = tmp_path / "decl.md"
    rc = main(["--dataset", str(ds), "--out", str(out)])
    assert rc == 0
    assert out.exists() and "Accuracy Declaration" in out.read_text(encoding="utf-8")
    assert "Wrote accuracy declaration" in capsys.readouterr().out


def test_main_stdout_when_no_out(tmp_path, capsys):
    ds = tmp_path / "h.jsonl"
    ds.write_text(
        json.dumps(
            {
                "source_type": "news",
                "signals": {"coherence": 80, "volatility": 30, "silence": 20, "gaming": 25},
                "label": 80,
            }
        ),
        encoding="utf-8",
    )
    rc = main(["--dataset", str(ds)])
    assert rc == 0
    assert "Accuracy Declaration" in capsys.readouterr().out
