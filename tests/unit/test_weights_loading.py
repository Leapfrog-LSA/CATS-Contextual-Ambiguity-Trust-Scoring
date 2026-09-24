"""Calibrated-weights loading in ``cats.scoring.weights``.

``_calibrated_table`` is what makes ``CATS_WEIGHTS_FILE`` (the shipped
``data/calibrated_weights.json``) take effect. Every failure mode must fall back
to the static WP 4.1 estimates instead of crashing a request.
"""

import json
import os

os.environ.setdefault("CATS_API_KEY", "test-key")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTAwMzI=")

import pytest  # noqa: E402

import cats.scoring.weights as weights  # noqa: E402
from cats.core.config import settings  # noqa: E402

NEWS = {"coherence": 0.410036, "volatility": 0.041765, "silence": 0.542548, "gaming": 0.005651}
DEFAULT = {"coherence": 0.129348, "volatility": 0.340519, "silence": 0.404427, "gaming": 0.125707}


@pytest.fixture
def weights_file(monkeypatch):
    """Point settings.weights_file at a path and reset the lru_cache around the test."""

    def _set(path):
        monkeypatch.setattr(settings, "weights_file", str(path) if path is not None else None)
        weights._calibrated_table.cache_clear()

    yield _set
    weights._calibrated_table.cache_clear()


def _write(tmp_path, payload) -> str:
    p = tmp_path / "calibrated_weights.json"
    p.write_text(payload if isinstance(payload, str) else json.dumps(payload), encoding="utf-8")
    return str(p)


def test_no_weights_file_uses_static_estimates(weights_file):
    weights_file(None)
    assert weights._calibrated_table() == {}
    assert weights.get_dynamic_weights({"source_type": "news"}) == weights._STATIC_WEIGHTS["news"]


def test_calibrated_file_with_weights_key_is_loaded_and_normalised(tmp_path, weights_file):
    # Same shape as data/calibrated_weights.json: metadata + a "weights" table.
    weights_file(_write(tmp_path, {"metric": "spearman", "weights": {"news": NEWS, "default": DEFAULT}}))
    table = weights._calibrated_table()
    assert set(table) == {"news", "default"}
    for group in table.values():
        assert abs(sum(group.values()) - 1.0) < 1e-9

    news = weights.get_dynamic_weights({"source_type": "news"})
    assert news == pytest.approx(NEWS, rel=1e-5)
    # "blog" maps to the "default" group, which is calibrated too.
    assert weights.get_dynamic_weights({"source_type": "blog"}) == pytest.approx(DEFAULT, rel=1e-5)


def test_bare_table_without_weights_key_is_accepted(tmp_path, weights_file):
    weights_file(_write(tmp_path, {"news": NEWS}))
    assert weights.get_dynamic_weights({"source_type": "news"}) == pytest.approx(NEWS, rel=1e-5)


def test_group_missing_from_calibrated_file_falls_back_to_static(tmp_path, weights_file):
    weights_file(_write(tmp_path, {"weights": {"news": NEWS}}))
    assert weights.get_dynamic_weights({"source_type": "social"}) == weights._STATIC_WEIGHTS["social"]


def test_returned_weights_are_a_copy(tmp_path, weights_file):
    weights_file(_write(tmp_path, {"weights": {"news": NEWS}}))
    first = weights.get_dynamic_weights({"source_type": "news"})
    first["coherence"] = 99.0
    assert weights.get_dynamic_weights({"source_type": "news"})["coherence"] == pytest.approx(NEWS["coherence"])
    static = weights.get_dynamic_weights({"source_type": "social"})
    static["gaming"] = 99.0
    assert weights._STATIC_WEIGHTS["social"]["gaming"] == 0.25


def test_missing_file_falls_back_to_static(tmp_path, weights_file):
    weights_file(tmp_path / "does_not_exist.json")
    assert weights._calibrated_table() == {}
    assert weights.get_dynamic_weights({"source_type": "news"}) == weights._STATIC_WEIGHTS["news"]


@pytest.mark.parametrize(
    "payload",
    [
        "{not json",  # malformed JSON (json.JSONDecodeError is a ValueError)
        {"weights": {"news": {"coherence": 0.5, "volatility": 0.9}}},  # sums to 1.4
        {"weights": {"news": {"coherence": "high"}}},  # non-numeric weight
    ],
)
def test_invalid_file_falls_back_to_static(tmp_path, weights_file, payload):
    weights_file(_write(tmp_path, payload))
    assert weights._calibrated_table() == {}
    assert weights.get_dynamic_weights({"source_type": "news"}) == weights._STATIC_WEIGHTS["news"]


@pytest.mark.parametrize(
    "payload",
    [
        [1, 2],  # top level is not a mapping
        {"weights": [1]},  # weights table is not a mapping
        {"weights": {"news": None}},  # group is not a mapping
        {"weights": {"news": [0.5, 0.5]}},  # group is a list
    ],
)
def test_wrongly_shaped_file_currently_raises(tmp_path, weights_file, payload):
    # KNOWN GAP, pinned on purpose: the docstring promises a static fallback for
    # invalid contents, but a structurally wrong file raises AttributeError,
    # which the loader does not catch (it catches ValueError/KeyError/TypeError).
    # lru_cache does not cache exceptions, so every evaluation would fail rather
    # than fall back. cats/scoring/weights.py is maintainer-gated (CLAUDE.md), so
    # the fix is left to a deliberate change; when it lands, move these payloads
    # into test_invalid_file_falls_back_to_static above.
    weights_file(_write(tmp_path, payload))
    with pytest.raises(AttributeError):
        weights.get_dynamic_weights({"source_type": "news"})


def test_unavailable_settings_fall_back_to_static(monkeypatch, weights_file):
    # _calibrated_table tolerates tooling/test contexts where settings can't be read.
    class _Broken:
        def __getattr__(self, name):
            raise RuntimeError("settings unavailable")

    import cats.core.config as config

    weights_file(None)
    monkeypatch.setattr(config, "settings", _Broken())
    weights._calibrated_table.cache_clear()
    assert weights._calibrated_table() == {}
