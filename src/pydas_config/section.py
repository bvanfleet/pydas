"""
So the big question is why?

Answer:

First, and foremost, to provide a common interface between several methods of storing configuration
data. Providing a common interface, or facade, helps with maintainability of this project, since I
can change the backend to add support for more types and current users might not care as long as
their code still works with reasonable expectations.

Second, providing a proxy object like this can allow for more interesting things, such as app setup
logging shortly after the configuration objects are read in. This might be beneficial to see if
there are chokepoints in how an application handles (e.g. passing data that configparser
interpretted as str vs int).

Lastly, and what will probably be the most influential answer, because I wanted to.
"""

import pathlib
from pydas_config.parsers import get_parser


class ConfigSection:
    """
    A proxy object for being able to interact with various configuration types
    (e.g. yaml vs command-line arguments).

    Attributes
    ----------
    data: dict
        Configuration raw data dictionary.

    Example
    -------
    >>> from proxy import ConfigSection
    >>> config = ConfigSection('test.ini')
    >>> print(config.version)
    >>> config['author'] = 'John Smith'
    """

    def __init__(self, value):
        # Some cases that this should handle:
        # 1. Parse CLI arguments: ConfigSection('args')
        # 2. Parse file: ConfigSection('config.yaml')
        # 3. Set dict object
        # 4. Set data to None
        #
        # I'll want to write up some unit tests for this and go from there.
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

        value = self.data[attr]
        if isinstance(value, dict):
            ConfigSection(value)

        return value

    def __delattr__(self, attr):
        del self[attr]

    # def update(self, updates):
    #     """Updates a ConfigSection with values from another ConfigSection."""
    #     new_data = dict()
    #     new_data.update(self.data)
    #     new_data.update(updates.data)
    #     self.data = new_data
