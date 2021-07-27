from rest_framework import viewsets, filters

from order.models.order import Order
from order.models.order_item import OrderItem

from order.serializers import OrderSerializer, OrderItemSerializer


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
