from .base import BaseAuthClient
from .google import GoogleFirestoreAuthClient


class AuthClientFactory:
    supported_clients = [GoogleFirestoreAuthClient]

    @classmethod
    def get_auth_client(cls, auth_type, auth_config) -> BaseAuthClient:
        for client in cls.supported_clients:
            if client.can_handle(auth_type):
                return client(auth_config)

        raise ValueError(
            f"Unsupported authentication type '{auth_type}' provided")
