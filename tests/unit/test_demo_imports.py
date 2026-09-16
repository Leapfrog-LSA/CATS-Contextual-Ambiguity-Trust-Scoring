"""Minimal check that the Gradio demo (examples/demo/app.py) imports and builds.

The demo is not part of the normal cats package or test surface -- it's an
example deployed separately as a Hugging Face Space -- so these tests skip
outright (not fail) when gradio isn't installed, via pytest.importorskip.
"""

import importlib.util
from pathlib import Path

import pytest

_APP_PATH = Path(__file__).resolve().parents[2] / "examples" / "demo" / "app.py"


def _load_app_module(name: str):
    spec = importlib.util.spec_from_file_location(name, _APP_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_demo_app_imports_and_builds_blocks():
    pytest.importorskip("gradio")
    import gradio as gr

    module = _load_app_module("cats_demo_app_build")

    assert isinstance(module.demo, gr.Blocks)


def test_rate_limiter_blocks_after_threshold():
    pytest.importorskip("gradio")

    module = _load_app_module("cats_demo_app_rate")
    module._request_log.clear()

    for _ in range(module._RATE_LIMIT):
        assert module._rate_limited("test-session") is False
    assert module._rate_limited("test-session") is True


def test_score_source_reports_rate_limit_message(monkeypatch):
    pytest.importorskip("gradio")

    module = _load_app_module("cats_demo_app_score")
    module._request_log.clear()
    for _ in range(module._RATE_LIMIT):
        module._rate_limited("blocked-session")

    monkeypatch.setattr(module, "_rate_limited", lambda key: True)

    result = module.score_source("https://esempio.it", "default", request=None)

    assert "Rate limit" in result[-1]
