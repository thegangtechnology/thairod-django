from django.db import models
from core.models import AbstractModel


class Product(AbstractModel):
    sku = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    repeatable = models.BooleanField(default=False)
