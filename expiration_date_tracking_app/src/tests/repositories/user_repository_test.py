import unittest
from repositories.user_repository import user_repository
from entities.merchant import Merchant

class TestUserRepository(unittest.TestCase):
  def setUp(self):
    user_repository.delete_all()
    self.merchant = Merchant("merchant", "password")
    

  def test_one_user_in_database_when_merchant_created(self):
    user_repository.create(self.merchant)
    users = user_repository.get_all()

    self.assertEqual(len(users), 1)

  def test_username_matches_when_merchant_created(self):
    user_repository.create(self.merchant)
    users = user_repository.get_all()

    self.assertEqual(users[0].username, "merchant")

