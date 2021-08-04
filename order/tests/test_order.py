from django.urls import reverse

from address.models import Address
from core.tests import BaseTestSimpleApiMixin
from order.models import Order
from thairod.utils.test_util import APITestCase


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
