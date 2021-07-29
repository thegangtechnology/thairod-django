from django.urls import reverse
from rest_framework.test import APITestCase

from address.models import Address
from core.tests import BaseTestSimpleApi
from procurement.models import Procurement
from product.models import ProductVariation
from thairod.utils.load_seed import load_seed
from warehouse.models import Warehouse


class ProcurementAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.set_up_user()
        self.model = Procurement
        self.obj = Procurement.objects.first()
        self.address = Address.objects.first()
        try:
            Warehouse.objects.get(id=1)
        except Warehouse.DoesNotExist:
            Warehouse.objects.create(id=1, address=self.address, name='test warehouse', tel='12345678901')
        self.list_url = reverse('procurement-list')
        self.detail_url = reverse('procurement-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "product_variation": ProductVariation.objects.first().id,
            "quantity": 10,
            "unit_price": 875.123,
            "warehouse": Warehouse.objects.first().id,
        }
