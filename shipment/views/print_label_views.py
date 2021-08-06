from os.path import join, dirname
from typing import Optional

from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.views import APIView

from order.dataclasses.order import CreateOrderParameter
from order.services.order_service import OrderService
from shipment.dataclasses.print_label import PrintLabelParam
from shipment.models import Shipment
from shipment.services.print_label_service import PrintLabelService
from shipment.utils.print_label_util import split_print_label
from thairod.services.shippop.api import ShippopAPI


class PrintSampleLabelView(APIView):
    permission_classes = [AllowAny]

    def get(self, request: Request):
        with transaction.atomic():
            with open(join(dirname(__file__), '../tests/ttt.html')) as f:
                label_html = f.read()
            labels = split_print_label(label_html)
            ro = OrderService().create_raw_order(CreateOrderParameter.example_with_valid_item())
            shipments = [ro.shipment] * len(labels)
            ret = PrintLabelService().generate_label_interleave(labels, shipments)
            transaction.set_rollback(True)
        return HttpResponse(ret)


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
        label = self.generate_label(param)
        if label is not None:
            return HttpResponse(label)
        else:
            return HttpResponseNotFound('None of the shipment has valid tracking code')

    def generate_label(self, param: PrintLabelParam) -> Optional[str]:
        shipments = Shipment.objects.filter(id__in=param.shipments).exclude(tracking_code__isnull=True).all()
        if len(shipments) == 0:
            return None
        shippop = ShippopAPI()
        label_html = shippop.print_multiple_labels(tracking_codes=[s.tracking_code for s in shipments])
        labels = split_print_label(label_html)
        return PrintLabelService().generate_label_interleave(labels, shipments)
