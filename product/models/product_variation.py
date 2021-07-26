from django.db import models
from core.models import AbstractModel
from product.models import Product


class ProductVariation(AbstractModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)