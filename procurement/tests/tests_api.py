from django.urls import reverse

from address.models import Address
from core.tests import BaseTestSimpleApiMixin
from procurement.models import Procurement
from product.models import ProductVariation
from thairod.utils.test_util import APITestCase
from warehouse.models import Warehouse


class ProcurementAPITestCase(APITestCase, BaseTestSimpleApiMixin):

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
