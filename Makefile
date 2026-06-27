.PHONY: install dev-install nlp-download test test-unit test-integration lint format \
        docker-up docker-down docker-build db-migrate db-revision clean help

## ── Setup ─────────────────────────────────────────────────────────────
install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements-dev.txt
	pre-commit install

nlp-download:
	python -m spacy download it_core_news_lg
	python -m textblob.download_corpora

## ── Tests ─────────────────────────────────────────────────────────────
test:
	pytest tests/ -v --cov=cats --cov-report=term-missing --cov-report=html

test-unit:
	pytest tests/unit/ -v --tb=short

test-integration:
	pytest tests/integration/ -v --tb=short

## ── Code quality ──────────────────────────────────────────────────────
lint:
	black --check cats/ tests/
	isort --check-only cats/ tests/
	flake8 cats/ tests/ --max-line-length=120 --extend-ignore=E203,W503
	mypy cats/ --ignore-missing-imports --no-strict-optional

format:
	black cats/ tests/
	isort cats/ tests/

## ── Docker ────────────────────────────────────────────────────────────
docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f app

## ── Database ──────────────────────────────────────────────────────────
db-migrate:
	alembic upgrade head

db-revision:
	@read -p "Migration message: " msg; alembic revision --autogenerate -m "$$msg"

db-downgrade:
	alembic downgrade -1

## ── Utilities ─────────────────────────────────────────────────────────
generate-key:
	@python -c "import secrets, base64; print(base64.b64encode(secrets.token_bytes(32)).decode())"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache dist build *.egg-info

help:
	@grep -E '^[a-zA-Z_-]+:' Makefile | awk -F: '{print $$1}' | column
