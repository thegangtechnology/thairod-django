from django.db import models
from core.models import AbstractModel
from product.models import ProductVariation
from shipment.models import Shipment


class OrderItem(AbstractModel):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, null=True)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=3)
