from dataclasses import asdict

from django.urls import reverse

from order.models import Order
from order.views import OrderService, CreateOrderParameter
from thairod.utils.test_util import TestCase, APITestCase


class TestCreateOrder(TestCase):

    def test_create_order(self):
        old_count = Order.objects.count()
        param = CreateOrderParameter.example_with_valid_item()
        OrderService().create_order(param)
        new_count = Order.objects.count()

        self.assertEqual(old_count + 1, new_count)


class TestCreateOrderAPI(APITestCase):
    def test_create_order_api(self):
        # note no login

        param = CreateOrderParameter.example_with_valid_item()
        url = reverse('create-order')
        res = self.client.post(url, data=asdict(param), format='json')
        self.assertEqual(res.status_code, 200)
