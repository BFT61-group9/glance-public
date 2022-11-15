"""
Test stuff
"""

import unittest

from user import validate_username as vu
from app_util import (
    get_all_file_path as fp
)




class TestUser(unittest.TestCase):
    def test_invalid_minlen(self):
        """minlen < 1"""
        self.assertRaises(ValueError, vu, "user", -1)

    def test_minlen(self):
        self.assertFalse(vu("username", 20))

    def test_number(self):
        self.assertFalse(vu("0nine", 3))

    def test_uppercase(self):
        self.assertTrue(vu("Alex", 3))

    def test_lowercase(self):
        self.assertTrue(vu("mingle", 3))

    def test_combination(self):
        self.assertTrue(vu("Bruh9", 3))
    
    def test_underscore(self):
        self.assertFalse(vu("Qui_ken", 3))
    
    def test_space(self):
        self.assertFalse(vu("Th3 Fish", 3))
    
    def test_blank_space(self):
        self.assertFalse(vu("blanK  ", 3))


class TestAppUtil(unittest.TestCase):
    def test_path(self):
        """Leave blank in file_type"""
        self.assertRaises(ValueError, fp, "")


if __name__ == "__main__":
    unittest.main()