from entities.merchant import Merchant

from repositories.user_repository import (
    user_repository as default_user_repository
)


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self._user_repository = user_repository
        self._user = None

    def register_merchant(self, username=None, password=None):
        if not username or not password:
            raise ValueError("Username or password missing")

        # username is at least 5 charaters long
        if len(username) < 5:
            raise ValueError("Username must be at least 5 characters long")

        # username is unique
        if self._user_repository.find_by_username(username):
            raise ValueError("Username already exists")

        # password is at least 8 characters long
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        merchant = Merchant(username, password)
        created_user = self._user_repository.create(merchant)

        return created_user

    def login(self, username=None, password=None):
        if not username or not password:
            raise ValueError("Username or password missing")

        user = self._user_repository.find_by_username(username)

        if not user:
            raise ValueError("User not found")

        if user.check_password(password):
            self._user = user
            return user

        raise ValueError("Wrong username or password")

    def get_current_user(self):
        return self._user

    def get_user_by_id(self, user_id=None):
        if not user_id:
            raise ValueError("User id missing")

        user = self._user_repository.get_user_by_id(user_id)

        return user


user_service = UserService()
