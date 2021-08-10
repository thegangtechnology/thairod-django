from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shipment.models import Shipment, BatchShipment, TrackingStatus
from shipment.serializers import ShipmentSerializer, TrackingStatusSerializer
from shipment.serializers.shipment_serializer import ShipmentAssignSerializer
from datetime import datetime


class ShipmentModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ShipmentSerializer
    queryset = Shipment.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'shipping_method', 'note', 'shippop_purchase_id', 'status', 'batch__name',
                     'label_printed']
    filterset_fields = ['label_printed', 'deliver', 'batch__name']

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
        product_variation_name = self.request.query_params.get('product_variation', None)
        created_date = self.request.query_params.get('created_date', None)
        if batch_name and not has_batch:
            queryset = queryset.filter(batch__name=batch_name)
        elif str(has_batch).lower() == 'true' or str(has_batch).lower() == 'false':
            has_batch = has_batch == str(has_batch).lower() == 'true'
            queryset = queryset.filter(batch__isnull=has_batch)
        if product_variation_name:
            queryset = queryset.filter(orderitem__product_variation__name=product_variation_name)
        if created_date:
            parsed_dt_string = datetime.strptime(created_date, '%Y-%m-%d')
            queryset = Shipment.objects.filter(created_date__day=parsed_dt_string.day,
                                               created_date__month=parsed_dt_string.month,
                                               created_date__year=parsed_dt_string.year)
        return queryset.order_by('-created_date')

    @action(detail=False, methods=['GET'])
    def stats(self, request):
        stats = Shipment.get_shipment_stats()
        return Response(stats)


class TrackingStatusModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TrackingStatusSerializer
    queryset = TrackingStatus.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['tracking_code', 'status']
