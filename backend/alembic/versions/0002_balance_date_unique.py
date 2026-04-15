"""Add unique constraint on account_balance.as_of_date

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_account_balance_as_of_date",
        "account_balance",
        ["as_of_date"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_account_balance_as_of_date",
        "account_balance",
        type_="unique",
    )
