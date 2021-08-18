import datetime
import secrets
from django.db import models
from core.models import AbstractModel


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
    # True if doctor doesn't have to confirm order
    # False otherwise
    auto_doctor_confirm = models.BooleanField(default=False)
    # True if order is already created, False otherwise
    order_created = models.BooleanField(default=False)

    @staticmethod
    def generate_hash_secret() -> str:
        secret = secrets.token_urlsafe(nbytes=32)
        return secret

    def is_doctor_link_hash_timestamp_expired(self, timezone_object: datetime.datetime) -> bool:
        from django.conf import settings
        if not self.doctor_link_hash_timestamp:
            return False
        diff = timezone_object - self.doctor_link_hash_timestamp
        diff_in_seconds = diff.total_seconds()
        return diff_in_seconds >= settings.DOCTOR_HASH_EXPIRATION_SECONDS

    def is_patient_link_hash_timestamp_expired(self, timezone_object: datetime.datetime) -> bool:
        from django.conf import settings
        if not self.patient_link_hash_timestamp:
            return False
        diff = timezone_object - self.patient_link_hash_timestamp
        diff_in_seconds = diff.total_seconds()
        return diff_in_seconds >= settings.PATIENT_HASH_EXPIRATION_SECONDS

    def patient_confirmation_url(self) -> str:
        from order_flow.services import OrderFlowService
        return OrderFlowService().patient_confirmation_url_from_hash(self.patient_link_hash)
