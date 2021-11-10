from abc import ABCMeta, abstractmethod

from pydas_metadata.models import Entity, Feature


class BaseDataClient(metaclass=ABCMeta):
    @abstractmethod
    def get_feature_data(self, feature: Feature, entity: Entity, options: list):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def can_handle(cls, source: str) -> bool:
        raise NotImplementedError()
