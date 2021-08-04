from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import AbstractModel
from product.models import ProductVariation
from shipment.models import Shipment


class FulfilmentStatus(models.IntegerChoices):
    PENDING = (0, _('PENDING'))
    FULFILLED = (1, _('FULFILLED'))


class OrderItem(AbstractModel):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, null=True)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=3)
    fulfilment_status = models.IntegerField(choices=FulfilmentStatus.choices, default=FulfilmentStatus.PENDING)

    @classmethod
    def example(cls):
        return OrderItem(
            product_variation=ProductVariation.example(),
            quantity=10,
            total_price=100
        )
