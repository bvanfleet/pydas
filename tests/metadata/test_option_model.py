import unittest

from pydas_metadata.models import Option


class TestOption(unittest.TestCase):
    def test_numeric_value(self):
        # arrange
        option = Option(name="minPrice", option_type="float")

        # act
        option.value = 30000

        # assert
        self.assertEqual(30000, option.value)
        self.assertIsInstance(option.value, int)

    def test_str_value(self):
        # arrange
        option = Option(name="colour", option_type="str")

        # act
        option.value = "Black"

        #  assert
        self.assertEqual("Black", option.value)
        self.assertIsInstance(option.value, str)

    def test_bool_value(self):
        # arrange
        test_cases = {
            "true": True,
            "TRUE": True,
            "True": True,
            "False": False,
            "false": False,
            "StrValue": False
        }

        for value, expected in test_cases.items():
            with self.subTest(value=value, expected=expected):
                # arrange
                option = Option(name="is_enabled",
                                option_type="bool",
                                value_text=value)

                # act
                result = option.value

                #  assert
                self.assertEqual(expected, result)
                self.assertIsInstance(result, bool)

    def test_json(self):
        # arrange
        expected_output = {
            "name": "colour",
            "company_symbol": "F",
            "feature_name": "make",
            "option_type": "str",
            "value": "Black",
            "value_number": None
        }
        option = Option(company_symbol="F",
                        feature_name="make",
                        name="colour",
                        option_type="str",
                        value_text="Black")

        # act
        json_option = option.__json__()

        # assert
        self.assertDictEqual(expected_output, json_option)
