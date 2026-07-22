"""add brew analyses

Revision ID: ce24ce9a070d
Revises: 3fb76fbc3a27
Create Date: 2026-07-21 15:24:36.741733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce24ce9a070d'
down_revision: Union[str, Sequence[str], None] = '3fb76fbc3a27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "brew_analyses",
        sa.Column("id", sa.Integer(), nullable=False),

        sa.Column(
            "previous_brew_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "current_brew_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "issue_detected",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "adjustment_made",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "result",
            sa.String(),
            nullable=True
        ),

        sa.Column(
            "recommendation",
            sa.String(),
            nullable=True
        ),

        sa.PrimaryKeyConstraint("id"),

        sa.ForeignKeyConstraint(
            ["previous_brew_id"],
            ["brews.id"]
        ),

        sa.ForeignKeyConstraint(
            ["current_brew_id"],
            ["brews.id"]
        ),
    )


def downgrade() -> None:
    op.drop_table("brew_analyses")
