from sqlalchemy import Column, Boolean, Integer, String

from pydas_metadata.models.base import Base, Jsonifiable


class FeatureToggle(Base, Jsonifiable):
    """
    An optional runtime configuration object for enabling specific
    features and functions within the sDAS platform.

    Attributes
    ----------
    id: int
        Unique identifier for the toggle.

    name: str
        Name of the feature that is associated with the FeatureToggle.
        While the name may be duplicated, it is recommended that it is
        unique for querying purposes.

    description: str
        User friendly description of what the feature does.

    is_enabled: boolean
        Flag indicating whether or not the feature is enabled.
    """
    __tablename__ = 'FeatureToggleBASE'

    id = Column('FeatureToggleID', Integer, primary_key=True,
                autoincrement=True)
    name = Column('ToggleNM', String(128), nullable=False)
    description = Column('ToggleDSC', String(255), nullable=False)
    is_enabled = Column('ToggleIsEnabledFLG', Boolean,
                        default=False, nullable=False)

    def __json__(self) -> dict:
        """Returns a jsonify-able representation of the feature object."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_enabled': self.is_enabled
        }
