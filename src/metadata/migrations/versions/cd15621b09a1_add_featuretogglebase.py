# pylint: disable=no-member,invalid-name,line-too-long,trailing-whitespace
"""Add FeatureToggleBASE

Revision ID: cd15621b09a1
Revises: 4546182d773f
Create Date: 2020-12-17 17:00:53.686260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd15621b09a1'
down_revision = '4546182d773f'
branch_labels = None
depends_on = None

feature_toggle = sa.table('FeatureToggleBASE',
                          sa.Column('FeatureToggleID',
                                    sa.Integer,
                                    primary_key=True,
                                    autoincrement=True),
                          sa.Column('ToggleNM',
                                    sa.String(128),
                                    nullable=False),
                          sa.Column('ToggleDSC',
                                    sa.String(255),
                                    nullable=False),
                          sa.Column('ToggleIsEnabledFLG',
                                    sa.Boolean,
                                    default=False,
                                    nullable=False))


def upgrade():
    op.create_table('FeatureToggleBASE',
                    sa.Column('FeatureToggleID',
                              sa.Integer,
                              primary_key=True,
                              autoincrement=True),
                    sa.Column('ToggleNM', sa.String(128), nullable=False),
                    sa.Column('ToggleDSC', sa.String(255), nullable=False),
                    sa.Column('ToggleIsEnabledFLG',
                              sa.Boolean,
                              default=False,
                              nullable=False))

    op.bulk_insert(feature_toggle,
                   [
                       {
                           'ToggleNM': 'enable_event_handlers',
                           'ToggleDSC': 'Allows the use of event handlers within the acquisition endpoint to trigger configurable actions in response to events.'
                       }
                   ])


def downgrade():
    op.drop_table('FeatureToggleBASE')
