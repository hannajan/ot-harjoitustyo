import unittest
from entities.user import User
from entities.user_role import UserRole
from services.user_service import UserService

class MockUserRepository:
    def __init__(self, users=None):
        self.users = users or []

    def create(self, user):
        self.users.append(user)

        return user
    
    def delete_all(self):
        self.users = []

    def get_all(self):
        return self.users
    
    def find_by_username(self, username):
        found_users = list(filter(lambda user: user.username == username, self.users))

        return found_users[0] if len(found_users) > 0 else None
    
    def get_user_by_id(self, user_id):
        found_users = list(filter(lambda user: user.user_id == user_id, self.users))

        return found_users[0] if len(found_users) > 0 else None
    
class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService(
            MockUserRepository()
        )

    def test_register_merchant_with_correct_info(self):
        merchant = self.user_service.register_merchant("Merchant", "Password")
        self.assertEqual(merchant.username, "Merchant")

    def test_register_merchant_with_no_username(self):
        with self.assertRaises(ValueError) as context:
            merchant = self.user_service.register_merchant(password="Password")

        self.assertEqual(str(context.exception), "Username or password missing")

    def test_register_merchant_with_password_too_short(self):
        with self.assertRaises(ValueError) as context:
            merchant = self.user_service.register_merchant("Merchant", "no")

        self.assertEqual(str(context.exception), "Password must be at least 8 characters long")
        
    def test_register_merchant_username_not_unique(self):
        merchant = self.user_service.register_merchant("Merchant", "Password")

        with self.assertRaises(ValueError) as context:
            merchant2 = self.user_service.register_merchant("Merchant", "secret123")

        self.assertEqual(str(context.exception), "Username already exists")

    def test_register_merchant_username_too_short(self):
        with self.assertRaises(ValueError) as context:
            merchant = self.user_service.register_merchant("no", "Password")
        
        self.assertEqual(str(context.exception), "Username must be at least 5 characters long")
 
    def test_login_merchant(self):
        self.user_service.register_merchant("Merchant", "Password")
        user = self.user_service.login("Merchant", "Password")

        current_user = self.user_service.get_current_user()

        self.assertEqual(user.username, "Merchant")
        self.assertEqual(current_user.username, "Merchant")
        self.assertEqual(user.user_id, current_user.user_id)

    def test_login_merchant_no_username(self):
        self.user_service.register_merchant("Merchant", "Password")
        with self.assertRaises(ValueError) as context:
            user = self.user_service.login(password="Password")

        self.assertEqual(str(context.exception), "Username or password missing")

    def test_login_with_nonexisting_user(self):
        with self.assertRaises(ValueError) as context:
            user = self.user_service.login("Nonexisting", "secret123")

        self.assertEqual(str(context.exception), "User not found")

    def test_login_with_wrong_password_fails(self):
        self.user_service.register_merchant("Merchant", "Password")

        with self.assertRaises(ValueError) as context:
            user = self.user_service.login("Merchant", "Wrongpassword")

        self.assertEqual(str(context.exception), "Wrong username or password")

    def test_get_user_by_id(self):
        user = self.user_service.register_merchant("Merchant", "Password")

        found_user = self.user_service.get_user_by_id(user.user_id)

        self.assertEqual(found_user.username, "Merchant")

    def test_get_user_by_id_raises_error_when_no_id_given(self):
        with self.assertRaises(ValueError) as context:
            found_user = self.user_service.get_user_by_id()

        self.assertEqual(str(context.exception), "User id missing")




