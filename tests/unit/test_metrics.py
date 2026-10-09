"""Tests for cats.core.metrics.render_latest (single and multi-worker)."""

import os
import subprocess
import sys

from cats.core.metrics import EVALUATIONS, render_latest

_INC = "from cats.core.metrics import EVALUATIONS; EVALUATIONS.labels('high').inc({n})"
_RENDER = "import sys; from cats.core.metrics import render_latest; sys.stdout.write(render_latest().decode())"


def _run(code: str, multiproc_dir: str) -> str:
    # prometheus_client reads PROMETHEUS_MULTIPROC_DIR when it is imported, so
    # each "worker" must be a fresh interpreter started with the variable set.
    env = {**os.environ, "PROMETHEUS_MULTIPROC_DIR": multiproc_dir}
    out = subprocess.run([sys.executable, "-c", code], env=env, capture_output=True, text=True, check=True)
    return out.stdout


def test_single_process_uses_default_registry(monkeypatch):
    monkeypatch.delenv("PROMETHEUS_MULTIPROC_DIR", raising=False)
    EVALUATIONS.labels("low").inc()
    text = render_latest().decode()
    assert "cats_evaluations_total" in text
    # The default registry also carries the process collector.
    assert "process_" in text or "python_info" in text


def test_multiprocess_mode_sums_every_worker(tmp_path):
    _run(_INC.format(n=2), str(tmp_path))
    _run(_INC.format(n=3), str(tmp_path))
    text = _run(_RENDER, str(tmp_path))
    assert 'cats_evaluations_total{band="high"} 5.0' in text
