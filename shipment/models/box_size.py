from __future__ import annotations

from django.db import models

from core.models import AbstractModel


class BoxSize(AbstractModel):
    name = models.CharField(max_length=255, unique=True)
    width = models.IntegerField()  # cm
    length = models.IntegerField()  # cm
    height = models.IntegerField()  # cm
    rank = models.IntegerField()  # priority when determining appropriate box size

    @classmethod
    def get_default_box_id(cls) -> int:
        from shipment.models.default_box_size import DefaultBoxSize
        return DefaultBoxSize.objects.first().default_box_size.id

    @classmethod
    def get_default_box(cls) -> BoxSize:
        return cls.objects.get(id=cls.get_default_box_id())
