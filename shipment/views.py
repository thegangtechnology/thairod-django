from rest_framework import viewsets
from shipment.models.shipment import Shipment
from shipment.serializiers import ShipmentSerializer


class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
