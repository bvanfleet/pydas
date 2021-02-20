from pydas_metadata.contexts import BaseContext


class MockContext(BaseContext):
    engine = None

    def __init__(self, **config):
        # We're not going to bother doing anything here as it's all a mock anyway.
        pass

    @classmethod
    def can_handle(cls, context_type):
        return context_type == "mock"

    def get_session_maker(self):
        def mock_session_maker():
            return MockSession()

        return mock_session_maker

    @classmethod
    def setup(cls, model: object, **query_config):
        MockSession.instances[model.__class__.__name__] = query_config


class MockSession:
    instances = {}

    def query(self, model: object):
        return MockQuery(**MockSession.instances[model.__class__.__name__])

    def add(self, *args):
        pass

    def commit(self, *args):
        pass


class MockQuery:
    def __init__(self, **config):
        self.config = config
        self.predicate = None

    def filter(self, predicate):
        self.predicate = predicate
        return self

    def __getattribute__(self, name: str):
        if name in ('config', 'predicate', 'filter'):
            return object.__getattribute__(self, name)

        if name not in self.config:
            raise AttributeError(f"MockSession does not have attribute {name}")

        return_value = self.config[name]
        return lambda *args, **kwargs: return_value
