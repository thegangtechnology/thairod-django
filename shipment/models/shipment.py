from django.db import models
from core.models import AbstractModel
from warehouse.models import Warehouse
from order.models import Order
from django.utils.translation import gettext_lazy as _
from shipment.models import TrackingStatus


# TODO: Abbreviation?
class ShipmentStatus(models.TextChoices):
    BOOKING = 'BOOKING', _('Book shipment to Shippop')
    CONFIRMED = 'CONFIRMED', _('Confirmed shipment')


class Shipment(AbstractModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    # This should be choices?
    shipping_method = models.CharField(max_length=255)
    tracking = models.ForeignKey(TrackingStatus, on_delete=models.CASCADE)
    label_printed = models.BooleanField(default=False)
    weight = models.DecimalField(decimal_places=3, max_digits=10)
    note = models.CharField(max_length=255)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # TODO: purchase model?
    purchase_id = models.CharField(max_length=255)
    status = models.CharField(max_length=9, choices=ShipmentStatus.choices, default=ShipmentStatus.BOOKING)
