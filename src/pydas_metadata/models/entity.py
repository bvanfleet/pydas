from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from pydas_metadata.models.base import Base
from pydas_metadata.models.entity_feature import EntityFeatureMap
from pydas_metadata.models.feature import Feature


class Entity(Base):
    """
    Base entity that data features are mapped to. This object groups features for dataset
    generation and provides additional metadata for user experience.

    Attributes
    ----------
    identifier: str
        Unique identifier for a entity. The value set should match the real-world identifier
        of the identifier being tracked in metadata.

    name: str
        The name of the entity.

    category: str
        The primary category or sector that the entity operates within.

    features: list[:class:`metadata.models.Feature`]
        Collection of `Feature` objects that are mapped to the entity.
    """
    __tablename__ = 'EntityBASE'

    identifier: str = Column('Identifier', String(10), primary_key=True)
    name: str = Column('Name', String)
    category: str = Column('Category', String)
    source: str = Column('SourceNM', String)

    features: List[Feature] = relationship('Feature', secondary=EntityFeatureMap)

    def __str__(self):
        return f'{self.identifier}, {self.name}, {self.category}'

    def __json__(self):
        """Returns a jsonify-able representation of the entity object.

        Note
        ----
        The features property will contain a reference URI to where the features
        can be retrieved.
        """
        # TODO: Consider adding a flask that allows the user to expand this to
        # include the feature(s) associated with the entity. This could reduce
        # the amount of API calls being made if there's a particularly large
        # entity.
        return {
            "identifier": self.identifier,
            "name": self.name,
            "category": self.category,
            "source": self.source,
            "features": {"$ref": f'/api/v1/companies/{self.identifier}/features'}
        }
