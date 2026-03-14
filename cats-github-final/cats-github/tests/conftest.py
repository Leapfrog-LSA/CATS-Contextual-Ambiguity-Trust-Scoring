"""
Shared pytest fixtures for CATS test suite.
"""
import os
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch

# ── env defaults before any import ────────────────────────────────────────────
os.environ.setdefault("CATS_API_KEY", "test-api-key-for-ci")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://cats:cats@localhost:5432/cats_test")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/1")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdC1rZXktMzItYnl0ZXMtZm9yLWNpLXRlc3Rpbmc=")
os.environ.setdefault("ENVIRONMENT", "test")


@pytest.fixture(autouse=True)
def mock_spacy_nlp():
    """Stub spaCy so unit tests run without model installed."""
    mock_doc = MagicMock()
    mock_doc.ents = []
    mock_nlp = MagicMock(return_value=mock_doc)

    with patch("cats.signals.coherence.nlp", mock_nlp):
        yield mock_nlp


@pytest.fixture
def sample_messages():
    """Minimal valid message list."""
    from cats.signals.types import Message
    return [
        Message("2026-01-01T10:00:00Z", "Il governo annuncia nuove misure economiche."),
        Message("2026-01-01T12:00:00Z", "Protesta dei lavoratori in piazza oggi."),
        Message("2026-01-01T14:00:00Z", "Il parlamento discute la legge di bilancio."),
    ]


@pytest.fixture
def default_weights():
    from cats.scoring.weights import DEFAULT_WEIGHTS
    return DEFAULT_WEIGHTS.copy()
