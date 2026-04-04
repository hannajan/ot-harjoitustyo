import unittest
from repositories.store_repository import store_repository
from repositories.user_repository import user_repository
from entities.store import Store
from entities.merchant import Merchant

class TestStoreRepository(unittest.TestCase):
  def setUp(self):
    store_repository.delete_all()
    user_repository.delete_all()

    self.merchant = Merchant("test-merchant", "password")
    self.user = user_repository.create(self.merchant)

    self.merchant2 = Merchant("merch_test", "secret123")
    self.user2 = user_repository.create(self.merchant2)

    self.merchant3 = Merchant("zero_merchant", "password")
    self.user3 = user_repository.create(self.merchant3)

    self.store = Store("Test Store", self.user.user_id)
    self.store2 = Store("Test Boutique", self.user.user_id)
    self.store3 = Store("Testfield Market", self.user2.user_id)

  def test_one_store_in_database_after_create(self):
    store_repository.create(self.store)
    stores = store_repository.get_all()

    self.assertEqual(len(stores), 1)

  def test_store_name_matches_when_store_created(self):
    store_repository.create(self.store)
    stores = store_repository.get_all()

    self.assertEqual(stores[0].name, "Test Store")

  def test_find_all_by_owner_id_works_when_owner_has_two_stores(self):
    store_repository.create(self.store)
    store_repository.create(self.store2)
    store_repository.create(self.store3)

    stores = store_repository.find_all_by_owner_id(self.user.user_id)

    self.assertEqual(len(stores), 2)
    self.assertEqual(stores[0].name, "Test Store")
    self.assertEqual(stores[1].name, "Test Boutique")

  def test_find_all_by_owner_id_works_when_owner_has_no_stores(self):
    store_repository.create(self.store)
    store_repository.create(self.store2)
    store_repository.create(self.store3)

    stores = store_repository.find_all_by_owner_id(self.user3.user_id)
    self.assertEqual(len(stores), 0)
