from order_flow.dataclasses import CreateOrderFlowRequest
from order_flow.models import OrderFlow
from order_flow.services import OrderFlowService
from order_flow.dataclasses.order_flow import OrderFlowResponse
from thairod.utils.test_util import TestCase, APITestCase
from django.urls import reverse
from rest_framework import status


class TestOrderFlowService(TestCase):

    # TODO: More test
    def test_create_order_flow(self):
        # minimal test because this is supposedly to be for next week
        old_count = OrderFlow.objects.count()
        OrderFlowService().create_order_flow(create_order_flow_request=CreateOrderFlowRequest.example())
        new_count = OrderFlow.objects.count()
        self.assertEqual(old_count + 1, new_count)

    def test_order_flow_to_create_order_flow_request(self):
        OrderFlowService().construct_create_order_parameter_from_order_flow_response(OrderFlowResponse.example())


class TestOrderFlowAPI(APITestCase):

    def test_invalid_query(self):
        url = reverse("order-flows-hash")
        response = self.client.get(url, {'doctor': 'a'}, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        url = reverse("order-flows-hash")
        response = self.client.get(url, {'patient': 'b'}, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
