from __future__ import annotations

from django.db import models

from core.models import AbstractModel
from thairod.settings import DEFAULT_BOX_SIZE


class BoxSize(AbstractModel):
    name = models.CharField(max_length=255, unique=True)
    width = models.IntegerField()  # cm
    length = models.IntegerField()  # cm
    height = models.IntegerField()  # cm
    rank = models.IntegerField()  # priority when determining appropriate box size

    @classmethod
    def get_default_box(cls) -> BoxSize:
        return cls.objects.filter(name=DEFAULT_BOX_SIZE).first()
