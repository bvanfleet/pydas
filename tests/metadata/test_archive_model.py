from datetime import datetime
import unittest

from pydas_metadata.contexts import MemoryContext
from pydas_metadata.models import Archive, Base, Entity


class TestArchive(unittest.TestCase):
    def setUp(self):
        self.archive = Archive(address='123abc',
                               filename='test-file.json',
                               company_symbols='aapl,googl',
                               date_created=datetime.now())
        self.context = MemoryContext()
        Base.metadata.create_all(self.context.engine)
        self._preseed_companies()

    def test_add_company(self):
        # arrange
        company = 'msft'
        expected_companies = 'aapl,googl,msft'

        # act
        self.archive.add_company(company)

        # assert
        self.assertEqual(expected_companies,
                         self.archive.company_symbols,
                         f"Company lists don't match! Expected: {expected_companies} | Actual: {self.archive.company_symbols}")

    def test_remove_company(self):
        # arrange
        company = 'googl'
        expected_companies = 'aapl'

        # act
        self.archive.remove_company(company)

        # assert
        self.assertEqual(expected_companies,
                         self.archive.company_symbols,
                         f"Company lists don't match! Expected: {expected_companies} | Actual: {self.archive.company_symbols}")

    def test_get_companies(self):
        # arrange
        expected_companies = ['aapl']
        expected_company_count = 1

        with self.context.get_session() as session:
            # act
            companies = self.archive.companies(session)

            # assert
            self.assertEqual(expected_company_count, len(companies))
            for company in companies:
                self.assertIn(company.identifier, expected_companies)

    def test_from_metadata(self):
        # arrange
        metadata = {
            'address': '123abc',
            'filename': 'test-file.json',
            'company_symbols': 'aapl,googl',
            'date_created': datetime.now()
        }

        # act
        archive = Archive.from_meta(metadata)

        # assert
        self.assertEqual(self.archive.address, archive.address)
        self.assertEqual(self.archive.filename, archive.filename)
        self.assertEqual(self.archive.company_symbols, archive.company_symbols)
        self.assertEqual(self.archive.date_created.date().isoformat(),
                         archive.date_created.date().isoformat())

    def _preseed_companies(self):
        self.aapl = Entity(name='Apple', identifier='aapl')
        self.msft = Entity(name='Microsoft', identifier='msft')

        with self.context.get_session() as session:
            session.add(self.aapl)
            session.add(self.msft)
