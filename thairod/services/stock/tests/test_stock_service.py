from thairod.services.stock.stock import StockService, StockInfo
from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import TestCase


class TestStockService(TestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        self.seed.full_production()

    def test_stock_info_total(self):
        stock = StockInfo(
            fulfilled=20,
            procured=30,
            ordered=30,
            adjustment=-5,
            to_be_shipped=10,
            pending=10
        )
        self.assertEqual(stock.current_total(), 5)

    def test_stock_service(self):
        stock = StockService().get_single_stock(self.seed.product_variations[0].id)
        self.assertEqual(
            stock,
            StockInfo(
                fulfilled=4,
                procured=30,
                ordered=7,
                to_be_shipped=4,
                adjustment=35,
                pending=3
            )
        )

    def test_stock_map(self):
        stocks = StockService().get_all_stock_map()
        pv_id0 = self.seed.product_variations[0].id
        pv_id1 = self.seed.product_variations[1].id
        exp = {
            pv_id0: StockInfo(
                fulfilled=4,
                procured=30,
                adjustment=35,
                pending=3,
                to_be_shipped=4,
                ordered=7),
            pv_id1: StockInfo(
                fulfilled=2,
                procured=40,
                adjustment=10,
                to_be_shipped=2,
                pending=1,
                ordered=3)
        }
        self.assertEqual(dict(stocks), exp)

    def test_stock_info_serialize_has_current_total(self):
        serializer = StockInfo.serializer()
        stock = StockInfo(
            fulfilled=4,
            procured=30,
            ordered=7,
            to_be_shipped=4,
            adjustment=35,
            pending=3
        )
        data = serializer(stock).data
        self.assertIn('current_total', data)
