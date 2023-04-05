"""add content column to post table

Revision ID: ccb62ee31924
Revises: 1ab4cdb0af1a
Create Date: 2023-03-31 19:25:07.455085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccb62ee31924'
down_revision = '1ab4cdb0af1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
