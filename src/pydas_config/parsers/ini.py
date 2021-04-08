import configparser

from pydas_config.parsers.base import BaseParser


class IniParser (BaseParser):
    @classmethod
    def parse(cls, **kwargs) -> dict:
        if 'filename' not in kwargs:
            raise KeyError

        parser = configparser.ConfigParser()
        parser.read(kwargs['filename'])

        # Get the global section into a dictionary without the section name.
        global_section = kwargs['global_section'] if 'global_section' in kwargs else 'pydas'
        global_config = {key: value
                         for key, value in parser.items(global_section)}

        # Return a super-dict with global and section maps.
        return {**global_config,
                **{section: {key: value
                             for key, value in parser.items(section)}
                   for section in parser.sections()
                   if section != 'pydas'}}
