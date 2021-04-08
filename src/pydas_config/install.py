"""
Command-line script for automating installation of stock data acquisition service
"""
from alembic.config import Config
from alembic import command

from pydas_config.builder import build_config


def create_connection_string(username, password, database):
    """Returns the formatted connection string to connect to MySQL instance"""
    return f'mysql://{username}:{password}@localhost:3306/{database}'


def setup_database(alembic_ini, connection_string):
    """Deploys the sDASAdmin database using alembic migrations
    Parameters
    ----------
    alembic_ini: str
        Path to alembic.ini file
    """
    alembic_cfg = Config(alembic_ini)
    alembic_cfg.set_main_option('sqlalchemy.url', connection_string)
    command.upgrade(alembic_cfg, "head")


def deploy_server():
    '''Deploys the sDAS REST API server'''
    # TODO: Determine how we can best automate the deployment of the REST API,
    #  we'll probably use uWSGI. However, would the following be the best
    #  method of doing this, or could we use a config file to better control
    #  the deployment?
    # try:
    #     subprocess.check_call([
    #         'uwsgi',
    #         '-s',
    #         '/tmp/pydas.sock',
    #         '--manage-script-name',
    #         '--mount',
    #         '/pydas=src/api/server:app'])
    # except subprocess.CalledProcessError as exc:
    #     print(exc)
    print('REST API server deployment is not yet supported')


def main():
    '''Primary entry point for the installation script.'''
    config = build_config(['pydas.yaml'])
    db_pass = config.database.password if 'password' in config.database else ''
    db_connect_str = create_connection_string(
        config.database.username,
        db_pass,
        config.database.initial_catalog)
    setup_database(config.alembic, db_connect_str)

    if 'api' in config:
        deploy_server()


if __name__ == '__main__':
    main()
