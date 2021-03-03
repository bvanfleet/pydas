# pylint: disable=C0114,C0115,C0116
# TODO: Determine how we can move the above rules into a pylintrc file for the testing directory
import unittest
import json

from pydas_metadata.models import Configuration


class TestConfigurationModel(unittest.TestCase):
    def test_valid_true(self):
        true_values = ['True', 'true']

        for value in true_values:
            with self.subTest(value=value):
                # arrange
                config = Configuration(value_text=value)

                # act
                actual_value = config.get_boolean_value()

                # assert
                self.assertTrue(actual_value)

    def test_returns_false_for_invalid_value(self):
        # arrange
        config = Configuration(value_text='FooBarBaz')

        # act
        actual_value = config.get_boolean_value()

        # assert
        self.assertFalse(actual_value)

    def test_returns_number_for_numeric_type(self):
        test_cases = [
            ('int', 42),
            ('float', 123.0),
            ('decimal', 456.789)
        ]

        for case in test_cases:
            with self.subTest(type=case[0], value=[1]):
                # arrange
                config = Configuration(name='test', type=case[0])

                # act
                config.value = case[1]

                # assert
                self.assertEqual(case[1], config.value)
                self.assertIsNotNone(config.value_number)

    def test_returns_string_for_nonnumeric_types(self):
        test_cases = [
            ('str', 'abc'),
            ('bytes', 'some bytes')
        ]

        for case in test_cases:
            with self.subTest(type=case[0], value=case[1]):
                # arrange
                config = Configuration(name='test', type=case[0])

                # act
                config.value = case[1]

                # assert
                self.assertEqual(case[1], config.value)
                self.assertIsNotNone(config.value_text)

    def test_returns_bool_for_bool_types(self):
        test_cases = {
            "true": True,
            "TRUE": True,
            True: True,
            "false": False,
            False: False
        }

        for value, expected in test_cases.items():
            with self.subTest(value=value, expected=expected):
                # arrange
                config = Configuration(name='test',
                                       type='bool',
                                       value_text=value)

                # act
                result = config.value

                # assert
                self.assertIsInstance(result, bool)
                self.assertEqual(expected, result)

    def test_json(self):
        # arrange
        config_id = 1
        name = 'test'
        config_type = 'str'
        value_text = 'testing'
        value_number = None

        expected_json = json.dumps({
            "id": config_id,
            "name": name,
            "type": config_type,
            "value_text": value_text,
            "value_number": value_number
        })

        config = Configuration(id=config_id,
                               name=name,
                               type=config_type,
                               value_text=value_text,
                               value_number=value_number)

        # act
        actual_json = json.dumps(config.__json__())

        # assert
        self.assertEqual(expected_json,
                         actual_json,
                         f"JSON doesn't match! Expected: {expected_json} | Actual: {actual_json}")
