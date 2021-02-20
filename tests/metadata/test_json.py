import unittest
from pydas_metadata import json


class MockImplementsJson:
    def __init__(self, value):
        self.value = value

    def __json__(self):
        return {
            'value': self.value
        }


class MockNotImplementJson:
    def __init__(self, value):
        self.value = value


class TestJson(unittest.TestCase):
    def setUp(self):
        self.valid_mock = MockImplementsJson('test')
        self.invalid_mock = MockNotImplementJson('test')

    def test_implements_json(self):
        # arrange
        expected_json = {
            'value': 'test'
        }

        # act
        result = json(self.valid_mock)

        # assert
        self.assertDictEqual(expected_json, result)

    def test_returns_str_json(self):
        # arrange
        expected_result = '{"value": "test"}'

        # act
        result = json(self.valid_mock, True)

        # assert
        self.assertEqual(expected_result, result)

    def test_throw_if_json_not_implemented(self):
        # arrange
        with self.assertRaises(AttributeError):
            # act
            json(self.invalid_mock)
