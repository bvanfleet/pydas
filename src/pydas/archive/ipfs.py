from datetime import datetime
import logging
from pydas_metadata.contexts.base import BaseContext
from pydas_metadata.models import Archive
from pydas.clients import IpfsArchiveClient


def upload_archive(dataset, connection_string: str, context: BaseContext, **kwargs) -> Archive:
    """
    Uploads a dataset to the IPFS cloud and returns an :class:`metadata.models.Archive`
    object.

    Parameters
    ----------
    dataset: dict | bytes
        Data to be uploaded to IPFS. If the dataset is of type ``dict``, then it needs
        to be jsonify-able.

    connection_string: str
        IPFS cloud connection string. The connection will follow a UNIX-like schema.
        Example: ``/dns/<hostname>/tcp/5000/https``.

    context: :class:`metadata.contexts.base.BaseContext`
        A metadata context to save the resulting :class:`metadata.models.Archive` object.

    **kwargs: dict[str, any]
        Additional arguments for function processing.

    Returns
    -------
    :class:`metadata.models.Archive`:
        An archive metadata object with the filename, address, and company symbols
        (if provided via ``**kwargs``).

    Raises
    ------
    TypeError:
        Raised if the dataset is not of type ``dict`` or ``bytes``.
    """
    client = IpfsArchiveClient(connection_string)
    if isinstance(dataset, dict):
        address = client.upload(dataset)
    elif isinstance(dataset, bytes):
        address = client.upload_bytes(dataset)
    else:
        raise TypeError(
            'Dataset to be uploaded must be a dictionary or bytes.')

    with context.get_session() as session:
        archive: Archive = session.query(Archive).filter(
            Archive.address == address).one_or_none()
        if archive is not None:
            logging.warning(
                'Found matching dataset in IPFS at address: %s.', address)
            company = kwargs['company_symbols'] if 'company_symbols' in kwargs else ''
            if company != '':
                logging.debug('Tagging company with symbol "%s"', company)
                archive.add_company(company)
        else:
            logging.debug('Uploaded dataset to IPFS at address: %s', address)
            symbols = kwargs['company_symbols'] if 'company_symbols' in kwargs else ''
            archive = Archive(address=address,
                              filename=f'dataset_{datetime.now().date().isoformat()}.json',
                              company_symbols=symbols)

        session.add(archive)

    return archive


def download_archive(dataset_id: str, connection_string: str) -> dict:
    """
    Downloads a dataset archived in IPFS and returns the JSON data.

    Parameters
    ----------
    dataset_id: str
        The IPFS address of the dataset to retrieve.

    connection_string: str
        IPFS cloud connection string. The connection will follow a UNIX-like schema.
        Example: ``/dns/<hostname>/tcp/5000/https``.

    Returns
    -------
    dict:
        JSON object retrieved from IPFS.

    Raises
    ------
    TypeError:
        Thrown if either of the parameters is ``NoneType``
    """
    if connection_string is None or connection_string.strip() == '':
        raise TypeError('A valid connection string must be provided')

    if dataset_id is None or dataset_id.strip() == '':
        raise TypeError('A valid dataset ID must be provided')

    client = IpfsArchiveClient(connection_string)
    return client.download_json(dataset_id)
