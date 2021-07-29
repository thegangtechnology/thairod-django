from rest_framework import serializers
from shipment.models import BatchShipment


class BatchShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchShipment
        fields = '__all__'
