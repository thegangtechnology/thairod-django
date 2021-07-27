from django.urls import reverse
from rest_framework.test import APITestCase

from address.models import Address
from core.tests import BaseTestSimpleApi
from order.models import Order
from shipment.models import TrackingStatus
from thairod.utils.load_seed import load_seed


class TrackingStatusAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.obj = TrackingStatus.objects.first()
        self.order = Order.objects.first()
        self.list_url = reverse('tracking-list')
        self.detail_url = reverse('tracking-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "tracking_code": "00123",
            "status": "PENDING"
        }
