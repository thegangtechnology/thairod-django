from django.urls import reverse

from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import APITestCase


class TestDashboardAPI(APITestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        self.seed.full_production()

    def test_dashboard_api(self):
        res = self.client.get(path=reverse('dashboard'))
        self.assertIn('cumulative_summaries', res.data)
        self.assertEqual(len(res.data['cumulative_summaries']), 4)
        self.assertEqual(len(res.data['interval_summaries']), 3)
