import logging
from typing import List

from blinker import Signal
from flask.signals import Namespace

from metadata.models import EventHandler
from pydas.routes.utils import get_session

from .type import SignalType

pydas_events = Namespace()


class SignalFactory:
    """API server signalling factory.

    Attributes
    ----------
    signals: List[:class:`metadata.models.EventHandler`]
        Collection of event handlers that are registered with the server.

    pre_acquisition: blinker.Signal
        Signal object for pre-acquisition event handling.

    pre_company: blinker.Signal
        Signal object for pre-company event handling.

    pre_feature: blinker.Signal
        Signal object for pre-feature event handling.

    on_error: blinker.Signal
        Signal object for exception and other error event handling.
    """
    signals: List[EventHandler] = []

    pre_acquisition: Signal = pydas_events.signal('pre-acquisition')
    pre_company: Signal = pydas_events.signal('pre-company')
    pre_feature: Signal = pydas_events.signal('pre-feature')
    post_feature: Signal = pydas_events.signal('post-feature')
    post_company: Signal = pydas_events.signal('post-company')
    post_acquisition: Signal = pydas_events.signal('post-acquisition')

    on_error: Signal = pydas_events.signal('on-error')

    @classmethod
    def register_signals(cls):
        """Registers a new event handler with the signalling factory."""
        logging.debug('Registering signals...')
        session = get_session()
        signals: List[EventHandler] = session.query(EventHandler).all()
        for signal in signals:
            logging.debug('Registering signal: %s', signal.name)
            try:
                cls.__map_signal(signal)
            except KeyError as exc:
                logging.warning(
                    "Unable to register handler '%s': %s", signal.name, exc)
                continue
            except ImportError as exc:
                logging.warning(exc)
                continue

            logging.debug('Registered signal: %s', signal.name)
            cls.signals.append(signal)

        logging.debug('Signals registered!')

    @classmethod
    def get_signals_for_type(cls, signal_type: SignalType):
        """
        Returns all event handlers that are registered for a particular
        event, e.g. ON_ERROR.

        Parameters
        ----------
        :class:`pydas.signals.SignalType`:
            Signal type to filter registered event handlers.

        Returns
        -------
        list[:class:`metadata.models.EventHandler`]:
            Collection of events that match the requested signal type.
        """
        matches = filter(lambda signal: SignalType[signal.type] == signal_type,
                         cls.signals)
        return matches

    @classmethod
    def __map_signal(cls, handler: EventHandler):
        if hasattr(SignalType, handler.type):
            if SignalType[handler.type] == SignalType.PRE_ACQUISITION:
                cls.pre_acquisition.connect(handler.function)
            elif SignalType[handler.type] == SignalType.PRE_COMPANY:
                cls.pre_company.connect(handler.function)
            elif SignalType[handler.type] == SignalType.PRE_FEATURE:
                cls.pre_feature.connect(handler.function)
            elif SignalType[handler.type] == SignalType.POST_FEATURE:
                cls.post_feature.connect(handler.function)
            elif SignalType[handler.type] == SignalType.POST_COMPANY:
                cls.post_company.connect(handler.function)
            elif SignalType[handler.type] == SignalType.POST_ACQUISITION:
                cls.post_acquisition.connect(handler.function)
            elif SignalType[handler.type] == SignalType.ON_ERROR:
                cls.on_error.connect(handler.function)
        else:
            raise KeyError(
                f'Handler with type "{handler.type}" is not supported')
