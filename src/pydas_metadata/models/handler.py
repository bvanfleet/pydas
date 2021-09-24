from sqlalchemy import Column, Integer, String

from pydas_metadata.models.base import Base, Jsonifiable


class Handler(Base, Jsonifiable):
    """Metadata object representing the handler function

    Attributes
    ----------
    id: int
        Unique identifier for the handler object.

    name: str
        Name of the function tracked by the handler object. This name must match
        the name of a function tracked in the `pydas.handlers` module.

    path: str
        Module path to the handler function. Used when dynamically calling the
        transformer.
    """
    __tablename__ = 'HandlerBASE'

    id: int = Column('HandlerID', Integer, primary_key=True)
    name: str = Column('Name', String)
    path: str = Column('Path', String)

    def __json__(self):
        """Returns a jsonify-able representation of the feature object."""
        return {
            "id": self.id,
            "name": self.name
        }
