from collections import defaultdict
from typing import DefaultDict

from django.db import models
from django.db.models import Sum

from core.models import AbstractModel
from product.models import ProductVariation
from warehouse.models import Warehouse


class Procurement(AbstractModel):
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, db_index=True)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(decimal_places=3, max_digits=8)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    @classmethod
    def total_procurement(cls, product_variation: ProductVariation) -> int:
        return cls.total_procurement_for_id(product_variation.id)

    @classmethod
    def total_procurement_for_id(cls, product_variation_id: int) -> int:
        ret = cls.objects.filter(product_variation_id=product_variation_id) \
            .values('product_variation_id').annotate(item_count=Sum('quantity'))
        return ret[0]['item_count'] if len(ret) > 0 else 0

    @classmethod
    def total_procurement_map(cls) -> DefaultDict[int, int]:
        """
        Returns:
            Dict[item_id, total]
        """
        res = cls.objects.values('product_variation_id').annotate(item_count=Sum('quantity'))
        ret = defaultdict(lambda: 0)
        ret.update({s['product_variation_id']: s['item_count'] for s in res})
        return ret
