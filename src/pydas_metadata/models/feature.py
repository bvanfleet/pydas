import dataclasses
import importlib

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from pydas_metadata.models.base import Base
from pydas_metadata.models.handler import Handler
from pydas_metadata import constants as const


class Feature(Base):
    '''
    Data point metadata for tracking what feature to acquire, how to acquire it, and
    information for user friendliness.

    Attributes
    ----------
    name: str
        Data feature name. This attribute is used when acquiring data, and should match the
        name of the feature represented in the external data provider's system.

    uri: str
        Data feature endpoint address template. Points to where the data can be acquired
        from. When used in the sDAS system, additional data points may be substituted in,
        e.g. company symbol.

    handler_id: int
        Identifier for the handler metadata object that contains the function used for
        acquiring feature data.

    description: str
        Data feature description for users to understand what data is acquired.

    handler_metadata: :class:`metadata.models.Handler`
        Acquisition handler object with matching handler ID.
    '''
    __tablename__ = 'FeatureBASE'

    name: str = Column('Name', String(50), primary_key=True)
    uri: str = Column('URI', String, nullable=False)
    handler_id: int = Column('HandlerID', Integer,
                             ForeignKey('HandlerBASE.HandlerID'))
    description: str = Column('Description', String(255), nullable=True)

    handler_metadata: Handler = relationship('Handler')

    def __str__(self):
        return f'{{name: {self.name}, uri: {self.uri}}}'

    @property
    def handler(self):
        """Callable function dynamically associated with the feature

        Returns
        -------
        Callable:
            Data acquisition function associated with the feature.
        """
        # TODO: Determine if there's a way we can remove this coupling by making
        # the handler_path configurable
        handlers = importlib.import_module('pydas.transformers')
        return getattr(handlers, self.handler_metadata.name)

    def get_value(self, data: dict) -> tuple:
        """Returns a tuple containing the feature data and date extracted from a larger object.

        Parameters
        ----------
        data: dict
            Object to extract feature data from.

        Returns
        -------
        tuple:
            Data point extracted from the given object.
        """
        value = data
        if dataclasses.is_dataclass(data):
            value = dataclasses.asdict(data)
        
        if self.name in value:
            return (value[self.name], value[const.DATE_PROPERTY])

        return const.STR_EMPTY

    def get_values(self, data: list) -> list:
        """Returns a list of tuples with the feature data and dates extracted from a larger
        data set acquired from the feature's handler function."""
        return [self.get_value(d) for d in data]

    def __json__(self):
        """Returns a jsonify-able representation of the feature object."""
        return {
            "name": self.name,
            "description": self.description,
            "uri": self.uri,
            "handler": {
                "id": self.handler_metadata.id,
                "name": self.handler_metadata.name
            }
        }
