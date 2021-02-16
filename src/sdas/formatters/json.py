
import logging
from typing import Any, Callable

from sdas.constants import SdasConstants, UtilityConstants
from sdas.formatters.base import BaseFormatter


class JsonFormatter(BaseFormatter):
    @classmethod
    def can_handle(cls, output_format: str) -> bool:
        return output_format == 'json'

    def transform(self, data: dict, **format_options) -> Any:
        # Create merged data container
        output = {
            'header': ['date'],
            'values': []
        }

        # merge in data from all lists
        for k, v in data.items():
            self._merge_list(output, k, v)

        return output

    def _merge_list(self, master: dict, key: str, values: list):
        logging.debug('Merging feature "%s" into output...', key)
        header_count = len(master[SdasConstants.header_property])
        for value in values:
            # Get index for row containing date (if found)
            def predicate(point):
                return point == value[1]

            idx = self._get_index(
                master[SdasConstants.multi_value_property], predicate)

            # Add missing dates and normalize row to insert missing column values
            if idx == -1:
                master[SdasConstants.multi_value_property].append([value[1], ])
                self._normalize_row(master[SdasConstants.multi_value_property][idx],
                                    header_count)

            # Append value to normalized row
            master[SdasConstants.multi_value_property][idx].append(value[0])

        # Update header collection and perform final normalization
        master[SdasConstants.header_property].append(key)
        header_count = len(master[SdasConstants.header_property])
        self._normalize_collection(master[SdasConstants.multi_value_property],
                                   header_count)

    def _get_index(self, source: list, predicate: Callable[[Any], bool]):
        for i, val in enumerate(source):
            if predicate(val[0]):
                return i

        return -1

    def _normalize_collection(self, collection: list, size: int):
        for row in collection:
            self._normalize_row(row, size)

    def _normalize_row(self, row: list, size: int):
        if len(row) < size:
            for _ in range(size - len(row)):
                row.append(UtilityConstants.str_empty)
