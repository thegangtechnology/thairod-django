from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from address.models import Address
from core.models import AbstractModel


# TODO: Abbreviation?
class OrderStatus(models.TextChoices):
    STARTED = 'STARTED', _('Doctor created')
    CHECKED_OUT = 'CHECKED_OUT', _('Payment is made')
    EXPIRED = 'EXPIRED', _('More than 24 hr. No effect on stock')


class Order(AbstractModel):
    status = models.CharField(
        max_length=11,
        choices=OrderStatus.choices,
        default=OrderStatus.STARTED,
    )
    # TODO: This looks like we should make a receiver table later? like patient list or sth.
    receiver_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    cid = models.CharField(max_length=255)
    orderer_name = models.CharField(max_length=255)
    orderer_license = models.CharField(max_length=255)
    order_time = models.DateTimeField(auto_now=True)  # TODO: Is this manual input?

    @classmethod
    def example(cls) -> Order:
        return Order(
            receiver_address=Address.example(),
            cid='1234567890123',
            orderer_name='คุณหมอ คนเก่ง',
            orderer_license='DOCTOR007'
        )
