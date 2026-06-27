"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-03-06
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "trust_scores",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("trace_id", sa.String(64), unique=True, nullable=False),
        sa.Column("source_id", sa.String(256), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("band", sa.String(32), nullable=False),
        sa.Column("signals", postgresql.JSONB(), nullable=False),
        sa.Column("weights", postgresql.JSONB(), nullable=False),
        sa.Column("context_data", postgresql.JSONB()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_trust_scores_trace_id", "trust_scores", ["trace_id"])
    op.create_index("ix_trust_scores_source_id", "trust_scores", ["source_id"])
    op.create_index("idx_source_created", "trust_scores", ["source_id", "created_at"])

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("trace_id", sa.String(64), nullable=False),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("encrypted_data", sa.Text(), nullable=False),
        sa.Column("user_id", sa.String(256)),
        sa.Column("ip_address", sa.String(64)),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_audit_logs_trace_id", "audit_logs", ["trace_id"])
    op.create_index("idx_trace_ts", "audit_logs", ["trace_id", "timestamp"])

    op.create_table(
        "contests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("trace_id", sa.String(64), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.Column("response", sa.Text()),
        sa.Column("user_id", sa.String(256)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("resolved_at", sa.DateTime(timezone=True)),
    )
    op.create_index("ix_contests_trace_id", "contests", ["trace_id"])


def downgrade() -> None:
    op.drop_table("contests")
    op.drop_table("audit_logs")
    op.drop_table("trust_scores")
