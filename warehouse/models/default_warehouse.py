from django.db import models
from django.db.models import PROTECT

from core.models import AbstractModel
from warehouse.models import Warehouse


class DefaultWarehouse(AbstractModel):
    # this table should have one row
    default_warehouse = models.ForeignKey(to=Warehouse, null=False, on_delete=PROTECT)
