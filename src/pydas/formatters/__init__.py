"""Classes for transforming acquired data into a desired form prior to output."""

from abc import ABCMeta, abstractmethod
from typing import Any, List

from .compression import CompressionFormatter
from .file import FileFormatter
from .json import JsonFormatter


class Formatter(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def can_handle(cls, output_format: str) -> bool:
        """
        Returns a value indicating whether this formatter supports the requested type.

        Parameters
        ----------
        output_format: str
            Name of the formatter being requested.

        Returns
        -------
        bool:
            Flag indicating whether the formatter supports the requested output format.
        """
        raise NotImplementedError()

    @abstractmethod
    def transform(self, data: dict, **format_options) -> Any:
        raise NotImplementedError()


class FormatterFactory:
    """
    Provides a centralized store for output formatters.

    The factory is pre-seeded with built-in formatters commonly used by the core sDAS solution.
    These formatters include :class:`pydas.formatters.FileFormatter`,
    :class:`pydas.formatters.FileFormatter`, and :class:`pydas.formatters.JsonFormatter`. There is
    also a ``register_formatter`` function for registering user-defined formatters for additional
    output formatting.

    Attributes
    ----------
    formatters: list[BaseFormatter]
        Collection of built-in output formatters.
    """

    formatters: List[Formatter] = [CompressionFormatter,
                                   FileFormatter,
                                   JsonFormatter]

    @classmethod
    def register_formatter(cls, formatter: Formatter):
        """
        Registers an output formatter with the factory.

        Parameters
        ----------
        formatter: any
            Output formatter to register.

        Raises
        ------
        TypeError:
            Thrown if the formatter is ``NoneType``.
        """
        if formatter is None:
            raise TypeError('formatter must not be None')

        cls.formatters.append(formatter)

    @classmethod
    def get_formatter(cls, output_format) -> Formatter:
        """
        Retrieves and returns an output formatter instance.

        Parameters
        ----------
        output_format: str
            The name of the output formatter to retrieve. Example: ``"file"``.

        Returns
        -------
        object:
            An output formatter that supports the given format.

        Raises
        ------
        KeyError:
            Thrown if there are no registered output formatters that supports
            the given format.
        """
        for formatter in cls.formatters:
            if formatter.can_handle(output_format):
                return formatter()

        raise KeyError(f'Unsupported output formatter: "{output_format}".')
