from dataclasses import asdict

from django.urls import reverse
from rest_framework.exceptions import ValidationError

from order.models import Order
from order.views import OrderService, CreateOrderParam
from shipment.models import Shipment
from shipment.models.box_size import BoxSize
from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import TestCase, APITestCase


class TestOrderService(TestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()

    def test_create_order(self):
        old_count = Order.objects.count()
        param = CreateOrderParam.example_with_valid_item()
        OrderService().create_order(param)
        new_count = Order.objects.count()
        self.assertEqual(old_count + 1, new_count)

    def test_create_order_did_send_line_message(self):
        param = CreateOrderParam.example_with_valid_item()
        self.line_mock.reset_mock()
        self.seed.procure_item(param.items[0].item_id, 100)
        res = OrderService().create_order(param)
        order = Order.objects.get(pk=res.order_id)
        self.assertEqual(self.line_mock.call_count, 2)  # once for created and once for fulfill
        lineuid = self.line_mock.call_args_list[0][0][0]
        msg = self.line_mock.call_args_list[0][0][1].text
        self.assertEqual(order.line_id, lineuid)
        self.assertIn(order.receiver_address.name, msg)
        self.assertIn(str(order.id), msg)

        lineuid = self.line_mock.call_args_list[1][0][0]
        msg = self.line_mock.call_args_list[1][0][1].text
        shipment: Shipment = order.shipment_set.first()
        self.assertEqual(order.line_id, lineuid)
        self.assertIn(order.receiver_address.name, msg)
        self.assertIn(shipment.tracking_code, msg)

    def test_create_order_correct_data(self):
        param = CreateOrderParam.example_with_valid_item()
        res = OrderService().create_order(param)
        order = Order.objects.get(pk=res.order_id)
        self.assertEqual(order.line_id, param.line_id)
        self.assertEqual(order.telemed_session_id, param.session_id)

    def test_determine_box_size(self):
        param = CreateOrderParam.example_with_valid_item()
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
        param = CreateOrderParam.example_with_valid_item()
        url = reverse('create-order')
        res = self.client.post(url, data=asdict(param), format='json')
        self.assertEqual(res.status_code, 200)


class TestCreateOrderParam(TestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        self.seed.full_production()

    def test_example_is_valid(self):
        param = CreateOrderParam.example_with_valid_item()
        serializer = CreateOrderParam.serializer()
        data = serializer(param).data
        valid = serializer(data=data).is_valid()
        self.assertTrue(valid)

    def test_item_not_exists(self):
        param = CreateOrderParam.example_with_valid_item()
        param.items[0].item_id = 99999
        with self.assertRaises(ValidationError) as cm:
            CreateOrderParam.validate_data(param)
        self.assertIn('99999', cm.exception.detail[0])

    def test_item_negative_quantity(self):
        param = CreateOrderParam.example_with_valid_item()
        param.items[0].quantity = -10
        with self.assertRaises(ValidationError) as cm:
            CreateOrderParam.validate_data(param)
        self.assertIn('negative', cm.exception.detail[0])

    def test_item_invalid_zipcode(self):
        param = CreateOrderParam.example_with_valid_item()
        param.shipping_address.zipcode = '99999'
        with self.assertRaises(ValidationError) as cm:
            CreateOrderParam.validate_data(param)
        self.assertIn('99999', cm.exception.detail[0])
