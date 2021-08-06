from shipment.models.box_size import BoxSize
from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import TestCase


class TestBoxSize(TestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()

    def test_default_box_id(self):
        ret = BoxSize.get_default_box_id()
        self.assertEqual(type(ret), int)

    def test_preferred_box_size(self):
        pv_ids = [pv.id for pv in self.seed.product_variations]
        box = BoxSize.determine_box_size_by_pv_ids(pv_ids=pv_ids)
        self.assertEqual(box.name, 'A')
