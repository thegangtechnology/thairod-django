from django.urls import reverse
from rest_framework.test import APITestCase

from address.models import Address
from core.tests import BaseTestSimpleApi
from order.models import Order
from thairod.utils.load_seed import load_seed


class OrderAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.obj = Order.objects.first()
        self.address = Address.objects.first()
        self.list_url = reverse('order-list')
        self.detail_url = reverse('order-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "receiver_name": "test_receiver_name",
            "receiver_address": self.address.pk,
            "receiver_tel": "23456",
            "cid": "qwerty",
            "order_by": "rtyuu",
            "order_time": "bangkok",
        }