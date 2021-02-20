from datetime import datetime
import unittest

from pydas_metadata.contexts import ContextFactory
from pydas_metadata.models import Archive
from tests.pydas.mocks import MockContext
from tests.pydas.fixtures import app_client


class TestArchive(unittest.TestCase):
    base_path = "/api/v1/archives/"

    def setUp(self):
        self.client = app_client()
        ContextFactory.supported_contexts += (MockContext,)

    def test_get_index(self):
        # arrange
        expected_archive = Archive(filename="test1.txt",
                                   company_symbols="test",
                                   date_created=datetime.now())
        MockContext.setup(Archive, all=[expected_archive])

        # act
        res = self.client.get(self.base_path)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertListEqual(res.json, [expected_archive.__json__()])
