from dataclasses import dataclass

from rest_framework import viewsets, filters
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from order.models.order import Order
from order.models.order_item import OrderItem
from order.serializers import OrderSerializer, OrderItemSerializer
from thairod.utils.auto_serialize import AutoSerialize, swagger_auto_serialize_schema


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
class CreateOrderParameter(AutoSerialize):
    name: str
    money: int

    @classmethod
    def example(cls):
        return cls(name='piti', money=234)

@dataclass
class CreateOrderResponse(AutoSerialize):
    a: str
    b: int

    @classmethod
    def example(cls):
        return cls(a="hello", b=44433434344)


class CreateOrderAPI(GenericAPIView):

    @swagger_auto_serialize_schema(CreateOrderParameter, CreateOrderResponse)
    def post(self, request: Request, format=None) -> Response:
        param = CreateOrderParameter.from_request(request)
        return CreateOrderResponse(a='str', b=param.money + 99).response()
