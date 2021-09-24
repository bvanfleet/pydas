import configparser
import os
import pathlib

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

    @classmethod
    def write(cls, filename: str, data: dict, section_name="pydas", replace=False):
        if data is None:
            raise ValueError("Data cannot be NoneType!")

        if filename is None:
            raise ValueError("A valid filename must be provided.")

        path = pathlib.Path(filename)
        if path.exists() and replace:
            os.remove(filename)

        with open(filename, 'a') as ini:
            ini.write(f"[{section_name}]\n")

        for key, value in data.items():
            if isinstance(value, dict):
                cls.write(filename, value, section_name=key)
            else:
                with open(filename, 'a') as ini:
                    ini.write(f"{key}={value}\n")
