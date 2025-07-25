

from datetime import timezone
import datetime
from suou.calendar import want_datetime, want_isodate

import unittest


class TestCalendar(unittest.TestCase):
    def setUp(self) -> None:
        ...
    def tearDown(self) -> None:
        ...

    def test_want_isodate(self):
        ## if test fails, make sure time zone is set to UTC.
        self.assertEqual(want_isodate(0, tz=timezone.utc), '1970-01-01T00:00:00+00:00')
        self.assertEqual(want_isodate(86400, tz=timezone.utc), '1970-01-02T00:00:00+00:00')
        self.assertEqual(want_isodate(1577840584.0, tz=timezone.utc), '2020-01-01T01:03:04+00:00')
        # TODO

    def test_want_datetime(self):
        self.assertEqual(want_datetime('2017-04-10T19:00:01', tz=timezone.utc) - want_datetime('2017-04-10T18:00:00', tz=timezone.utc), datetime.timedelta(seconds=3601))
        # TODO 

    