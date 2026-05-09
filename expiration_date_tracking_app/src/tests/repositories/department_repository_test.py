import unittest
from repositories.shelf_repository import shelf_repository
from repositories.department_repository import (
  department_repository,
  get_department_by_row
)
from repositories.store_repository import store_repository
from repositories.user_repository import user_repository
from repositories.permission_repository import permission_repository
from entities.department import Department
from entities.merchant import Merchant
from entities.store import Store


class TestDepartmentRepository(unittest.TestCase):
    def setUp(self):
        permission_repository.delete_all()
        shelf_repository.delete_all()
        department_repository.delete_all()
        store_repository.delete_all()
        user_repository.delete_all()

        self.user = user_repository.create(
            Merchant("test-merchant", "password"))

        self.store = store_repository.create(
            Store("Test Store", self.user.user_id))

        self.department = Department(self.store.store_id, "Hams", 2, "dep_id1")

    def test_one_department_in_database_after_create(self):
        department_repository.create(self.department)
        departments = department_repository.get_by_store(self.store.store_id)

        self.assertEqual(len(departments), 1)

    def test_get_by_id_works_with_valid_id(self):
        department = department_repository.create(self.department)

        found_department = department_repository.get_by_id(department_id=department.department_id)

        self.assertEqual(found_department.name, "Hams")
        self.assertEqual(found_department.check_days_before, 2)

    def test_update_department_works(self):
        department = department_repository.create(self.department)
        department.check_days_before = 5

        department_repository.update(department)

        updated_department = department_repository.get_by_id(department_id=department.department_id)

        self.assertEqual(updated_department.name, "Hams")
        self.assertEqual(updated_department.check_days_before, 5)
        self.assertNotEqual(updated_department.check_days_before, 2)

    def test_get_department_by_row_returns_none_if_no_row(self):
        department = get_department_by_row(None)

        self.assertIsNone(department)
