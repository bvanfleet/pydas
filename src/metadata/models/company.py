from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from metadata.models.base import Base
from metadata.models.company_feature import CompanyFeatureMap


class Company(Base):
    """
    Base entity that data features are mapped to. This object groups features for dataset
    generation and provides additional metadata for user experience.

    Attributes
    ----------
    symbol: str
        Unique identifier for a company. The value set should match the real-world symbol
        of the symbol being tracked in metadata.

    name: str
        The name of the company.

    market: str
        The primary market or sector that the company operates within.

    features: list[:class:`metadata.models.Feature`]
        Collection of `Feature` objects that are mapped to the company.
    """
    __tablename__ = 'CompanyBASE'

    symbol: str = Column('Symbol', String(10), primary_key=True)
    name: str = Column('Name', String)
    market: str = Column('Market', String)

    features: list = relationship('Feature',
                                  secondary=CompanyFeatureMap)

    def __str__(self):
        return f'{self.symbol}, {self.name}, {self.market}'

    def __json__(self):
        """Returns a jsonify-able representation of the company object.

        Note
        ----
        The features property will contain a reference URI to where the features
        can be retrieved.
        """
        # TODO: Consider adding a flask that allows the user to expand this to
        # include the feature(s) associated with the company. This could reduce
        # the amount of API calls being made if there's a particularly large
        # company.
        return {
            "symbol": self.symbol,
            "name": self.name,
            "market": self.market,
            "features": {"$ref": f'/api/v1/companies/{self.symbol}/features'}
        }
