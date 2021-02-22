"""Server configuration functions and class definitions"""
from logging.config import dictConfig

from dependency_injector.errors import Error

from pydas.containers import config_container

# pylint: disable=invalid-name
# Many of the Flask-style config names don't support the default naming convention


class Config:
    """Represents configuration for the server, including database details"""

    def __init__(self, config_path: str):
        config_container.config.from_yaml(config_path)
        self.TESTING = config_container.config.testing() or False

        with config_container.config.database as db_config:
            self.DB_DIALECT = db_config.dialect()
            self.DB_SERVER = db_config.hostname() or 'localhost'
            self.DB_PORT = db_config.port() or 3306
            self.DB_NAME = db_config.initial_catalog() or 'pydasadmin'
            self.DB_USER = db_config.username()

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

    @classmethod
    def setup_logging(cls, filepath: str):
        '''
        Configures the logging with a given log file. If none
        are provided, then the default 'logs.conf' is used.
        If no logging configuration files are provided or
        found, then the default logging is used.
        '''
        config_container.config.from_yaml(filepath, required=True)
        try:
            dictConfig(config_container.config.logging())
        except Error:
            pass
