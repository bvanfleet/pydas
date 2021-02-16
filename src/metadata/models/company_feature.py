'''Mapping table module for metadata ORM usage'''
from metadata.models.base import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Table


CompanyFeatureMap = Table('CompanyFeatureBASE', Base.metadata,
                          Column('CompanyFeatureID',
                                 Integer,
                                 primary_key=True,
                                 autoincrement=True,
                                 nullable=False),
                          Column('FeatureName',
                                 String(50),
                                 ForeignKey('FeatureBASE.Name'),
                                 nullable=False),
                          Column('CompanySymbol',
                                 String(50),
                                 ForeignKey('CompanyBASE.Symbol'),
                                 nullable=False))
