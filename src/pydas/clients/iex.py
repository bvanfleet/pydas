"""Contains IEX Cloud specific client for data retrieval via REST API"""
import logging

from pydas.clients.base import BaseDataClient


# pylint: disable=too-few-public-methods
class IexClient(BaseDataClient):
    """
    Contains IEX Cloud metadata and method for retrieving feature data from IEX Cloud API.

    Attributes
    ----------
    key: str
        API key used to authenticate with the IEX servers.

    version: str
        Version of IEX Cloud API to use. Default: ``/v1``.

    base_uri: str
        The base path to make requests against. Default: ``'https://cloud.iexapis.com'``.
    """

    def __init__(self, apiKey: str):
        self.key = apiKey
        self.version = '/v1'
        self.base_uri = 'https://cloud.iexapis.com'

    @classmethod
    def can_handle(cls, source: str) -> bool:
        return source.lower() == 'iex'

    def get_feature_data(self, feature, company, options):
        """Retrieves data from IEX Cloud REST API using the feature handler

        Parameters
        ----------
        feature: Feature
            Metadata about what to retrieve from IEX API endpoint

        Returns
        -------
        list:
            Collection of data from IEX API.
        dict:
            Data point from IEX API.
        """
        url = (self.base_uri +
               self.version +
               feature.uri.format(symbol=company.symbol))
        logging.debug('Requesting data at %s', url)
        return feature.handler(url, options, self.key)
