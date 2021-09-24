import argparse
import sys

from pydas_config.parsers.base import BaseParser


class ArgumentParser (BaseParser):
    '''
    Command-line argument parser.
    '''

    @classmethod
    def parse(cls, **kwargs) -> dict:
        '''
        Parses the command-line arguments and returns a dictionary object with the applied values.
        '''
        arg_parser = argparse.ArgumentParser(prog='pydas-setup',
                                             allow_abbrev=False,
                                             argument_default=argparse.SUPPRESS,
                                             description='''Python Data Acquisition Service
                                             installation script for configuring the metadata
                                             database and REST API on a server.''')

        # Config file path args
        arg_parser.add_argument('-c',
                                '--config',
                                dest='config_file',
                                default='pydas.yaml',
                                help='''Path to pyDAS configuration file (Default: pydas.yaml).''',
                                required=True)

        arg_parser.add_argument('-a',
                                '--alembic',
                                dest='alembic',
                                type=str,
                                default='alembic.ini',
                                help='''Path to alembic configuration file for database development
                                (Default: alembic.ini).''')

        # Database connection args
        arg_parser.add_argument('-d',
                                '--database',
                                dest='database',
                                type=str,
                                default='pydasadmin',
                                help='Database name to deploy metadata database into.')
        arg_parser.add_argument('--dialect',
                                dest='dialect',
                                default='mysql',
                                type=str,
                                help='Database dialect to connect to (Default: mysql).')
        arg_parser.add_argument('-u',
                                '--user',
                                dest='username',
                                type=str,
                                default='root',
                                help='Database username for opening connections.')
        arg_parser.add_argument('-p',
                                '--password',
                                dest='password',
                                type=str,
                                help='Database password for opening connections.')

        # REST API args
        arg_parser.add_argument('--deploy-rest',
                                dest='deploy_rest_api',
                                action='store_true',
                                help='''Flag indicating whether the REST API server should be
                                deployed. DO NOT USE THIS OPTION! uWSGI support is not currently
                                supported and using this flag will result in undefined/unsupported
                                behavior.''')

        # Parse the command line arguments and build the configuration object manually before
        # returning it.
        args = arg_parser.parse_args(sys.argv)
        config = {
            'database': {
                'dialect': args.dialect,
                'initial_catalog': args.database,
                'username': args.username,
                'password': args.password,
                'port': args.port,
                'hostname': args.hostname
            },
            'alembic': {}
        }
        return config
