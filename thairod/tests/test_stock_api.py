from django.urls import reverse

from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import APITestCase


class TestStockAPI(APITestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        self.seed.full_production()

    def test_stock_api(self):
        res = self.client.get(reverse('get-stock'),
                              data={'pv_id': [pv.id for pv in self.seed.product_variations]})
        self.assertIn('stocks', res.data)
        self.assertEqual(len(res.data['stocks']), 2)
