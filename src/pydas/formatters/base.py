from abc import ABCMeta, abstractmethod
from typing import Any


class BaseFormatter(metaclass=ABCMeta):
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
