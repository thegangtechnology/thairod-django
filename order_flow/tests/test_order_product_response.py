from order_flow.dataclasses import OrderedProductInfo
from thairod.utils.test_util import TestCase
from order.dataclasses.cart_item import CartItem
from thairod.utils.load_seed import load_realistic_seed


class TestOrderProductResponse(TestCase):

    def setUp(self):
        seed = load_realistic_seed()
        self.seed = seed

    def test_ordered_product(self):
        cart_item = CartItem(item_id=self.seed.product_variations[0].id, quantity=10)
        ordered_product = OrderedProductInfo.from_cart_item(cart_item)
        assert ordered_product.id == cart_item.item_id
        assert ordered_product.quantity == 10
        assert self.seed.product_variations[0].description == ordered_product.description
