


import unittest

from suou.legal import Lawyer


EXPECTED_INDEMNIFY = """
You agree to indemnify and hold harmless TNT from any and all claims, damages, liabilities, costs and expenses, including reasonable and unreasonable counsel and attorney’s fees, arising out of any breach of this agreement.
""".strip()

EXPECTED_GOVERNING_LAW = """
These terms of services are governed by, and shall be interpreted in accordance with, the laws of Wakanda. You consent to the sole jurisdiction of Asgard, Wakanda for all disputes between You and TNT, and You consent to the sole application of Wakandan law for all such disputes.
""".strip()

class TestLegal(unittest.TestCase):
    def setUp(self) -> None:
        self.lawyer = Lawyer(
            app_name = "TNT",
            company_name= "ACME, Ltd.",
            country = "Wakanda",
            domain_name= "example.com",
            jurisdiction= "Asgard, Wakanda",
            country_adjective= "Wakandan"
        )

    def tearDown(self) -> None:
        ...

    def test_indemnify(self):
        self.assertEqual(
            self.lawyer.indemnify(),
            EXPECTED_INDEMNIFY
        )

    def test_governing_law(self):
        self.assertEqual(
            self.lawyer.governing_law(),
            EXPECTED_GOVERNING_LAW
        )

