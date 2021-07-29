from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.tests import BaseTestSimpleApi
from order.models import Order
from shipment.models import Shipment, TrackingStatus, BatchShipment
from thairod.utils.load_seed import load_seed
from warehouse.models import Warehouse


class ShipmentAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.model = Shipment
        self.set_up_user()
        self.obj = Shipment.objects.first()
        self.batch_shipments = BatchShipment.objects.first()
        self.warehouse = Warehouse.objects.first()
        self.tracking = TrackingStatus.objects.first()
        self.order = Order.objects.first()
        self.list_url = reverse('shipment-list')
        self.detail_url = reverse('shipment-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "warehouse": self.warehouse.pk,
            "shipping_method": "testshipping_method",
            "order": self.order.pk,
            "title": "testtitle23456",
            "weight": 2345.678,
            "note": "test note",
            "shippop_purchase": 1234,
            "tracking_code": "jlkjsdalfkj",
            "courier_tracking_code": "asfdsafdsaf"
        }

    def test_assign_batch_to_shipment(self):
        url = reverse("shipment-assign", kwargs={"pk": self.obj.pk})
        response = self.client.post(url, {"batch_name": self.batch_shipments.name}, format='json')
        print(response.data)
        self.assertEqual(response.data['batch_name'], self.batch_shipments.name)
        self.assertEqual(response.data['is_assigned'], True)
        self.assertEqual(response.status_code, 200)

    def test_assign_invalid_batch_to_shipment(self):
        url = reverse("shipment-assign", kwargs={"pk": self.obj.pk})
        response = self.client.post(url, {"batch_name": None}, format='json')
        self.assertEqual(response.data, 'Batch Name is None.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
