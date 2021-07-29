from contextlib import contextmanager
from unittest.mock import patch


from order.models import Order
from order.views import OrderService, CreateOrderParameter
from thairod.services.shippop.api import ShippopAPI
from thairod.services.shippop.data import OrderResponse, OrderLineResponse
from thairod.utils.load_seed import load_seed
from thairod.utils.test_util import TestCase


class TestCreateOrder(TestCase):
    reset_sequences = True

    def setUp(self):
        load_seed()

    def mocked_create_order_response(self) -> OrderResponse:
        return OrderResponse(
            status=True,
            purchase_id=1,
            total_price=100,
            lines=[
                OrderLineResponse(
                    status=True,
                    tracking_code='tacking_code',
                    price=25,
                    discount=10,
                    from_address=None,
                    to_address=None,
                    courier_tracking_code='c_track'
                )
            ]
        )

    @contextmanager
    def patch_shippop(self):
        with patch.object(ShippopAPI, 'create_order', return_value=self.mocked_create_order_response()) as mock:
            with patch.object(ShippopAPI, 'confirm_order', return_value='True'):
                yield mock

    def test_create_order(self):
        with self.patch_shippop() as _:
            old_count = Order.objects.count()
            OrderService().create_order(
                CreateOrderParameter.example()
            )
            new_count = Order.objects.count()

            self.assertEqual(old_count + 1, new_count)
