"""create table items

Revision ID: 3e0f39cfce6c
Revises: e2dfac967220
Create Date: 2023-01-16 22:46:58.458213

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e0f39cfce6c'
down_revision = 'e2dfac967220'
branch_labels = None
depends_on = None


def upgrade() -> None:
     op.create_table(
        'items',
        sa.Column('item_id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(45), nullable=False, unique=True),
        sa.Column('date_created', sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column('date_modified', sa.DateTime, server_default=sa.func.current_timestamp())

    )
    


def downgrade() -> None:
    op.drop_table('items')
