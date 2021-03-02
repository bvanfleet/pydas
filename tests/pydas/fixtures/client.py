from pydas import create_app
from pydas_metadata.contexts import ContextFactory
from pydas_metadata.models.event_handler import EventHandler

from tests.pydas.mocks import MockContext


def app_client():
    ContextFactory.supported_contexts += (MockContext,)
    MockContext.setup(EventHandler, all=list())

    app = create_app('test_pydas.yaml')
    return app.test_client()
