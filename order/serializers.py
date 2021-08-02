from rest_framework import serializers

from order.models import Order, OrderItem
from address.serializers import AddressSerializer
from product.serializers.product_variation_serializer import ProductVariationSerializer


class OrderSerializer(serializers.ModelSerializer):
    receiver_address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product_variation = ProductVariationSerializer(read_only=True, allow_null=True)

    class Meta:
        model = OrderItem
        fields = '__all__'
