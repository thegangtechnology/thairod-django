from django.urls import reverse
from thairod.utils.test_util import APITestCase

from core.tests import BaseTestSimpleApiMixin
from product.models import Product, ProductImage
from thairod.utils.load_seed import load_seed


class ProductImageAPITestCase(APITestCase, BaseTestSimpleApiMixin):
    @classmethod
    def setUpTestData(cls):
        load_seed()

    def setUp(self):
        self.model = Product
        self.obj = ProductImage.objects.first()
        self.list_url = reverse('product-image-list')
        self.detail_url = reverse('product-image-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "product": Product.objects.first().id,
            "order_index": 1,
            "path": "www.example.com",
        }
