from django.urls import reverse
from rest_framework import status

from core.tests import BaseTestSimpleApiMixin
from product.models import Product, ProductVariation
from product.models.product_variation import ProductVariationUnit
from thairod.utils.test_util import APITestCase


class ProductVariationAPITestCase(APITestCase, BaseTestSimpleApiMixin):

    def setUp(self):
        self.model = ProductVariation
        self.obj = ProductVariation.objects.first()
        self.list_url = reverse('product-variation-list')
        self.detail_url = reverse('product-variation-detail', kwargs={'pk': self.obj.pk})
        self.valid_field = {
            "product": Product.objects.first().id,
            "price": 2133.123,
            "name": "product test name",
            "description": "test description"
        }

    def test_update(self) -> None:
        self.set_up_user()
        response = self.client.put(self.detail_url, {
            "product": Product.objects.first().id,
            "price": 3133.123,
            "name": "product update name",
            "description": "test update description",
            "unit": ProductVariationUnit.PACKS
        }, format='json')
        self.assertEqual(response.data['unit'], ProductVariationUnit.PACKS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
