from django.urls import reverse
from rest_framework.test import APITestCase

from address.models import Address
from core.tests import BaseTestSimpleApi
from thairod.utils.load_seed import load_seed
from warehouse.models import Warehouse


class WarehouseAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.model = Warehouse
        self.obj = Warehouse.objects.first()
        self.address = Address.objects.first()
        self.list_url = reverse('warehouse-list')
        self.detail_url = reverse('warehouse-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "name": "warehouse name",
            "address": self.address.pk,
            "tel": "0987654321",
        }
