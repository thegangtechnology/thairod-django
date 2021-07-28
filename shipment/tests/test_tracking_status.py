from django.urls import reverse
from rest_framework.test import APITestCase

from core.tests import BaseTestSimpleApi
from order.models import Order
from shipment.models import TrackingStatus, Shipment
from thairod.utils.load_seed import load_seed


class TrackingStatusAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.model = TrackingStatus
        self.obj = TrackingStatus.objects.first()
        self.order = Order.objects.first()
        self.shipment = Shipment.objects.first()
        self.list_url = reverse('tracking-list')
        self.detail_url = reverse('tracking-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "status": "PENDING",
            "price": 2345.124,
            "discount": 123.124,
            "shipment": self.shipment.pk,
            "courier_code": "123456789",
            "courier_tracking_code": "987654321"
        }
