import logging
from os import path
from pathlib import Path

import boto3
from botocore import UNSIGNED
from botocore.config import Config

from pydas_metadata.contexts.base import BaseContext
from pydas_metadata.models import Entity, Configuration, Feature

from pydas.clients.base import BaseDataClient


class AwsS3Client(BaseDataClient):
    def __init__(self, **kwargs):
        if 'context' not in kwargs:
            raise KeyError('A valid data context must be provided!')

        self.context: BaseContext = kwargs['context']
        self._client = boto3.client('s3',
                                    config=Config(signature_version=UNSIGNED))

    @classmethod
    def can_handle(cls, source: str) -> bool:
        return source.lower() == "aws"

    def get_feature_data(self, feature: Feature, entity: Entity, options: list):
        self._fetch_dataset(entity.identifier, feature.name)

    def _fetch_dataset(self, bucket, key):
        objects = self._client.list_objects(Bucket=bucket, Prefix=key)
        logging.debug('Fetching %s objects from AWS S3...',
                      len(objects["Contents"]))
        base_path_config: Configuration = self.context.get_configuration(
            'outputFilePath')
        logging.debug('Dataset will be stored in %s.', base_path_config.value)

        for obj in objects['Contents']:
            logging.debug('Downloading %s...', obj["Key"])
            object_filename = path.normpath(path.join(base_path_config.value,
                                                      bucket,
                                                      obj['Key']))
            if not path.exists(path.dirname(object_filename)):
                logging.debug('Creating subdirectory %s...',
                              path.dirname(object_filename))
                Path(path.dirname(object_filename)).mkdir(parents=True)

            self._client.download_file(Bucket=bucket,
                                       Key=obj['Key'],
                                       Filename=object_filename)
            logging.debug('Dataset object downloaded!')
