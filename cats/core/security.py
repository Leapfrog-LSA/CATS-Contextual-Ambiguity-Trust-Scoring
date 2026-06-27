import hmac
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import redis.asyncio as aioredis
import structlog
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

from cats.core.config import settings

logger = structlog.get_logger()

_JWT_PRIVATE_KEY: Optional[str] = None
_JWT_PUBLIC_KEY: Optional[str] = None


def init_jwt_keys() -> None:
    global _JWT_PRIVATE_KEY, _JWT_PUBLIC_KEY
    key_path = os.environ.get("JWT_PRIVATE_KEY_FILE")
    if key_path and os.path.isfile(key_path):
        with open(key_path) as f:
            _JWT_PRIVATE_KEY = f.read()
        from cryptography.hazmat.primitives.serialization import load_pem_private_key
        priv = load_pem_private_key(_JWT_PRIVATE_KEY.encode(), password=None)
        from cryptography.hazmat.primitives import serialization
        _JWT_PUBLIC_KEY = priv.public_key().public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()
        logger.info("jwt_keys_loaded", source="file")
        return

    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    _JWT_PRIVATE_KEY = priv.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode()
    _JWT_PUBLIC_KEY = priv.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    logger.warning("jwt_keys_generated", source="ephemeral",
                   hint="Set JWT_PRIVATE_KEY_FILE for persistent keys")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    payload = data.copy()
    payload['exp'] = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.jwt_access_token_expire_minutes)
    )
    return jwt.encode(payload, _JWT_PRIVATE_KEY, algorithm='RS256')


def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, _JWT_PUBLIC_KEY, algorithms=['RS256'])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')


_LUA_SLIDING_INCR = (
    'local key    = KEYS[1]\n'
    'local now    = tonumber(ARGV[1])\n'
    'local window = tonumber(ARGV[2])\n'
    'local limit  = tonumber(ARGV[3])\n'
    'local ttl    = tonumber(ARGV[4])\n'
    'redis.call(\'ZREMRANGEBYSCORE\', key, 0, now - window)\n'
    'local count = redis.call(\'ZCARD\', key)\n'
    'if count < limit then\n'
    '    redis.call(\'ZADD\', key, now, now)\n'
    '    redis.call(\'EXPIRE\', key, ttl)\n'
    '    return 1\n'
    'end\n'
    'return 0\n'
)

redis_client: Optional[aioredis.Redis] = None


async def init_redis() -> None:
    global redis_client
    redis_client = await aioredis.from_url(
        settings.redis_url, encoding='utf-8', decode_responses=True
    )


async def check_rate_limit(client_id: str) -> bool:
    now = datetime.now(timezone.utc).timestamp()
    w = settings.redis_rate_limit_window_seconds
    result = await redis_client.eval(
        _LUA_SLIDING_INCR, 1,
        f'ratelimit:{client_id}',
        now, w, settings.redis_rate_limit_max, w * 2,
    )
    return bool(result)


def get_client_ip(request: Request) -> str:
    fwd = request.headers.get('X-Forwarded-For')
    if fwd:
        return fwd.split(',')[0].strip()
    return request.client.host if request.client else 'unknown'


def verify_api_key(api_key: str) -> bool:
    if hmac.compare_digest(api_key, settings.cats_api_key):
        return True
    if settings.cats_api_key_prev and hmac.compare_digest(api_key, settings.cats_api_key_prev):
        return True
    return False


class APIKeyBearer(HTTPBearer):
    async def __call__(self, request: Request) -> str:
        cred: HTTPAuthorizationCredentials = await super().__call__(request)
        if not verify_api_key(cred.credentials):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')
        if not await check_rate_limit(get_client_ip(request)):
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail='Rate limit exceeded')
        return cred.credentials


api_key_bearer = APIKeyBearer()
