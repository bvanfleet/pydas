# pylint: disable=no-member,invalid-name,line-too-long,trailing-whitespace
"""Add IsEnabled column to EventHandlerBASE

Revision ID: f73a9aa46c77
Revises: 6b5369ab5224
Create Date: 2021-02-17 20:15:42.776190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f73a9aa46c77'
down_revision = '6b5369ab5224'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('EventHandlerBASE',
                  sa.Column('IsEnabled', sa.Boolean, nullable=False, default=False))


def downgrade():
    op.drop_column('EventHandlerBASE', 'IsEnabled')
