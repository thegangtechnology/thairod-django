from dataclasses import asdict

from django.urls import reverse
from rest_framework.exceptions import ValidationError

from order.models import Order
from order.views import OrderService, CreateOrderParameter
from shipment.models.box_size import BoxSize
from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import TestCase, APITestCase


class TestOrderService(TestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()

    def test_create_order(self):
        old_count = Order.objects.count()
        param = CreateOrderParameter.example_with_valid_item()
        OrderService().create_order(param)
        new_count = Order.objects.count()
        self.assertEqual(old_count + 1, new_count)

    def test_create_order_correct_data(self):
        param = CreateOrderParameter.example_with_valid_item()
        res = OrderService().create_order(param)
        order = Order.objects.get(pk=res.order_id)
        self.assertEqual(order.line_id, param.line_id)
        self.assertEqual(order.telemed_session_id, param.session_id)

    def test_determine_box_size(self):
        param = CreateOrderParameter.example_with_valid_item()
        box = OrderService().determine_box_size(param)
        self.assertEqual(type(box), BoxSize)

    def test_order_restricted_product_twice(self):
        pv = self.seed.make_product(restricted=True)

        res = self.seed.order_item(pv.id)
        self.assertTrue(res.success)

        try:
            self.seed.order_item(pv.id)
            self.assertTrue(False, msg='should raise validation error')
        except ValidationError as e:
            self.assertIn('cid', e.detail)

    def test_order_restricted_then_non_restricted(self):
        res_pv = self.seed.make_product(restricted=True)
        free_pv = self.seed.make_product(restricted=False)

        res = self.seed.order_item(res_pv.id)
        self.assertTrue(res.success)
        res = self.seed.order_item(free_pv.id)
        self.assertTrue(res.success)

    def test_order_non_restricted_then_restricted(self):
        res_pv = self.seed.make_product(restricted=True)
        free_pv = self.seed.make_product(restricted=False)

        res = self.seed.order_item(free_pv.id)
        self.assertTrue(res.success)
        res = self.seed.order_item(res_pv.id)
        self.assertTrue(res.success)

    def test_different_ppl_order_restricted_product(self):
        res_pv = self.seed.make_product(restricted=True)

        res = self.seed.order_item(res_pv.id, cid='111')
        self.assertTrue(res.success)
        res = self.seed.order_item(res_pv.id, cid='222')
        self.assertTrue(res.success)


class TestCreateOrderAPI(APITestCase):
    def test_create_order_api(self):
        # note no login
        param = CreateOrderParameter.example_with_valid_item()
        url = reverse('create-order')
        res = self.client.post(url, data=asdict(param), format='json')
        self.assertEqual(res.status_code, 200)
