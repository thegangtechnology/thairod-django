from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shipment.models import Shipment, BatchShipment, TrackingStatus
from shipment.serializers import ShipmentSerializer, TrackingStatusSerializer
from shipment.serializers.shipment_serializer import ShipmentAssignSerializer


class ShipmentModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ShipmentSerializer
    queryset = Shipment.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'shipping_method', 'note', 'shippop_purchase_id', 'status', 'batch__name']
    filterset_fields = ['batch__name']

    @action(detail=True, methods=['POST'])
    def assign(self, request, *args, **kwargs):
        batch_name = request.data.get('batch_name', None)
        shipment = self.get_object()
        if batch_name is None:
            return Response("Batch Name is None.", status=400)
        batch = BatchShipment.objects.get(name=batch_name)
        shipment.batch = batch
        shipment.save()
        return Response(ShipmentAssignSerializer(shipment).data)


class TrackingStatusModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TrackingStatusSerializer
    queryset = TrackingStatus.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['tracking_code', 'status']
