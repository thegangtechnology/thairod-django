from order_flow.dataclasses import CreateOrderFlowRequest, CheckoutDoctorOrderRequest, DoctorOrder, \
    PatientConfirmationRequest
from order_flow.models import OrderFlow
from order_flow.services import OrderFlowService
from thairod.utils.load_seed import load_realistic_seed
from order_flow.dataclasses.order_flow import OrderFlowResponse
from thairod.utils.test_util import TestCase, APITestCase
from order.dataclasses.cart_item import CartItem
from order.dataclasses.shipping_address import ShippingAddress
from django.urls import reverse
from rest_framework import status
import json
from os.path import join, dirname
from order_flow.exceptions import OrderAlreadyConfirmedException, PatientAlreadyConfirmedException


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
            order_flow_request.items = [CartItem(item_id=self.seed.product_variations[0].id, quantity=1)]
            order_flow_response = OrderFlowService().create_order_flow(create_order_flow_request=order_flow_request)
            # auto doctor confirm should be true
            self.assertTrue(order_flow_response.auto_doctor_confirm)
            # should have patient link hash
            self.assertIsNotNone(order_flow_response.patient_link_hash)
            self.assertIsNotNone(order_flow_response.patient_link_hash_timestamp)

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
        filename = 'create_order_flow_confirm_false.json'
        with open(join(dirname(__file__), filename), 'r') as json_file:
            order_flow_json = json.load(json_file)
            order_flow_request = CreateOrderFlowRequest(**order_flow_json)
            order_flow_request.items = [CartItem(item_id=self.seed.product_variations[0].id, quantity=1)]
            order_flow_response = OrderFlowService().create_order_flow(create_order_flow_request=order_flow_request)
            self.assertFalse(order_flow_response.auto_doctor_confirm)
            self.assertFalse(order_flow_response.doctor_order.is_confirmed)
            self.assertEqual(order_flow_response.patient_link_hash_timestamp, None)
            self.assertEqual(len(order_flow_response.doctor_order.items), 1)
            self.assertEqual(order_flow_response.doctor_order.items[0].id, self.seed.product_variations[0].id)
            self.assertEqual(order_flow_response.doctor_order.items[0].quantity, 1)
            self.assertEqual(order_flow_response.doctor_order.items[0].description,
                             self.seed.product_variations[0].description)

    def test_override_initial_order_before_confirm(self):
        items = [CartItem(item_id=self.seed.product_variations[0].id, quantity=1)]
        order_flow_request = CreateOrderFlowRequest.example(items=items)
        order_flow_response = OrderFlowService().create_order_flow(create_order_flow_request=order_flow_request)
        # still initial order
        self.assertEqual(len(order_flow_response.doctor_order.items), 1)
        self.assertEqual(order_flow_response.doctor_order.items[0].id, self.seed.product_variations[0].id)
        # no patient hash yet
        self.assertTrue(order_flow_response.patient_link_hash is None)
        new_item = [CartItem(item_id=self.seed.product_variations[1].id, quantity=1)]
        doctor_checkout = CheckoutDoctorOrderRequest(doctor_link_hash=order_flow_response.doctor_link_hash,
                                                     doctor_order=DoctorOrder(items=new_item))
        response = OrderFlowService().write_doctor_order_to_order_flow(checkout_doctor_order_request=doctor_checkout)
        # should be new order and patient hash should be created
        self.assertEqual(response.doctor_link_hash, doctor_checkout.doctor_link_hash)
        self.assertTrue(response.patient_link_hash is not None)
        self.assertEqual(response.doctor_order.items[0].id, self.seed.product_variations[1].id)
        self.assertEqual(order_flow_response.doctor_order.items[0].quantity, 1)
        self.assertEqual(order_flow_response.doctor_order.items[0].description,
                         self.seed.product_variations[1].description)

    def test_override_doctor_order_after_confirm(self):
        order_flow_request = CreateOrderFlowRequest.example(items=[])
        order_flow_response = OrderFlowService().create_order_flow(create_order_flow_request=order_flow_request)
        # no patient hash yet
        self.assertTrue(order_flow_response.patient_link_hash is None)
        new_item = [CartItem(item_id=self.seed.product_variations[0].id, quantity=1)]
        doctor_checkout = CheckoutDoctorOrderRequest(doctor_link_hash=order_flow_response.doctor_link_hash,
                                                     doctor_order=DoctorOrder(items=new_item))
        response = OrderFlowService().write_doctor_order_to_order_flow(checkout_doctor_order_request=doctor_checkout)
        # should be new order and patient hash should be created
        self.assertEqual(response.doctor_link_hash, doctor_checkout.doctor_link_hash)
        self.assertTrue(response.patient_link_hash is not None)
        self.assertEqual(response.doctor_order.items[0].id, self.seed.product_variations[0].id)
        self.assertEqual(response.doctor_order.items[0].quantity, 1)
        self.assertEqual(response.doctor_order.items[0].description,
                         self.seed.product_variations[0].description)
        # if try to override should go boom boom
        with self.assertRaises(OrderAlreadyConfirmedException):
            OrderFlowService().write_doctor_order_to_order_flow(
                checkout_doctor_order_request=doctor_checkout)

    def test_confirm_patient(self):
        filename = 'create_order_flow_confirm_true.json'
        with open(join(dirname(__file__), filename), 'r') as json_file:
            order_flow_json = json.load(json_file)
            order_flow_request = CreateOrderFlowRequest(**order_flow_json)
            order_flow_request.items = [CartItem(item_id=self.seed.product_variations[0].id, quantity=1)]
            order_flow_response = OrderFlowService().create_order_flow(create_order_flow_request=order_flow_request)
            patient_confirmation = PatientConfirmationRequest(patient_link_hash=order_flow_response.patient_link_hash,
                                                              address=ShippingAddress.example())
            OrderFlowService().save_patient_confirmation_and_make_order(
                patient_confirmation_request=patient_confirmation)
            flow = OrderFlow.objects.get(patient_link_hash=order_flow_response.patient_link_hash)
            self.assertTrue(flow.order_created)
            # try to make order again should get error
            with self.assertRaises(PatientAlreadyConfirmedException):
                OrderFlowService().save_patient_confirmation_and_make_order(
                    patient_confirmation_request=patient_confirmation)


