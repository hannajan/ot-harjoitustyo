import uuid


class Store:
    def __init__(self, name, owner_id, store_id=None):
        self.store_id = store_id or str(uuid.uuid4())
        self.name = name
        self.owner_id = owner_id
