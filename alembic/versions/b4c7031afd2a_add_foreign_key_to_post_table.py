"""add foreign key to post table

Revision ID: b4c7031afd2a
Revises: 3e910563ecbc
Create Date: 2023-04-05 10:24:09.977095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4c7031afd2a'
down_revision = '3e910563ecbc'
branch_labels = None
depends_on = None


#alembic revision -m "add last few columns to post table" how to create revisions for upgrade and downgrade
#alembic upgrade/downgrade {revision_number}: to upgrade or downgrade
#alembic current : to check the current revision that you are on
#alembic heads: to check the latest revision that you have..
#alembic upgrade head: to migrate to the latest revision
#alembic downgrade +1, -1 and so on...to move up one step or down by another step..

def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users', 
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraints('posusers_fk', table_name = "posts")
    op.drop_column('posts', 'owner_id')
    pass
