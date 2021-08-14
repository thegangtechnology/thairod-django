from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from order.dataclasses.order import CreateOrderResponse, CreateOrderParam
from order.models.order import Order
from order.models.order_item import OrderItem
from order.serializers import OrderSerializer, OrderItemSerializer
from order.services.order_service import OrderService
from django.conf import settings
from thairod.utils.auto_serialize import swagger_auto_serialize_post_schema
from thairod.utils.decorators import ip_whitelist


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


class CreateOrderAPI(APIView):
    permission_classes = [AllowAny]

    # TODO this white list need to be per account
    @ip_whitelist(settings.TELEMED_WHITELIST)
    @swagger_auto_serialize_post_schema(CreateOrderParam, CreateOrderResponse)
    def post(self, request: Request, format=None) -> Response:
        param = CreateOrderParam.from_post_request(request)
        service = OrderService()
        return service.create_order(param).to_response()
