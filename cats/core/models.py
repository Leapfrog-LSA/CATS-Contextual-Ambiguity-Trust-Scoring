from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Float, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from cats.core.db import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)  # D-01: timezone-aware everywhere


class TrustScore(Base):
    __tablename__ = "trust_scores"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(128), nullable=False, default="default", index=True)
    trace_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    source_id: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    band: Mapped[str] = mapped_column(String(32), nullable=False)
    signals: Mapped[dict] = mapped_column(JSONB, nullable=False)
    weights: Mapped[dict] = mapped_column(JSONB, nullable=False)
    context_data: Mapped[Optional[dict]] = mapped_column("context_data", JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
    __table_args__ = (Index("idx_source_created", "source_id", "created_at"),)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(128), nullable=False, default="default", index=True)
    trace_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(64), nullable=False)
    encrypted_data: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[Optional[str]] = mapped_column(String(256))
    ip_address: Mapped[Optional[str]] = mapped_column(String(64))
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
    __table_args__ = (Index("idx_trace_ts", "trace_id", "timestamp"),)


class Contest(Base):
    __tablename__ = "contests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(128), nullable=False, default="default", index=True)
    trace_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="pending", nullable=False)
    response: Mapped[Optional[str]] = mapped_column(Text)
    user_id: Mapped[Optional[str]] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, nullable=False)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
