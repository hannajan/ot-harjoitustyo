import unittest
from entities.department import Department

class TestDepartment(unittest.TestCase):

    def test_created_departmnet_has_correct_attributes(self):
        department = Department("store_id123", "Test Department", 7, "dep_id_123")

        self.assertEqual(department.name, "Test Department")
        self.assertEqual(department.check_days_before, 7)
        self.assertEqual(department.department_id, "dep_id_123")
        self.assertEqual(department.store_id, "store_id123")
