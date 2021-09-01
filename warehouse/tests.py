from django.urls import reverse

from address.models import Address
from core.tests import BaseTestSimpleApiMixin, BaseTestReadOnlySimpleApiMixin
from thairod.utils.test_util import APITestCase
from warehouse.models import Warehouse


class WarehouseAPITestCase(BaseTestSimpleApiMixin, APITestCase, BaseTestReadOnlySimpleApiMixin):

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
        self.set_up_user()
