import unittest
from repositories.user_repository import user_repository
from entities.merchant import Merchant

class TestUserRepository(unittest.TestCase):
  def setUp(self):
    user_repository.delete_all()
    self.merchant = Merchant("merchant", "password")
    self.merchant2 = Merchant("storeowner", "secret123")
    self.merchant3 = Merchant("merchant_test", "verysafepassword")
    

  def test_one_user_in_database_when_merchant_created(self):
    user_repository.create(self.merchant)
    users = user_repository.get_all()

    self.assertEqual(len(users), 1)

  def test_username_matches_when_merchant_created(self):
    user_repository.create(self.merchant)
    users = user_repository.get_all()

    self.assertEqual(users[0].username, "merchant")

  def test_find_merchant_by_username_returns_correct_user(self):
    

    user_repository.create(self.merchant)
    user_repository.create(self.merchant2)
    user_repository.create(self.merchant3)

    user = user_repository.find_by_username("storeowner")

    self.assertEqual(user.username, "storeowner")


