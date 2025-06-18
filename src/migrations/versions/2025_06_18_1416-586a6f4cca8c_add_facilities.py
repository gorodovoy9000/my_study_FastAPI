"""add_facilities

Revision ID: 586a6f4cca8c
Revises: c818c12ec10f
Create Date: 2025-06-18 14:16:50.588667

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "586a6f4cca8c"
down_revision: Union[str, None] = "c818c12ec10f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "facilities_rooms_at",
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["facility_id"], ["facilities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("facility_id", "room_id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("facilities_rooms_at")
    op.drop_table("facilities")
