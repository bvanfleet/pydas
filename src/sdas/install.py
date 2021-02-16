"""
Command-line script for automating installation of stock data acquisition service
"""
import argparse
from alembic.config import Config
from alembic import command


def parse_arguments():
    '''
    Configures the command line arguments parser for the script and returns a map of parsed values
    '''
    arg_parser = argparse.ArgumentParser(
        prog='sdas-setup', allow_abbrev=False, argument_default=argparse.SUPPRESS,
        description='''
        Stock Data Acquisition Service installation script for configuring the
        metadata database and REST API on a server.
        ''')

    # Config file path args
    arg_parser.add_argument('-a', '--alembic', dest='alembic', type=str,
                            required=False, default='alembic.ini',
                            help='Path to alembic configuration file (typically alembic.ini)')

    # Database connection args
    arg_parser.add_argument('-d', '--database', dest='database', type=str,
                            required=False, default='sdasadmin',
                            help='Database name to deploy metadata database into')
    arg_parser.add_argument('-u', '--user', dest='username', type=str,
                            required=False, default='root',
                            help='Database username for opening connections')
    arg_parser.add_argument('-p', '--password', dest='password', type=str, required=False,
                            help='Database password for opening connections')

    # REST API args
    arg_parser.add_argument('--deploy-rest', dest='deploy_rest_api',
                            action='store_true', default=False,
                            help='''
                            Flag indicating whether the REST API server should be deployed.
                            DO NOT USE THIS OPTION! uWSGI support is not currently supported
                            and using this flag will result in undefined/unsupported behavior.
                            ''')

    return arg_parser.parse_args()


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
    #         '/tmp/sdas.sock',
    #         '--manage-script-name',
    #         '--mount',
    #         '/sdas=src/api/server:app'])
    # except subprocess.CalledProcessError as exc:
    #     print(exc)
    print('REST API server deployment is not yet supported')


def main():
    '''Primary entry point for the installation script.'''
    args = parse_arguments()
    db_pass = args.password if 'password' in args else ''
    db_connect_str = create_connection_string(
        args.username, db_pass, args.database)
    setup_database(args.alembic, db_connect_str)

    if args.deploy_rest_api:
        deploy_server()


if __name__ == '__main__':
    main()
