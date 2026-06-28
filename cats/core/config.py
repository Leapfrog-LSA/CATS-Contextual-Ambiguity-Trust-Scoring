from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    cats_api_key: str
    cats_api_key_prev: Optional[str] = None

    # Optional multi-tenant API keys: CSV of "key:tenant" pairs. Keys not listed
    # here (e.g. cats_api_key / cats_api_key_prev) resolve to the "default" tenant.
    api_keys: Optional[str] = None

    jwt_access_token_expire_minutes: int = 30

    database_url: str
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_timeout: int = 30
    db_pool_recycle: int = 3600
    db_pool_pre_ping: bool = True

    redis_url: str
    redis_rate_limit_max: int = 30
    redis_rate_limit_window_seconds: int = 60
    redis_validator_ttl_seconds: int = 120

    audit_encryption_key: str
    audit_retention_days: int = 90

    spacy_model: str = "it_core_news_lg"
    nlp_gaming_min_tokens: int = 10

    # Sentiment backend for the volatility signal: "textblob" (default, light)
    # or "bert" (requires requirements-bert.txt; falls back to textblob if the
    # transformers model is unavailable).
    sentiment_backend: str = "textblob"
    sentiment_model: str = "neuraly/bert-base-italian-cased-sentiment"

    # Coherence backend: "ner" (default, spaCy NER + Jaccard) or "sbert"
    # (requires requirements-sbert.txt; falls back to "ner" if the
    # sentence-transformers model is unavailable).
    coherence_backend: str = "ner"
    coherence_model: str = "paraphrase-multilingual-MiniLM-L12-v2"

    # Optional path to a calibrated weights file (see cats.calibration);
    # falls back to the static per-source-type estimates when unset.
    weights_file: Optional[str] = None

    environment: str = "production"
    log_level: str = "INFO"

    cors_origins: str = ""


settings = Settings()  # type: ignore[call-arg]  # values populated from env / .env
