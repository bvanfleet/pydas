import unittest
from pydas_metadata.contexts import DatabaseContext, MemoryContext
from pydas_metadata.models import Base, Configuration


class TestOrmContext(unittest.TestCase):
    """Provides initial unit testing for the ORM package used by the sDAS system."""

    def test_can_connect(self):
        # arrange
        context = DatabaseContext('pydasadmin', 'root')

        # act
        with context.get_session() as session:
            # assert
            self.assertIsNotNone(
                session,
                "Expected the session returned from the context session factory to not be None.")

    def test_get_config(self):
        # arrange
        cases = [
            {'name': 'test1', 'is_none': False},
            {'name': 'test2', 'is_none': True}
        ]

        context = MemoryContext()
        Base.metadata.create_all(context.engine)
        with context.get_session() as session:
            session.add(Configuration(
                name='test1', type='str', value_text='foo'))

        for case in cases:
            with self.subTest(name=case['name'], is_none=case['is_none']):
                # act
                config = context.get_configuration(case['name'])

                # assert
                if case['is_none']:
                    self.assertIsNone(config)
                else:
                    self.assertIsNotNone(config)
                    self.assertEqual(config, 'foo')
