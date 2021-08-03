from django.urls import reverse
from thairod.utils.test_util import APITestCase

from core.tests import BaseTestSimpleApiMixin
from product.models import Product
from thairod.utils.load_seed import load_seed


class ProductAPITestCase(BaseTestSimpleApiMixin, APITestCase):


    def setUp(self):
        self.mode = Product
        self.obj = Product.objects.first()
        self.list_url = reverse('product-list')
        self.detail_url = reverse('product-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "sku": "test_product_sku",
            "name": "test product name",
            "description": "23456",
        }
