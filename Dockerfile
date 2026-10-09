FROM python:3.14-slim AS base

RUN groupadd -r cats && useradd -r -g cats -d /app cats
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS runtime

COPY cats/ cats/
COPY alembic.ini .
COPY alembic/ alembic/

# Calibrated production weights: without this file in the image, a
# CATS_WEIGHTS_FILE pointing at it logs a warning and the engine silently
# falls back to the static (unvalidated) weight estimates.
COPY data/calibrated_weights.json data/calibrated_weights.json

# NLTK_DATA must be a world-readable path: corpora are downloaded as root at
# build time but read by the non-root `cats` user at runtime.
ENV NLTK_DATA=/usr/local/share/nltk_data
RUN python -m spacy download it_core_news_lg && python -m textblob.download_corpora

# Worker processes. uvicorn reads WEB_CONCURRENCY as its --workers default.
# One worker uses at most ~1.5 cores (one serialised NLP thread per process),
# so more workers use more cores, at ~1.1 GB of RAM each for the spaCy model
# (docs/load_test_2026-09.md). docker-compose.yml raises it to 2.
ENV WEB_CONCURRENCY=1

# Prometheus multiprocess mode: every worker writes its metrics here and
# GET /metrics sums them (cats/core/metrics.py). The directory must exist
# before the app imports prometheus_client, and is emptied at each start so a
# new container does not inherit the counters of a previous run.
ENV PROMETHEUS_MULTIPROC_DIR=/tmp/cats-prometheus
RUN mkdir -p "$PROMETHEUS_MULTIPROC_DIR" && chown cats:cats "$PROMETHEUS_MULTIPROC_DIR"

USER cats
EXPOSE 8000

CMD ["sh", "-c", "rm -f \"$PROMETHEUS_MULTIPROC_DIR\"/*.db && exec uvicorn cats.api.main:app --host 0.0.0.0 --port 8000"]
