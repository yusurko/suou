

import unittest

from suou import dei_args

class TestDei(unittest.TestCase):
    def setUp(self) -> None:
        ...

    def tearDown(self) -> None:
        ...

    def test_dei_args(self):
        
        def func_a(*, a: int, b: int):
            """Trivial function for the purpose of the test"""
            return a - b == 0

        func_b = dei_args(c='a', d='b')(func_a)

        with self.assertRaises(TypeError):
            func_a(c=1, b=2)
        
        self.assertTrue(func_a(a=1, b=1))
        self.assertFalse(func_b(c=1, b=2))
        self.assertFalse(func_b(a=1, d=2))
        self.assertFalse(func_b(a=1, b=2))
        
        with self.assertRaises(TypeError):
            func_b(c=1, b="a")