"""create table users

Revision ID: 3182bd16cf09
Revises: 
Create Date: 2023-01-14 23:02:05.420410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3182bd16cf09'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer, primary_key=True, Autoincrement=True),
        sa.Column('username', sa.String(45), nullable=False, unique=True),
        sa.Column('email', sa.String(50), nullable=False, unique=True),
        sa.Column('password', sa.Text(), nullable=False),
        sa.Column('date_created', sa.DateTime, server_default=sa.func.current_timestamp()),
        sa.Column('date_modified', sa.DateTime, server_default=sa.func.current_timestamp())

    )


def downgrade() -> None:
    op.drop_table('users')
