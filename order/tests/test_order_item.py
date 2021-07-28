from django.urls import reverse
from rest_framework.test import APITestCase

from address.models import Address
from core.tests import BaseTestSimpleApi
from order.models import OrderItem
from product.models import ProductVariation
from shipment.models import Shipment
from thairod.utils.load_seed import load_seed


class OrderItemAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.model = OrderItem
        self.obj = OrderItem.objects.first()
        self.address = Address.objects.first()
        self.list_url = reverse('order-item-list')
        self.detail_url = reverse('order-item-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "shipment_id": Shipment.objects.first().id,
            "product_variation": ProductVariation.objects.first().id,
            "quantity": 1212,
            "total_price": 1234.567,
            "order_by": "id",
        }
