"""
Command-line script for automating installation of stock data acquisition service
"""
from alembic.config import Config
from alembic import command

from pydas_config import build_config, Configuration
from pydas_config.parsers import get_parser


def create_connection_string(username: str, password: str, port: int, database: str):
    """Returns the formatted connection string to connect to MySQL instance"""

    # TODO: Determine better way of writing this to support both MySQL and SQLite databases.
    return f'mysql://{username}:{password}@localhost:{port}/{database}'


def setup_database(config: Configuration, connection_string):
    """Deploys the sDASAdmin database using alembic migrations"""
    alembic_cfg = Config()
    alembic_cfg.set_main_option('script_location', config.script_location)
    alembic_cfg.set_main_option('sqlalchemy.url', connection_string)
    command.upgrade(alembic_cfg, "head")


def deploy_server(config: dict):
    '''Deploys the sDAS REST API server'''
    uwsgi = {
        'socket': f'{config.hostname}:{config.get_int("port")}',
        'chdir': config.path,
        'pythonpath': config.pythonpath,
        'uid': config.username,
        'gid': config.group,
        'manage-script-name': True,
        'mount': config.mount,
        'virtualenv': config.envpath
    }
    writer = get_parser('ini')
    writer.write('pydas.ini', uwsgi, replace=True)


def main():
    '''Primary entry point for the installation script.'''
    config: Configuration = build_config('pydas.yaml')
    db_pass = config.database.password if 'password' in config.database else ''
    db_connect_str = create_connection_string(
        config.database.username,
        db_pass,
        config.database.get_int('port'),
        config.database.initial_catalog)
    setup_database(config.alembic, db_connect_str)

    if 'api' in config:
        deploy_server(config.uwsgi)


if __name__ == '__main__':
    main()
