from rest_framework import serializers
from shipment.models.tracking_status import TrackingStatus


class TrackingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingStatus
        fields = '__all__'
