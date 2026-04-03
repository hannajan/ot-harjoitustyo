from .user import User
from .user_role import UserRole


class Merchant(User):
    def __init__(self, username, password):
        super().__init__(username=username, password=password, role=UserRole.MERCHANT)
