"""add a column

Revision ID: 0c861e0d233d
Revises: f5cd35ea6443
Create Date: 2023-01-29 16:24:46.177157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c861e0d233d'
down_revision = 'f5cd35ea6443'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('items', sa.Column('bucket_id', sa.Integer))


def downgrade() -> None:
     op.drop_column('items', 'bucket_id')
