from collections import defaultdict
from typing import DefaultDict

from django.db import models
from django.db.models import Sum

from core.models import AbstractModel
from product.models import ProductVariation
from warehouse.models import Warehouse


class StockAdjustment(AbstractModel):
    quantity = models.IntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, db_index=True)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    @classmethod
    def total_adjustment_for_id(cls, id: int) -> int:
        ret = cls.objects.filter(product_variation_id=id) \
            .values('product_variation_id') \
            .annotate(total_count=Sum('quantity'))
        return 0 if len(ret) == 0 else ret[0]['total_count']

    @classmethod
    def total_adjustment(cls, product_variation: ProductVariation):
        return cls.total_adjustment_for_id(product_variation.id)

    @classmethod
    def total_adjustment_map(cls) -> DefaultDict[int, int]:
        res = cls.objects.values('product_variation_id').annotate(total_count=Sum('quantity'))
        ret = defaultdict(lambda: 0)
        ret.update({r['product_variation_id']: r['total_count'] for r in res})
        return ret
