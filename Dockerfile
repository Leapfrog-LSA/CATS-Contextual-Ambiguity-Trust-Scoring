FROM python:3.11-slim AS base

RUN groupadd -r cats && useradd -r -g cats -d /app cats
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS runtime

COPY cats/ cats/
COPY alembic.ini .
COPY alembic/ alembic/

RUN python -m spacy download it_core_news_lg

USER cats
EXPOSE 8000

CMD ["uvicorn", "cats.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
