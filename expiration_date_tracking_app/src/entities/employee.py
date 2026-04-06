from .user import User
from .user_role import UserRole


class Employee(User):
    def __init__(self, username, password, employer_id, user_id=None):
        super().__init__(
            username=username,
            password=password,
            role=UserRole.EMPLOYEE,
            user_id=user_id
            )
        self.employer_id = employer_id
        self.password_is_temporary = True

    def set_password_is_temporary_to_false(self):
        self.password_is_temporary = False

        return self
