from __future__ import annotations

import datetime
from typing import Optional
from django.db.models import QuerySet
from django.db import models
from django.utils import timezone

from core.models import AbstractModel


class BatchShipment(AbstractModel):
    name = models.CharField(max_length=255, unique=True)

    @classmethod
    def example(cls) -> BatchShipment:
        return BatchShipment(name='random_batch')

    @classmethod
    def _generate_batch_name(cls, print_date: datetime.date, batch_name: str):
        return f"{print_date.strftime('%Y-%m-%d')}_{batch_name}"

    @classmethod
    def generate_auto_batch_name(cls, date: Optional[datetime.datetime] = None):
        from shipment.services.batch_shipment_service import BatchShipmentService
        date = timezone.now() if date is None else date
        d = BatchShipmentService.determine_print_date(date)
        return cls._generate_batch_name(d, 'auto')

    @classmethod
    def generate_batch_name(cls, date: Optional[datetime.datetime] = None) -> str:
        from shipment.services.batch_shipment_service import BatchShipmentService
        date = timezone.now() if date is None else date
        batch_no = cls.count_created_today(date) + 1
        d = BatchShipmentService.determine_print_date(date)
        return cls._generate_batch_name(d, str(batch_no))

    @classmethod
    def count_created_today(cls, date: Optional[datetime.datetime] = None) -> int:
        from shipment.services.batch_shipment_service import BatchShipmentService
        print_batch = BatchShipmentService.determine_print_datetime(date)
        date_range = print_batch - datetime.timedelta(days=1), print_batch
        return (BatchShipment.objects
                .filter(created_date__range=date_range)
                .count())

    # batch that has shipment yet to be deliver
    @classmethod
    def get_pending_deliver_batch(cls) -> QuerySet:
        return cls.objects.filter(shipment__deliver=False).distinct()
