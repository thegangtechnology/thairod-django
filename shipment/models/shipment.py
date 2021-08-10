from __future__ import annotations

import datetime
from typing import Iterable, Optional

from django.db import models
from django.db.models import OuterRef, Exists, QuerySet

from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Q
from core.models import AbstractModel
from order.models.order import Order
from shipment.models import BatchShipment
from shipment.models.box_size import BoxSize
from thairod.utils import tzaware
from thairod.utils.query_util import smart_range, replace_hour
from warehouse.models import Warehouse


class ShipmentStatus(models.TextChoices):
    # Shippop process status
    CREATED = 'CREATED', _('Order for shipment created')
    FULFILLED = 'FULFILLED', _('All Order Items are Fulfilled')
    BOOKED = 'BOOKED', _('Book shipment to Shippop')
    # Our delivery status
    CONFIRMED = 'CONFIRMED', _('Confirmed shipment')  # ที่ต้องจัดส่ง
    # TODO: Bring them back next week
    # PRINTED = 'PRINTED', _('Printed')  # พิมพ์ใบจัดส่งแล้ว
    # DELIVERING = 'DELIVERING', _('Delivering')  # ดำเนินการส่งแล้ว
    # DELIVERED = 'DELIVERED', _('Delivered')  # ส่งมอบสำเร็จ


class Shipment(AbstractModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    # This should be choices?
    shipping_method = models.CharField(max_length=255)
    label_printed = models.BooleanField(default=False)
    deliver = models.BooleanField(default=False)  # แปลว่า ส่งออกหรือยัง ไม่เกี่ยวว่าของถึงหรือไม่ถึง
    weight = models.DecimalField(decimal_places=3, max_digits=10, null=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    shippop_purchase_id = models.IntegerField(null=True)
    tracking_code = models.CharField(max_length=255, blank=True, null=True)
    courier_tracking_code = models.CharField(max_length=255, null=True, blank=True)
    shippop_confirm_date_time = models.DateTimeField(null=True, default=None, db_index=True)
    status = models.CharField(max_length=9, choices=ShipmentStatus.choices, default=ShipmentStatus.CREATED)
    batch = models.ForeignKey(BatchShipment, on_delete=models.CASCADE, null=True, blank=True)
    box_size = models.ForeignKey(BoxSize, null=False, default=BoxSize.get_default_box_id, on_delete=models.RESTRICT)
    cancelled = models.BooleanField(default=False)
    fulfilled_date = models.DateTimeField(null=True, default=None)
    booked_date = models.DateTimeField(null=True, default=None)

    @classmethod
    def _annotated_shipments(cls):
        from order.models import OrderItem
        from order.models.order_item import FulfilmentStatus
        has_pending = OrderItem.objects.filter(
            shipment_id=OuterRef('id'),
            fulfilment_status=FulfilmentStatus.PENDING
        )
        return Shipment.objects.annotate(has_pending=Exists(has_pending))

    @classmethod
    def ready_to_ship_shipments(cls) -> QuerySet:
        return Shipment.objects.filter(status=ShipmentStatus.CONFIRMED)

    @classmethod
    def daily_shipment(cls, date: datetime.date) -> QuerySet:
        from thairod import settings
        dt = tzaware.datetime(date.year, date.month, date.day)
        dt = replace_hour(dt, settings.SHIPPOP_LOT_CUTTING_TIME)
        return Shipment.objects.filter(
            shippop_confirm_date_time__range=(dt - datetime.timedelta(days=1), dt)
        )

    @classmethod
    def pending_shipments(cls) -> QuerySet:
        return cls._annotated_shipments().filter(status=ShipmentStatus.CREATED,
                                                 cancelled=False,
                                                 has_pending=True)

    def cancel_shipment(self):
        from order.models.order_item import FulfilmentStatus
        self.cancelled = True
        for oi in self.orderitem_set.all():
            oi.fulfilment_status = FulfilmentStatus.CANCELLED

    def mark_fulfilled(self):
        self.status = ShipmentStatus.FULFILLED
        self.fulfilled_date = tzaware.now()
        self.save()

    def mark_booked(self):
        self.status = ShipmentStatus.BOOKED
        self.booked_date = tzaware.now()
        self.save()

    def mark_confirmed(self):
        self.status = ShipmentStatus.CONFIRMED
        self.shippop_confirm_date_time = tzaware.now()
        self.save()

    @classmethod
    def ready_to_fulfill_shipments(cls) -> Iterable[Shipment]:
        return cls._annotated_shipments().filter(status=ShipmentStatus.CREATED,
                                                 cancelled=False,
                                                 has_pending=False)

    @classmethod
    def ready_to_book_shipments(cls) -> Iterable[Shipment]:
        qs = cls.objects.filter(status=ShipmentStatus.FULFILLED,
                                cancelled=False)

        return qs.all()

    @property
    def is_ready_to_fulfill(self):
        return self.status == ShipmentStatus.CREATED and self.has_no_pending and not self.cancelled

    @property
    def is_ready_to_book(self):
        return self.status == ShipmentStatus.FULFILLED and not self.cancelled

    @property
    def has_no_pending(self):
        from order.models.order_item import FulfilmentStatus
        has_pending = self.orderitem_set.filter(fulfilment_status=FulfilmentStatus.PENDING).exists()
        return not has_pending

    @classmethod
    def total_shipment_created(cls,
                               begin: Optional[datetime.datetime] = None,
                               end: Optional[datetime.datetime] = None
                               ):
        return Shipment.objects.filter(smart_range('created_date', begin, end)).count()

    @classmethod
    def total_shipment_confirmed(cls,
                                 begin: Optional[datetime.date] = None,
                                 end: Optional[datetime.date] = None
                                 ):
        return (Shipment.objects
                .filter(status=ShipmentStatus.CONFIRMED)
                .filter(smart_range('shippop_confirm_date_time', begin, end))
                .count())

    @classmethod
    def get_shipment_stats(cls) -> QuerySet:
        return cls.objects.all().aggregate(total=Count('id'),
                                           not_printed=Count(
                                               'id',
                                               filter=Q(label_printed=False) & Q(deliver=False)),
                                           printed_not_deliver=Count(
                                               'id',
                                               filter=Q(label_printed=True) & Q(deliver=False)),
                                           delivered=Count(
                                               'id',
                                               filter=Q(label_printed=True) & Q(deliver=True)),
                                           assigned=Count('batch'),
                                           not_assigned=Count('id',
                                                              filter=Q(batch=None))
                                           )

    @classmethod
    def example(cls) -> Shipment:
        return Shipment(
            warehouse=Warehouse.example(),
            title='Example Shipment',
            shipping_method='SPE',
            order=Order.example(),
            shippop_purchase_id=12345,
            tracking_code='SP12345',
            courier_tracking_code='TG12345',
            status=ShipmentStatus.CONFIRMED,
            batch=BatchShipment.example()
        )
