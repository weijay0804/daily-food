"""create restaurant table

Revision ID: b72954e14932
Revises: Create restaurant table
Create Date: 2023-04-29 19:31:39.602780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b72954e14932'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'restaurant',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('address', sa.Text(), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('lat', sa.Float(), nullable=False),
        sa.Column('lng', sa.Float(), nullable=False),
        sa.Column('is_enable', sa.Boolean(), nullable=False),
        sa.Column('create_at', sa.DateTime(), nullable=False),
        sa.Column('update_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('idx_lat_lng', 'lat', 'lng'),
    )


def downgrade() -> None:
    op.drop_table('restaurant')
