from django.urls import reverse

from core.tests import BaseTestSimpleApiMixin
from product.models import ProductVariation
from stock_adjustment.models import StockAdjustment
from thairod.utils.test_util import APITestCase
from warehouse.models import Warehouse


class StockAdjustmentAPITestCase(APITestCase, BaseTestSimpleApiMixin):

    def setUp(self):
        self.set_up_user()
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
