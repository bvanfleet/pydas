from datetime import datetime

from pydas.formatters.base import BaseFormatter


class FileFormatter(BaseFormatter):
    """Data formatter for converting an in-memory data object into a delimited file"""

    @classmethod
    def can_handle(cls, output_format: str) -> bool:
        return output_format.lower() == 'file'

    def transform(self, data: dict, **format_options):
        """
        Transform a data object into a delimited file (typically a comma-delimited file).

        Parameters
        ----------
        data: any
            Data for be formatted.

        format_options: dict
            Additional formatting options.

        Returns
        -------
        str:
            Local filepath to the formatted data file.
        """

        filename = f'data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        full_filename = f'{format_options["output_path"]}/{filename}'

        with open(full_filename, 'w') as file:
            if format_options['include_headers'] in ['True', 'true']:
                file.write(
                    format_options['field_delimiter'].join(data['header']))
                file.write(self.__get_control_character(
                    format_options['row_delimiter']))

            for row in data['values']:
                # TODO: Replace the default text qualifiers with configurable values.
                row = format_options['field_delimiter'].join(f'"{field}"' for field in row)
                file.write(row)
                file.write(self.__get_control_character(
                    format_options['row_delimiter']))

        return full_filename

    def __get_control_character(self, value):
        ctrl_char_map = {
            "\\n": "\n",
            "\\r": "\r",
            "\\r\\n": "\r\n",
            "\\v": "\v"
        }

        if value in ctrl_char_map:
            return ctrl_char_map[value]

        return value
