"""Track the aggregation-engine version on trust_scores

The v1.3.0 polarity fix changed scoring semantics: scores produced by the
pre-1.3 engine are not comparable with current ones, and /explain must not
silently re-decompose old rows with new semantics. Rows created before this
column existed stay NULL (= pre-1.3 engine).

Revision ID: 003
Revises: 002
Create Date: 2026-07-05
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("trust_scores", sa.Column("engine_version", sa.String(16), nullable=True))


def downgrade() -> None:
    op.drop_column("trust_scores", "engine_version")
