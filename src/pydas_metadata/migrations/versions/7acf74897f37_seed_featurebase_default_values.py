# pylint: disable=no-member,invalid-name,line-too-long,trailing-whitespace
"""Seed FeatureBASE default values

Revision ID: 7acf74897f37
Revises: 59e233e9e1b5
Create Date: 2020-11-05 23:03:36.086108

"""
from alembic import op
import sqlalchemy as sa

feature = sa.table('FeatureBASE',
                   sa.Column('Name', sa.String(length=50), nullable=False),
                   sa.Column('URI', sa.String(length=255), nullable=False),
                   sa.Column('HandlerID', sa.Integer(), nullable=True),
                   sa.Column('Description', sa.String(length=255), nullable=True))


feature_values = [
    {'Name': 'open', 'URI': '/stocks/{symbol:}/chart',
     'HandlerID': 1, 'Description': 'Initial price of stock at start of a trading day.'},
    {'Name': 'high', 'URI': '/stocks/{symbol:}/chart',
     'HandlerID': 1, 'Description': 'Highest price a stock reaches on a given day.'},
    {'Name': 'low', 'URI': '/stocks/{symbol:}/chart',
     'HandlerID': 1, 'Description': 'Lowest price a stock reaches on a given day.'},
    {'Name': 'close', 'URI': '/stocks/{symbol:}/chart',
     'HandlerID': 1, 'Description': 'Final price of a stock at the end of a trading day.'},
    {'Name': 'volume', 'URI': '/stocks/{symbol:}/chart',
     'HandlerID': 1, 'Description': 'Total number of shares available to trade on a given day.'},
    {'Name': 'beta', 'URI': '/stock/{symbol:}/advanced-stats',
     'HandlerID': 2, 'Description': 'Measure of volatility for a given asset compared to its market.'},
    {'Name': 'bbands', 'URI': '/stock/{symbol:}/indicator/bbands',
     'HandlerID': 3, 'Description': 'Bollinger Band, a technical analysis tool used to determine overbought and oversold assets.'},
    {'Name': 'natr', 'URI': '/stock/{symbol:}/indicator/natr',
     'HandlerID': 3, 'Description': 'Normalized Average True Range, a technical analysis indicator that measures market volatility.'},
    {'Name': 'macd', 'URI': '/stock/{symbol:}/indicator/macd',
     'HandlerID': 3, 'Description': 'Moving Average Convergence Divergence, an indicator that measures trend momentum using two moving averages.'},
    {'Name': 'rsi', 'URI': '/stock/{symbol:}/indicator/rsi',
     'HandlerID': 3, 'Description': sa.sql.null()},
    {'Name': 'cci', 'URI': '/stock/{symbol:}/indicator/cci',
     'HandlerID': 3, 'Description': sa.sql.null()},
    {'Name': 'sma', 'URI': '/stock/{symbol:}/indicator/sma',
     'HandlerID': 3, 'Description': sa.sql.null()},
    {'Name': 'ema', 'URI': '/stock/{symbol:}/indicator/ema',
     'HandlerID': 3, 'Description': sa.sql.null()},
    {'Name': 'adx', 'URI': '/stock/{symbol:}/indicator/adx',
     'HandlerID': 3, 'Description': sa.sql.null()},
    {'Name': 'adxr', 'URI': '/stock/{symbol:}/indicator/adxr',
     'HandlerID': 3, 'Description': sa.sql.null()},
    {'Name': 'stoch', 'URI': '/stock/{symbol:}/indicator/stoch',
     'HandlerID': 3, 'Description': sa.sql.null()}
]

# revision identifiers, used by Alembic.
revision = '7acf74897f37'
down_revision = '59e233e9e1b5'
branch_labels = None
depends_on = None


def upgrade():
    op.bulk_insert(feature, feature_values)


def downgrade():
    connection = op.get_bind()
    connection.execute(
        feature.delete()
    )
