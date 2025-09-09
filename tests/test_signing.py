



import time
import unittest

from suou.codecs import want_bytes, b64decode, z85decode
from suou.iding import Siq
from suou.signing import UserSigner


class TestSigning(unittest.TestCase):
    def setUp(self) -> None:
        # use deterministic secrets in testing
        self.signer = UserSigner(
            z85decode('suou-test!'), # master secret
            Siq(1907492221233425151961830768246784), # user id
            b64decode('e7YXG4ob22mBCxoPvgewlAsfiZE2MFu50aP_gtnXW2v2')
        )
    def tearDown(self) -> None:
        ...

    def test_UserSigner_token(self):
        # self coherence test
        TIMESTAMP = 1757426896
        with self.assertWarns(UserWarning):
            tok = self.signer.token(test_timestamp=TIMESTAMP)
        self.assertIsInstance(tok, str)
        self.assertEqual(tok, 'AF4L78gAAAAAAAAAAAAA.aMA00A.0au9HDfOJZv-gpudEevT6Squ8go')

        tok2 = self.signer.token()
        tim = int(time.time())
        if tim != TIMESTAMP:
            self.assertNotEqual(tok2, tok)

        tokp = UserSigner.split_token(tok)
        self.assertEqual(tokp[0], z85decode('0a364:n=hu000000000'))
        self.assertEqual(tokp[1], TIMESTAMP)

        