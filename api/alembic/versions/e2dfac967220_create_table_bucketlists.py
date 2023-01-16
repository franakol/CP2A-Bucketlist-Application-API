"""create table bucketlists

Revision ID: e2dfac967220
Revises: 3182bd16cf09
Create Date: 2023-01-16 22:39:59.710014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2dfac967220'
down_revision = '3182bd16cf09'
branch_labels = None
depends_on = None


def upgrade() -> None:
     op.create_table(
        'bucketlists',
        sa.Column('bucket_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(45), nullable=False, unique=True),
        sa.Column('date_created', sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column('date_modified', sa.DateTime, server_default=sa.func.current_timestamp())

    )


def downgrade() -> None:
    op.drop_table('bucketlists')
