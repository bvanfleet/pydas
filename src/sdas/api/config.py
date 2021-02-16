"""Server configuration functions and class definitions"""
import json
import logging
from logging.config import fileConfig


def setup_logging(filepath: str = 'logs.conf'):
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


def load_config(filepath: str):
    """Reads in a configuration JSON file and returns the generated object"""
    logging.debug('Loading user configuration at path "%s"', filepath)
    try:
        with open(filepath, "r") as config_file:
            return json.load(config_file)
    except Exception as ex:
        logging.error(
            'Unable to parse configuration file: %s',
            ex,
            stack_info=True)


class ProductionConfig:
    """Represents configuration for the server, including database details"""
    class __Config:
        """Backing class to ProductionConfig"""
        DB_SERVER = 'localhost'
        DB_PORT = 3306
        DB_NAME = 'sdasadmin'
        DB_USER = 'root'

        def __init__(self, db_server, db_port, db_name, db_user):
            self.DB_SERVER = db_server
            self.DB_PORT = db_port
            self.DB_NAME = db_name
            self.DB_USER = db_user

        @property
        def DATABASE_URI(self):
            """The connection string URI to access the database"""
            return f'mysql://{self.DB_USER}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}'

    # The instance property makes this class implement the singleton pattern,
    # since we only want one configuration across the server.
    instance = None
    __raw_config = None

    def __init__(self, configPath='appsettings.json'):
        self.__raw_config = load_config(configPath)
        database_config = self.__raw_config['database']

        if ProductionConfig.instance is None:
            ProductionConfig.instance = ProductionConfig.__Config(
                database_config['hostname'],
                database_config['port'],
                database_config['initial catalog'],
                database_config['user']
            )
        else:
            ProductionConfig.instance.DB_SERVER = database_config['hostname']
            ProductionConfig.instance.DB_PORT = database_config['port']
            ProductionConfig.instance.DB_NAME = database_config['initial catalog']
            ProductionConfig.instance.DB_USER = database_config['user']

    @property
    def raw_config(self):
        """The read in configuration object"""
        return self.__raw_config
