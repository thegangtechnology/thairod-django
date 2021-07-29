from dataclasses import dataclass
from typing import List

from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, filters
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


from shipment.models import Shipment, TrackingStatus
from shipment.serializers.shipment_serializer import ShipmentSerializer
from shipment.serializers.tracking_status_serializer import TrackingStatusSerializer
from shipment.utils.print_label_util import split_print_label
from thairod.services.shippop.api import ShippopAPI
from thairod.utils.auto_serialize import AutoSerialize


class ShipmentModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = ShipmentSerializer
    queryset = Shipment.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'shipping_method', 'note', 'shippop_purchase_id', 'status']


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
