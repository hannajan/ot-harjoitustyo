import unittest
from entities.user import User
from entities.user_role import UserRole

class TestUser(unittest.TestCase):

  def test_create_merchant_with_password(self):
    user = User(username="Merchant", password="Password", role=UserRole.MERCHANT)

    self.assertEqual(user.username, "Merchant")

  def test_create_merchant_without_password_fails(self):
    with self.assertRaises(ValueError) as context:
      user = User(username="Merchant", role=UserRole.MERCHANT)

    self.assertEqual(str(context.exception), "Password or password_hash must be provided")

  def test_create_merchant_with_incorrect_role_fails(self):
    with self.assertRaises(ValueError) as context:
      user = User(username="Merchant", password="Password", role="customer")

    self.assertEqual(str(context.exception), "Invalid role")

  def test_check_password_works(self):
    user = User(username="Merchant", password="CorrectPassword", role=UserRole.MERCHANT)

    was_correct = user.check_password("CorrectPassword")
    was_not_correct = user.check_password("WrongPassword")

    self.assertEqual(was_correct, True)
    self.assertEqual(was_not_correct, False)