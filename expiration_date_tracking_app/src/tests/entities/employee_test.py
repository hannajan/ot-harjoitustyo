import unittest
from entities.employee import Employee
from entities.user_role import UserRole

class TestEmployee(unittest.TestCase):
    
    def test_created_employee_has_correct_attributes(self):
        employee = Employee("test-employee", "password", "id123")

        self.assertEqual(employee.username, "test-employee")
        self.assertTrue(employee.password.startswith("$2b$"))
        self.assertEqual(employee.employer_id, "id123")
        self.assertEqual(employee.password_is_temporary, True)
        self.assertEqual(employee.role, UserRole.EMPLOYEE)
        self.assertIsInstance(employee.user_id, str)
        self.assertIsNotNone(employee.user_id)

    def test_set_password_is_temporary_to_false_works(self):
        employee = Employee("test-employee", "password", "id123")

        employee.set_password_is_temporary_to_false()

        self.assertEqual(employee.password_is_temporary, False)