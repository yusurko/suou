

import unittest
from suou.calendar import not_greater_than
from suou.validators import not_less_than, yesno

class TestValidators(unittest.TestCase):
    def setUp(self):
        ...
    def tearDown(self):
        ...
    def test_yesno(self):
        self.assertFalse(yesno('false'))
        self.assertFalse(yesno('FALSe'))
        self.assertTrue(yesno('fasle'))
        self.assertTrue(yesno('falso'))
        self.assertTrue(yesno('zero'))
        self.assertTrue(yesno('true'))
        self.assertFalse(yesno('0'))
        self.assertTrue(yesno('00'))
        self.assertTrue(yesno('.'))
        self.assertTrue(yesno('2'))
        self.assertTrue(yesno('o'))
        self.assertFalse(yesno('oFF'))
        self.assertFalse(yesno('no'))
        self.assertFalse(yesno(False))
        self.assertTrue(yesno(True))
        self.assertFalse(yesno(''))

    def test_not_greater_than(self):
        self.assertTrue(not_greater_than(5)(5))
        self.assertTrue(not_greater_than(5)(3))
        self.assertFalse(not_greater_than(3)(8))

    def test_not_less_than(self):
        self.assertTrue(not_less_than(5)(5))
        self.assertFalse(not_less_than(5)(3))
        self.assertTrue(not_less_than(3)(8))