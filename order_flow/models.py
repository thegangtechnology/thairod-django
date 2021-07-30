from django.db import models
from core.models import AbstractModel
from django.utils import timezone
import secrets


class OrderFlow(AbstractModel):
    doctor_link_hash = models.CharField(max_length=255)
    doctor_link_hash_timestamp = models.DateTimeField(auto_now_add=True)
    # data that doctor send in when create the shopping link
    doctor_info = models.JSONField()
    # order that doctor choose from Thairod Mall
    doctor_order = models.JSONField(null=True, blank=True)
    patient_link_hash = models.CharField(max_length=255, null=True, blank=True)
    patient_link_hash_timestamp = models.DateTimeField(null=True, blank=True)
    # confirm address from patient
    patient_confirmation = models.JSONField(null=True, blank=True)

    @staticmethod
    def generate_hash_secret() -> str:
        secret = secrets.token_urlsafe(nbytes=32)
        return secret

    def is_doctor_link_hash_timestamp_expired(self, timezone_object: timezone) -> bool:
        diff = timezone_object - self.doctor_link_hash_timestamp
        diff_in_seconds = diff.total_seconds()
        diff_in_hours = divmod(diff_in_seconds, 3600)[0]
        # if the difference is more than 2 hour
        # the link is expired
        return diff_in_hours >= 2
