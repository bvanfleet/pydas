# pylint: disable=no-member,invalid-name,line-too-long,trailing-whitespace
"""Add ArchiveBASE table

Revision ID: 4546182d773f
Revises: e2cd94551cbc
Create Date: 2020-12-16 12:44:08.789235

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4546182d773f'
down_revision = 'e2cd94551cbc'
branch_labels = None
depends_on = None

configuration = sa.table('ConfigurationBASE',
                         sa.Column('Id',
                                   sa.Integer(),
                                   primary_key=True,
                                   autoincrement=True,
                                   nullable=False),
                         sa.Column('Name',
                                   sa.String(length=128),
                                   nullable=False),
                         sa.Column('Type',
                                   sa.String(length=50),
                                   nullable=False),
                         sa.Column('ValueTXT',
                                   sa.String(length=255),
                                   nullable=True),
                         sa.Column('ValueNBR', sa.Float(), nullable=True))


def upgrade():
    op.create_table('ArchiveBASE',
                    sa.Column('AddressTXT', sa.String(255), primary_key=True),
                    sa.Column('FileNM', sa.String(255), nullable=False),
                    sa.Column('CreatedDTS',
                              sa.DateTime,
                              default=sa.sql.func.now(),
                              nullable=False),
                    sa.Column('CompanySymbolsTXT',
                              sa.String(255),
                              nullable=False))
    op.bulk_insert(
        configuration,
        [
            {
                'Name': 'archiveIpfsConnectionString',
                'Type': 'str',
                'ValueTXT': '/dns/ipfs.infura.io/tcp/5001/https'
            }
        ])


def downgrade():
    op.drop_table('ArchiveBASE')
