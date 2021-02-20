# pylint: disable=no-member,invalid-name,line-too-long,trailing-whitespace
"""Seed CompanyBASE default values

Revision ID: 2994705c603d
Revises: 7acf74897f37
Create Date: 2020-11-05 23:16:46.490160

"""
from alembic import op
import sqlalchemy as sa

company = sa.table('CompanyBASE',
                   sa.Column('Symbol', sa.String(length=10), nullable=False),
                   sa.Column('Name', sa.String(length=128), nullable=True),
                   sa.Column('Market', sa.String(length=50), nullable=True))

companies = [
    {'Symbol': 'AAPL', 'Name': 'Apple, Inc.', 'Market': 'Technology'},
    {'Symbol': 'GOOGL', 'Name': 'Alphabet, Inc.', 'Market': 'Technology'},
    {'Symbol': 'MSFT', 'Name': 'Microsoft Corp.', 'Market': 'Technology'}
]


# revision identifiers, used by Alembic.
revision = '2994705c603d'
down_revision = '7acf74897f37'
branch_labels = None
depends_on = None


def upgrade():
    op.bulk_insert(company, companies)


def downgrade():
    connection = op.get_bind()
    connection.execute(
        company.delete()
    )
