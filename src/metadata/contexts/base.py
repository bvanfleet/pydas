from abc import ABCMeta, abstractmethod

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from metadata import models

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

    @abstractmethod
    def get_session_maker(self):
        '''
        Returns the data store connection session. Must be implemented in a derived class.

        Returns
        -------
        :class:`sqlalchemy.orm.Session`:
            Metadata data store connection instance.
        '''
        raise NotImplementedError()

    def get_configuration(self, name: str) -> models.Configuration:
        session_maker = self.get_session_maker()
        session = session_maker()
        query = session.query(models.Configuration).filter(
            models.Configuration.name == name)
        return query.first()
