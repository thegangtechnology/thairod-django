from collections import defaultdict
from typing import DefaultDict

from django.db import models
from django.db.models import Sum, QuerySet
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _

from core.models import AbstractModel
from product.models import ProductVariation
from shipment.models import Shipment


class FulfilmentStatus(models.IntegerChoices):
    PENDING = (0, _('PENDING'))
    FULFILLED = (1, _('FULFILLED'))
    CANCELLED = (2, _('CANCELLED'))


class OrderItem(AbstractModel):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, null=True, db_index=True)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, null=True, db_index=True)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=3)
    fulfilment_status = models.IntegerField(choices=FulfilmentStatus.choices, default=FulfilmentStatus.PENDING)
    fulfill_datetime = models.DateTimeField(default=None, null=True)

    def fulfill(self):
        OrderItem.objects.filter(id=self.id).update(
            fulfilment_status=FulfilmentStatus.FULFILLED,
            fulfill_datetime=Now())

    class Meta:
        indexes = [
            models.Index(fields=['fulfilment_status', 'product_variation'])
        ]

    @classmethod
    def example(cls):
        return OrderItem(
            product_variation=ProductVariation.example(),
            quantity=10,
            total_price=100
        )

    @classmethod
    def total_fulfilled_for_id(cls, id: int) -> int:
        qs = cls.objects.filter(fulfilment_status=FulfilmentStatus.FULFILLED,
                                product_variation_id=id) \
            .values('product_variation_id').annotate(total_count=Sum('quantity'))

        return qs[0]['total_count'] if len(qs) > 0 else 0

    @classmethod
    def total_fulfilled(cls, product_variation: ProductVariation) -> int:
        return cls.total_fulfilled_for_id(product_variation.id)

    @classmethod
    def total_fulfilled_map(cls) -> DefaultDict[int, int]:
        qs = cls.objects.filter(fulfilment_status=FulfilmentStatus.FULFILLED) \
            .values('product_variation_id').annotate(total_count=Sum('quantity'))

        ret = defaultdict(lambda: 0)
        ret.update({s['product_variation_id']: s['total_count'] for s in qs})
        return ret

    @classmethod
    def sorted_pending_order_items(cls) -> QuerySet:
        return cls.objects.filter(fulfilment_status=FulfilmentStatus.PENDING) \
            .order_by('shipment__order__order_time')
