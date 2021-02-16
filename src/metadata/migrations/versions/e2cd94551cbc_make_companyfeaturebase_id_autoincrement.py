# pylint: disable=no-member,invalid-name,line-too-long,trailing-whitespace
"""Make CompanyFeatureBASE ID autoincrement

Revision ID: e2cd94551cbc
Revises: 2dc53194ff59
Create Date: 2020-11-12 09:54:40.449767

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2cd94551cbc'
down_revision = '2dc53194ff59'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'CompanyFeatureBASE',
        'CompanyFeatureID',
        existing_type=sa.types.INTEGER,
        autoincrement=True,
        nullable=False
    )


def downgrade():
    op.alter_column(
        'CompanyFeatureBASE',
        'CompanyFeatureID',
        existing_type=sa.types.INTEGER,
        autoincrement=False,
        nullable=False
    )
