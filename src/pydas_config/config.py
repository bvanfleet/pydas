import pathlib
from pydas_config.parsers import get_parser


class Configuration:
    """
    A proxy object for being able to interact with various configuration types
    (e.g. yaml vs command-line arguments).

    Attributes
    ----------
    data: dict
        Configuration raw data dictionary.

    Example
    -------
    >> > from proxy import ConfigSection
    >> > config = ConfigSection('test.ini')
    >> > print(config.version)
    >> > config['author'] = 'John Smith'
    """

    def __init__(self, value=None):
        if value is None:
            self.data = dict()
        elif isinstance(value, str):
            if value == 'args':
                parser = get_parser()
                self.data = parser.parse()
            else:
                path = pathlib.Path(value)
                if not (path.exists() or path.is_file()):
                    raise ValueError(
                        f"Unable to create configuration from file '{value}'")

                parser = get_parser(parser_type=path.suffix.strip("."))
                self.data = parser.parse(filename=value)
        else:
            self.data: dict = value

    def __contains__(self, value):
        return value in self.data

    def __getitem__(self, idx):
        return self.data[idx]

    def __setitem__(self, idx, value):
        self.data[idx] = value

    def __delitem__(self, idx):
        del self.data[idx]

    def __getattr__(self, attr):
        if attr == 'data':
            raise AttributeError

        if attr not in self.data:
            raise KeyError(f"'{attr}' not found in configuration")

        value = self.data[attr]
        if isinstance(value, dict):
            return Configuration(value)

        return value

    def __delattr__(self, attr):
        del self[attr]

    def update(self, value):
        """Updates the configuration with given values.

        Parameters
        ----------
        value: dict | : class: `Configuration`
            Values to update the configuration with.
        """
        if value is None:
            return

        if isinstance(value, dict):
            self.data.update(value)
        elif isinstance(value, Configuration):
            self.data.update(value.data)
        else:
            raise TypeError("Unsupported data type for update values!")

    def get_int(self, attr) -> int:
        """
        Returns the requested attribute as an int.
        """
        return self.get_type(attr, int)

    def get_bool(self, attr) -> bool:
        """
        Returns the requested attribute as a bool.
        """
        return self.get_type(attr, bool)

    def get_str(self, attr) -> str:
        """
        Returns the requested attribute as a str.
        """
        return self.get_type(attr, str)

    def get_type(self, attr: str, _type: type):
        """
        Returns a requested attribute casted to a given type.

        Parameters
        ----------
        attr: str
            Attribute name being requested.

        _type: type
            Type to cast the attribute to.
        """
        value = self[attr]
        if value is not None and not isinstance(value, _type):
            return _type(value)

        return value
