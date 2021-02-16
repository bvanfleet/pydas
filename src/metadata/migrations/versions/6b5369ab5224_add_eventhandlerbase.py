# pylint: disable=no-member,invalid-name,line-too-long,trailing-whitespace
"""Add EventHandlerBASE

Revision ID: 6b5369ab5224
Revises: cd15621b09a1
Create Date: 2020-12-18 11:56:23.159750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b5369ab5224'
down_revision = 'cd15621b09a1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('EventHandlerBASE',
                    sa.Column('HandlerID',
                              sa.Integer,
                              primary_key=True,
                              autoincrement=True),
                    sa.Column('HandlerNM',
                              sa.String(128),
                              nullable=False),
                    sa.Column('HandlerDSC',
                              sa.String(255),
                              nullable=True),
                    sa.Column('HandlerPathTXT',
                              sa.String(255),
                              nullable=False),
                    sa.Column('HandlerTypeCD', sa.String(15), nullable=False))


def downgrade():
    op.drop_table('EventHandlerBASE')
