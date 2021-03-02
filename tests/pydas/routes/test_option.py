import unittest

from pydas_metadata.models import Option
from tests.pydas.mocks import MockContext
from tests.pydas.fixtures import app_client


class TestOptionRoute(unittest.TestCase):
    base_path = "/api/v1/options/"

    def setUp(self):
        self.client = app_client()

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

    def test_get_option(self):
        # arrange
        expected_option = Option(name="range",
                                 feature_name="open",
                                 company_symbol="gme",
                                 option_type="str",
                                 value_text="3m")
        alternate_option = Option(name="range",
                                  feature_name="open",
                                  company_symbol="gme",
                                  option_type="str",
                                  value_text="3m")
        MockContext.setup(
            Option, all=[expected_option, alternate_option], filter=None)

        # act
        res = self.client.get(self.base_path + expected_option.name)

        # assert
        self.assertEqual(len(res.json), 2)
        self.assertEqual(res.json,
                         [expected_option.__json__(), alternate_option.__json__()])
