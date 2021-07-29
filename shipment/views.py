from typing import List

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpRequest
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
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
from thairod.utils.auto_serialize import AutoSerialize
from dataclasses import dataclass


class ShipmentModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
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
    serializer_class = TrackingStatusSerializer
    queryset = TrackingStatus.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['tracking_code', 'status']


@dataclass
class PrintLabelParam(AutoSerialize):
    shipments: List[int]

    @classmethod
    def example(cls):
        return ['1', '2', '3']


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


class PrintLabelService:

    def generate_label_interleave(self, labels: List[str], shipments: List[Shipment]) -> str:
        pairs = list(zip(labels, shipments))
        template = loader.get_template('shipping_label.html')
        context = {
            'pairs': pairs,
            'left_over': []
        }
        s = template.render(context)
        return s


# TODO: Refactor to dataclass
@dataclass
class GeneratedBatchNameResponse(AutoSerialize):
    name: str

    @classmethod
    def example(cls):
        return cls(name="2021-07-29_1")


class BatchShipmentModelViewSet(viewsets.ModelViewSet):
    serializer_class = BatchShipmentSerializer
    queryset = BatchShipment.objects.all()
    filter_backends = [filters.SearchFilter]

    @action(detail=False, methods=['GET'], url_path='next_generated_name')
    def get_next_generated_batch_name(self, request):
        return GeneratedBatchNameResponse(name=BatchShipment.generate_batch_name()).to_response()


@csrf_exempt
def print_label(request: HttpRequest):
    shipment_id: str = request.GET.get("shipment_id", None)
    if shipment_id is None or shipment_id.isdigit():
        return HttpResponseBadRequest()
    # optimize this
    shipment = Shipment.objects.select_related().get(id=shipment_id)
    # purchase_id = shipment.shippop_purchase_id
    # receiver_name = shipment.order.receiver_name
    items = shipment.orderitem_set.select_related().all()
    for item in items:
        print(item.product_variation.name)
    if shipment is None:
        return HttpResponseBadRequest()
    return JsonResponse({'id': shipment_id})
