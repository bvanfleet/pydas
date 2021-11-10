'''Mapping table module for metadata ORM usage'''
from pydas_metadata.models.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Table


EntityFeatureMap = Table('EntityFeatureBASE', Base.metadata,
                          Column('EntityFeatureID',
                                 Integer,
                                 primary_key=True,
                                 autoincrement=True,
                                 nullable=False),
                          Column('FeatureName',
                                 String(50),
                                 ForeignKey('FeatureBASE.Name'),
                                 nullable=False),
                          Column('EntityID',
                                 String(50),
                                 ForeignKey('EntityBASE.Identifier'),
                                 nullable=False))
