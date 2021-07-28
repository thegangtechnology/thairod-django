from django.db import models
from core.models import AbstractModel


class Address(AbstractModel):
    name = models.CharField(max_length=255)
    lat = models.DecimalField(decimal_places=7, max_digits=15, null=True)
    lon = models.DecimalField(decimal_places=7, max_digits=15, null=True)
    house_number = models.CharField(max_length=255)
    subdistrict = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=5)
    country = models.CharField(max_length=255)
    telno = models.CharField(max_length=255)
    note = models.CharField(max_length=255, blank=True, default="")
