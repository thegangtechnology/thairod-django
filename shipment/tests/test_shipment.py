from django.urls import reverse
from rest_framework import status

from core.tests import BaseTestSimpleApiMixin
from order.models import Order
from shipment.models import Shipment, TrackingStatus, BatchShipment
from thairod.utils.load_seed import RealisticSeed
from thairod.utils.test_util import APITestCase, TestCase
from warehouse.models import Warehouse


class ShipmentAPITestCase(APITestCase, BaseTestSimpleApiMixin):

    def setUp(self):
        self.set_up_user()
        self.model = Shipment
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
        self.assertEqual(response.data['batch_name'], self.batch_shipments.name)
        self.assertEqual(response.data['is_assigned'], True)
        self.assertEqual(response.status_code, 200)

    def test_assign_invalid_batch_to_shipment(self):
        url = reverse("shipment-assign", kwargs={"pk": self.obj.pk})
        response = self.client.post(url, {"batch_name": None}, format='json')
        self.assertEqual(response.data, 'Batch Name is None.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestShipment(TestCase):
    with_seed = False

    def setUp(self):
        self.seed = RealisticSeed.load_realistic_seed()
        self.seed.full_production()

    def test_ready_to_ship(self):
        shipments = Shipment.ready_to_book_shipments()
        self.assertEqual(len(shipments), 4)
