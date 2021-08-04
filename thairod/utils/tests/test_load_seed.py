from thairod.utils.load_seed import load_meaningful_seed
from thairod.utils.test_util import TestCase
from warehouse.models import Warehouse


class TestLoadSeed(TestCase):
    with_seed = False

    def setUp(self):
        load_meaningful_seed()

    def test_warehouse(self):
        zip_code = Warehouse.default_warehouse().address.postal_code
        self.assertEqual(len(zip_code), 5)
