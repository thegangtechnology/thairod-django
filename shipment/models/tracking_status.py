from django.db import models
from core.models import AbstractModel


class TrackingStatus(AbstractModel):
    tracking_code = models.CharField(max_length=255)
    # TODO: ENUM?
    status = models.CharField(max_length=255)
