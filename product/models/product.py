from __future__ import annotations

from django.db import models

from core.models import AbstractModel


class Product(AbstractModel):
    sku = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    repeatable = models.BooleanField(default=False)

    @classmethod
    def example(cls) -> Product:
        return Product(
            sku='a1234',
            name='hello',
            description='magic box'
        )
