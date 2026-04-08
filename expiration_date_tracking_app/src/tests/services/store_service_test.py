import unittest
from services.store_service import StoreService
from entities.store import Store
from entities.merchant import Merchant

class MockStoreRepository:
  def __init__(self):
    self.stores = []

  def create(self, store):
    self.stores.append(store)

    return store
  
  def find_all_by_owner_id(self, owner_id):
    found_stores = list(
            filter(lambda store: store.owner_id == owner_id, self.stores))

    return found_stores
  
  def delete_all(self):
    self.stores = []

  def get_all(self):
    return self.stores
  
class MockUserService:
    def __init__(self):
      self.merchant = Merchant("test", "password", user_id="id123")

    def get_current_user(self):
        return self.merchant
  

class TestStoreService(unittest.TestCase):
  def setUp(self):
    self.store_service = StoreService(MockStoreRepository(), MockUserService())

  def test_create_store_returns_store(self):
    
    store = self.store_service.create_store("SuperStore")

    self.assertIsInstance(store, Store)
    self.assertEqual(store.name, "SuperStore")
    self.assertEqual(store.owner_id, "id123")

  def test_create_store_without_name_fails(self):

    with self.assertRaisesRegex(ValueError, "Store name must be given"):
      noname = self.store_service.create_store()

  def test_create_store_with_name_too_short_fails(self):

    with self.assertRaisesRegex(ValueError, "Store name must be at least 3 characters long"):
      self.store_service.create_store("no")

  def test_get_stores_by_owner(self):
    self.store_service.create_store("Nice Store")
    self.store_service.create_store("Big Store")

    stores = self.store_service.get_stores_by_owner("id123")   

    self.assertEqual(len(stores), 2)
    self.assertEqual(stores[0].name, "Nice Store")
    self.assertEqual(stores[1].name, "Big Store")