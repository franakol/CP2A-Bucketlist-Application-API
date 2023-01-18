"""Add a column

Revision ID: f5cd35ea6443
Revises: 3e0f39cfce6c
Create Date: 2023-01-17 16:30:13.490371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5cd35ea6443'
down_revision = '3e0f39cfce6c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('bucketlists', sa.Column('created_by', sa.Integer))


def downgrade() -> None:
    op.drop_column('bucketlists', 'created_by')
