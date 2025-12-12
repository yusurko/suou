

import unittest

from suou.mat import Matrix


class TestMat(unittest.TestCase):
    def setUp(self):
        self.m_a = Matrix([
            [2, 2],
            [1, 3]
        ])
        self.m_b = Matrix([
            [1], [-4]
        ])
    def tearDown(self) -> None:
        ...
    def test_transpose(self):
        self.assertEqual(
            self.m_a.T,
            Matrix([
                [2, 1],
                [2, 3]
            ])
        )
        self.assertEqual(
            self.m_b.T,
            Matrix([[1, -4]])
        )
    def test_mul(self):
        self.assertEqual(
            self.m_b.T @ self.m_a,
            Matrix([
                [-2, -10]
            ])
        )
        self.assertEqual(
            self.m_a @ self.m_b,
            Matrix([
                [-6], [-11]
            ])
        )
    def test_shape(self):
        self.assertEqual(self.m_a.shape(), (2, 2))
        self.assertEqual(self.m_b.shape(), (2, 1))
        self.assertEqual(self.m_b.T.shape(), (1, 2))