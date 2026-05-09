import unittest

from repositories.shelf_repository import (
  shelf_repository,
  get_shelf_by_row
)
from repositories.department_repository import department_repository
from repositories.store_repository import store_repository
from repositories.user_repository import user_repository
from repositories.permission_repository import permission_repository

from entities.shelf import Shelf
from entities.department import Department
from entities.store import Store
from entities.merchant import Merchant

class TestShelfRepository(unittest.TestCase):
    def setUp(self):
        permission_repository.delete_all()
        shelf_repository.delete_all()
        department_repository.delete_all()
        store_repository.delete_all()
        user_repository.delete_all()

        user = user_repository.create(Merchant("test_kauppias", "salasana"))
        store = store_repository.create(Store("Test Kauppa", user.user_id))
        self.department = department_repository.create(Department(store.store_id, "Test osasto", 3))
        self.shelf = shelf_repository.create(Shelf(self.department.department_id, "Some shelf"))
        self.shelf2 = shelf_repository.create(Shelf(self.department.department_id, "Another shelf"))

    def test_create_shelf_works(self):
        test_shelf = shelf_repository.create(Shelf(self.department.department_id, "Test shelf"))


        self.assertEqual(test_shelf.name, "Test shelf")
        self.assertEqual(test_shelf.department_id, self.department.department_id)
        self.assertIsNotNone(test_shelf.shelf_id)
        self.assertEqual(test_shelf.is_default, False)

    def test_create_defaut_shelf_works(self):
        default_shelf = shelf_repository.create_default_shelf(self.department.department_id)

        self.assertEqual(default_shelf.name, "Shelf 1")
        self.assertEqual(default_shelf.is_default, True)
        self.assertEqual(default_shelf.department_id, self.department.department_id)

    def test_get_by_id_works(self):
        shelf = shelf_repository.get_by_id(self.shelf.shelf_id)

        self.assertEqual(shelf.name, "Some shelf")
        self.assertEqual(shelf.department_id, self.department.department_id)
        self.assertEqual(shelf.shelf_id, self.shelf.shelf_id)
        self.assertEqual(shelf.is_default, False)
      
    def test_update_works(self):
        self.shelf.name = "Changed name"
        shelf_repository.update(self.shelf)

        shelf = shelf_repository.get_by_id(self.shelf.shelf_id)

        self.assertEqual(shelf.name, "Changed name")
        self.assertNotEqual(shelf.name, "Some shelf")

    def test_get_shelves_by_department_works(self):
        shelves = shelf_repository.get_shelves_by_department(self.department.department_id)

        self.assertEqual(len(shelves), 2)

        self.assertTrue(any(shelf.name == "Some shelf" for shelf in shelves))
        self.assertTrue(any(shelf.name == "Another shelf" for shelf in shelves))

    def test_get_shelf_by_row_returns_none_if_no_row(self):
        shelf = get_shelf_by_row(None)

        self.assertIsNone(shelf)

