from abc import ABCMeta, abstractmethod


class BaseAuthClient(metaclass=ABCMeta):
    """
    Authentication client for validating an auth token and getting user roles.
    """

    @classmethod
    @abstractmethod
    def can_handle(cls, auth_type):
        """
        Returns flag indicating whether the client supports the requested authentication type.

        Parameters
        ----------
        auth_type: str
            Identifier for the type of authentication being performed.

        Returns
        -------
        bool:
            True if the client supports the requested auth_type; otherwise, False.
        """
        raise NotImplementedError

    @abstractmethod
    def validate_token(self, token):
        """
        Validates the given authentication token against an auth provider and returns the user ID
        (uid). If the token is invalid an error specific to the library will be thrown (e.g.
        Google firebase auth may throw an `InvalidIdTokenError` if the token contains an invalid
        value).

        Parameters
        ----------
        token: object
            Authorization token to validate. This token typically follows the JWT token protocol.

        Returns
        -------
        int | str:
            User identifier from the given, validated token.
        """
        raise NotImplementedError

    @abstractmethod
    def get_roles(self, uid) -> list:
        """
        Gets the assigned roles for the user with matching uid.
        """
        raise NotImplementedError
