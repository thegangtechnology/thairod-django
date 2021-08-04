from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import AbstractModel
from order.models.order import Order
from shipment.models import BatchShipment
from shipment.models.box_size import BoxSize
from warehouse.models import Warehouse


class ShipmentStatus(models.TextChoices):
    # Shippop process status
    CREATED = 'CREATED', _('Order for shipment created')
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
    status = models.CharField(max_length=9, choices=ShipmentStatus.choices, default=ShipmentStatus.CREATED)
    batch = models.ForeignKey(BatchShipment, on_delete=models.CASCADE, null=True, blank=True)
    box_size = models.ForeignKey(BoxSize, null=False, default=BoxSize.get_default_box_id, on_delete=models.RESTRICT)

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
