from django.db import models
from core.models import AbstractModel
from warehouse.models import Warehouse
from product.models import ProductVariation


class StockAdjustment(AbstractModel):
    quantity = models.IntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    reason = models.TextField()
