from enum import Enum


class SignalType(Enum):
    '''Supported signal types for use with the sDAS acquisition pipeline.

    Attributes
    ----------
    PRE_ACQUISITION: 1
      Flag for events that should be signalled prior to data acquisition.

    PRE_COMPANY: 2
      Flag for events that should be signalled prior to company metadata processing.

    PRE_FEATURE: 3
      Flag for events that should be signalled prior to feature metadata processing.

    POST_FEATURE: 4
      Flag for events that should be signalled after to feature metadata processing.

    POST_COMPANY: 5
      Flag for events that should be signalled after to company metadata processing.

    POST_ACQUISITION: 6
      Flag for events that should be signalled after to data acquisition.

    ON_ERROR: 7
      Flag for events that should be signalled in the event of an exception.
    '''
    PRE_ACQUISITION = 1
    PRE_COMPANY = 2
    PRE_FEATURE = 3
    POST_FEATURE = 4
    POST_COMPANY = 5
    POST_ACQUISITION = 6
    ON_ERROR = 7
