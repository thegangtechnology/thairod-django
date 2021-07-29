from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import AbstractModel
from order.models.order import Order
from warehouse.models import Warehouse
from shipment.models import BatchShipment


# TODO: Abbreviation?
class ShipmentStatus(models.TextChoices):
    CREATED = 'CREATED', _('Order for shipment created')
    BOOKED = 'BOOKED', _('Book shipment to Shippop')
    CONFIRMED = 'CONFIRMED', _('Confirmed shipment')


class Shipment(AbstractModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    # This should be choices?
    shipping_method = models.CharField(max_length=255)
    label_printed = models.BooleanField(default=False)
    weight = models.DecimalField(decimal_places=3, max_digits=10, null=True)
    note = models.CharField(max_length=255)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shippop_purchase_id = models.IntegerField(null=True)
    tracking_code = models.CharField(max_length=255, blank=True, null=True)
    courier_tracking_code = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=9, choices=ShipmentStatus.choices, default=ShipmentStatus.CREATED)
    batch = models.ForeignKey(BatchShipment, on_delete=models.CASCADE, null=True)
