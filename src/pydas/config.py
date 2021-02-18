"""Server configuration functions and class definitions"""
from configparser import ConfigParser
import logging
from logging.config import fileConfig

# pylint: disable=invalid-name
# Many of the Flask-style config names don't support the default naming convention


def load_config(filepath: str):
    """Reads in a configuration JSON file and returns the generated object"""
    logging.debug('Loading user configuration at path "%s"', filepath)
    parser = ConfigParser()
    if len(parser.read(filepath)) == 0:
        logging.error(
            'Unable to parse configuration file: %s',
            filepath,
            stack_info=True)

    return parser


class Config:
    """Represents configuration for the server, including database details"""

    def __init__(self, config_path: str = 'pydas.ini'):
        self._raw_config = load_config(config_path)
        if 'database' not in self._raw_config:
            raise KeyError(
                "pyDAS INI configuration requires a valid database section.")

        db_config = self._raw_config['database']

        self.DB_DIALECT = db_config['dialect'] if 'dialect' in db_config else None
        self.DB_SERVER = db_config['hostname'] if 'hostname' in db_config else 'localhost'
        self.DB_PORT = db_config['port'] if 'port' in db_config else 3306
        self.DB_NAME = (db_config['initial_catalog']
                        if 'initial_catalog' in db_config
                        else 'pydasadmin')
        self.DB_USER = db_config['username'] if 'username' in db_config else None

    @property
    def DB_URI(self):
        """The connection string URI to access the database"""
        if self.DB_DIALECT == 'mysql':
            return f'mysql://{self.DB_USER}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}'

        if self.DB_DIALECT == 'sqlite':
            return f'sqlite://{self.DB_NAME}'

        raise KeyError(f"Unsupported database dialect: {self.DB_DIALECT}")

    @property
    def DB_CONFIG(self):
        """Returns a dictionary of the database configuration with simplified key names."""
        return {
            'hostname': self.DB_SERVER,
            'port': self.DB_PORT,
            'username': self.DB_USER,
            'database': self.DB_NAME
        }

    @property
    def raw_config(self):
        """The read in configuration object"""
        return self._raw_config

    @classmethod
    def setup_logging(cls, filepath: str):
        '''
        Configures the logging with a given log file. If none
        are provided, then the default 'logs.conf' is used.
        If no logging configuration files are provided or
        found, then the default logging is used.
        '''
        try:
            with open(filepath) as config:
                fileConfig(config)
        except FileNotFoundError:
            pass
