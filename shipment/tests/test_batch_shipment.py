from django.urls import reverse
from rest_framework.test import APITestCase
from core.tests import BaseTestSimpleApi
from shipment.models import BatchShipment
from thairod.utils.load_seed import load_seed


class BatchShipmentAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.model = BatchShipment
        self.obj = BatchShipment.objects.first()
        self.list_url = reverse('batch-shipment-list')
        self.detail_url = reverse('batch-shipment-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "name": "test BATCH"
        }
