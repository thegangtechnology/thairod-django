from django.urls import reverse
from rest_framework import status
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
            "status": "PENDING",
            "price": 2345.124,
            "discount": 123.124,
            "courier_code": "123456789",
            "courier_tracking_code": "987654321"
        }

    def test_create(self) -> None:
        response = self.client.post(self.list_url, self.valid_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self) -> None:
        response = self.client.put(self.detail_url, self.valid_field, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

