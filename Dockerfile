FROM python:3.11-slim AS base

RUN groupadd -r cats && useradd -r -g cats -d /app cats
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS runtime

COPY cats/ cats/
COPY alembic.ini .
COPY alembic/ alembic/
# Validated calibrated weights: docs recommend CATS_WEIGHTS_FILE=data/
# calibrated_weights.json. Without the file in the image, weight loading
# silently falls back to the unvalidated static table (only a log warning).
COPY data/calibrated_weights.json data/calibrated_weights.json

# NLTK_DATA must be a world-readable path: corpora are downloaded as root at
# build time but read by the non-root `cats` user at runtime.
ENV NLTK_DATA=/usr/local/share/nltk_data
RUN python -m spacy download it_core_news_lg && python -m textblob.download_corpora

USER cats
EXPOSE 8000

CMD ["uvicorn", "cats.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
