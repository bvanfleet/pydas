def mock_handler(uri: str, **kwargs):
    if 'throw' in kwargs:
        if kwargs['throw'] == True:
            raise KeyError('Throw was set to true')
