from sqlalchemy import Column, Float, Integer, String

from pydas_metadata.models.base import Base


class Configuration(Base):
    """Model used to set system-wide runtime configuration.

    Attributes
    ----------
    id: int
        Unique identifier for the Configuration instance.

    name: str
        Name of the configuration object.

    type: str
        Data type of the value that the Configuration instance holds.

    value_text: str | any
        Textual value set for the instance. Values stored also includes
        `bytes` and `boolean` types.

    value_number: decimal | float | int
        Numeric value set for the instance.
    """
    __tablename__ = 'ConfigurationBASE'

    _supported_number_types = ['float', 'int', 'decimal']

    id: int = Column('Id', Integer, primary_key=True)
    name: str = Column('Name', String, nullable=False)
    type: str = Column('Type', String, nullable=False)
    value_text: str = Column('ValueTXT', String)
    value_number = Column('ValueNBR', Float)

    @property
    def value(self):
        """
        Returns the value set on the configuration. Depending on the configuration.type,
        the value returned will come from either the `value_number` or `value_text` attribute.
        """
        if self.type in self._supported_number_types:
            return self.value_number

        if self.type == 'bool':
            return self.get_boolean_value()

        return self.value_text

    @value.setter
    def value(self, new_value):
        """
        Sets the value of the configuration. Depending on the configuration.type
        set, the value stored will be inserted into the number- or text-value
        variable. When an attribute is set, the other attribute is set to `None`.

        Parameter
        ---------
        any:
            Value to set in the configuration.
        """
        if self.type in self._supported_number_types:
            self.value_number = new_value
            self.value_text = None
        else:
            self.value_number = None
            self.value_text = new_value

    def get_boolean_value(self):
        """Returns the boolean value from the configuration object's value_text"""
        return self.value_text.lower() == 'true'

    def __json__(self):
        """Returns a jsonify-able representation of the configuration object."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "value_text": self.value_text,
            "value_number": self.value_number
        }
