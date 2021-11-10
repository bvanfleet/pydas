# pylint: disable=no-member,invalid-name,line-too-long,trailing-whitespace
"""alter_entity_add_source_column

Revision ID: 98461c379c18
Revises: da13020a988c
Create Date: 2021-11-10 09:33:39.921367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98461c379c18'
down_revision = 'da13020a988c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('entitybase', sa.Column('SourceNM', sa.String(50), nullable=False))


def downgrade():
    op.drop_column('entitybase', 'SourceNM')
