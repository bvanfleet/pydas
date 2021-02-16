import logging
from metadata.models import Feature as dbFeature
from sdas import handlers
from sdas.feature_mapper.feature import Feature


class FeatureMap:
    """Contains a mapping between configurable features and their metadata.

    *DEPRECATED*: This should no longer be used! Instead, use the metadata.models API.

    Attributes
    ----------
    map: dict
        The dictionary containing feature names as keys and tuples with the URI and handler method.
    """

    def __init__(self):
        """Initializes a new instance of the feature_map class"""
        logging.warn(
            '''DEPRECATED: The FeatureMap is no longer maintained and should not be used!
            We recommend the use of the metadata.models API for interacting with features.
            The sdas.feature_mapper module will be removed in a future date. 
            ''')
        self.map: dict = {
            'open': ('/stock/{symbol:}/chart', handlers.batch_handler),
            'close': ('/stock/{symbol:}/chart', handlers.batch_handler),
            'high': ('/stock/{symbol:}/chart', handlers.batch_handler),
            'low': ('/stock/{symbol:}/chart', handlers.batch_handler),
            'volume': ('/stock/{symbol:}/chart', handlers.batch_handler),
            'beta': ('/stock/{symbol:}/advanced-stats', handlers.range_handler),
            'bbands': ('/stock/{symbol:}/indicator/bbands', handlers.tech_indicators_handler),
            'natr': ('/stock/{symbol:}/indicator/natr', handlers.tech_indicators_handler),
            'macd': ('/stock/{symbol:}/indicator/macd', handlers.tech_indicators_handler),
            'rsi': ('/stock/{symbol:}/indicator/rsi', handlers.tech_indicators_handler),
            'cci': ('/stock/{symbol:}/indicator/cci', handlers.tech_indicators_handler),
            'sma': ('/stock/{symbol:}/indicator/sma', handlers.tech_indicators_handler),
            'ema': ('/stock/{symbol:}/indicator/ema', handlers.tech_indicators_handler),
            'adx': ('/stock/{symbol:}/indicator/adx', handlers.tech_indicators_handler),
            'adxr': ('/stock/{symbol:}/indicator/adxr', handlers.tech_indicators_handler),
            'stoch': ('/stock/{symbol:}/indicator/stoch', handlers.tech_indicators_handler)
        }

    def get_feature(self, name: str, symbol: str, options: list) -> Feature:
        """Retrieves and initializes a Feature with a given name.

        Parameters
        ----------
        name: str
            Feature name to retrieve and initialize
        symbol: str
            Asset symbol to assign to feature
        options: list
            Collection of feature options

        Returns
        -------
        Feature
            Initialized feature with matching name; otherwise, `None`
        """
        if name in self.map:
            map_tup: tuple = self.map[name]
            return Feature(
                name,
                map_tup[0].format(symbol=symbol),
                map_tup[1],
                options)

        return None

    @classmethod
    def technical_indicators(cls, session) -> list:
        """Returns technical indicator features."""
        query = session.query(dbFeature).filter(dbFeature.handler_id == 3)
        features = query.all()
        return [feature.name for feature in features]
