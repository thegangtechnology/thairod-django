from django.db import models

from core.models import AbstractModel
from shipment.models.shipment import Shipment


class TrackingStatus(AbstractModel):
    status = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(decimal_places=3, max_digits=8, null=True)
    discount = models.DecimalField(decimal_places=3, max_digits=8, null=True)
    courier_code = models.CharField(max_length=255, blank=True, null=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    courier_tracking_code = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)
