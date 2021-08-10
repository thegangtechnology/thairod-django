from django.utils import timezone

from thairod.utils import tzaware
from thairod.utils.test_util import TestCase


class TestTZAware(TestCase):
    def test_now(self):
        got = tzaware.now()
        self.assertEqual(got.tzinfo.tzname(None), timezone.get_current_timezone().tzname(None))

    def test_datetime(self):
        got = tzaware.datetime(2021, 8, 23, 8)
        self.assertEqual(got.tzinfo.tzname(None), timezone.get_current_timezone().tzname(None))
        self.assertEqual(got.hour, 8)
