import importlib
import logging
from typing import Callable

from sqlalchemy import Boolean, Column, Integer, String

from metadata.models.base import Base


class EventHandler(Base):
    """
    Metadata object for tracking a function that can be called dynamically at
    runtime.

    Attributes
    ----------
    id: int
        Unique identifier for the EventHandler instance.

    name: str
        Name of the event handler. This name does not have to match the name
        of the function that is called. It can be a user-friendly value.

    description: str
        Details of the function that may be called.

    path: str
        Fully-qualified path to the function tracked by the EventHandler instance.
        This path follows the form: `path.to.module:function_name`.

    type: str
        A type code that identifies when the function may be called. Example: `"ON_ERROR"`.
    """
    __tablename__ = 'EventHandlerBASE'

    id: int = Column('HandlerID', Integer,
                     primary_key=True, autoincrement=True)
    name: str = Column('HandlerNM', String(128), nullable=False)
    description: str = Column('HandlerDSC', String(255), nullable=True)
    path: str = Column('HandlerPathTXT', String(255), nullable=False)
    type: str = Column('HandlerTypeCD', String(15), nullable=False)
    is_enabled: bool = Column('IsEnabled',
                              Boolean,
                              nullable=False,
                              default=False)

    @property
    def function(self) -> Callable:
        """Returns the function associated with the EventHandler.

        Returns
        -------
        Callable:
            Function with a matching path and name tracked by the EventHandler.

        Raises
        ------
        KeyError:
            Thrown if the path or function name are invalid, or cannot be found.
        """
        handler_path = self.path.partition(':')
        logging.debug('Importing module "%s".', handler_path[0])
        module = importlib.import_module(handler_path[0])
        if hasattr(module, handler_path[2]):
            logging.debug('Returning function "%s".', handler_path[2])
            func = getattr(module, handler_path[2])
            return func
        else:
            raise KeyError(
                f'Unable to find handler "{handler_path[2]}" in module "{handler_path[0]}"')

    def __call__(self, *args, **kwargs):
        logging.debug('Calling function at %s...', self.path)
        return self.function(*args, **kwargs)
