import unittest

from entities.permission import Permission
from entities.merchant import Merchant
from entities.store import Store
from entities.employee import Employee

from repositories.permission_repository import permission_repository
from repositories.shelf_repository import shelf_repository
from repositories.store_repository import store_repository
from repositories.user_repository import user_repository
from repositories.department_repository import department_repository


class TestPermissionReposiotry(unittest.TestCase):
    def setUp(self):
        permission_repository.delete_all()
        shelf_repository.delete_all()
        department_repository.delete_all()
        store_repository.delete_all()
        user_repository.delete_all()

        emloyer = user_repository.create(Merchant("merch", "password"))
        self.store = store_repository.create(Store("Store", emloyer.user_id))
        self.store2 = store_repository.create(Store("Second", emloyer.user_id))
        self.employee = user_repository.create(
            Employee("test_employee", "secret123", emloyer.user_id))

    def test_set_permission_works(self):
        permission_repository.set_permission(
            self.employee.user_id, self.store.store_id, Permission.VIEW)

        permission = permission_repository.find_permission(
            self.employee.user_id, self.store.store_id)

        self.assertEqual(permission, "view")

        permission_repository.set_permission(
            self.employee.user_id, self.store.store_id, Permission.EDIT)

        updated_permission = permission_repository.find_permission(
            self.employee.user_id, self.store.store_id)

        self.assertEqual(updated_permission, "edit")
        self.assertNotEqual(updated_permission, "view")

    def test_find_permission_returns_no_access_if_no_permisson_exists(self):
        permission = permission_repository.find_permission(
            self.employee.user_id, self.store2.store_id)

        self.assertEqual(permission, "no access")

    def test_find_permission_by_employee_id_works(self):
        permission_repository.set_permission(
            self.employee.user_id, self.store.store_id, Permission.VIEW)
        permission_repository.set_permission(
            self.employee.user_id, self.store2.store_id, Permission.MANAGE)

        permissions = permission_repository.find_permissions_by_employee_id(
            self.employee.user_id)

        self.assertEqual(len(permissions), 2)
