"""remove_username

Revision ID: 7e89e630a1f2
Revises: 586a6f4cca8c
Create Date: 2025-08-29 12:56:49.426546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e89e630a1f2'
down_revision: Union[str, None] = '586a6f4cca8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(op.f('users_username_key'), 'users', type_='unique')
    op.drop_column('users', 'username')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column('users', sa.Column('username', sa.VARCHAR(length=200), autoincrement=False, nullable=False))
    op.create_unique_constraint(op.f('users_username_key'), 'users', ['username'], postgresql_nulls_not_distinct=False)
