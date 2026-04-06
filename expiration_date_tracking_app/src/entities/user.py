import uuid
import bcrypt
from .user_role import UserRole


def _hash_password(password):
    if password:
        if isinstance(password, str):
            if not password.startswith("$2b$"):
                return bcrypt.hashpw(password.encode("utf-8"),
                                     bcrypt.gensalt()).decode("utf-8")
        if isinstance(password, bytes):
            if not password.startswith(b"$2b$"):
                return bcrypt.hashpw(password, bcrypt.gensalt())
        return password

    raise ValueError("Password must be provided")


class User:
    def __init__(self, username, role, password=None, user_id=None):
        self.user_id = user_id or str(uuid.uuid4())
        self.username = username
        self.password_is_temporary = False
        self.employer_id = None
        self.password = _hash_password(password)

        if role in (UserRole.EMPLOYEE, UserRole.MERCHANT):
            self.role = role
        else:
            raise ValueError("Invalid role")

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def set_password(self, new_password):
        self.password = bcrypt.hashpw(new_password.encode("utf-8"),
                                      bcrypt.gensalt()).decode("utf-8")
        return self

    def is_employee(self):
        return self.role == UserRole.EMPLOYEE
