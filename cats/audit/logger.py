import base64
import json
import os
from datetime import datetime, timezone, timedelta
from typing import Optional

import redis.asyncio as aioredis
import structlog
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cats.core.config import settings
from cats.core.models import AuditLog, Contest

logger = structlog.get_logger()

_gcm: Optional[AESGCM] = None


def _get_gcm() -> AESGCM:
    global _gcm
    if _gcm is None:
        key = base64.b64decode(settings.audit_encryption_key)
        if len(key) != 32:
            raise ValueError("AUDIT_ENCRYPTION_KEY must be exactly 32 bytes (256-bit) base64-encoded")
        _gcm = AESGCM(key)
    return _gcm


def _encrypt(data: dict) -> str:
    nonce = os.urandom(12)
    ct = _get_gcm().encrypt(nonce, json.dumps(data).encode(), None)
    return base64.b64encode(nonce + ct).decode()


def _decrypt(blob: str) -> dict:
    raw = base64.b64decode(blob)
    return json.loads(_get_gcm().decrypt(raw[:12], raw[12:], None).decode())


async def log_evaluation(
    db: AsyncSession, trace_id: str, data: dict,
    user_id: Optional[str] = None, ip: Optional[str] = None,
) -> None:
    db.add(AuditLog(
        trace_id=trace_id, event_type="evaluation",
        encrypted_data=_encrypt(data), user_id=user_id,
        ip_address=ip, timestamp=datetime.now(timezone.utc),
    ))
    await db.flush()


async def log_contest(
    db: AsyncSession, trace_id: str, reason: str,
    user_id: Optional[str] = None,
) -> int:
    c = Contest(
        trace_id=trace_id, reason=reason, status="pending",
        user_id=user_id, created_at=datetime.now(timezone.utc),
    )
    db.add(c)
    await db.commit()
    await db.refresh(c)
    return c.id


async def get_audit_log(db: AsyncSession, trace_id: str) -> Optional[dict]:
    r = await db.execute(
        select(AuditLog).where(AuditLog.trace_id == trace_id)
        .order_by(AuditLog.timestamp.desc())
    )
    a = r.scalars().first()
    if not a:
        return None
    return {
        "trace_id": a.trace_id,
        "event_type": a.event_type,
        "data": _decrypt(a.encrypted_data),
        "timestamp": a.timestamp.isoformat(),
    }


_redis: Optional[aioredis.Redis] = None


async def init_redis_logger(redis_url: str) -> None:
    global _redis
    _redis = await aioredis.from_url(redis_url, decode_responses=True)


async def purge_expired_audits(db: AsyncSession) -> None:
    acquired = await _redis.set("cats:purge_lock", "1", nx=True, ex=300)
    if not acquired:
        logger.info("purge_skipped", reason="lock_held")
        return
    try:
        cutoff = datetime.now(timezone.utc) - timedelta(days=settings.audit_retention_days)
        res = await db.execute(select(AuditLog).where(AuditLog.timestamp < cutoff))
        old = res.scalars().all()
        for row in old:
            await db.delete(row)
        await db.commit()
        logger.info("purge_done", deleted=len(old))
    finally:
        await _redis.delete("cats:purge_lock")
