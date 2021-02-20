from sqlalchemy.engine import create_engine

from pydas_metadata.contexts.base import BaseContext, session_factory


class MemoryContext(BaseContext):
    """
    Memory connection context, handles data store session setup and object insertion.
    This context supports both the SQLite database and in-memory metadata storage.

    Example
    -------
    >>> from metadata.models import Base
    >>> from metadata.contexts import MemoryContext
    >>> context = MemoryContext()
    >>> Base.metadata.create_all(context.engine)

    In this example we create an in-memory data context, which is useful when you do not need to
    persist the data, or when the data is already persisted elsewhere. Once the context is
    created, it's passed to the `Base.metadata.create_all(context.engine)` function, which
    initializes the in-memory database.
    """

    def __init__(self, **config):
        connection_path = (config['database']
                           if 'database' in config
                           else ':memory:')
        self.engine = create_engine(f'sqlite:///{connection_path}')

    @classmethod
    def can_handle(cls, context_type: str) -> bool:
        return context_type == 'sqlite'

    def get_session_maker(self):
        """Returns a Session factory object for connecting to the database"""
        session_factory.configure(bind=self.engine)
        return session_factory
