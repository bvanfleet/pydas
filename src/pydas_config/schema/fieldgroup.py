class FieldGroup:
    def __init__(self, fields: dict, is_required=True):
        self.fields = fields
        self.is_required = is_required

    def __getitem__(self, name):
        if name in self.fields:
            return self.fields[name]

        raise KeyError(f"Invalid schema field name provided: {name}")
