import unittest
from pydas_metadata.models import Feature, Handler


class TestFeatureModel(unittest.TestCase):
    def setUp(self):
        self.handler = Handler(id=1, name='test_handler')
        self.feature = Feature(name='TestFeature',
                               uri='path/to/data',
                               handler_id=1,
                               description='This is a test feature',
                               handler_metadata=self.handler)

    def test_json(self):
        # arrange
        expected_json = {
            'name': 'TestFeature',
            'description': 'This is a test feature',
            'uri': 'path/to/data',
            'handler': {
                'id': 1,
                'name': 'test_handler'
            }
        }

        # act
        actual_json = self.feature.__json__()

        # assert
        self.assertEqual(expected_json,
                         actual_json,
                         f"JSON doesn't match! Expected: {expected_json} | Actual: {actual_json}")

    def test_get_value(self):
        test_rows = [
            ({'OtherFeature': 'badValue', 'date': '2012-12-21'}, False),
            ({'TestFeature': 'goodValue', 'date': '2020-12-32'}, True)
        ]

        expected_tuple = ('goodValue', '2020-12-32')

        for row in test_rows:
            with self.subTest(row=row):
                # arrange
                data = row[0]
                should_extract = row[1]

                # act
                result = self.feature.get_value(data)

                # assert
                if should_extract:
                    self.assertIsInstance(result, tuple)
                    self.assertTupleEqual(
                        expected_tuple,
                        result,
                        f"Values don't match! Expected: {expected_tuple} | Actual: {result}")
                else:
                    self.assertIsInstance(result, str)
                    self.assertEqual(
                        '', result, f'Expected an empty string! Actual: {result}')

    def test_get_values(self):
        # arrange
        expected_list = [('Value1', '2020-12-01'),
                         '',
                         ('Value3', '2020-12-03')]
        data = [{'TestFeature': 'Value1', 'date': '2020-12-01'},
                {'OtherTestFeature': 'Value2', 'date': '2020-12-02'},
                {'TestFeature': 'Value3', 'date': '2020-12-03'}]

        # act
        result = self.feature.get_values(data)

        # assert
        self.assertIsInstance(result, list)
        self.assertEqual(3, len(result))
        self.assertListEqual(expected_list, result)
