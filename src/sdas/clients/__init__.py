"""REST API clients used for retrieving stock data."""

from typing import List

from .aws import AwsS3Client
from .base import BaseDataClient
from .iex import IexClient
from .ipfs import IpfsArchiveClient


class DataClientFactory:
    clients: List[BaseDataClient] = [IexClient, AwsS3Client]

    @classmethod
    def register_client(cls, client: BaseDataClient):
        cls.clients.append(client)

    @classmethod
    def get_client(cls, source_type: str, **kwargs) -> BaseDataClient:
        for client in cls.clients:
            if client.can_handle(source_type):
                return client(**kwargs)

        raise TypeError(f'No supported clients found for type: {source_type}')
