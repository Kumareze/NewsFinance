"""Add 'neutral' to sentiment check constraint

Revision ID: 8f3b2c1a4d5e
Revises: 6e0ccf8e9180
Create Date: 2026-07-25 03:57:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8f3b2c1a4d5e'
down_revision: Union[str, None] = '6e0ccf8e9180'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the old constraint and add updated one including 'neutral'
    op.execute(
        "ALTER TABLE news DROP CONSTRAINT IF EXISTS chk_news_sentiment"
    )
    op.create_check_constraint(
        "chk_news_sentiment",
        "news",
        "sentiment IN ('positive', 'negative', 'neutral')"
    )


def downgrade() -> None:
    # Revert back to original constraint
    op.execute(
        "ALTER TABLE news DROP CONSTRAINT IF EXISTS chk_news_sentiment"
    )
    op.create_check_constraint(
        "chk_news_sentiment",
        "news",
        "sentiment IN ('positive', 'negative')"
    )