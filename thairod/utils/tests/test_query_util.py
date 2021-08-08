import datetime

from django.test import TestCase
from django.utils.timezone import now
from future.backports.datetime import timedelta

from thairod.utils import query_util


class TestQueryUtil(TestCase):
    with_seed = False

    def test_both_none(self):
        q = query_util.smart_range('a', None, None)

        self.assertEqual(len(q.children), 0)

    def test_begin_only(self):
        begin = now()
        q = query_util.smart_range('a', begin, None)
        self.assertEqual(q.children[0], ('a__ge', begin))

    def test_end_only(self):
        end = now()
        q = query_util.smart_range('a', None, end)
        self.assertEqual(q.children[0], ('a__lt', end))

    def test_begin_end(self):
        end = now()
        begin = now()
        q = query_util.smart_range('a', begin, end)
        self.assertEqual(q.children[0], ('a__range', (begin, end)))


class TestSmartEqual(TestCase):
    def test_normal(self):
        q = query_util.smart_equal('a', 10)
        self.assertEqual(q.children[0], ('a', 10))

    def test_normal(self):
        q = query_util.smart_equal('a', None)
        self.assertEqual(q.children, [])


class TestToInterval(TestCase):
    def test_to_interval(self):
        anchor = datetime.datetime(1982, 8, 23)
        dates = [
            anchor,
            anchor - timedelta(days=2),
            anchor - timedelta(days=1)
        ]
        intervals = query_util.to_intervals(dates)
        print(intervals)
        exp = [(dates[2], dates[0]), (dates[1], dates[2])]
        print(exp)
        self.assertListEqual(
            intervals, exp
        )


class TestDateRange(TestCase):
    def test_date_range_positive(self):
        anchor = datetime.datetime(1982, 8, 23)
        got = query_util.date_range(anchor, 3)
        exp = [datetime.datetime(1982, 8, x) for x in [23, 24, 25, 26]]
        self.assertListEqual(
            got, exp
        )

    def test_date_range_negative(self):
        anchor = datetime.datetime(1982, 8, 23)
        got = query_util.date_range(anchor, -3)
        exp = [datetime.datetime(1982, 8, x) for x in [23, 22, 21, 20]]
        self.assertListEqual(
            got, exp
        )


class TestReplaceHour(TestCase):
    def test_replace_hour(self):
        d = datetime.datetime(1982, 8, 23, 10, 11, 12, 13)
        got = query_util.replace_hour(d, 9)
        exp = datetime.datetime(1982, 8, 23, 9, 0, 0, 0)
        self.assertEqual(got, exp)


class TestRoundNextNearestHour(TestCase):
    def test_after_time(self):
        d = datetime.datetime(1982, 8, 23, 10, 11, 12, 13)
        got = query_util.round_to_next_nearest_hour(d, 9)
        exp = datetime.datetime(1982, 8, 24, 9)
        self.assertEqual(got, exp)

    def test_before_time(self):
        d = datetime.datetime(1982, 8, 23, 2, 11, 12, 13)
        got = query_util.round_to_next_nearest_hour(d, 9)
        exp = datetime.datetime(1982, 8, 23, 9)
        self.assertEqual(got, exp)
