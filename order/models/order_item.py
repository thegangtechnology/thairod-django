import datetime
import logging
from collections import defaultdict
from typing import DefaultDict, Optional

from django.db import models
from django.db.models import Sum, QuerySet
from django.utils.translation import gettext_lazy as _

from core.models import AbstractModel
from product.models import ProductVariation
from shipment.models import Shipment
from thairod.utils import tzaware
from thairod.utils.query_util import smart_range, smart_equal

logger = logging.getLogger(__name__)


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
            fulfill_datetime=tzaware.now())
        logger.info(f'Fulfill: oi_id: {self.id:d}, pv_id: {self.product_variation_id: d}')
        if self.shipment.is_ready_to_fulfill:
            self.shipment.mark_fulfilled()

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
    def _total_with_status_for_id(cls,
                                  status: Optional[FulfilmentStatus],
                                  id: int,
                                  date_col: str,
                                  begin: Optional[datetime.date] = None,
                                  end: Optional[datetime.date] = None):
        qs = (cls.objects
              .filter(smart_equal('fulfilment_status', status))
              .filter(product_variation_id=id)
              .filter(smart_range(date_col, begin, end))
              .values('product_variation_id')
              .annotate(total_count=Sum('quantity')))

        return qs[0]['total_count'] if len(qs) > 0 else 0

    @classmethod
    def total_pending_for_id(cls,
                             id: int,
                             created_begin: Optional[datetime.datetime] = None,
                             created_end: Optional[datetime.datetime] = None) -> int:
        return cls._total_with_status_for_id(status=FulfilmentStatus.PENDING,
                                             id=id,
                                             date_col='created_date',
                                             begin=created_begin,
                                             end=created_end)

    @classmethod
    def total_fulfilled_for_id(cls,
                               id: int,
                               fulfill_begin: Optional[datetime.datetime] = None,
                               fulfill_end: Optional[datetime.datetime] = None) -> int:
        return cls._total_with_status_for_id(status=FulfilmentStatus.FULFILLED,
                                             id=id,
                                             date_col='fulfill_datetime',
                                             begin=fulfill_begin,
                                             end=fulfill_end
                                             )

    @classmethod
    def total_ordered_for_id(cls,
                             id: int,
                             created_begin: Optional[datetime.datetime] = None,
                             created_end: Optional[datetime.datetime] = None) -> int:
        return cls._total_with_status_for_id(status=None,
                                             id=id,
                                             date_col='created_date',
                                             begin=created_begin,
                                             end=created_end
                                             )

    @classmethod
    def total_fulfilled(cls, product_variation: ProductVariation, **kwds) -> int:
        return cls.total_fulfilled_for_id(product_variation.id, **kwds)

    @classmethod
    def total_ready_to_ship(cls, pv_id: int, begin: datetime.datetime, end: datetime.datetime) -> int:
        from shipment.models.shipment import ShipmentStatus
        return (OrderItem.objects
                .filter(product_variation_id=pv_id)
                .filter(shipment__status=ShipmentStatus.CONFIRMED)
                .exclude(shipment__cancelled=True)
                .filter(smart_range('shipment__shippop_confirm_date_time', begin, end))
                .count())

    @classmethod
    def total_ready_to_ship_map(cls,
                                begin: Optional[datetime.datetime] = None,
                                end: Optional[datetime.datetime] = None) -> DefaultDict[int, int]:
        from shipment.models.shipment import ShipmentStatus
        qs = (OrderItem.objects
              .filter(shipment__status=ShipmentStatus.CONFIRMED)
              .exclude(shipment__cancelled=True)
              .filter(smart_range('shipment__shippop_confirm_date_time', begin, end))
              .values('product_variation_id').annotate(total_count=Sum('quantity')))
        ret = defaultdict(lambda: 0)
        ret.update({s['product_variation_id']: s['total_count'] for s in qs})
        return ret

    @classmethod
    def _total_map_for_status(cls,
                              status: Optional[FulfilmentStatus],
                              date_col: str,
                              begin: Optional[datetime.datetime] = None,
                              end: Optional[datetime.datetime] = None
                              ):
        qs = (cls.objects
              .filter(smart_equal('fulfilment_status', status))
              .filter(smart_range(date_col, begin, end))
              .values('product_variation_id').annotate(total_count=Sum('quantity')))

        ret = defaultdict(lambda: 0)
        ret.update({s['product_variation_id']: s['total_count'] for s in qs})
        return ret

    @classmethod
    def total_fulfilled_map(cls,
                            fulfill_begin: Optional[datetime.datetime] = None,
                            fulfull_end: Optional[datetime.datetime] = None) -> DefaultDict[int, int]:
        return cls._total_map_for_status(FulfilmentStatus.FULFILLED,
                                         date_col='fulfill_datetime',
                                         begin=fulfill_begin,
                                         end=fulfull_end)

    @classmethod
    def total_pending_map(cls,
                          created_begin: Optional[datetime.date] = None,
                          created_end: Optional[datetime.date] = None) -> DefaultDict[int, int]:
        return cls._total_map_for_status(FulfilmentStatus.PENDING,
                                         date_col='create_date',
                                         begin=created_begin,
                                         end=created_end)

    @classmethod
    def total_ordered_map(cls,
                          created_begin: Optional[datetime.date] = None,
                          created_end: Optional[datetime.date] = None) -> DefaultDict[int, int]:
        return cls._total_map_for_status(status=None,
                                         date_col='create_date',
                                         begin=created_begin,
                                         end=created_end)

    @classmethod
    def sorted_pending_order_items(cls) -> QuerySet:
        return cls.objects.filter(fulfilment_status=FulfilmentStatus.PENDING) \
            .order_by('shipment__order__order_time')
