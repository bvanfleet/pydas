from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from pydas_metadata import models
from pydas_metadata.models.base import Base, Jsonifiable


class Archive(Base, Jsonifiable):
    '''
    Contains metadata for storing datasets within a file archival system.

    Attributes
    ----------
    address: str
        The dataset resource address for retrieving the dataset file. In an
        IPFS archive, this address will correlate to the hash of the uploaded
        dataset.

    filename: str
        Filename of the dataset that's stored in the archive. This value may be
        system generated if the archive system does not create a filename.

    date_created: datetime
        Date and time the dataset was created. If the specific time is unavailable,
        then just the time will be set to T00:00:00.000. All dates should be set
        and returned in an ISO format.

    company_symbols: str
        Comma-delimited list of company symbols associated with the dataset.
    '''
    __tablename__ = 'ArchiveBASE'

    address: str = Column('AddressTXT', String(255), primary_key=True)
    filename: str = Column('FileNM', String(255), nullable=False)
    date_created: datetime = Column(
        'CreatedDTS', DateTime, default=func.now(), nullable=False)
    company_symbols: str = Column(
        'CompanySymbolsTXT', String(255), nullable=False)

    # TODO: Consider adding statistical columns to this, such as download count.

    def companies(self, session: Session) -> list:
        '''
        Returns all companies associated with the archived dataset.

        Parameters
        ----------
        session: sqlalchemy.orm.Session
            Metadata database session for retrieving all :class:`metadata.models.Company` objects.

        Returns
        -------
        list[metadata.models.Company]:
            Collection of companies associated with this archived dataset.
        '''
        symbols = self.company_symbols.split(',')
        companies = session.query(models.Company).filter(
            models.Company.symbol.in_(symbols))
        return companies.all()

    def add_company(self, company_symbol: str):
        '''
        Appends a given company symbol to the archive symbol list if the symbol
        is not present in the current list. Otherwise, this is a no-op.

        Parameters
        ----------
        company_symbol: str
          Company symbol to append to the symbol list.
        '''
        symbols = self.company_symbols.split(',')
        if company_symbol not in symbols:
            symbols.append(company_symbol)
            self.company_symbols = (',').join(symbols)

    def remove_company(self, company_symbol: str):
        '''
        Removes a given company symbol from the archive symbol list if the
        symbol is not present in the current list. Otherwise, this is a no-op.

        Parameters
        ----------
        company_symbol: str
          Company symbol to remove from the symbol list.
        '''
        symbols = self.company_symbols.split(',')
        if company_symbol in symbols:
            retain = [symbol for symbol in symbols if symbol != company_symbol]
            self.company_symbols = (',').join(retain)

    @classmethod
    def from_meta(cls, metadata: dict):
        """Parses a metadata dictionary object and returns and Archive instance.

        Parameters
        ----------
        metadata: dict
            Raw dictionary object used to construct the Archive instance.

        Returns
        -------
        Archive:
            Dataset archive instance with values set from metadata dictionary.

        Raises:
        -------
        KeyError:
            Raised if any of the required properties is not found within the
            metadata dictionary.
        """
        return Archive(
            address=_get_meta_property('address', metadata),
            filename=_get_meta_property('filename', metadata),
            date_created=_get_meta_property('date_created', metadata),
            company_symbols=_get_meta_property('company_symbols', metadata))

    def __json__(self):
        """Returns a jsonify-able representation of the Archive object."""
        return {
            'address': self.address,
            'filename': self.filename,
            'date_created': self.date_created.isoformat(),
            'company_symbols': self.company_symbols
        }


def _get_meta_property(property_name: str, metadata: dict):
    if property_name not in metadata:
        raise KeyError(
            f'Expected property "{property_name}" in metadata, but none found!')

    return metadata[property_name]
