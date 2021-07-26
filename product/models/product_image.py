from django.db import models
from core.models import AbstractModel
from product.models import Product


class ProductImage(AbstractModel):
    # TODO: Django has image field no?
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_index = models.IntegerField()
    path = models.CharField(max_length=255)
