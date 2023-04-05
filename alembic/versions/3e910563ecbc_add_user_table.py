"""add user table

Revision ID: 3e910563ecbc
Revises: ccb62ee31924
Create Date: 2023-03-31 19:34:01.245811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e910563ecbc'
down_revision = 'ccb62ee31924'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'), #primary key
                    sa.UniqueConstraint('email') #no duplicate emails
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
