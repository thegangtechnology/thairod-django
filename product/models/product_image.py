from django.db import models
from core.models import AbstractModel
from product.models import Product


class ProductImage(AbstractModel):
    # TODO: Django has image field no?
    # https://docs.djangoproject.com/en/3.2/topics/files/
    # following the doc above, we don't need this model.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_index = models.IntegerField()
    path = models.CharField(max_length=255)
