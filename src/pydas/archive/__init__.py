'''
This module will provide the functionality for sDAS to archive data sets. This
module relies on additional modules scattered around the sDAS project repo,
such as: metadata.models.archive and pydas.routes.archive. This module
provides the post-acquisition handler functionality specifically.

Any Archive handler that uploads data will follow the basic form:

``def archive_upload_func(dataset: dict) -> str``

In this form, the return of the function will be the address of the dataset
that was archived. If the dataset is invalid, then a TypeError will be raised.
'''
import logging

from pydas_metadata.contexts import DatabaseContext

from .ipfs import download_archive
from .ipfs import upload_archive


def archive_handler(*args, **kwargs):
    """Stores the given dataset within the IPFS archive."""
    if 'data' not in kwargs:
        raise KeyError('Dataset for archive must not be NoneType.')

    symbols = kwargs['company_symbol'] if 'company_symbol' in kwargs else ''
    context = DatabaseContext('pydasadmin', 'root')
    connection_string = context.get_configuration(
        'archiveIpfsConnectionString')

    if connection_string is None:
        raise TypeError(
            'No IPFS connection string found, please configure archive connection string!')

    return upload_archive(kwargs['data'],
                          connection_string.value,
                          context,
                          company_symbols=symbols)
