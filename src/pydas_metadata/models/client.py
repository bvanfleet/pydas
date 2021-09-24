from sqlalchemy import Column, Integer, String

from pydas_metadata.models.base import Base, Jsonifiable


class Client(Base, Jsonifiable):
    id = Column('ClientID', Integer, primary_key=True, auto_increment=True)
    name = Column('Name', String, nullable=False)
    path = Column('Path', String, nullable=False)
