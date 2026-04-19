import unittest
from repositories.user_repository import user_repository
from repositories.store_repository import store_repository
from entities.merchant import Merchant
from entities.employee import Employee


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        store_repository.delete_all()
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

    def test_get_user_by_id_returns_correct_user(self):
        user_repository.create(self.merchant)
        user_repository.create(self.merchant2)
        user_repository.create(self.merchant3)

        user = user_repository.get_user_by_id(self.merchant3.user_id)

        self.assertEqual(user.username, "merchant_test")

    def test_update_password_works(self):
        merchant = user_repository.create(self.merchant)
        employee = Employee("employee", "password", merchant.user_id)
        created_employee = user_repository.create(employee)
        user_repository.update_password(
            created_employee.user_id, "newpassword", False)
        found_employee = user_repository.get_user_by_id(
            created_employee.user_id)
        self.assertEqual(found_employee.check_password("password"), False)
        self.assertEqual(found_employee.check_password("newpassword"), True)

    def test_find_all_by_employer_id_works(self):
        merchant = user_repository.create(self.merchant)
        user_repository.create(
            Employee("worker", "password", merchant.user_id))
        user_repository.create(
            Employee("employee", "secret123", merchant.user_id))

        employees = user_repository.find_all_by_employer_id(merchant.user_id)

        self.assertEqual(len(employees), 2)
        self.assertEqual(employees[0].username, "worker")
        self.assertEqual(employees[1].username, "employee")
