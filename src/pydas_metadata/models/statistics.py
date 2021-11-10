from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from pydas_metadata.models.base import Base
from pydas_metadata.models.entity import Entity
from pydas_metadata.models.feature import Feature


class Statistics(Base):
    """
    Row count data associated with a particular :class:`metadata.models.Company`
    and :class:`metadata.models.Feature`.

    Attributes
    ----------
    company_symbol: str
        Symbol of the company that is associated with this entry.

    feature_name: str
        Name of the feature that is associated with this entry.

    retrieval_datetime: datetime
        Date and time that the acquisition took place, implies the datetime
        that this entry was created.

    row_count: int
        Number of rows that was acquired for the feature, limited to the
        company.

    company: :class:`metadata.models.Company`
        The company with a matching symbol that is associated with this entry.

    feature: :class:`metadata.models.Feature`
        The feature with a matching name that is associated with this entry.
    """
    __tablename__ = 'StatisticsBASE'

    company_symbol: str = Column('CompanySymbol',
                                 String(10),
                                 ForeignKey('EntityBASE.Identifier'),
                                 primary_key=True)
    feature_name: str = Column('FeatureName',
                               String(50),
                               ForeignKey('FeatureBASE.Name'),
                               primary_key=True)
    retrieval_datetime: datetime = Column(
        'RetrievalDTS', DateTime, primary_key=True)
    row_count: int = Column('RowCount', Integer)

    company: Entity = relationship('Entity')
    feature: Feature = relationship('Feature')

    def __json__(self):
        """Returns a jsonify-able representation of the statistics object."""
        return {
            "company_symbol": self.company_symbol,
            "feature_name": self.feature_name,
            "retrieval_datetime": self.retrieval_datetime,
            "total_row_count": int(self.row_count)
        }
