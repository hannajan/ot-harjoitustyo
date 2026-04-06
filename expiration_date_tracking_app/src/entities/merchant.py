from .user import User
from .user_role import UserRole


class Merchant(User):
    def __init__(self, username, password, user_id=None):
        super().__init__(
            username=username,
            password=password,
            role=UserRole.MERCHANT,
            user_id=user_id)
        self.stores = None
        self.employees = None
