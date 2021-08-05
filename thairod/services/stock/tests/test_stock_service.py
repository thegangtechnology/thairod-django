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
            adjustment=-5,
            pending=10
        )
        self.assertEqual(stock.current_total, 5)

    def test_stock_service(self):
        stock = StockService().get_single_stock(self.seed.product_variations[0].id)
        self.assertEqual(
            stock,
            StockInfo(
                fulfilled=4,
                procured=30,
                adjustment=35,
                pending=3
            )
        )

    def test_stock_map(self):
        stocks = StockService().get_all_stock_map()
        self.assertEqual(dict(stocks),
                         {
                             self.seed.product_variations[0].id: StockInfo(fulfilled=4, procured=30, adjustment=35,
                                                                           pending=3),
                             self.seed.product_variations[1].id: StockInfo(fulfilled=2, procured=40, adjustment=10,
                                                                           pending=1)
                         })
