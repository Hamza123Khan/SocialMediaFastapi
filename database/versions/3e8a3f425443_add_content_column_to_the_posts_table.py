"""add content column to the posts table

Revision ID: 3e8a3f425443
Revises: e89cb774641c
Create Date: 2024-06-30 15:07:07.209853

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e8a3f425443'
down_revision: Union[str, None] = 'e89cb774641c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('Content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','Content')
    pass
