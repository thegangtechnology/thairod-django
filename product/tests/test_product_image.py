from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.tests import BaseTestSimpleApi
from product.models import Product, ProductImage
from thairod.utils.load_seed import load_seed


class ProductImageAPITestCase(BaseTestSimpleApi, APITestCase):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.obj = ProductImage.objects.first()
        self.list_url = reverse('product-image-list')
        self.detail_url = reverse('product-image-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "product": Product.objects.first().id,
            "order_index": 1,
            "path": "www.example.com",
        }
