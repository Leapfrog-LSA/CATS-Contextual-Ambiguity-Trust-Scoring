"""Add tenant_id for row-level multi-tenancy

Revision ID: 002
Revises: 001
Create Date: 2026-06-28
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_TABLES = ("trust_scores", "audit_logs", "contests")


def upgrade() -> None:
    for table in _TABLES:
        # server_default backfills existing rows to the "default" tenant.
        op.add_column(table, sa.Column("tenant_id", sa.String(128), nullable=False, server_default="default"))
        op.create_index(f"ix_{table}_tenant_id", table, ["tenant_id"])


def downgrade() -> None:
    for table in _TABLES:
        op.drop_index(f"ix_{table}_tenant_id", table_name=table)
        op.drop_column(table, "tenant_id")
