import datetime

import freezegun
from django.urls import reverse

from thairod import settings
from thairod.utils import tzaware
from thairod.utils.load_seed import RealisticSeed
from thairod.utils.query_util import round_to_next_nearest_hour
from thairod.utils.test_util import APITestCase


class TestPrintOfTheDayAPI(APITestCase):
    with_seed = False
    patch_shippop = False

    def prepare_seed(self, prepare_date: datetime.datetime):
        with freezegun.freeze_time(prepare_date):
            seed = RealisticSeed.load_realistic_seed()
            # there is a slight chance this will fail around 9am due to time skip
            seed.full_production()

    def _test_print(self, prepare_date: datetime.datetime, print_date: datetime.date):
        self.prepare_seed(prepare_date=prepare_date)
        print('aaa', prepare_date, prepare_date.date(), print_date)
        url = reverse('print-of-the-day')
        res = self.client.get(url, {'date': print_date})
        return res

    def test_print_of_the_day_before(self):
        prepare_date = tzaware.datetime(2021, 8, 4, 21)
        print_date = datetime.date(2021, 8, 5)
        res = self._test_print(prepare_date, print_date)
        self.assertEqual(res.status_code, 200)

    def test_print_of_the_day_same_day_before(self):
        prepare_date = tzaware.datetime(2021, 8, 5, 6)
        print_date = datetime.date(2021, 8, 5)
        res = self._test_print(prepare_date, print_date)
        self.assertEqual(res.status_code, 200)

    def test_print_of_the_day_after(self):
        prepare_date = tzaware.datetime(2021, 8, 5, 6)
        print_date = datetime.date(2021, 8, 6)
        res = self._test_print(prepare_date, print_date)
        self.assertEqual(res.status_code, 404)

    @freezegun.freeze_time(tzaware.datetime(2021, 8, 5, 8))
    def test_print_of_the_day_no_date_before(self):
        self.prepare_seed(prepare_date=tzaware.datetime(2021, 8, 5, 8))
        url = reverse('print-of-the-day')
        today = tzaware.now()
        date = round_to_next_nearest_hour(today, settings.SHIPPOP_LOT_CUTTING_TIME).date()
        res = self.client.get(url, {'date': date})
        self.assertEqual(res.status_code, 200)  # depending on time of day

    @freezegun.freeze_time(tzaware.datetime(2021, 8, 6, 10))
    def test_print_of_the_day_no_date_after(self):
        self.prepare_seed(prepare_date=tzaware.datetime(2021, 8, 5, 8))
        url = reverse('print-of-the-day')
        today = tzaware.now()
        date = round_to_next_nearest_hour(today, settings.SHIPPOP_LOT_CUTTING_TIME).date()
        res = self.client.get(url, {'date': date})
        self.assertEqual(res.status_code, 404)  # depending on time of day
