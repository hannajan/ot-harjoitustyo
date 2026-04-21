from entities.merchant import Merchant
from entities.employee import Employee
from entities.user_role import UserRole
from entities.temporary_password import TemporaryPassword
from entities.permission import Permission

from repositories.user_repository import (
    user_repository as default_user_repository
)

from repositories.permission_repository import (
    permission_repository as default_permission_repository
)

class UserService:
    def __init__(self, user_repository=default_user_repository, permission_repository=default_permission_repository):
        self._user_repository = user_repository
        self._permission_repository = permission_repository
        self._user = None

    def validate_username(self, username):
        # username is at least 5 charaters long
        if len(username) < 5:
            raise ValueError("Username must be at least 5 characters long")

        # username is unique
        if self._user_repository.find_by_username(username):
            raise ValueError("Username already exists")

        return True

    def validate_password(self, password):
        # password is at least 8 characters long
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        return True

    def register_merchant(self, username=None, password=None):
        if not username or not password:
            raise ValueError("Username or password missing")

        self.validate_username(username)
        self.validate_password(password)

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

    def create_new_employee(self, username=None):
        generator = TemporaryPassword()

        current_user = self.get_current_user()
        if not current_user.role == UserRole.MERCHANT:
            raise ValueError("Only merchants can create new employees")

        if not username:
            raise ValueError("Username missing")

        self.validate_username(username)
        password = generator.generate_temporary_password()
        print(password)

        employee = Employee(username, password, current_user.user_id)
        self._user_repository.create(employee)

        return password

    def update_employee_password(self, new_password):
        if self._user.role != UserRole.EMPLOYEE:
            raise ValueError("User role is not employee")

        if not self.validate_password(new_password):
            raise ValueError("New password must be 8 characters long")
        self._user = self._user.set_password(new_password)
        self._user = self._user.set_password_is_temporary_to_false()
        self._user_repository.update_password(
            self._user.user_id,
            self._user.password,
            self._user.password_is_temporary
        )

    def get_employees(self):
        current_user = self.get_current_user()
        if not current_user or current_user.role != UserRole.MERCHANT:
            return []

        return self._user_repository.find_all_by_employer_id(current_user.user_id)

    def logout(self):
        self._user = None

    def get_employee_store_permission(self, employee_id, store_id):
        return self._permission_repository.find_permission(employee_id, store_id) 

    def set_employee_store_permission(self, employee_id, store_id, permission):
        self._permission_repository.set_permission(employee_id, store_id, permission)

    def get_employee_stores(self, employee_id):
        from services.store_service import store_service
        
        permissions = self._permission_repository.find_permissions_by_employee_id(employee_id)

        stores = []
        for permission in permissions:
            if permission["permission"] != Permission.NOACCESS:
                store = store_service.get_store_by_id(permission["store_id"])
                if store:
                    stores.append(store)

        return stores


user_service = UserService()
