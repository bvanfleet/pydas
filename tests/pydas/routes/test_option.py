import unittest

from metadata.contexts import ContextFactory
from metadata.models import Option
from tests.pydas.mocks import MockContext
from tests.pydas.fixtures import app_client


class TestOptionRoute(unittest.TestCase):
    base_path = "/api/v1/options/"

    def setUp(self):
        self.client = app_client()
        ContextFactory.supported_contexts += (MockContext,)

    def test_get_index(self):
        # arrange
        expected_option = Option(name="range",
                                 feature_name="open",
                                 company_symbol="gme",
                                 option_type="str",
                                 value_text="3m")
        MockContext.setup(Option, all=[expected_option])

        # act
        res = self.client.get(self.base_path)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertListEqual(res.json, [expected_option.__json__()])

    def test_post_index(self):
        # arrange
        option_json = dict(name="range",
                           feature_name="open",
                           company_symbol="gme",
                           option_type="str",
                           value_text="3m",
                           value_number=None)
        MockContext.setup(Option)

        # act
        res = self.client.post(self.base_path, json=option_json)

        # assert
        self.assertEqual(res.status_code, 201)
