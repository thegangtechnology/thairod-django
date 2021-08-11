from order_flow.dataclasses import CreateOrderFlowParam, CheckoutDoctorOrderRequest, DoctorOrder, \
    PatientConfirmationRequest
from order_flow.models import OrderFlow
from order_flow.services import OrderFlowService
from thairod.utils.load_seed import load_realistic_seed
from thairod.utils.test_util import APITestCase
from order.dataclasses.cart_item import CartItem
from order.dataclasses.shipping_address import ShippingAddress
from django.urls import reverse
from rest_framework import status


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
        order_flow_request = CreateOrderFlowParam.example(items=[])
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

    def test_doctor_confirm_not_exist_hash_api(self):
        new_item = [CartItem(item_id=self.seed.product_variations[0].id, quantity=1)]
        doctor_checkout = CheckoutDoctorOrderRequest(doctor_link_hash="kkkkk",
                                                     doctor_order=DoctorOrder(items=new_item)).to_data()
        url = reverse("order-flows-doctor-checkout")
        response = self.client.post(url, doctor_checkout, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_confirm_api(self):
        items = [CartItem(item_id=self.seed.product_variations[0].id, quantity=1)]
        order_flow_request = CreateOrderFlowParam.example(items=items, auto_doctor_confirm=True)
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

    def test_patient_confirm_not_exist_hash_api(self):
        patient_confirmation = PatientConfirmationRequest(patient_link_hash="abcd",
                                                          address=ShippingAddress.example()).to_data()
        url = reverse("order-flows-patient-checkout")
        response = self.client.post(url, patient_confirmation, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
