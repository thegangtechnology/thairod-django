from procurement.models import Procurement
from thairod.utils.load_seed import load_realistic_seed
from thairod.utils.test_util import TestCase


class TestProcurement(TestCase):
    with_seed = False

    def setUp(self):
        seed = load_realistic_seed()
        self.seed = seed

        Procurement.objects.create(
            product_variation=seed.product_variations[0],
            quantity=20,
            unit_price=30.1,
            warehouse=seed.warehouses[0])

        Procurement.objects.create(
            product_variation=seed.product_variations[0],
            quantity=30,
            unit_price=30.1,
            warehouse=seed.warehouses[0])

        Procurement.objects.create(
            product_variation=seed.product_variations[1],
            quantity=10,
            unit_price=30.1,
            warehouse=seed.warehouses[0])

    def test_total_procurement(self):
        total = Procurement.total_procurement(self.seed.product_variations[0])
        self.assertEqual(total, 50)

    def test_total_procurement_empty(self):
        total = Procurement.total_procurement_for_id(99998877)
        self.assertEqual(total, 0)

    def test_total_procurement_map(self):
        p_map = Procurement.total_procurement_map()
        self.assertDictEqual(dict(p_map), {
            self.seed.product_variations[0].id: 50,
            self.seed.product_variations[1].id: 10})
        self.assertEqual(p_map[999888], 0)
