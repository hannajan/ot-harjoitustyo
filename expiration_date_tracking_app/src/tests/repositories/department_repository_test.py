import unittest
from repositories.department_repository import department_repository
from repositories.store_repository import store_repository
from repositories.user_repository import user_repository
from entities.department import Department
from entities.merchant import Merchant
from entities.store import Store


class TestDepartmentRepository(unittest.TestCase):
    def setUp(self):
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
