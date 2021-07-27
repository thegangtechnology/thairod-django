from django.db import models

from core.models import AbstractModel


class TrackingStatus(AbstractModel):
    tracking_code = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(decimal_places=3, max_digits=8, null=True)
    discount = models.DecimalField(decimal_places=3, max_digits=8, null=True)
    courier_code = models.CharField(max_length=10, blank=True, null=True)
    courier_tracking_code = models.CharField(max_length=20, blank=True, null=True)
