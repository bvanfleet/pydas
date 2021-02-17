from datetime import datetime
from enum import Enum
import gzip
from os import path
from pathlib import Path
import shutil
from typing import Any
from zipfile import ZipFile

from pydas.formatters.base import BaseFormatter


class CompressionType(Enum):
    """
    Collection of supported compression types for a :class:`pydas.formatters.CompressionFormatter`.

    Attributes
    ----------
    GZIP: 1
        Gzip compression for archives of extension ``.gz``.

    ZIP: 2
        Zip compression for archives of extension ``.zip``.

    TAR: 3
        Tarball compression for archives of extension ``.tar``.
    """
    GZIP = 1
    ZIP = 2
    TAR = 3

    @classmethod
    def get_compression_type(cls, output_format: str):
        """
        Returns the appropriate compression type identified from the given output format.

        Parameters
        ----------
        output_format: str
            Format used to identify the appropriate compression type.

        Returns
        -------
        :class:`pydas.formatters.compression.CompressionType`:
            Compression type that matches the given output format.

        Raises
        ------
        :class:`KeyError`:
            Thrown if the output format has no identifiable compression type supported.
        """
        output = output_format.lower()
        if output == 'zip':
            return cls.ZIP

        if output in ['gzip', 'gz']:
            return cls.GZIP

        if output in ['tarball', 'tar']:
            return cls.TAR

        raise KeyError('Unsupported compression type given!')


class CompressionFormatter(BaseFormatter):
    @classmethod
    def can_handle(cls, output_format: str) -> bool:
        try:
            CompressionType.get_compression_type(output_format)
            return True
        except KeyError:
            return False

    def transform(self, data: dict, **format_options) -> Any:
        """
        Transform a data object into a compressed file.

        Parameters
        ----------
        data: any
            Data to be formatted.

        format_options: dict
            Additional formatting options.

        Returns
        -------
        str:
            Local filepath to the formatted data file.
        """
        if 'output_format' not in format_options:
            raise KeyError(
                'Output format is required to determine appropriate compression type.')

        output_format = format_options['output_format']
        output_path = format_options['path']
        compression_type = CompressionType.get_compression_type(output_format)
        archives: list = []

        for key, files in data.items():
            filename = f'{key}_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
            if compression_type == CompressionType.ZIP:
                archive_name = path.join(output_path, f'{filename}.zip')
                with ZipFile(archive_name, 'w') as zipfile:
                    for file in files:
                        archive_filename = Path(file)
                        zipfile.write(file,
                                      arcname=archive_filename.name)

                archives.append((key, archive_name))

            if compression_type == CompressionType.GZIP:
                archive_name = path.join(output_path, f'{filename}.gz')
                with gzip.open(archive_name, 'wb') as gzipfile:
                    for file in files:
                        shutil.copyfileobj(file, gzipfile)

                archives.append((key, archive_name))

        return archives
