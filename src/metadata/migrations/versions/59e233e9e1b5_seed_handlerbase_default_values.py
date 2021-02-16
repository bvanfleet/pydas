# pylint: disable=no-member,invalid-name,line-too-long,trailing-whitespace
"""Seed HandlerBASE default values

Revision ID: 59e233e9e1b5
Revises: 93b6e6de2af0
Create Date: 2020-11-05 22:49:27.952691

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59e233e9e1b5'
down_revision = '93b6e6de2af0'
branch_labels = None
depends_on = None

handler = sa.table('HandlerBASE',
                   sa.Column('HandlerID', sa.Integer(), nullable=False),
                   sa.Column('Name', sa.String(length=128), nullable=False),)


def upgrade():
    op.bulk_insert(handler, [
        {'HandlerID': 1, 'Name': 'batch_handler'},
        {'HandlerID': 2, 'Name': 'range_handler'},
        {'HandlerID': 3, 'Name': 'tech_indicators_handler'}
    ])


def downgrade():
    connection = op.get_bind()
    connection.execute(
        handler.delete()
    )
