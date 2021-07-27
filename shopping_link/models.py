from django.db import models
from core.models import AbstractModel


class ShoppingLink(AbstractModel):
    callback_url = models.CharField(max_length=255)
    # want to keep it flexible.
    raw_json_data = models.JSONField()
