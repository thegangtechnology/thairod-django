from thairod.services.quick_snapshot.quick_snapshot_service import QuickSnapshotService
from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import TestCase


class TestQuickSnapshotService(TestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        self.seed.full_production()

    def test_qsr(self):
        qsr = QuickSnapshotService.build_quick_snapshot_response()
        self.assertEqual(len(qsr.orders), 10)
        self.assertEqual(len(qsr.order_flows), 3)
