"""add forign key to post table

Revision ID: 6268108315c9
Revises: d6920c5ba94a
Create Date: 2024-06-30 15:27:37.729506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6268108315c9'
down_revision: Union[str, None] = 'd6920c5ba94a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users",
                          local_cols=['user_id'],
                          remote_cols=['id'],
                          ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'user_id')
    pass
