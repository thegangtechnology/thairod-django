from shipment.dataclasses.batch_shipment import AssignBatchToShipmentRequest
from shipment.models import BatchShipment, Shipment


class BatchShipmentService:

    @classmethod
    def assign_batch_to_shipments(cls,
                                  assign_batch_to_shipment_request: AssignBatchToShipmentRequest) -> None:
        batch_shipment, _ = BatchShipment.objects.get_or_create(name=assign_batch_to_shipment_request.batch_name)
        shipments = Shipment.objects.filter(id__in=assign_batch_to_shipment_request.shipments)
        for shipment in shipments:
            shipment.batch = batch_shipment
            shipment.save()
