from django.db import models

from core.models import AbstractModel
from product.models import ProductVariation
from warehouse.models import Warehouse


class Procurement(AbstractModel):
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=3, max_digits=8)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
