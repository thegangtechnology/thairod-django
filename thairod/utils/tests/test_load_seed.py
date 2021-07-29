from thairod.utils.load_seed import load_meaningful_seed
from thairod.utils.test_util import TestCaseNoDB
from warehouse.models import Warehouse


class TestLoadSeed(TestCaseNoDB):

    def setUp(self):
        load_meaningful_seed()

    def test_warehouse(self):
        zip_code = Warehouse.default_warehouse().address.postal_code
        self.assertEqual(len(zip_code), 5)
