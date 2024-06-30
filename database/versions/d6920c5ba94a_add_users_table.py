"""add users table

Revision ID: d6920c5ba94a
Revises: 3e8a3f425443
Create Date: 2024-06-30 15:14:16.698745

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6920c5ba94a'
down_revision: Union[str, None] = '3e8a3f425443'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users',sa.Column('id', sa.Integer(), nullable=False),
                            sa.Column('username', sa.String(), nullable=False),
                            sa.Column('email', sa.String(), nullable=False),
                            sa.Column('password', sa.String(), nullable=False),
                            sa.Column('create_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_column('users')
    pass
