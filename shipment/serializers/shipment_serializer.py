from rest_framework import serializers
from shipment.models import Shipment


class ShipmentSerializer(serializers.ModelSerializer):
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
