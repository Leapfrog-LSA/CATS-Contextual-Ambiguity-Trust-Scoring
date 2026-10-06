import hashlib
import hmac
from datetime import datetime, timezone
from typing import Awaitable, List, Optional, cast

import redis.asyncio as aioredis
import structlog
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from cats.core.config import settings

logger = structlog.get_logger()

_LUA_SLIDING_INCR = (
    "local key    = KEYS[1]\n"
    "local now    = tonumber(ARGV[1])\n"
    "local window = tonumber(ARGV[2])\n"
    "local limit  = tonumber(ARGV[3])\n"
    "local ttl    = tonumber(ARGV[4])\n"
    "redis.call('ZREMRANGEBYSCORE', key, 0, now - window)\n"
    "local count = redis.call('ZCARD', key)\n"
    "if count < limit then\n"
    "    redis.call('ZADD', key, now, now)\n"
    "    redis.call('EXPIRE', key, ttl)\n"
    "    return 1\n"
    "end\n"
    "return 0\n"
)

redis_client: Optional[aioredis.Redis] = None


async def init_redis() -> None:
    global redis_client
    redis_client = await aioredis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)


async def check_rate_limit(client_id: str) -> bool:
    now = datetime.now(timezone.utc).timestamp()
    w = settings.redis_rate_limit_window_seconds
    # redis encodes all ARGV as bulk strings on the wire; the Lua script reads
    # them back with tonumber(), so passing str() is equivalent and type-clean.
    raw = redis_client.eval(
        _LUA_SLIDING_INCR,
        1,
        f"ratelimit:{client_id}",
        str(now),
        str(w),
        str(settings.redis_rate_limit_max),
        str(w * 2),
    )
    return bool(await cast(Awaitable[int], raw))


def get_client_ip(request: Request) -> str:
    # X-Forwarded-For is only meaningful behind a proxy that sets it (the
    # bundled nginx does). When the app is exposed directly a client could
    # spoof it, so honour the header only when TRUST_PROXY_HEADERS is on.
    if settings.trust_proxy_headers:
        fwd = request.headers.get("X-Forwarded-For")
        if fwd:
            return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def rate_limit_id(api_key: str, request: Request) -> str:
    """Rate-limit bucket key: per API key (fair across tenants behind one NAT),
    falling back to client IP for malformed/empty credentials. The key is
    hashed so raw secrets never appear in Redis keys."""
    if api_key:
        return "key:" + hashlib.sha256(api_key.encode()).hexdigest()[:32]
    return "ip:" + get_client_ip(request)


def _key_tenant_map() -> dict:
    """Parse the optional CATS_API_KEYS "key:tenant" CSV into a dict."""
    raw = settings.api_keys
    out: dict = {}
    if raw:
        for pair in raw.split(","):
            pair = pair.strip()
            if not pair:
                continue
            key, _, tenant = pair.partition(":")
            key = key.strip()
            if key:
                out[key] = tenant.strip() or "default"
    return out


def verify_api_key(api_key: str) -> bool:
    candidates = [settings.cats_api_key]
    if settings.cats_api_key_prev:
        candidates.append(settings.cats_api_key_prev)
    candidates.extend(_key_tenant_map().keys())
    return any(hmac.compare_digest(api_key, c) for c in candidates)


# Threat model T7: a short key leaves the per-IP failed-auth limiter as the only
# barrier against guessing. 32 characters is what `secrets.token_urlsafe(24)`
# produces; the documented generator (`token_urlsafe(32)`) gives 43.
MIN_API_KEY_LENGTH = 32


def weak_api_keys(min_length: int = MIN_API_KEY_LENGTH) -> List[str]:
    """Where a configured API key is shorter than ``min_length``.

    Returns labels such as ``"CATS_API_KEY"`` or ``"CATS_API_KEYS (tenant
    acme)"``, never the key itself, so the result is safe to log.
    """
    weak = []
    if len(settings.cats_api_key) < min_length:
        weak.append("CATS_API_KEY")
    if settings.cats_api_key_prev and len(settings.cats_api_key_prev) < min_length:
        weak.append("CATS_API_KEY_PREV")
    for key, tenant in _key_tenant_map().items():
        if len(key) < min_length:
            weak.append(f"CATS_API_KEYS (tenant {tenant})")
    return weak


def check_api_key_strength() -> None:
    """Refuse to start in production with a short API key (threat model T7).

    Outside ``ENVIRONMENT=production`` (the default) a short key only logs a
    warning, so local development and the test suites keep their short keys.
    """
    weak = weak_api_keys()
    if not weak:
        return
    if settings.environment == "production":
        raise RuntimeError(
            f"Refusing to start: {', '.join(weak)} shorter than {MIN_API_KEY_LENGTH} characters. "
            'Generate a key with `python -c "import secrets; print(secrets.token_urlsafe(32))"`, '
            "or set ENVIRONMENT=development for local use."
        )
    logger.warning("api_key_weak", keys=weak, min_length=MIN_API_KEY_LENGTH, env=settings.environment)


def resolve_tenant(api_key: str) -> str:
    """Tenant bound to the API key server-side (never client-supplied)."""
    for key, tenant in _key_tenant_map().items():
        if hmac.compare_digest(api_key, key):
            return tenant
    return "default"


def get_tenant(request: Request) -> str:
    """Tenant resolved by APIKeyBearer for the current request."""
    return getattr(request.state, "tenant_id", "default")


class APIKeyBearer(HTTPBearer):
    async def __call__(self, request: Request) -> str:  # type: ignore[override]
        cred: HTTPAuthorizationCredentials = await super().__call__(request)
        if not verify_api_key(cred.credentials):
            # Failed attempts are rate-limited per client IP: the per-key
            # limiter below only ever runs for valid keys, so without this an
            # attacker would get unlimited guesses at the key space.
            if not await check_rate_limit("authfail:" + get_client_ip(request)):
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        if not await check_rate_limit(rate_limit_id(cred.credentials, request)):
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
        request.state.tenant_id = resolve_tenant(cred.credentials)
        return cred.credentials


api_key_bearer = APIKeyBearer()
