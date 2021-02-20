# pylint: disable=no-member,invalid-name,line-too-long,trailing-whitespace
"""Seed ConfigurationBASE default values

Revision ID: 2dc53194ff59
Revises: 2994705c603d
Create Date: 2020-11-05 23:19:53.417234

"""
from alembic import op
import sqlalchemy as sa


configuration = sa.table('ConfigurationBASE',
                         sa.Column('Id', sa.Integer(), nullable=False),
                         sa.Column('Name', sa.String(
                             length=128), nullable=False),
                         sa.Column('Type', sa.String(
                             length=50), nullable=False),
                         sa.Column('ValueTXT', sa.String(
                             length=255), nullable=True),
                         sa.Column('ValueNBR', sa.Float(), nullable=True))

configurations = [
    {'Id': 1, 'Name': 'apiKey', 'Type': 'str',
     'ValueTXT': sa.sql.null()},
    {'Id': 2, 'Name': 'apiUrl', 'Type': 'str',
     'ValueTXT': 'https://cloud.iexapis.com'},
    {'Id': 3, 'Name': 'apiVersion', 'Type': 'str',
     'ValueTXT': '/v1'},
    {'Id': 4, 'Name': 'outputFormat', 'Type': 'str',
     'ValueTXT': 'file'},
    {'Id': 5, 'Name': 'outputFilePath', 'Type': 'str',
     'ValueTXT': sa.sql.null()},
    {'Id': 6, 'Name': 'outputFileRowDelimiter', 'Type': 'str',
     'ValueTXT': '\\n'},
    {'Id': 7, 'Name': 'outputFileFieldDelimiter', 'Type': 'str',
     'ValueTXT': ','},
    {'Id': 8, 'Name': 'outputFileTextQualifier', 'Type': 'str',
     'ValueTXT': '"'},
    {'Id': 9, 'Name': 'outputFileHasHeaderRow', 'Type': 'str',
     'ValueTXT': 'True'}
]

# revision identifiers, used by Alembic.
revision = '2dc53194ff59'
down_revision = '2994705c603d'
branch_labels = None
depends_on = None


def upgrade():
    op.bulk_insert(configuration, configurations)


def downgrade():
    connection = op.get_bind()
    connection.execute(
        configuration.delete()
    )
