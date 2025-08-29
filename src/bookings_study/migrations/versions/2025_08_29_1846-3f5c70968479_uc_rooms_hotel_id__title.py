"""uc_rooms-hotel_id__title

Revision ID: 3f5c70968479
Revises: 3c294d3f1e62
Create Date: 2025-08-29 18:46:42.972138

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "3f5c70968479"
down_revision: Union[str, None] = "3c294d3f1e62"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uc_hotels-hotel_id__title", "rooms", ["hotel_id", "title"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uc_hotels-hotel_id__title", "rooms", type_="unique")
