import unittest
from entities.user import User
from entities.user_role import UserRole


class TestUser(unittest.TestCase):
    def setUp(self):
      self.user = User(username="Merchant", password="Password", role=UserRole.MERCHANT)

    def test_create_merchant_with_password(self):
        self.assertEqual(self.user.username, "Merchant")

    def test_create_merchant_without_password_fails(self):
        with self.assertRaises(ValueError) as context:
            user1 = User(username="Merchant", role=UserRole.MERCHANT)

        self.assertEqual(str(context.exception), "Password must be provided")

    def test_create_merchant_with_incorrect_role_fails(self):
        with self.assertRaises(ValueError) as context:
            user1 = User(username="Merchant",
                        password="Password", role="customer")

        self.assertEqual(str(context.exception), "Invalid role")

    def test_check_password_works(self):
        was_correct = self.user.check_password("Password")
        was_not_correct = self.user.check_password("WrongPassword")

        self.assertEqual(was_correct, True)
        self.assertEqual(was_not_correct, False)

    def test_is_employee_works(self):
        user1 = User(username="Merchant", password="Password", role=UserRole.MERCHANT)
        user2 = User(username="Employee", password="Password", role=UserRole.EMPLOYEE)

        self.assertEqual(user1.is_employee(), False)
        self.assertEqual(user2.is_employee(), True)

    def test_set_password_works(self):
        self.user.set_password("NewPassword")

        self.assertEqual(self.user.check_password("Password"), False)
        self.assertEqual(self.user.check_password("NewPassword"), True)

    def test_hashed_password_is_not_hashed_again(self):
        testuser = User(username=self.user.username, password=self.user.password, role=UserRole.MERCHANT)
        password = self.user.password
        bytes_password = password.encode('utf-8')
        testuser2 = User(username=self.user.username, password=bytes_password, role=UserRole.MERCHANT)
        self.assertEqual(testuser.password, password)
        self.assertEqual(testuser2.password.decode('utf-8'), password)

    def test_bytes_password_is_hashed(self):
        password = "password".encode('utf-8')
        user = User(username="name", password=password, role=UserRole.MERCHANT )

        self.assertNotEqual(user.password, password)
