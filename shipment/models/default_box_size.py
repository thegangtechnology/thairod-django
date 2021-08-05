from __future__ import annotations

from django.db import models
from django.db.models import PROTECT

from core.models import AbstractModel
from shipment.models.box_size import BoxSize


class DefaultBoxSize(AbstractModel):
    default_box_size = models.ForeignKey(BoxSize, null=False, on_delete=PROTECT)
