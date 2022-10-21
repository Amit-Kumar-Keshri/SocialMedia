"""add last few columns to posts table

Revision ID: 2aea45dcc143
Revises: b2fcfcb31093
Create Date: 2022-10-20 21:07:21.921557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2aea45dcc143'
down_revision = 'b2fcfcb31093'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default = 'TRUE')),  
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable = False, server_default =sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
