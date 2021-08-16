from django.urls import reverse

from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import APITestCase


class TestDashboardAPI(APITestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        self.seed.full_production()
        self.set_up_user()

    def test_dashboard_api(self):
        res = self.client.get(path=reverse('dashboard'))
        self.assertEqual(res.status_code, 200)
        self.assertIn('latest_summary', res.data)
        self.assertEqual(len(res.data['interval_summaries']), 7)
