"""Add indexes on expenses.date and expenses.category

Revision ID: 0003
Revises: 0002
Create Date: 2026-04-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Speeds up year-based filtering (func.extract("year", date) benefits from
    # an index on the column itself for range scans on large datasets).
    op.create_index("ix_expenses_date", "expenses", ["date"])
    # Speeds up category filter, which is the most common non-date filter.
    op.create_index("ix_expenses_category", "expenses", ["category"])


def downgrade() -> None:
    op.drop_index("ix_expenses_category", table_name="expenses")
    op.drop_index("ix_expenses_date", table_name="expenses")
