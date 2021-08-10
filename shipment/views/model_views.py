from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Avg, Count, Q
from shipment.models import Shipment, BatchShipment, TrackingStatus
from shipment.serializers import ShipmentSerializer, TrackingStatusSerializer
from shipment.serializers.shipment_serializer import ShipmentAssignSerializer


class ShipmentModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ShipmentSerializer
    queryset = Shipment.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'shipping_method', 'note', 'shippop_purchase_id', 'status', 'batch__name',
                     'label_printed']
    filterset_fields = ['label_printed', 'deliver']

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

    def get_queryset(self):
        queryset = Shipment.objects.all()
        batch_name = self.request.query_params.get('batch', None)
        has_batch = self.request.query_params.get('batch_isnull', None)
        if batch_name and not has_batch:
            queryset = queryset.filter(batch__name=batch_name)
        elif str(has_batch).lower() == 'true' or str(has_batch).lower() == 'false':
            has_batch = has_batch == str(has_batch).lower() == 'true'
            queryset = queryset.filter(batch__isnull=has_batch)
        return queryset.order_by('-created_date')

    @action(detail=False, methods=['GET'])
    def stats(self, request):
        stats = Shipment.objects.all().aggregate(total=Count('id'),
                                                 not_printed=Count(
                                                     'id',
                                                     filter=Q(label_printed=False) & Q(deliver=False)),
                                                 printed_not_deliver=Count(
                                                     'id',
                                                     filter=Q(label_printed=True) & Q(deliver=False)),
                                                 delivered=Count(
                                                     'id',
                                                     filter=Q(label_printed=True) & Q(deliver=True)),
                                                 assigned=Count('batch'),
                                                 not_assigned=Count('id',
                                                                    filter=Q(batch=None))
                                                 )
        return Response(stats)


class TrackingStatusModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TrackingStatusSerializer
    queryset = TrackingStatus.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['tracking_code', 'status']
