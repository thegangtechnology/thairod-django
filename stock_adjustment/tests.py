from django.urls import reverse
from rest_framework.test import APITestCase


from core.tests import BaseTestSimpleApi
from product.models import ProductVariation
from stock_adjustment.models import StockAdjustment
from thairod.utils.load_seed import load_seed
from warehouse.models import Warehouse


class StockAdjustmentAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.model = StockAdjustment
        self.obj = StockAdjustment.objects.first()
        self.warehouse = Warehouse.objects.first()
        self.product_variation = ProductVariation.objects.first()
        self.list_url = reverse('stock-adjustments-list')
        self.detail_url = reverse('stock-adjustments-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "warehouse": self.warehouse.pk,
            "quantity": 1234,
            "product_variation": self.product_variation.pk,
            "reason": "random text"
        }
