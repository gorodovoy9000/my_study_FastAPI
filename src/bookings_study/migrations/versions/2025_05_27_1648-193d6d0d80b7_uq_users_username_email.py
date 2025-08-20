"""uq_users_username_email

Revision ID: 193d6d0d80b7
Revises: 662a817f44a7
Create Date: 2025-05-27 16:48:40.634322

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "193d6d0d80b7"
down_revision: Union[str, None] = "662a817f44a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])
    op.create_unique_constraint(None, "users", ["username"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint(None, "users", type_="unique")
