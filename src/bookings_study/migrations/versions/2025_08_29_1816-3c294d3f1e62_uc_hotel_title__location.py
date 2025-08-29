"""uc_hotel-title__location

Revision ID: 3c294d3f1e62
Revises: 7e89e630a1f2
Create Date: 2025-08-29 18:16:44.610923

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "3c294d3f1e62"
down_revision: Union[str, None] = "7e89e630a1f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
        "uc_hotels-title__location", "hotels", ["title", "location"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uc_hotels-title__location", "hotels", type_="unique")
