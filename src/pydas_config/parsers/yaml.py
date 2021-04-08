import yaml
from pydas_config.parsers.base import BaseParser


class YamlParser (BaseParser):
    @classmethod
    def parse(cls, **kwargs) -> dict:
        if 'filename' not in kwargs:
            raise KeyError

        with open(kwargs['filename']) as file:
            data = yaml.load(file, Loader=yaml.Loader)
            return data
