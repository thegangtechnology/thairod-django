from django.urls import reverse

from core.tests import BaseTestSimpleApiMixin
from product.models import Product, ProductImage
from thairod.utils.test_util import APITestCase


class ProductImageAPITestCase(APITestCase, BaseTestSimpleApiMixin):

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
