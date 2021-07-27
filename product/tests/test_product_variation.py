from django.urls import reverse
from rest_framework.test import APITestCase
from core.tests import BaseTestSimpleApi
from product.models import Product, ProductVariation
from thairod.utils.load_seed import load_seed


class ProductVariationAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.obj = ProductVariation.objects.first()
        self.list_url = reverse('product-variation-list')
        self.detail_url = reverse('product-variation-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "product": Product.objects.first().id,
            "price": 2133.123,
            "name": "product test name",
            "description": "test description"
        }