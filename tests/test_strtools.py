


import unittest

from suou.strtools import PrefixIdentifier
from pydantic import ValidationError

class TestStrtools(unittest.TestCase):
    def setUp(self) -> None:
        ...

    def tearDown(self) -> None:
        ...

    def test_PrefixIdentifier_empty(self):
        pi = PrefixIdentifier(None)
        self.assertEqual(pi.hello, 'hello')
        self.assertEqual(pi['with spaces'], 'with spaces')
        self.assertEqual(pi['\x1b\x00'], '\x1b\0')
        self.assertEqual(pi.same_thing, pi['same_thing'])

        with self.assertRaises(ValidationError):
            pi[0]

        self.assertEqual(f'{PrefixIdentifier(None)}', f'{PrefixIdentifier("")}')

    def test_PrefixIdentifier_get_nostr(self):
        with self.assertRaises(TypeError):
            pi = PrefixIdentifier(1)
            pi.hello

        with self.assertRaises(TypeError):
            PrefixIdentifier([99182])
        
        with self.assertRaises(TypeError):
            PrefixIdentifier(b'alpha_')
    

        