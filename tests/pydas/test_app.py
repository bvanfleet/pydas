import unittest

from .fixtures import app_client


class TestApplication(unittest.TestCase):
    def test_app_startup(self):
        # arrange
        client = app_client()

        # act
