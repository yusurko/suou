

import datetime
import unittest

from suou.iding import Siq, SiqType, SiqGen, make_domain_hash


class TestIding(unittest.TestCase):
    def setUp(self) -> None:
        ...
    def tearDown(self) -> None:
        ...
    def test_generation(self):
        gen = SiqGen('0', shard_id=256)
        gen.set_cur_timestamp(datetime.datetime(2020,1,1))
        i1 = gen.generate_one(SiqType.CONTENT)
        self.assertEqual(i1, 7451106619238957490390643507207)
        i2_16 = gen.generate_list(SiqType.CONTENT, 15)
        self.assertIsInstance(i2_16, list)
        self.assertEqual(i2_16[0], i1 + 8)
        self.assertEqual(i2_16[14], i1 + 120)

        gen.set_cur_timestamp(datetime.datetime(2021, 1, 1))
        i17 = gen.generate_one(SiqType.CONTENT)
        self.assertEqual(i17, 7600439181106854559196223897735)

    def test_domain_hash(self):
        self.assertEqual(make_domain_hash('0'), 0)
        self.assertEqual(make_domain_hash('example.com'), 2261653831)

    def test_representation(self):
        i1 = Siq(7451106619238957490390643507207)
        self.assertEqual(i1.to_hex(), "5e0bd2f0000000000000000007")
        self.assertEqual(i1.to_did(), "did:siq:iuxvojaaf4c6s6aaaaaaaaaaaaaah")