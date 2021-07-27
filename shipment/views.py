from rest_framework import viewsets, filters

from shipment.models import Shipment, TrackingStatus

from shipment.serializers.shipment_serializer import ShipmentSerializer
from shipment.serializers.tracking_status_serializer import TrackingStatusSerializer


class ShipmentModelViewSet(viewsets.ModelViewSet):
    serializer_class = ShipmentSerializer
    queryset = Shipment.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'shipping_method', 'note', 'shippop_purchase_id', 'status']


class TrackingStatusModelViewSet(viewsets.ModelViewSet):
    serializer_class = TrackingStatusSerializer
    queryset = TrackingStatus.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['tracking_code', 'status']
