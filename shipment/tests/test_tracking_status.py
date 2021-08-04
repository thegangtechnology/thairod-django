from django.urls import reverse

from core.tests import BaseTestSimpleApiMixin
from order.models import Order
from shipment.models import TrackingStatus, Shipment
from thairod.utils.test_util import APITestCase


class TrackingStatusAPITestCase(BaseTestSimpleApiMixin, APITestCase):

    def setUp(self):
        self.model = TrackingStatus
        self.set_up_user()
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
