import datetime
from typing import Optional

from shipment.dataclasses.batch_shipment import AssignBatchToShipmentParam, \
    UnassignBatchToShipmentParam
from shipment.models import BatchShipment, Shipment
from django.conf import settings
from thairod.utils import tzaware
from thairod.utils.query_util import round_to_next_nearest_hour


class BatchShipmentService:

    @classmethod
    def assign_batch_to_shipments(cls,
                                  assign_batch_to_shipment_param: AssignBatchToShipmentParam) -> None:
        param = assign_batch_to_shipment_param
        batch_shipment, _ = BatchShipment.objects.get_or_create(name=param.batch_name)
        shipments = Shipment.objects.filter(id__in=param.shipments)
        for shipment in shipments:
            shipment.batch = batch_shipment
            shipment.save()

    @classmethod
    def unassign_batch_shipments(cls, unassign_batch_to_shipment_param: UnassignBatchToShipmentParam) -> None:
        param = unassign_batch_to_shipment_param
        shipments = Shipment.objects.filter(id__in=param.shipments)
        for shipment in shipments:
            shipment.batch = None
            shipment.save()

    @classmethod
    def determine_print_datetime(cls, date: Optional[datetime.datetime] = None):
        date = tzaware.now() if date is None else date
        return round_to_next_nearest_hour(date, settings.SHIPPOP_LOT_CUTTING_TIME)

    @classmethod
    def determine_print_date(cls, date: Optional[datetime.datetime] = None) -> datetime.date:
        return cls.determine_print_datetime(date).date()
