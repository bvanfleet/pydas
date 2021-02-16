from abc import ABCMeta, abstractmethod

from metadata.models import Company, Feature


class BaseDataClient(metaclass=ABCMeta):
    @abstractmethod
    def get_feature_data(self, feature: Feature, company: Company, options: list):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def can_handle(cls, source: str) -> bool:
        raise NotImplementedError()
