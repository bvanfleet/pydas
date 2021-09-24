"""
The basic unit of operation for the pyDAS platform is a transformer. All data transformers
implement the `class`::Transformer abstract class.
"""
from abc import ABC, abstractmethod
import importlib
from types import FunctionType
from typing import Any


class Transformer(ABC):
    """The base interface for a data transformer."""

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Any:
        """
        Executes a data transformation on the data provided. The transformed data is then returned.
        Any type of parameters can be taken in and utilized by the data transformer.
        """
        raise NotImplementedError()


class DynamicTransformer(Transformer):
    """
    Provides a data transformer that is resolved at runtime based upon a given name and module
    path.
    """

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def __call__(self, *args, **kwargs):
        """
        Executes a data transformation on the data provided. The transformed data is then returned.
        Any type of parameters can be taken in and utilized by the data transformer. The function
        that is called is imported at the time this transformer is called.

        Raises
        ------
        ImportError:
            Raised if the module or function are invalid.

        TypeError:
            Raised if the transformer named is not a function.
        """
        module = importlib.import_module(self.path)
        if not hasattr(module, self.name):
            raise ImportError()

        transformer = getattr(module, self.name)
        if not isinstance(transformer, FunctionType):
            raise TypeError()

        return transformer(*args, **kwargs)
