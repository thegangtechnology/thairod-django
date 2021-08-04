from procurement.models import Procurement
from product.models import Product, ProductVariation
from thairod.utils.test_util import TestCase
from warehouse.models import Warehouse


class TestProcurement(TestCase):
    with_db = False

    def setUp(self):
        warehouse = Warehouse.example()
        warehouse.address.save()
        warehouse.save()

        product = Product.example()
        product.save()

        product_variation = ProductVariation.example()
        product_variation.product = product
        product_variation.save()
        product_variation2 = ProductVariation.example()
        product_variation2.product = product
        product_variation2.save()
        self.warehouse = warehouse
        self.product_variation = product_variation
        self.product_variation2 = product_variation2

        Procurement.objects.create(
            product_variation=self.product_variation,
            quantity=20,
            unit_price=30.1,
            warehouse=self.warehouse)

        Procurement.objects.create(
            product_variation=self.product_variation,
            quantity=30,
            unit_price=30.1,
            warehouse=self.warehouse)

        Procurement.objects.create(
            product_variation=self.product_variation2,
            quantity=10,
            unit_price=30.1,
            warehouse=self.warehouse)

    def test_total_procurement(self):
        total = Procurement.total_procurement(self.product_variation)
        self.assertEqual(total, 50)

    def test_total_procurement_empty(self):
        total = Procurement.total_procurement_for_id(99998877)
        self.assertEqual(total, 0)

    def test_total_procurement_map(self):
        p_map = Procurement.total_procurement_map()
        self.assertDictEqual(dict(p_map), {
            self.product_variation.id: 50,
            self.product_variation2.id: 10})
        self.assertEqual(p_map[999888], 0)
