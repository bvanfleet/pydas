'''
Metadata data source connection contexts.
'''

from .base import BaseContext
from .database import DatabaseContext
from .memory import MemoryContext


class ContextFactory:
    supported_contexts = (DatabaseContext, MemoryContext)

    @classmethod
    def get_context(cls, context_type: str, **context_config) -> BaseContext:
        """Returns a :class:`BaseContext` implementation that matches the given context type.

        Parameters
        ----------
        context_type: str
            Data store dialect to construct a supported context for.

        context_config: dict
            Additional context configuration values.

        Raises
        ------
        ValueError:
            Raised if the context type doesn't have a supported implementation.

        Example
        -------
        >>> from metadata.contexts import ContextFactory
        >>> context = ContextFactory.get_context('sqlite', database='pydas.db')
        """
        for context in cls.supported_contexts:
            if context.can_handle(context_type):
                return context(**context_config)

        raise ValueError(
            f"Unsupported context dialect detected: {context_type}")
