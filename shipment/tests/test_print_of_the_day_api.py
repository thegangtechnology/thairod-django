import datetime

from django.urls import reverse

from thairod import settings
from thairod.utils.load_seed import RealisticSeed
from thairod.utils.query_util import round_to_next_nearest_hour
from thairod.utils.test_util import APITestCase


class TestPrintOfTheDayAPI(APITestCase):
    with_seed = False
    patch_shippop = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        # there is a slight chance this will fail around 9am due to time skip
        self.seed.full_production()

    def test_print_of_the_day(self):
        url = reverse('print-of-the-day')
        today = datetime.datetime.now()
        date = round_to_next_nearest_hour(today, settings.SHIPPOP_LOT_CUTTING_TIME).date()
        res = self.client.get(url, {'date': date})
        self.assertEqual(res.status_code, 200)

    def test_print_of_the_day_no_date(self):
        url = reverse('print-of-the-day')
        today = datetime.datetime.now()
        date = round_to_next_nearest_hour(today, settings.SHIPPOP_LOT_CUTTING_TIME).date()

        res = self.client.get(url, {'date': date})
        self.assertIn(res.status_code, [200, 404])  # depending on time of day
