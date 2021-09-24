"""REST API clients used for retrieving stock data."""

from abc import ABCMeta, abstractmethod
from typing import List

from .aws import AwsS3Client
from .iex import IexClient
from .ipfs import IpfsArchiveClient

from pydas_metadata.models import Company, Feature


class DataClient(metaclass=ABCMeta):
    @abstractmethod
    def get_feature_data(self, feature: Feature, company: Company, options: list):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def can_handle(cls, source: str) -> bool:
        raise NotImplementedError()


class DataClientFactory:
    clients: List[DataClient] = [IexClient, AwsS3Client]

    @classmethod
    def register_client(cls, client: DataClient):
        cls.clients.append(client)

    @classmethod
    def get_client(cls, source_type: str, **kwargs) -> DataClient:
        for client in cls.clients:
            if client.can_handle(source_type):
                return client(**kwargs)

        raise TypeError(f'No supported clients found for type: {source_type}')
