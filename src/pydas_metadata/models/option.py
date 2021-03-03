from sqlalchemy import Column, Float, ForeignKey, String

from pydas_metadata.models.base import Base


class Option(Base):
    """Feature option for providing additional runtime configuration.

    Attributes
    ==========
    name: str
        Option name. May be used during the creation of acquisition query
        parameters. It is recommended that this name matches the name of
        any query parameters that its value may be associated with.

    company_symbol: str
        Company identifier.

    feature_name: str
        Name of the feature the option is associated with.

    option_type: str
        Data type for the feature option. This data type is used to control
        how the underlying data is stored.

    value_text: str
        Data member for storing textual data, including binary and boolean
        values.

    value_number: int | float | decimal
        Data member for storing numeric values, e.g. int or decimal.
    """
    __tablename__ = 'OptionBASE'

    _supported_number_types = ['float', 'int', 'decimal']

    name: str = Column('Name', String, primary_key=True)
    company_symbol: str = Column('CompanySymbol', String, ForeignKey(
        'CompanyFeatureBASE.CompanySymbol'), primary_key=True)
    feature_name: str = Column('FeatureName', String, ForeignKey(
        'CompanyFeatureBASE.FeatureName'), primary_key=True)
    option_type: str = Column('Type', String, nullable=False)
    value_text: str = Column('ValueTXT', String)
    value_number = Column('ValueNBR', Float)

    @property
    def value(self):
        """
        Returns the appropriate value property based upon the option type.
        """
        if self.option_type in self._supported_number_types:
            return self.value_number

        if self.option_type == 'bool':
            return self.get_boolean_value()

        return self.value_text

    @value.setter
    def value(self, new_value):
        if self.option_type in self._supported_number_types:
            self.value_number = new_value
            self.value_text = None
        else:
            self.value_text = new_value
            self.value_number = None

    def get_boolean_value(self):
        """Returns the boolean value from the option's value_text"""
        if isinstance(self.value_text, str):
            return self.value_text.lower() == 'true'

        if isinstance(self.value_text, bool):
            return self.value_text

        raise TypeError('Invalid value set for configuration')

    def __json__(self):
        """Returns a jsonify-able representation of the feature object."""
        return {
            "name": self.name,
            "company_symbol": self.company_symbol,
            "feature_name": self.feature_name,
            "option_type": self.option_type,
            "value": self.value_text,
            "value_number": self.value_number
        }
