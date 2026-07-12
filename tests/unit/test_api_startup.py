import os

os.environ.setdefault("CATS_API_KEY", "test-key")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTAwMzI=")

from cats.api import main  # noqa: E402


class TestDegradedNlpStartup:
    """A missing spaCy model must degrade the API, not block startup (WP 4.1)."""

    def test_missing_model_does_not_block_startup(self, monkeypatch):
        def boom(model_name):
            raise OSError(f"Can't find model '{model_name}'")

        monkeypatch.setattr(main, "init_nlp", boom)
        main.init_nlp_or_degrade()  # must not raise

    def test_model_loaded_when_available(self, monkeypatch):
        loaded = {}
        monkeypatch.setattr(main, "init_nlp", lambda m: loaded.setdefault("model", m))
        main.init_nlp_or_degrade()
        assert loaded["model"] == main.settings.spacy_model
