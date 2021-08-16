from rest_framework.reverse import reverse

from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import APITestCase


class TestQuickSnapshotAPI(APITestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        self.seed.full_production()
        self.set_up_user()

    def test_quick_snapshot_api(self):
        res = self.client.get(path=reverse('quick-snapshot'))
        self.assertEqual(res.status_code, 200)
        self.assertIn('orders', res.data)
        self.assertIn('order_flows', res.data)
