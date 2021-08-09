import datetime
from dataclasses import dataclass
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
from thairod.utils.auto_serialize import swagger_auto_serialize_get_schema, AutoSerialize


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


@dataclass
class PrintOfTheDayParam(AutoSerialize):
    date: Optional[datetime.date]


class PrintOfTheDayView(APIView):
    @swagger_auto_serialize_get_schema(
        query_type=PrintOfTheDayParam,
        operation_description='Print Shipment Label for the entire day',
        manual_parameters=[Parameter('date', in_='query', type='date', description='print date', example='2021-08-23')]
    )
    def get(self, request: Request) -> HttpResponse:
        param = PrintOfTheDayParam.from_get_request(request)
        shipments = Shipment.daily_shipment(date=param.date).all()

        param = PrintLabelParam(shipments=[s.id for s in shipments])
        label = PrintLabelService().generate_label(param)
        if label is not None:
            return HttpResponse(label)
        else:
            return HttpResponseNotFound('None of the shipment has valid tracking code')


class PrintLabelView(APIView):
    @swagger_auto_schema(
        operation_description='Print Shipment Label support multiple label via ?shipments=1&shipments=2&shipments=3',
        manual_parameters=[Parameter('shipments', in_='query', type='integer', description='shipment id', example='1')]
    )
    def get(self, request: Request) -> HttpResponse:
        param = PrintLabelParam(
            shipments=request.query_params.getlist('shipments')
        )
        if not param.shipments:
            return HttpResponseBadRequest('Empty Shipments.')
        label = PrintLabelService().generate_label(param)
        if label is not None:
            return HttpResponse(label)
        else:
            return HttpResponseNotFound('None of the shipment has valid tracking code')
