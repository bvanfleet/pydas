"""Classes for transforming acquired data into a desired form prior to output."""

from typing import List

from .base import BaseFormatter
from .compression import CompressionFormatter
from .file import FileFormatter
from .json import JsonFormatter


class FormatterFactory:
    """
    Provides a centralized store for output formatters.

    The factory is pre-seeded with built-in formatters commonly used by the core sDAS solution.
    These formatters include :class:`sdas.formatters.FileFormatter`,
    :class:`sdas.formatters.FileFormatter`, and :class:`sdas.formatters.JsonFormatter`. There is
    also a ``register_formatter`` function for registering user-defined formatters for additional
    output formatting.

    Attributes
    ----------
    formatters: list[BaseFormatter]
        Collection of registered output formatters.
    """

    formatters: List[BaseFormatter] = [
        CompressionFormatter,
        FileFormatter,
        JsonFormatter]

    @classmethod
    def register_formatter(cls, formatter: BaseFormatter):
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
    def get_formatter(cls, output_format) -> BaseFormatter:
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
