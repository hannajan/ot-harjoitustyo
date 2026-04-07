import unittest
import re
from entities.temporary_password import TemporaryPassword

class TestTemporaryPassword(unittest.TestCase):
  def setUp(self):
    self.generator = TemporaryPassword()

  def test_password_correct_format(self):
    password = self.generator.generate_temporary_password()

    pattern = r'^(chocolate|popcycle|marshmallow)[1-9]{3}$'
    self.assertRegex(password, pattern)