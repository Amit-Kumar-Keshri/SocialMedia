"""add content column to posts table

Revision ID: 8b8fba6a8cb1
Revises: bc8a877170ac
Create Date: 2022-10-20 18:57:21.544747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b8fba6a8cb1'
down_revision = 'bc8a877170ac'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable= False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
