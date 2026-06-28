from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from cats.core.db import Base


def _now():
    return datetime.now(timezone.utc)  # D-01: timezone-aware everywhere


class TrustScore(Base):
    __tablename__ = "trust_scores"
    id = Column(Integer, primary_key=True)
    trace_id = Column(String(64), unique=True, nullable=False, index=True)
    source_id = Column(String(256), nullable=False, index=True)
    score = Column(Float, nullable=False)
    band = Column(String(32), nullable=False)
    signals = Column(JSONB, nullable=False)
    weights = Column(JSONB, nullable=False)
    context_data = Column("context_data", JSONB)
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)
    __table_args__ = (Index("idx_source_created", "source_id", "created_at"),)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    trace_id = Column(String(64), nullable=False, index=True)
    event_type = Column(String(64), nullable=False)
    encrypted_data = Column(Text, nullable=False)
    user_id = Column(String(256))
    ip_address = Column(String(64))
    timestamp = Column(DateTime(timezone=True), default=_now, nullable=False)
    __table_args__ = (Index("idx_trace_ts", "trace_id", "timestamp"),)


class Contest(Base):
    __tablename__ = "contests"
    id = Column(Integer, primary_key=True)
    trace_id = Column(String(64), nullable=False, index=True)
    reason = Column(Text, nullable=False)
    status = Column(String(32), default="pending", nullable=False)
    response = Column(Text)
    user_id = Column(String(256))
    created_at = Column(DateTime(timezone=True), default=_now, nullable=False)
    resolved_at = Column(DateTime(timezone=True))
