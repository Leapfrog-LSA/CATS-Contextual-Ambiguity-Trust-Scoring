"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-03-06
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "trust_scores",
        sa.Column("id",         sa.Integer(), nullable=False),
        sa.Column("trace_id",   sa.String(64),  nullable=False),
        sa.Column("source_id",  sa.String(256), nullable=False),
        sa.Column("score",      sa.Float(),     nullable=False),
        sa.Column("band",       sa.String(32),  nullable=False),
        sa.Column("signals",    postgresql.JSONB(), nullable=False),
        sa.Column("weights",    postgresql.JSONB(), nullable=False),
        sa.Column("metadata",   postgresql.JSONB()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("trace_id"),
    )
    op.create_index("idx_source_created", "trust_scores", ["source_id", "created_at"])

    op.create_table(
        "audit_logs",
        sa.Column("id",             sa.Integer(), nullable=False),
        sa.Column("trace_id",       sa.String(64),  nullable=False),
        sa.Column("event_type",     sa.String(64),  nullable=False),
        sa.Column("encrypted_data", sa.Text(),      nullable=False),
        sa.Column("user_id",        sa.String(256)),
        sa.Column("ip_address",     sa.String(64)),
        sa.Column("timestamp",      sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_trace_ts", "audit_logs", ["trace_id", "timestamp"])

    op.create_table(
        "contests",
        sa.Column("id",          sa.Integer(), nullable=False),
        sa.Column("trace_id",    sa.String(64), nullable=False),
        sa.Column("reason",      sa.Text(),     nullable=False),
        sa.Column("status",      sa.String(32), nullable=False, server_default="pending"),
        sa.Column("response",    sa.Text()),
        sa.Column("user_id",     sa.String(256)),
        sa.Column("created_at",  sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contests_trace_id"), "contests", ["trace_id"])


def downgrade() -> None:
    op.drop_table("contests")
    op.drop_index("idx_trace_ts", table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_index("idx_source_created", table_name="trust_scores")
    op.drop_table("trust_scores")
