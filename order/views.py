import functools
from dataclasses import dataclass, asdict

from django.views.decorators.csrf import csrf_exempt
from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, filters
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_dataclasses.serializers import DataclassSerializer

from order.models.order import Order
from order.models.order_item import OrderItem
from order.serializers import OrderSerializer, OrderItemSerializer
from thairod.utils.decorators import swagger_example


class OrderModelViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['receiver_name', 'receiver_address', 'receiver_tel', 'cid', 'order_time']


class OrderItemModelViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['total_price', 'shipment__title', 'product_variation__name']

@dataclass
class CreateOrderParameter:
    name: str
    money: int

@swagger_example(CreateOrderParameter(name='piti', money=12000))
class CreateOrderParameterSerializer(DataclassSerializer[CreateOrderParameter]):
    class Meta:
        dataclass = CreateOrderParameter

@dataclass
class CreateOrderResponse:
    a: str
    b: int

@swagger_example(CreateOrderResponse(a="hello", b=44444))
class CreateOrderResponseSerializer(DataclassSerializer[CreateOrderResponse]):
    class Meta:
        swagger_schema_fields = {
            "example": asdict(CreateOrderResponse(a="hello", b=22)),
        }
        dataclass = CreateOrderResponse

class CreateOrderAPI(GenericAPIView):

    @swagger_auto_schema(
        request_body=CreateOrderParameterSerializer,
        responses={200:CreateOrderResponseSerializer})
    def post(self, request: Request, format=None):
        serializer = CreateOrderParameterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        param: CreateOrderParameter = serializer.save()
        return Response({"2222name": param.name, "Money": param.money + 10})
