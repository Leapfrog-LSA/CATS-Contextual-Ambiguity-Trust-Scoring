from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # S-02: dual API-key rotation
    cats_api_key: str
    cats_api_key_prev: Optional[str] = None

    jwt_secret_key: str
    jwt_algorithm: str = "RS256"
    jwt_access_token_expire_minutes: int = 30

    # I-02: parametrized pool
    database_url: str
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_timeout: int = 30
    db_pool_recycle: int = 3600
    db_pool_pre_ping: bool = True

    # I-01: validator TTL = 2x rate-limit window
    redis_url: str
    redis_rate_limit_max: int = 30
    redis_rate_limit_window_seconds: int = 60
    redis_validator_ttl_seconds: int = 120   # 2 x window

    audit_encryption_key: str
    audit_retention_days: int = 90

    # N-02: gaming min-tokens guard
    spacy_model: str = "it_core_news_lg"
    nlp_gaming_min_tokens: int = 10

    environment: str = "production"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
