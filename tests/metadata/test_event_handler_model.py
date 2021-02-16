import unittest
from unittest import expectedFailure
import types

from metadata.models import EventHandler


class TestEventHandler(unittest.TestCase):
    def setUp(self):
        self.handler = EventHandler(name='test_handler',
                                    path='tests.metadata.mocks:mock_handler',
                                    type='ON_ERROR')

    def test_handler_call(self):
        # arrange
        uri = 'foo/bar/baz'

        # act
        self.handler(uri, throw=False)

        # assert
        self.assertIsInstance(self.handler.function, types.FunctionType)

    def test_function_throw(self):
        # arrange
        should_throw = True

        with self.assertRaises(KeyError):
            # act - assert
            self.handler('', throw=should_throw)

    def test_throw_if_invalid_handler_path(self):
        # arrange
        path = 'tests.metadata.mocks:this_function_shouldnt_exist'
        self.handler.path = path

        with self.assertRaises(KeyError):
            # act - assert
            self.handler('')
