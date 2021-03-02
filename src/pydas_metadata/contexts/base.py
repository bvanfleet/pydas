from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from typing import Generator

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from pydas_metadata import models

session_factory = sessionmaker()


class BaseContext(metaclass=ABCMeta):
    '''
    Base abstract class for interacting with metadata data store.

    Attributes
    ----------
    engine: :class:`sqlalchemy.engine.Engine`
        The core ORM engine for connecting to, and communicating with, the metadata data store.
    '''
    engine: Engine = None

    @classmethod
    @abstractmethod
    def can_handle(cls, context_type: str) -> bool:
        """
        Returns a flag indicating whether this class can handle the given context type.

        Parameters
        ----------
        context_type: str
            Data store type of the context being requested.
        """
        raise NotImplementedError()

    @contextmanager
    @abstractmethod
    def get_session(self) -> Generator[Session, None, None]:
        '''
        Returns the data store connection session. Must be implemented as a generator function in a
        derived class. This allows the use of properly managed session objects.

        Returns
        -------
        :class:`sqlalchemy.orm.Session`:
            Metadata data store connection instance.

        Example
        -------
        >>> from pydas_metadata.contexts import MemoryContext
        >>> from pydas_metadata.models import Configuration
        >>> context = MemoryContext()
        >>> with context.get_session() as session:
        ...     api_key = session.query(Configuration).filter(Configuration.name=='apiKey')
        ...     print(api_key)
        '''
        raise NotImplementedError()

    def get_configuration(self, name: str):
        with self.get_session() as session:
            query = session.query(models.Configuration).filter(
                models.Configuration.name == name)
            config = query.first()
            return config.value if config is not None else None

    def get_feature_toggle(self, name: str) -> bool:
        with self.get_session() as session:
            query = session.query(models.FeatureToggle).filter(
                models.FeatureToggle.name == name)
            toggle = query.first()
            return toggle.is_enabled if toggle is not None else False
