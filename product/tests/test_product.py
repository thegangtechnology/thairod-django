from django.urls import reverse

from core.tests import BaseTestSimpleApiMixin, BaseTestReadOnlySimpleApiMixin
from product.models import Product
from thairod.utils.test_util import APITestCase


class ProductAPITestCase(BaseTestSimpleApiMixin, APITestCase, BaseTestReadOnlySimpleApiMixin):

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
        self.set_up_user()
