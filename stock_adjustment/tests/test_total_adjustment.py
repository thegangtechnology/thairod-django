from stock_adjustment.models import StockAdjustment
from thairod.utils.load_seed import load_realistic_seed
from thairod.utils.test_util import TestCase


class TestTotalAdjustment(TestCase):
    with_seed = False

    def setUp(self):
        self.seed = load_realistic_seed()
        StockAdjustment.objects.create(
            product_variation=self.seed.product_variations[0],
            warehouse=self.seed.warehouses[0],
            quantity=20,
            reason='feel like it'
        )

        StockAdjustment.objects.create(
            product_variation=self.seed.product_variations[0],
            warehouse=self.seed.warehouses[0],
            quantity=-5,
            reason='feel like it'
        )

        StockAdjustment.objects.create(
            product_variation=self.seed.product_variations[1],
            warehouse=self.seed.warehouses[0],
            quantity=30,
            reason='feel like it'
        )

    def test_total_adjustment(self):
        stock = StockAdjustment.total_adjustment(self.seed.product_variations[0])
        self.assertEqual(stock, 15)

    def test_total_adjustment_no_data(self):
        stock = StockAdjustment.total_adjustment_for_id(9998888)
        self.assertEqual(stock, 0)

    def test_total_adjustment_map(self):
        ta_map = StockAdjustment.total_adjustment_map()
        self.assertDictEqual(ta_map,
                             {
                                 self.seed.product_variations[0].id: 15,
                                 self.seed.product_variations[1].id: 30,
                             })
