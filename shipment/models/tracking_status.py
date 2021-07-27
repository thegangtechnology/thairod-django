from django.db import models
from core.models import AbstractModel


class TrackingStatus(AbstractModel):
    tracking_code = models.CharField(max_length=20)
    status = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=0.3, max_digits=8)
    discount = models.DecimalField(decimal_places=0.3, max_digits=8)
    courier_code = models.CharField(max_length=10)
    courier_tracking_code = models.CharField(max_length=20)
