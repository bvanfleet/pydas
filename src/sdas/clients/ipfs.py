import logging

import ipfshttpclient as ipfs


class IpfsArchiveClient:
    """
    An HTTP client wrapper for uploading and downloading datasets in a IPFS.
    """

    def __init__(self, connection_string: str = None):
        if connection_string:
            self._client = ipfs.connect(connection_string, session=True)
        else:
            self._client = ipfs.connect(session=True)

    def upload(self, data) -> str:
        '''
        Uploads a dataset to IPFS and returns the address hash

        Parameters
        ----------
        data: any
            Data to be uploaded to IPFS.

        Returns
        -------
        str:
            IPFS address to retrieve the data from.

        Raises
        ------
        TypeError:
            Thrown if the data passed is ``NoneType``.
        '''
        if data is None:
            raise TypeError('Unable to upload null dataset.')

        logging.debug('Uploading JSON dataset to IPFS archive...')
        return self._client.add_json(data)

    def upload_bytes(self, data) -> str:
        if data is None:
            raise TypeError('Unable to upload null dataset.')

        logging.debug('Uploading dataset bytes to IPFS archive...')
        return self._client.add_bytes(data)

    def download(self, address: str, destination: str):
        """
        Downloads a dataset file from IPFS and saves it to the given destination.

        Parameters
        ----------
        address: str
            The IPFS address to retrieve the dataset from.

        destination: str
            The location to save the downloaded file to.
        """
        logging.debug(f'Downloading dataset at address: {address}')
        self._client.get(address, destination)

    def download_json(self, address: str) -> dict:
        """
        Downloads and returns JSON data from IPFS.

        Parameters
        ----------
        address: str
            The IPFS address to retrieve the dataset JSON from.

        Returns
        -------
        dict:
            JSON object retrieved from IPFS.
        """
        logging.debug(f'Downloading JSON dataset at address {address}')
        return self._client.get_json(address)

    def close(self):
        '''Closes the IPFS HTTP client.'''
        self._client.close()