class TestOrderFlowAPI(APITestCase):

    def setUp(self):
        seed = load_realistic_seed()
        self.seed = seed

    def test_invalid_query(self):
        url = reverse("order-flows-hash")
        response = self.client.get(url, {'doctor': 'a'}, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        url = reverse("order-flows-hash")
        response = self.client.get(url, {'patient': 'b'}, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_doctor_confirm_api(self):
        order_flow_request = CreateOrderFlowRequest.example(items=[])
        order_flow_response = OrderFlowService().create_order_flow(create_order_flow_request=order_flow_request)
        # no patient hash yet
        self.assertTrue(order_flow_response.patient_link_hash is None)
        new_item = [CartItem(item_id=self.seed.product_variations[0].id, quantity=1)]
        doctor_checkout = CheckoutDoctorOrderRequest(doctor_link_hash=order_flow_response.doctor_link_hash,
                                                     doctor_order=DoctorOrder(items=new_item)).to_data()
        url = reverse("order-flows-doctor-checkout")
        response = self.client.post(url, doctor_checkout, format='json')
        # should be new order and patient hash should be created
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('doctor_link_hash'), doctor_checkout.get('doctor_link_hash'))
        self.assertTrue(response.data.get('patient_link_hash') is not None)
        # try again should be 400
        response = self.client.post(url, doctor_checkout, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_confirm_api(self):
        items = [CartItem(item_id=self.seed.product_variations[0].id, quantity=1)]
        order_flow_request = CreateOrderFlowRequest.example(items=items, auto_doctor_confirm=True)
        order_flow_response = OrderFlowService().create_order_flow(create_order_flow_request=order_flow_request)
        patient_confirmation = PatientConfirmationRequest(patient_link_hash=order_flow_response.patient_link_hash,
                                                          address=ShippingAddress.example()).to_data()
        url = reverse("order-flows-patient-checkout")
        response = self.client.post(url, patient_confirmation, format='json')
        # 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        flow = OrderFlow.objects.get(patient_link_hash=order_flow_response.patient_link_hash)
        # order created
        self.assertTrue(flow.order_created)
        
        # bad request, already create for this order.
        url = reverse("order-flows-patient-checkout")
        response = self.client.post(url, patient_confirmation, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)