from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    cats_api_key: str
    cats_api_key_prev: Optional[str] = None

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

    environment: str = "production"
    log_level: str = "INFO"

    cors_origins: str = ""


settings = Settings()
