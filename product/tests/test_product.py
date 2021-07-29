from django.urls import reverse
from rest_framework.test import APITestCase

from core.tests import BaseTestSimpleApi
from product.models import Product
from thairod.utils.load_seed import load_seed


class ProductAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

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
