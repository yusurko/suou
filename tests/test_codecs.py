

import binascii
import unittest
from suou.codecs import b64encode, b64decode

B1 = b'N\xf0\xb4\xc3\x85\n\xf9\xb6\x9a\x0f\x82\xa6\x99G\x07#'
B2 = b'\xbcXiF,@|{\xbe\xe3\x0cz\xa8\xcbQ\x82'
B3 = b"\xe9\x18)\xcb'\xc2\x96\xae\xde\x86"
B4 = B1[-2:] + B2[:-2]
B5 = b'\xff\xf8\xa7\x8a\xdf\xff'


class TestCodecs(unittest.TestCase):
    def setUp(self) -> None:
        ...
    def tearDown(self) -> None:
        ...

    #def runTest(self):
    #    self.test_b64encode()
    #    self.test_b64decode()

    def test_b64encode(self):
        self.assertEqual(b64encode(B1), 'TvC0w4UK-baaD4KmmUcHIw')
        self.assertEqual(b64encode(B2), 'vFhpRixAfHu-4wx6qMtRgg')
        self.assertEqual(b64encode(B3), '6RgpyyfClq7ehg')
        self.assertEqual(b64encode(B4), 'ByO8WGlGLEB8e77jDHqoyw')
        self.assertEqual(b64encode(B5), '__init__')
        self.assertEqual(b64encode(B1[:4]), 'TvC0ww')
        self.assertEqual(b64encode(b'\0' + B1[:4]), 'AE7wtMM')
        self.assertEqual(b64encode(b'\0\0\0\0\0' + B1[:4]), 'AAAAAABO8LTD')
        self.assertEqual(b64encode(b'\xff'), '_w')
        self.assertEqual(b64encode(b''), '')
    
    def test_b64decode(self):
        self.assertEqual(b64decode('TvC0w4UK-baaD4KmmUcHIw'), B1)
        self.assertEqual(b64decode('vFhpRixAfHu-4wx6qMtRgg'), B2)
        self.assertEqual(b64decode('6RgpyyfClq7ehg'), B3)
        self.assertEqual(b64decode('ByO8WGlGLEB8e77jDHqoyw'), B4)
        self.assertEqual(b64decode('__init__'), B5)
        self.assertEqual(b64decode('TvC0ww'), B1[:4])
        self.assertEqual(b64decode('AE7wtMM'), b'\0' + B1[:4])
        self.assertEqual(b64decode('AAAAAABO8LTD'), b'\0\0\0\0\0' + B1[:4])
        self.assertEqual(b64decode('_w'), b'\xff')
        self.assertEqual(b64decode(''), b'')

        self.assertRaises(binascii.Error, b64decode, 'C')

        
