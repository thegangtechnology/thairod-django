from order_flow.dataclasses import CreateOrderFlowRequest
from order_flow.models import OrderFlow
from order_flow.services import OrderFlowService
from thairod.utils.load_seed import load_realistic_seed
from order_flow.dataclasses.order_flow import OrderFlowResponse
from thairod.utils.test_util import TestCase, APITestCase
from order.dataclasses.cart_item import CartItem
from django.urls import reverse
from rest_framework import status
import json
from os.path import join, dirname


class TestOrderFlowService(TestCase):

    def setUp(self):
        seed = load_realistic_seed()
        self.seed = seed

    def test_create_order_flow(self):
        items = [CartItem(item_id=self.seed.product_variations[0].id, quantity=1)]
        old_count = OrderFlow.objects.count()
        OrderFlowService().create_order_flow(create_order_flow_request=CreateOrderFlowRequest.example(items=items))
        new_count = OrderFlow.objects.count()
        self.assertEqual(old_count + 1, new_count)

    def test_order_flow_to_create_order_flow_request(self):
        OrderFlowService().construct_create_order_parameter_from_order_flow_response(OrderFlowResponse.example())

    def test_create_order_flow_with_doctor_confirm(self):
        filename = 'create_order_flow_confirm_true.json'
        with open(join(dirname(__file__), filename), 'r') as json_file:
            order_flow_json = json.load(json_file)
            order_flow_request = CreateOrderFlowRequest(**order_flow_json)
            order_flow_response = OrderFlowService().create_order_flow(create_order_flow_request=order_flow_request)
            self.assertTrue(order_flow_response.auto_doctor_confirm)
            self.assertEqual(order_flow_response.patient_link_hash_timestamp, None)

    def test_create_order_flow_with_doctor_not_confirm(self):
        filename = 'create_order_flow_confirm_false.json'
        with open(join(dirname(__file__), filename), 'r') as json_file:
            order_flow_json = json.load(json_file)
            order_flow_request = CreateOrderFlowRequest(**order_flow_json)
            order_flow_response = OrderFlowService().create_order_flow(create_order_flow_request=order_flow_request)
            self.assertFalse(order_flow_response.auto_doctor_confirm)
            self.assertEqual(order_flow_response.patient_link_hash_timestamp, None)

    def test_create_order_flow_no_order(self):
        filename = 'create_order_flow_no_items.json'
        with open(join(dirname(__file__), filename), 'r') as json_file:
            order_flow_json = json.load(json_file)
            order_flow_request = CreateOrderFlowRequest(**order_flow_json)
            order_flow_response = OrderFlowService().create_order_flow(create_order_flow_request=order_flow_request)
            self.assertFalse(order_flow_response.auto_doctor_confirm)
            self.assertEqual(order_flow_response.patient_link_hash_timestamp, None)
            self.assertEqual(order_flow_response.doctor_order, None)

    def test_create_order_flow_with_order(self):
        filename = 'create_order_flow_confirm_true.json'
        with open(join(dirname(__file__), filename), 'r') as json_file:
            order_flow_json = json.load(json_file)
            order_flow_request = CreateOrderFlowRequest(**order_flow_json)
            order_flow_request.items = [CartItem(item_id=self.seed.product_variations[0].id, quantity=1)]
            order_flow_response = OrderFlowService().create_order_flow(create_order_flow_request=order_flow_request)
            self.assertTrue(order_flow_response.auto_doctor_confirm)
            self.assertFalse(order_flow_response.doctor_order.is_confirmed)
            self.assertEqual(order_flow_response.patient_link_hash_timestamp, None)
            self.assertEqual(len(order_flow_response.doctor_order.items), 1)
            self.assertEqual(order_flow_response.doctor_order.items[0].id, self.seed.product_variations[0].id)
            self.assertEqual(order_flow_response.doctor_order.items[0].quantity, 1)
            self.assertEqual(order_flow_response.doctor_order.items[0].description,
                             self.seed.product_variations[0].description)

    # test create override order when patient hash is create


class TestOrderFlowAPI(APITestCase):

    def test_invalid_query(self):
        url = reverse("order-flows-hash")
        response = self.client.get(url, {'doctor': 'a'}, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        url = reverse("order-flows-hash")
        response = self.client.get(url, {'patient': 'b'}, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
