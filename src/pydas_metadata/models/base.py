"""Base ORM declarative model definition module"""
from abc import ABC, abstractmethod

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Jsonifiable(ABC):
    """
    Defines the contract for a model that can be represented in a JSON format.
    """

    @abstractmethod
    def __json__(self) -> dict:
        """Returns a jsonify-able representation of the feature object."""
        raise NotImplementedError()
