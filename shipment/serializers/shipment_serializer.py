from rest_framework import serializers
from shipment.models import Shipment
from order.serializers import OrderItemSerializer
from shipment.serializers.batch_shipment_serializer import BatchShipmentSerializer


class ShipmentSerializer(serializers.ModelSerializer):
    order = OrderItemSerializer(source='orderitem_set', many=True, read_only=True, allow_null=True)
    batch = BatchShipmentSerializer(allow_null=True, read_only=True)

    class Meta:
        model = Shipment
        fields = '__all__'


class ShipmentAssignSerializer(serializers.ModelSerializer):
    batch_name = serializers.SerializerMethodField()
    is_assigned = serializers.SerializerMethodField()

    class Meta:
        model = Shipment
        fields = ['id', 'title', 'batch_name', 'is_assigned']

    def get_batch_name(self, obj):
        return obj.batch.name

    def get_is_assigned(self, obj):
        return obj.batch is not None
