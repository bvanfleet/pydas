from abc import abstractmethod, ABC


class BaseParser (ABC):
    """A base class that provides a method for parsing configuration data."""

    @classmethod
    @abstractmethod
    def parse(cls, **kwargs) -> dict:
        """Parses data (taken from an implementation specific source) and returns a dictionary."""
        raise NotImplementedError
