import json as j


def json(model, as_str=False):
    '''
    Returns as JSON representation of the object.

    Parameters
    ----------
    as_str: bool
      Flag indicating whether a ``dict`` or string JSON representation
      should be returned. Default is ``False``, or ``dict`` form.

    Returns
    -------
    str:
      String form of JSON representation if ``as_str`` is ``True``.

    dict:
      Dictionary form of JSON representation. Default, or if
      ``as_str`` is ``False``.

    Raises
    ------
    AttributeError:
      Raised if of the model given doesn't implement the ``__json__``
      function.
    '''
    if not hasattr(model, '__json__'):
        raise AttributeError('Model does not implement the __json__ function.')

    if as_str:
        return j.dumps(model.__json__())

    return model.__json__()
