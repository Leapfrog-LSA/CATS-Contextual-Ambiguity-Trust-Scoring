# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder
WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt && \
    /install/bin/python -m spacy download it_core_news_lg --target /install/lib/python3.11/site-packages

# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime
WORKDIR /app

# Non-root user for security
RUN addgroup --system cats && adduser --system --ingroup cats cats

COPY --from=builder /install /usr/local
COPY --chown=cats:cats cats/ ./cats/
COPY --chown=cats:cats alembic.ini .
COPY --chown=cats:cats alembic/ ./alembic/

USER cats
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "cats.api.main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "1", "--loop", "uvloop", "--log-level", "info"]
