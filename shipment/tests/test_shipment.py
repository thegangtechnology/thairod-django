from django.urls import reverse
from rest_framework.test import APITestCase

from address.models import Address
from core.tests import BaseTestSimpleApi
from order.models import Order
from shipment.models import Shipment, TrackingStatus
from thairod.utils.load_seed import load_seed
from warehouse.models import Warehouse


class ShipmentAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.obj = Shipment.objects.first()
        self.warehouse = Warehouse.objects.first()
        self.tracking = TrackingStatus.objects.first()
        self.order = Order.objects.first()
        self.list_url = reverse('shipment-list')
        self.detail_url = reverse('shipment-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "warehouse": self.warehouse.pk,
            "tracking": self.tracking.pk,
            "order": self.order.pk,
            "title": "testtitle23456",
            "shipping_method": "testshipping_method",
            "weight": 2345.678,
            "note": "test note",
            "shippop_purchase_id": "1234abcd"
        }