from datetime import datetime, timedelta
from typing import Iterable

import pytz
from django.urls import reverse

from address.models import Address
from core.tests import BaseTestSimpleApiMixin
from order.dataclasses.cart_item import CartItem
from order.dataclasses.order import CreateOrderParameter
from order.models import Order
from order.models.order_item import FulfilmentStatus, OrderItem
from order.services.order_service import OrderService
from thairod.utils.load_seed import load_realistic_seed
from thairod.utils.test_util import APITestCase, TestCase


class OrderAPITestCase(BaseTestSimpleApiMixin, APITestCase):

    def setUp(self):
        self.model = Order
        self.obj = Order.objects.first()
        self.address = Address.objects.first()
        self.list_url = reverse('order-list')
        self.detail_url = reverse('order-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "receiver_address": self.address.pk,
            "cid": "qwerty",
            "orderer_name": 'piti',
            "orderer_license": 'sun',
        }


class TestOrderItemTotal(TestCase):
    with_seed = False

    def sample_orders(self, product_variation_id: int, n: int):
        for i in range(n):
            cart = CartItem(item_id=product_variation_id, quantity=1)
            param = CreateOrderParameter.example(items=[cart])
            order = OrderService().create_raw_order(param)
            if i % 2 == 0:
                for item in order.shipment.orderitem_set.all():
                    item.fulfill()

    def setUp(self):
        seed = load_realistic_seed()
        self.seed = seed

        self.sample_orders(self.seed.product_variations[0].id, 20)
        self.sample_orders(self.seed.product_variations[1].id, 50)

    def test_fulfill(self):
        item = OrderItem.objects.filter(fulfilment_status=FulfilmentStatus.PENDING).first()
        self.assertEqual(item.fulfilment_status, FulfilmentStatus.PENDING)
        item.fulfill()
        fulfilled_item = OrderItem.objects.get(pk=item.id)
        self.assertEqual(fulfilled_item.fulfilment_status, FulfilmentStatus.FULFILLED)
        self.assertGreaterEqual(fulfilled_item.fulfill_datetime,
                                datetime.now(pytz.utc) - timedelta(seconds=1))

    def test_total_fulfilled(self):
        total = OrderItem.total_fulfilled(self.seed.product_variations[0])
        self.assertEqual(total, 10)

    def test_total_fulfilled_not_found(self):
        total = OrderItem.total_fulfilled_for_id(999888)
        self.assertEqual(total, 0)

    def test_total_fulfilled_map(self):
        got = OrderItem.total_fulfilled_map()
        self.assertDictEqual(dict(got), {
            self.seed.product_variations[0].id: 10,
            self.seed.product_variations[1].id: 25,
        })
        self.assertEqual(got[30], 0)

    def test_total_pending(self):
        total = OrderItem.total_pending_for_id(self.seed.product_variations[0].id)
        self.assertEqual(total, 10)

    def test_sorted_pending_order(self):
        qs: Iterable[OrderItem] = OrderItem.sorted_pending_order_items()
        pending_items = list(qs)
        for pending_item in pending_items:
            self.assertEqual(pending_item.fulfilment_status, FulfilmentStatus.PENDING)
        self.assertLessEqual(
            pending_items[0].shipment.order.order_time,
            pending_items[1].shipment.order.order_time
        )
