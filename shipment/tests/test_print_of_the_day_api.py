from django.urls import reverse

from thairod.utils.load_seed import RealisticSeed
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
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
