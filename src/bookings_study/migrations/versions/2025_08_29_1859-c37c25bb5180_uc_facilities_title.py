"""uc_facilities-title

Revision ID: c37c25bb5180
Revises: 3f5c70968479
Create Date: 2025-08-29 18:59:18.889720

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c37c25bb5180"
down_revision: Union[str, None] = "3f5c70968479"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint("uc_facilities-title", "facilities", ["title"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uc_facilities-title", "facilities", type_="unique")
