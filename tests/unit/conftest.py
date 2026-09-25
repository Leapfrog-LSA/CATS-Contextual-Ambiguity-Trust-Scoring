"""Unit-test defaults for the settings ``cats.core.config.Settings`` requires.

``Settings`` has no defaults for these four variables, and several unit modules
reach it at import time (directly, or through ``cats.signals.sentiment`` and
``cats.calibration.build_dataset``). This conftest is loaded before any module
under ``tests/unit/`` is imported, so every module collects on its own
(``pytest tests/unit/test_signals.py``), not only when an earlier module in the
same run happened to set them.

``setdefault``: exported values (the CI ``test`` job's) still win. The values
match the ones the unit modules already set for themselves. The file lives in
``tests/unit/`` and not in ``tests/``, because ``tests/integration/test_api.py``
sets its own ``DATABASE_URL``, pointing at a real test database.
"""

import os

os.environ.setdefault("CATS_API_KEY", "test-key")
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://x:x@localhost/x")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("AUDIT_ENCRYPTION_KEY", "dGVzdGtleXRlc3RrZXl0ZXN0a2V5dGVzdGtleTAwMzI=")
