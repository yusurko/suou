

import unittest
from suou.validators import yesno

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