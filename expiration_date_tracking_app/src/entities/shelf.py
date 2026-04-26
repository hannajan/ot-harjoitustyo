import uuid


class Shelf:
    def __init__(self, department_id, name, is_default=False, shelf_id=None):
        self.shelf_id = shelf_id or str(uuid.uuid4())
        self.department_id = department_id
        self.name = name
        self.is_default = is_default
