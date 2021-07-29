from django.http import HttpResponse, HttpResponseBadRequest
from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, filters
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from shipment.utils.print_label_util import split_print_label
from thairod.services.shippop.api import ShippopAPI
from rest_framework.decorators import action
from shipment.models import Shipment, TrackingStatus, BatchShipment
from shipment.serializers.shipment_serializer import ShipmentSerializer, ShipmentAssignSerializer
from shipment.serializers.tracking_status_serializer import TrackingStatusSerializer
from shipment.serializers.batch_shipment_serializer import BatchShipmentSerializer
from rest_framework.response import Response
from shipment.dataclasses.batch_shipment import GeneratedBatchNameResponse, AssignBatchToShipmentRequest
from shipment.dataclasses.print_label import PrintLabelParam
from shipment.services.print_label_service import PrintLabelService
from shipment.services.batch_shipment_service import BatchShipmentService


class ShipmentModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = ShipmentSerializer
    queryset = Shipment.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'shipping_method', 'note', 'shippop_purchase_id', 'status']

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


class PrintLabelView(APIView):
    @swagger_auto_schema(
        operation_description='Print Shipment Label support multiple label via ?shipments=1&shipments=2&shipments=3',
        manual_parameters=[Parameter('shipments', in_='query', type='integer', description='shipment id', example='1')]
    )
    def get(self, request: Request):
        param = PrintLabelParam(
            shipments=request.query_params.getlist('shipments')
        )
        if not param.shipments:
            return HttpResponseBadRequest('Empty Shipments.')
        return HttpResponse(self.generate_label(param))

    def generate_label(self, param: PrintLabelParam) -> str:
        shipments = Shipment.objects.filter(id__in=param.shipments)
        shippop = ShippopAPI()
        label_html = shippop.print_multiple_labels(tracking_codes=[s.tracking_code for s in shipments])
        labels = split_print_label(label_html)
        return PrintLabelService().generate_label_interleave(labels, shipments)


class BatchShipmentModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BatchShipmentSerializer
    queryset = BatchShipment.objects.all()
    filter_backends = [filters.SearchFilter]

    @swagger_auto_schema(
        operation_description='Get a next batch name generated by the system',
        responses={200: GeneratedBatchNameResponse.serializer()}
    )
    @action(detail=False, methods=['GET'], url_path='next_generated_name')
    def get_next_generated_batch_name(self, request):
        return GeneratedBatchNameResponse(name=BatchShipment.generate_batch_name()).to_response()

    @swagger_auto_schema(
        operation_description='Assign batch name to the given shipments. This will create a new batch'
                              'name if not yet existed',
        request_body=AssignBatchToShipmentRequest.serializer(),
        responses={200: ''}
    )
    @action(detail=False, methods=['POST'], url_path='assign')
    def assign_batch(self, request):
        assign_batch_to_shipment_request = AssignBatchToShipmentRequest.from_post_request(request=request)
        BatchShipmentService().assign_batch_to_shipments(
            assign_batch_to_shipment_request=assign_batch_to_shipment_request)
        return Response()
