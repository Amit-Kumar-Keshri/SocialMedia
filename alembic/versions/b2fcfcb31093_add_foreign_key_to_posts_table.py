"""add foreign key to posts table

Revision ID: b2fcfcb31093
Revises: 03f78be54b6b
Create Date: 2022-10-20 19:35:26.616096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2fcfcb31093'
down_revision = '03f78be54b6b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # added a owner_id column for foreign key
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable= False))
    # setup foreign key code
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
