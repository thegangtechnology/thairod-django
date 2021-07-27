from django.db import models
from core.models import AbstractModel
from django.utils import timezone
import secrets


class ShoppingLink(AbstractModel):
    callback_secret = models.CharField(max_length=255)
    # want to keep it flexible.
    raw_json_data = models.JSONField()
    is_expired = models.BooleanField(default=False)

    @staticmethod
    def generate_callback_secret() -> str:
        secret = secrets.token_urlsafe(nbytes=32)
        return secret

    def update_is_expired(self, timezone_object: timezone) -> None:
        diff = timezone_object - self.created_date
        diff_in_seconds = diff.total_seconds()
        diff_in_hours = divmod(diff_in_seconds, 3600)[0]
        # if the difference is more than 2 hour
        # the link is expired
        if diff_in_hours >= 2:
            self.is_expired = True
            self.save()
