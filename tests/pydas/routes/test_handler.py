import unittest

from metadata.contexts import ContextFactory
from metadata.models import Handler
from tests.pydas.mocks import MockContext
from tests.pydas.fixtures import app_client


class TestHandlerRoute(unittest.TestCase):
    base_path = "/api/v1/handlers/"

    def setUp(self):
        self.client = app_client()
        ContextFactory.supported_contexts += (MockContext,)

    def test_get_index(self):
        # arrange
        expected_handler = Handler(id=1,
                                   name="test_handler")
        MockContext.setup(Handler, all=[expected_handler])

        # act
        res = self.client.get(self.base_path)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertListEqual(res.json, [expected_handler.__json__()])
