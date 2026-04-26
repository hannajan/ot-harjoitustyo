import uuid


class Department:
    def __init__(self, store_id, name, check_days_before, department_id=None):
        self.department_id = department_id or str(uuid.uuid4())
        self.store_id = store_id
        self.name = name
        self.check_days_before = check_days_before
