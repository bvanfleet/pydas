class Field:
    def __init__(self, data_type: type, is_required=True):
        self.data_type = data_type
        self.is_required = is_required
        # TODO: Determine if we should validate a range of acceptable values (e.g. DB dialect)

    def validate(self, value) -> bool:
        if value is None:
            return not self.is_required

        return isinstance(value, self.data_type)
