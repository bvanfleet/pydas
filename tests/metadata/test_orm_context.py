import unittest
from metadata.contexts import DatabaseContext, MemoryContext
from metadata.models import Base, Configuration


class TestOrmContext(unittest.TestCase):
    """Provides initial unit testing for the ORM package used by the sDAS system."""

    def test_can_connect(self):
        # arrange
        context = DatabaseContext('sdasadmin', 'root')
        session_factory = context.get_session_maker()

        # act
        session = session_factory()

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
        session = context.get_session_maker()()
        session.add(Configuration(name='test1', type='str', value_text='foo'))
        session.commit()

        for case in cases:
            with self.subTest(name=case['name'], is_none=case['is_none']):
                # act
                config = context.get_configuration(case['name'])

                # assert
                if case['is_none']:
                    self.assertIsNone(config)
                else:
                    self.assertIsNotNone(config)
