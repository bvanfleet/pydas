import argparse

from pydas_config.parsers.base import BaseParser

# TODO: Need to develop this config to match yaml and ini structures more closely.


class ArgumentParser (BaseParser):
    @classmethod
    def parse(cls, **kwargs) -> dict:
        '''
        Configures the command line arguments parser for the script and returns a map of parsed values
        '''
        arg_parser = argparse.ArgumentParser(
            prog='pydas-setup', allow_abbrev=False, argument_default=argparse.SUPPRESS,
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
                                required=False, default='pydasadmin',
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

        return vars(arg_parser.parse_args())
