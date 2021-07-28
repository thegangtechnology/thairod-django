from __future__ import annotations
from core.models import AbstractModel
from django.db import models
from address.models import Address


class Warehouse(AbstractModel):
    name = models.CharField(max_length=255)
    tel = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.RESTRICT, null=False)

    @classmethod
    def default_warehouse(cls) -> Warehouse:
        return Warehouse.objects.first()
