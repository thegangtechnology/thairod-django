from rest_framework import serializers

from order.models import Order, OrderItem
from product.serializers.product_variation_serializer import ProductVariationSerializer


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product_variation = ProductVariationSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'
