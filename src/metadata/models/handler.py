from sqlalchemy import Column, Integer, String

from metadata.models.base import Base


class Handler(Base):
    """Metadata object representing the handler function

    Attributes
    ----------
    id: int
        Unique identifier for the handler object.

    name: str
        Name of the function tracked by the handler object. This name must match
        the name of a function tracked in the `pydas.handlers` module.
    """
    __tablename__ = 'HandlerBASE'

    id: int = Column('HandlerID', Integer, primary_key=True)
    name: str = Column('Name', String)

    def __json__(self):
        """Returns a jsonify-able representation of the feature object."""
        return {
            "id": self.id,
            "name": self.name
        }
