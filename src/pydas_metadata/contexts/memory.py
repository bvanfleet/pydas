from sqlalchemy.engine import create_engine

from pydas_metadata.contexts.base import BaseContext, session_factory


class MemoryContext(BaseContext):
    """
    Memory connection context, handles data store session setup and object insertion.
    This context supports both the SQLite database and in-memory metadata storage.

    Example
    -------
    >>> from pydas_metadata.models import Base
    >>> from pydas_metadata.contexts import MemoryContext
    >>> context = MemoryContext()
    >>> Base.metadata.create_all(context.engine)

    In this example we create an in-memory data context, which is useful when you do not need to
    persist the data, or when the data is already persisted elsewhere. Once the context is
    created, it's passed to the `Base.metadata.create_all(context.engine)` function, which
    initializes the in-memory database.

    Example
    -------
    >>> from pydas_metadata.contexts import MemoryContext
    >>> from pydas_metadata.models import Company
    >>> context = MemoryContext(database='metadata.sqlite')
    >>> session = context.get_session()
    >>> for company in session.query(Company).all():
    ...     print(company.symbol)

    In this example, we connect to a SQLite database, query all
    :class:`pydas_metadata.models.Company` objects, and print each company's symbol.
    """

    def __init__(self, **config):
        connection_path = (config['database']
                           if 'database' in config
                           else ':memory:')
        self.engine = create_engine(f'sqlite:///{connection_path}')
        session_factory.configure(bind=self.engine)

    @classmethod
    def can_handle(cls, context_type: str) -> bool:
        return context_type == 'sqlite'

    def get_session(self):
        """Returns a Session factory object for connecting to the database"""
        return session_factory()
