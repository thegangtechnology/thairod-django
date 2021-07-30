from order.models import Order
from order.views import OrderService, CreateOrderParameter
from product.models import ProductVariation
from thairod.utils.test_util import TestCase


class TestCreateOrder(TestCase):

    def test_create_order(self):
        old_count = Order.objects.count()
        param = CreateOrderParameter.example_with_valid_item()
        OrderService().create_order(param)
        new_count = Order.objects.count()

        self.assertEqual(old_count + 1, new_count)
